from user import User

class Admin(User):
    def __init__(self, login, password, role='admin'):
        super().__init__(login, password, role)

    def add_user(self, users, new_login, new_password, new_role):
        users[new_login] = User(new_login, new_password, new_role)

    def change_user_role(self, user, new_role):
        user.role = new_role

    def remove_user(self, users, login):
        if login in users:
            del users[login]
    @classmethod
    def from_dict(cls, data):
        return cls(data['login'], data['password'], data['role'])