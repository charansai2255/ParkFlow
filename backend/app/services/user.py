from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user import create_user, get_user_by_email
from app.schemas.user import UserCreate


class EmailAlreadyRegisteredError(Exception):
    pass


def register_user(db: Session, user_data: UserCreate) -> User:
    normalized_email = str(user_data.email).lower()

    existing_user = get_user_by_email(
        db,
        normalized_email,
    )

    if existing_user is not None:
        raise EmailAlreadyRegisteredError

    password_hash = hash_password(user_data.password)

    try:
        return create_user(
            db,
            name=user_data.name.strip(),
            email=normalized_email,
            password_hash=password_hash,
        )
    except IntegrityError as exc:
        db.rollback()
        raise EmailAlreadyRegisteredError from exc