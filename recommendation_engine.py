from models import Session, Resource


class RecommendationEngine:
    def __init__(self, user_style):
        self.style = user_style

    def generate_list(self, subject=None):
        db = Session()

        q = db.query(Resource).filter(Resource.StyleMatch == self.style)

        if subject and subject != "All":
            q = q.filter(Resource.Subject == subject)

        resources = q.all()
        db.close()

        interactive = []
        videos = []
        other = []

        for r in resources:
            if r.Type == "Interactive":
                interactive.append(r)
            elif r.Type == "Video":
                videos.append(r)
            else:
                other.append(r)

        return interactive + videos + other