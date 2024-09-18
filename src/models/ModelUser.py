from database.db import get_connection
from .entities.User import User


class ModelUser():

    @classmethod
    def login(self, user):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT id, username, password, fullname FROM [user] WHERE username = ?""",
                    (user.username,)
                )
                row = cursor.fetchone()

                if row != None:
                    user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])
                    return user
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT id, username, fullname FROM [user] WHERE id = {}".format(id)
                cursor.execute(sql)
                row = cursor.fetchone()
                if row != None:
                    return User(row[0], row[1], None, row[2])
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)