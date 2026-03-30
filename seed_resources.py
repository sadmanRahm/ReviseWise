from models import Session, Resource

db = Session()

resources = [

    # ================= GCSE MATHS =================
    {
        "Title": "GCSE Algebra Revision",
        "Type": "Notes",
        "StyleMatch": "Read/Write",
        "Subject": "Maths",
        "VideoLink": "https://www.physicsandmathstutor.com/maths-revision/gcse-edexcel/algebra/",
        "FilePath": None
    },
    {
        "Title": "Trigonometry Explained",
        "Type": "Video",
        "StyleMatch": "Visual",
        "Subject": "Maths",
        "VideoLink": "https://www.youtube.com/watch?v=ZLz1JfZpKkU",
        "FilePath": None
    },
    {
        "Title": "Maths Exam Techniques (Audio)",
        "Type": "Audio",
        "StyleMatch": "Auditory",
        "Subject": "Maths",
        "VideoLink": "https://www.bbc.co.uk/bitesize/guides/zp9mn39/revision/1",
        "FilePath": None
    },
    {
        "Title": "GCSE Maths Practice Questions",
        "Type": "Interactive",
        "StyleMatch": "Kinaesthetic",
        "Subject": "Maths",
        "VideoLink": "https://www.corbettmaths.com/contents/",
        "FilePath": None
    },

    # ================= GCSE BIOLOGY =================
    {
        "Title": "Cell Structure Revision",
        "Type": "Notes",
        "StyleMatch": "Visual",
        "Subject": "Biology",
        "VideoLink": "https://www.bbc.co.uk/bitesize/topics/znyycdm",
        "FilePath": None
    },
    {
        "Title": "GCSE Biology Key Terms",
        "Type": "Notes",
        "StyleMatch": "Read/Write",
        "Subject": "Biology",
        "VideoLink": "https://www.physicsandmathstutor.com/biology-revision/gcse-aqa/",
        "FilePath": None
    },
    {
        "Title": "Respiration Explained",
        "Type": "Audio",
        "StyleMatch": "Auditory",
        "Subject": "Biology",
        "VideoLink": "https://www.bbc.co.uk/bitesize/topics/zvrrd2p",
        "FilePath": None
    },
    {
        "Title": "Required Practical: Microscopy",
        "Type": "Interactive",
        "StyleMatch": "Kinaesthetic",
        "Subject": "Biology",
        "VideoLink": "https://www.cognitoedu.org/courses/gcse-biology",
        "FilePath": None
    },

    # ================= GCSE PHYSICS =================
    {
        "Title": "Forces and Motion Diagrams",
        "Type": "Notes",
        "StyleMatch": "Visual",
        "Subject": "Physics",
        "VideoLink": "https://www.bbc.co.uk/bitesize/topics/z4brd2p",
        "FilePath": None
    },
    {
        "Title": "GCSE Physics Formula Sheet",
        "Type": "Notes",
        "StyleMatch": "Read/Write",
        "Subject": "Physics",
        "VideoLink": "https://www.physicsandmathstutor.com/physics-revision/gcse-aqa/",
        "FilePath": None
    },
    {
        "Title": "Energy Transfers Explained",
        "Type": "Audio",
        "StyleMatch": "Auditory",
        "Subject": "Physics",
        "VideoLink": "https://www.bbc.co.uk/bitesize/topics/zd9cwmn",
        "FilePath": None
    },
    {
        "Title": "Electric Circuits Practice",
        "Type": "Interactive",
        "StyleMatch": "Kinaesthetic",
        "Subject": "Physics",
        "VideoLink": "https://www.corbettmaths.com/topics/electricity/",
        "FilePath": None
    },

    # ================= GCSE CHEMISTRY =================
    {
        "Title": "Periodic Table Visual Guide",
        "Type": "Notes",
        "StyleMatch": "Visual",
        "Subject": "Chemistry",
        "VideoLink": "https://www.bbc.co.uk/bitesize/topics/zs6hvcw",
        "FilePath": None
    },
    {
        "Title": "Chemical Reactions Summary",
        "Type": "Notes",
        "StyleMatch": "Read/Write",
        "Subject": "Chemistry",
        "VideoLink": "https://www.physicsandmathstutor.com/chemistry-revision/gcse-aqa/",
        "FilePath": None
    },
    {
        "Title": "Acids and Alkalis Explained",
        "Type": "Audio",
        "StyleMatch": "Auditory",
        "Subject": "Chemistry",
        "VideoLink": "https://www.bbc.co.uk/bitesize/topics/z9ddmp3",
        "FilePath": None
    },
    {
        "Title": "Required Practical: Titration",
        "Type": "Interactive",
        "StyleMatch": "Kinaesthetic",
        "Subject": "Chemistry",
        "VideoLink": "https://www.cognitoedu.org/courses/gcse-chemistry",
        "FilePath": None
    }
]

for r in resources:
    db.add(Resource(**r))

db.commit()
db.close()

print("GCSE preset resources with external links added.")


