from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from common.security import validated_user_password, generate_hash_password
from models.User import User


def check_user_password(db: Session, email: str, password: str) -> bool:
    user = get_user_by_email(db=db, email=email)
    if user is None:
        return False
    return validated_user_password(user.password, password)


def check_old_password(user: User, old_password: str) -> None:
    if validated_user_password(user.password, old_password):
        return True
    return None


def change_user_password(
    db: Session, user: User, new_password: str, is_commit: bool = True
) -> None:
    user.password = generate_hash_password(new_password)
    db.add(user)
    if is_commit:
        db.commit()
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    q = select(User).filter(User.email == email)
    user = db.execute(q).scalar()
    return user


def change_passowrd(
    db: Session, user: User, new_password: str, is_commit: bool = True
) -> None:
    user.password = generate_hash_password(password=new_password)
    db.add(user)
    if is_commit:
        db.commit()
    return user
