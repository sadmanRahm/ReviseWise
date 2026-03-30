from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import func
import bcrypt

engine = create_engine("sqlite:///revise_wise.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "User"

    UserID = Column(Integer, primary_key=True, autoincrement=True)
    Email = Column(String, unique=True, nullable=False)
    PasswordHash = Column(String, nullable=False)
    Style = Column(String, default="Undetermined")
    is_teacher = Column(Integer, default=0)

    progress = relationship("Progress", back_populates="user", cascade="all, delete-orphan")
    posts = relationship("ForumPost", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, email, password, is_teacher=0):
        self.Email = email
        self.PasswordHash = self._hash_password(password)
        self.is_teacher = is_teacher

    def _hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.PasswordHash.encode("utf-8"))

    def update_style(self, new_style):
        self.Style = new_style


class Resource(Base):
    __tablename__ = "Resource"

    ResourceID = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String, nullable=False)
    Type = Column(String, nullable=False)
    StyleMatch = Column(String, nullable=False)
    Subject = Column(String, nullable=False)
    VideoLink = Column(String)
    FilePath = Column(String)
    DateAdded = Column(Date, default=date.today)

    progress = relationship("Progress", back_populates="resource", cascade="all, delete-orphan")


class Progress(Base):
    __tablename__ = "Progress"

    ProgressID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    ResourceID = Column(Integer, ForeignKey("Resource.ResourceID"), nullable=False)
    CompletionPercent = Column(Integer, default=0)
    LastAccessed = Column(Date, default=date.today)

    user = relationship("User", back_populates="progress")
    resource = relationship("Resource", back_populates="progress")


class QuizQuestion(Base):
    __tablename__ = "QuizQuestion"

    QuestionID = Column(Integer, primary_key=True, autoincrement=True)
    QuestionText = Column(String, nullable=False)
    OptionA = Column(String)
    OptionB = Column(String)
    OptionC = Column(String)
    OptionD = Column(String)
    StyleA = Column(String)
    StyleB = Column(String)
    StyleC = Column(String)
    StyleD = Column(String)


class ForumPost(Base):
    __tablename__ = "ForumPost"

    PostID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID", ondelete="CASCADE"), nullable=False)
    Content = Column(String, nullable=False)
    Timestamp = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="posts")


Base.metadata.create_all(engine)

