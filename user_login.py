from flask_login import *


class UserLogin(UserMixin):
    def add_info_user(self, user_id, db):
        self.__user = db.get_info_user(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])

    def get_name(self):
        return str(self.__user['name'])

    def get_avatar(self):
        return str(self.__user['avatar'])

    def get_psw(self):
        return str(self.__user['password'])