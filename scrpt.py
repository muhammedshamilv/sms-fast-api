from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User  
from app.settings import DATABASE_URL

SQLALCHEMY_DATABASE_URL = DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_test_user(email: str, password: str):
    hashed_password = User.hash_password(password)
    user = User(email=email, hashed_password=hashed_password)
    return user

def main():
    test_email = "testuser@gmail.com"
    mock_password = "1234"
    user = create_test_user(email=test_email, password=mock_password)

    session = SessionLocal()
    try:
        session.add(user)
        session.commit()
        print("Test user created successfully.")
    except Exception as e:
        session.rollback()
        print(f"Failed to create test user: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
