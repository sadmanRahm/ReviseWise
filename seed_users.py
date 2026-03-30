from models import Session, User

db = Session()

teacher = User(
    email="teacher@test.com",
    password="teacher123",
    is_teacher=1
)

student = User(
    email="student@test.com",
    password="student123",
    is_teacher=0
)

db.add_all([teacher, student])
db.commit()
db.close()

print("Test users created.")
