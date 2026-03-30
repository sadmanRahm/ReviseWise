from models import Session, QuizQuestion

db = Session()

questions = [

    {
        "QuestionText": "You are learning a new topic. What helps you most?",
        "OptionA": "Watching diagrams or videos",
        "OptionB": "Listening to explanations",
        "OptionC": "Reading notes or books",
        "OptionD": "Trying it out yourself",
        "StyleA": "Visual",
        "StyleB": "Auditory",
        "StyleC": "Read/Write",
        "StyleD": "Kinaesthetic"
    },

    {
        "QuestionText": "How do you usually revise for exams?",
        "OptionA": "Using mind maps and diagrams",
        "OptionB": "Talking through topics with others",
        "OptionC": "Rewriting notes",
        "OptionD": "Doing lots of practice questions",
        "StyleA": "Visual",
        "StyleB": "Auditory",
        "StyleC": "Read/Write",
        "StyleD": "Kinaesthetic"
    },

    {
        "QuestionText": "When a teacher explains something new, you prefer:",
        "OptionA": "Seeing it written or drawn on the board",
        "OptionB": "Listening carefully to the explanation",
        "OptionC": "Reading about it afterwards",
        "OptionD": "Trying an example yourself",
        "StyleA": "Visual",
        "StyleB": "Auditory",
        "StyleC": "Read/Write",
        "StyleD": "Kinaesthetic"
    },

    {
        "QuestionText": "What helps you remember information best?",
        "OptionA": "Pictures, charts, or colours",
        "OptionB": "Repeating it out loud",
        "OptionC": "Writing it down several times",
        "OptionD": "Using it in a real situation",
        "StyleA": "Visual",
        "StyleB": "Auditory",
        "StyleC": "Read/Write",
        "StyleD": "Kinaesthetic"
    },

    {
        "QuestionText": "If you are given instructions, you prefer them to be:",
        "OptionA": "Shown using diagrams or demonstrations",
        "OptionB": "Explained verbally",
        "OptionC": "Written step-by-step",
        "OptionD": "Learnt by doing the task",
        "StyleA": "Visual",
        "StyleB": "Auditory",
        "StyleC": "Read/Write",
        "StyleD": "Kinaesthetic"
    },

    {
        "QuestionText": "When revising at home, you usually:",
        "OptionA": "Watch videos or look at diagrams",
        "OptionB": "Listen to recordings or talk through ideas",
        "OptionC": "Read textbooks or notes",
        "OptionD": "Practise questions or activities",
        "StyleA": "Visual",
        "StyleB": "Auditory",
        "StyleC": "Read/Write",
        "StyleD": "Kinaesthetic"
    },

    {
        "QuestionText": "Which revision method do you enjoy the most?",
        "OptionA": "Using colour-coded notes or mind maps",
        "OptionB": "Group discussions",
        "OptionC": "Writing summaries",
        "OptionD": "Interactive tasks or experiments",
        "StyleA": "Visual",
        "StyleB": "Auditory",
        "StyleC": "Read/Write",
        "StyleD": "Kinaesthetic"
    },

    {
        "QuestionText": "When learning a skill, what helps you improve fastest?",
        "OptionA": "Watching someone demonstrate it",
        "OptionB": "Having it explained step-by-step",
        "OptionC": "Reading instructions carefully",
        "OptionD": "Practising it yourself",
        "StyleA": "Visual",
        "StyleB": "Auditory",
        "StyleC": "Read/Write",
        "StyleD": "Kinaesthetic"
    },

    {
        "QuestionText": "If you forget something in a lesson, you usually:",
        "OptionA": "Picture it in your head",
        "OptionB": "Talk it through",
        "OptionC": "Write it down again",
        "OptionD": "Try it out practically",
        "StyleA": "Visual",
        "StyleB": "Auditory",
        "StyleC": "Read/Write",
        "StyleD": "Kinaesthetic"
    },

    {
        "QuestionText": "What type of homework do you prefer?",
        "OptionA": "Creating posters or diagrams",
        "OptionB": "Presentations or discussions",
        "OptionC": "Written tasks or essays",
        "OptionD": "Practical or interactive tasks",
        "StyleA": "Visual",
        "StyleB": "Auditory",
        "StyleC": "Read/Write",
        "StyleD": "Kinaesthetic"
    },

    {
        "QuestionText": "When revising a difficult topic, you are most likely to:",
        "OptionA": "Draw it out visually",
        "OptionB": "Explain it to someone else",
        "OptionC": "Read multiple explanations",
        "OptionD": "Apply it to practice questions",
        "StyleA": "Visual",
        "StyleB": "Auditory",
        "StyleC": "Read/Write",
        "StyleD": "Kinaesthetic"
    },

    {
        "QuestionText": "Which helps you stay focused while revising?",
        "OptionA": "Visual organisation like charts",
        "OptionB": "Background explanations or discussion",
        "OptionC": "Structured written notes",
        "OptionD": "Active tasks and movement",
        "StyleA": "Visual",
        "StyleB": "Auditory",
        "StyleC": "Read/Write",
        "StyleD": "Kinaesthetic"
    },

    {
        "QuestionText": "You understand a topic best after:",
        "OptionA": "Seeing examples",
        "OptionB": "Hearing explanations",
        "OptionC": "Reading about it",
        "OptionD": "Doing practice tasks",
        "StyleA": "Visual",
        "StyleB": "Auditory",
        "StyleC": "Read/Write",
        "StyleD": "Kinaesthetic"
    },

    {
        "QuestionText": "Which classroom activity helps you learn most?",
        "OptionA": "Watching videos or slides",
        "OptionB": "Class discussions",
        "OptionC": "Reading worksheets",
        "OptionD": "Hands-on activities",
        "StyleA": "Visual",
        "StyleB": "Auditory",
        "StyleC": "Read/Write",
        "StyleD": "Kinaesthetic"
    },

    {
        "QuestionText": "When revising the night before a test, you usually:",
        "OptionA": "Review diagrams or visuals",
        "OptionB": "Talk through key points",
        "OptionC": "Read notes carefully",
        "OptionD": "Do last-minute practice questions",
        "StyleA": "Visual",
        "StyleB": "Auditory",
        "StyleC": "Read/Write",
        "StyleD": "Kinaesthetic"
    },

    {
        "QuestionText": "If you had to teach someone else, you would:",
        "OptionA": "Use diagrams or drawings",
        "OptionB": "Explain it verbally",
        "OptionC": "Give them written notes",
        "OptionD": "Show them how to do it",
        "StyleA": "Visual",
        "StyleB": "Auditory",
        "StyleC": "Read/Write",
        "StyleD": "Kinaesthetic"
    }

]

for q in questions:
    db.add(QuizQuestion(**q))

db.commit()
db.close()

print("16 quiz questions added successfully.")


