from os import path
from .exception import ServerException


class Users:
    users = {}

    @staticmethod
    def addUser(user: str, ps: str, ip: str):
        Users.users[user] = {"password": ps, "ip": ip}

    @staticmethod
    def user(user: str):
        if user in Users.users:
            return Users.users[user]
        return None

    @staticmethod
    def load(file_path: str):
        if not path.isfile(file_path):
            raise ServerException("path '%s' not found" % path)

        with open(file_path, "r") as auth_file:
            for line in auth_file.readlines():
                line = line.strip().split(':')
                Users.addUser(line[0], line[1], line[2])

