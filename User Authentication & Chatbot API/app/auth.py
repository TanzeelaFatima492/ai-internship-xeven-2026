from sqlalchemy.orm import Session

from app.models import User
from app.utils.hashing import Hash


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not Hash.verify(password, user.password):
        return None

    return user