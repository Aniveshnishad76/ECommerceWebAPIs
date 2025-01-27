"""user model file"""
from datetime import datetime
from typing import List
from src.config.constants import UserStatusConstant
from src.config.env import get_settings
from src.db.session import get_db, save_new_row, update_old_row, select_all, select_first, delete
from src.services.user.schema import UserSchema

db = get_db()
config = get_settings()


class UserModel:
    """class to query user table schema"""

    @classmethod
    def create(cls, **kw):
        """method to save new user"""
        obj = UserSchema(**kw)
        obj.created_on = datetime.now()
        obj.updated_on = datetime.now()
        save_new_row(obj)
        return obj

    @classmethod
    def patch(cls, _id: int, **kw):
        """method to Update user"""
        obj = db.query(UserSchema).filter(UserSchema.id == _id).first()
        for key, value in kw.items():
            setattr(obj, key, value)
        obj.updated_on = datetime.now()
        update_old_row(obj)
        return cls.get_user(_id=_id)

    @classmethod
    def get_user(cls, _id: int = None, email: str = None, ids: List[int] = None, password: str = None, user_name: str = None, is_admin: bool = False):
        """get user by id"""
        rows = db.query(UserSchema).filter(UserSchema.status == UserStatusConstant.Active)
        if _id:
            rows = rows.filter(UserSchema.id == _id)
        if email:
            rows = rows.filter(UserSchema.email == email)
        if ids:
            rows = rows.filter(UserSchema.id.in_(ids))
        if password:
            rows = rows.filter(UserSchema.password_hash == password)
        if is_admin:
            rows = rows.filter(UserSchema.is_admin == is_admin)
        if user_name:
            rows = rows.filter(UserSchema.username == user_name)
        if not _id and not email:
            rows = select_all(rows)
        else:
            rows = select_first(rows)
        return rows

    @classmethod
    def delete(cls, _id: int):
        """delete user by id"""
        rows = db.query(UserSchema).filter(UserSchema.status == UserStatusConstant.Active)
        if _id:
            rows = rows.filter(UserSchema.id == _id)
        return delete(rows)
