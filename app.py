import os
import random
from datetime import date
from functools import wraps

# flask imports - render_template is for returning html pages, request is for form data
from flask import Flask, render_template, request, session, redirect, url_for, flash
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename

from models import Session, User, Progress, Resource, QuizQuestion, ForumPost
from auth_manager import AuthManager
from quiz_processor import QuizProcessor
from recommendation_engine import RecommendationEngine
from forum_moderator import ForumModerator


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "f3a91bcd7e")

# folder where teacher uploaded files get saved
UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "docx", "pptx", "mp4"}


def allowed_file(fname):
    # checks the file extension is one we allow
    if "." not in fname:
        return False
    ext = fname.rsplit(".", 1)[-1].lower()
    return ext in ALLOWED_EXTENSIONS


# decorator so i dont have to repeat the session check in every route
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrap


# pulled this out into its own function because i was repeating it in dashboard and leaderboard
def get_completion_stats(progress_rows):
    total = len(progress_rows)
    done = 0
    for row in progress_rows:
        if row.CompletionPercent == 100:
            done += 1
    pct = round((done / total) * 100) if total > 0 else 0
    return done, total, pct


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form["email"].strip()
    password = request.form["password"]

    # authenticate returns the user id if successful, None if not
    uid = AuthManager().login(email, password)

    if not uid:
        flash("Incorrect login details.", "danger")
        return render_template("login.html")

    db = Session()
    user = db.get(User, uid)
    is_teacher = user.is_teacher
    db.close()

    # store in session so other routes know who's logged in
    session["user_id"] = uid
    session["is_teacher"] = int(is_teacher)
    return redirect(url_for("dashboard"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]
        role = request.form.get("role")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template("register.html")

        # convert role string to integer flag for the database
        teacher_flag = 1 if role == "teacher" else 0
        success, msg = AuthManager().register(email, password, teacher_flag)

        if success:
            flash("Account created. You can now log in.", "success")
            return redirect(url_for("login"))
        flash(msg, "danger")

    return render_template("register.html")


@app.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    db = Session()
    questions = db.query(QuizQuestion).all()
    db.close()

    if request.method == "POST":
        # build list of answers from the form - each question is named q1, q2 etc
        answers = []
        for q in questions:
            answers.append(request.form.get("q" + str(q.QuestionID), ""))

        style = QuizProcessor(answers).calculate_style()

        # save the result to the user's record in the db
        db = Session()
        user = db.get(User, session["user_id"])
        user.update_style(style)
        db.commit()
        db.close()

        session["quiz_result"] = style
        session["learning_style"] = style
        return redirect(url_for("display_result"))

    # shuffle the options for each question so the order isnt always the same
    for q in questions:
        opts = list(zip(
            [q.OptionA, q.OptionB, q.OptionC, q.OptionD],
            [q.StyleA,  q.StyleB,  q.StyleC,  q.StyleD]
        ))
        random.shuffle(opts)
        q.OptionA, q.StyleA = opts[0]
        q.OptionB, q.StyleB = opts[1]
        q.OptionC, q.StyleC = opts[2]
        q.OptionD, q.StyleD = opts[3]

    return render_template("quiz.html", questions=questions)


@app.route("/display_result")
@login_required
def display_result():
    style = session.get("quiz_result")
    if not style:
        flash("Please complete the quiz first.", "warning")
        return redirect(url_for("quiz"))

    # match style to a description - used if/elif instead of a dict as its clearer
    desc = ""
    if style == "Visual":
        desc = "You learn best through diagrams and videos."
    elif style == "Auditory":
        desc = "You learn best by listening and discussion."
    elif style == "Read/Write":
        desc = "You learn best through reading and writing notes."
    elif style == "Kinaesthetic":
        desc = "You learn best through practical activities."

    return render_template("display_result.html", style=style, description=desc)


@app.route("/recommendations")
@login_required
def recommendations():
    db = Session()
    user = db.get(User, session["user_id"])
    style = user.Style
    db.close()

    # redirect to quiz if they havent done it yet
    if style == "Undetermined":
        flash("Take the quiz first so resources can be personalised.", "warning")
        return redirect(url_for("quiz"))

    subject = request.args.get("subject", "All")
    resources = RecommendationEngine(style).generate_list(subject)
    subjects = ["All", "Maths", "Biology", "English", "History", "Geography", "Languages"]

    return render_template(
        "recommendations.html",
        resources=resources,
        subjects=subjects,
        selected_subject=subject
    )


@app.route("/complete_resource", methods=["POST"])
@login_required
def complete_resource():
    resource_id = request.form.get("resource_id")

    if not resource_id:
        flash("Something went wrong.", "danger")
        return redirect(url_for("dashboard"))

    db = Session()
    row = db.query(Progress).filter(
        Progress.UserID == session["user_id"],
        Progress.ResourceID == int(resource_id)
    ).first()

    # update existing row or create one if it doesnt exist yet
    if row:
        row.CompletionPercent = 100
        row.LastAccessed = date.today()
    else:
        db.add(Progress(
            UserID=session["user_id"],
            ResourceID=int(resource_id),
            CompletionPercent=100,
            LastAccessed=date.today()
        ))

    db.commit()
    db.close()
    flash("Marked as completed.", "success")
    return redirect(url_for("dashboard"))


@app.route("/delete_resource/<int:resource_id>", methods=["POST"])
@login_required
def delete_resource(resource_id):
    # only teachers should be able to delete
    if session.get("is_teacher") != 1:
        flash("You do not have permission to do that.", "danger")
        return redirect(url_for("dashboard"))

    db = Session()
    resource = db.get(Resource, resource_id)
    if resource:
        db.delete(resource)
        db.commit()
        flash("Resource deleted.", "info")
    else:
        flash("Resource not found.", "warning")

    db.close()
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
@login_required
def dashboard():
    db = Session()
    all_resources = db.query(Resource).all()
    prog = db.query(Progress).filter(Progress.UserID == session["user_id"]).all()

    # if a new resource was added after the user registered, they wont have a progress row for it
    # so this loop adds one with 0% so it shows up on the dashboard
    tracked = [p.ResourceID for p in prog]
    for r in all_resources:
        if r.ResourceID not in tracked:
            db.add(Progress(
                UserID=session["user_id"],
                ResourceID=r.ResourceID,
                CompletionPercent=0,
                LastAccessed=date.today()
            ))
    db.commit()

    # reload with resource data joined in so we can access resource.Subject etc in the template
    prog = (
        db.query(Progress)
        .options(joinedload(Progress.resource))
        .filter(Progress.UserID == session["user_id"])
        .all()
    )

    # group progress rows by subject for the dashboard table layout
    by_subject = {}
    for row in prog:
        subj = row.resource.Subject
        if subj not in by_subject:
            by_subject[subj] = []
        by_subject[subj].append(row)

    done, total, pct = get_completion_stats(prog)
    db.close()

    return render_template(
        "dashboard.html",
        progress_by_subject=by_subject,
        completed_count=done,
        not_started_count=total - done,
        overall_completion=pct
    )


@app.route("/leaderboard")
@login_required
def leaderboard():
    db = Session()
    users = db.query(User).all()

    board = []
    for u in users:
        prog = db.query(Progress).filter(Progress.UserID == u.UserID).all()
        done, total, overall = get_completion_stats(prog)
        board.append({
            "email": u.Email,
            "style": u.Style,
            "completed": done,
            "overall": overall
        })

    db.close()

    # sort by overall completion percentage, highest first
    board.sort(key=lambda x: x["overall"], reverse=True)
    return render_template("leaderboard.html", users=board)


@app.route("/upload_resource", methods=["GET", "POST"])
@login_required
def upload_resource():
    if session.get("is_teacher") != 1:
        flash("Only teachers can upload resources.", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        res_type = request.form.get("type")
        style = request.form.get("style")
        subject = request.form.get("subject")
        video_link = request.form.get("video_link", "").strip()

        # handle file upload if one was provided
        file_path = None
        upload = request.files.get("video_file")
        if upload and upload.filename != "" and allowed_file(upload.filename):
            fname = secure_filename(upload.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            upload.save(os.path.join(UPLOAD_FOLDER, fname))
            file_path = fname

        db = Session()
        db.add(Resource(
            Title=title,
            Type=res_type,
            StyleMatch=style,
            Subject=subject,
            VideoLink=video_link if video_link else None,
            FilePath=file_path
        ))
        db.commit()
        db.close()

        flash("Resource uploaded.", "success")
        return redirect(url_for("dashboard"))

    return render_template("upload_resource.html")


@app.route("/forum", methods=["GET", "POST"])
@login_required
def forum():
    msg = None

    if request.method == "POST":
        content = request.form.get("content", "")

        # run post through moderator before saving - returns None if blocked
        clean, warning = ForumModerator().moderate_post(content)

        if clean is None:
            msg = warning
        else:
            db = Session()
            db.add(ForumPost(UserID=session["user_id"], Content=clean))
            db.commit()
            db.close()

            if warning:
                msg = warning
            else:
                msg = "Post published."

    db = Session()
    posts = (
        db.query(ForumPost)
        .options(joinedload(ForumPost.user))
        .order_by(ForumPost.PostID.desc())
        .all()
    )
    db.close()

    return render_template("forum.html", posts=posts, message=msg)


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("is_teacher", None)
    session.pop("quiz_result", None)
    flash("Logged out.", "info")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)