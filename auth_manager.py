from models import Session, User


class AuthManager:

    def login(self, email, password):
        db = Session()
        user = db.query(User).filter(User.Email == email).first()
        db.close()

        if not user:
            return None
        if not user.authenticate(password):
            return None
        return user.UserID

    def register(self, email, password, is_teacher=0):
        db = Session()
        check = db.query(User).filter(User.Email == email).first()

        if check:
            db.close()
            return False, "Email already exists."

        db.add(User(email, password, is_teacher=is_teacher))
        db.commit()
        db.close()
        return True, "Registered successfully. You can now login."