import json

class User:
    def __init__(self, login, password, role):
        self.login = login
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            'login': self.login,
            'password': self.password,
            'role': self.role
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['login'], data['password'], data['role'])

    def change_password(self, new_password):
        self.password = new_password
