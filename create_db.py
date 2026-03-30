from models import Base, engine


def rebuild_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("done - tables dropped and recreated")


if __name__ == "__main__":
    rebuild_database()