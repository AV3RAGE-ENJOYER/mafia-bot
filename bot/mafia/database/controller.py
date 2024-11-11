import psycopg2

from mafia.database.models import Admin, User

class PostgresDatabase:

    def __init__(self, DB_URL: str) -> None:
        try:
            self.conn = psycopg2.connect(DB_URL)
        except:
            print("Can't establish connection to database")

        self.cursor = self.conn.cursor()

    def check_user(self, user_id: int) -> bool:
        self.cursor.execute("SELECT 1 FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()

    def get_users(self) -> list:
        self.cursor.execute("SELECT * FROM users")
        
        users = []

        for user in self.cursor.fetchall():
            users.append(User(*user))
                    
        return users

    def count_users(self) -> int:
        self.cursor.execute("SELECT COUNT(user_id) FROM users")

        return self.cursor.fetchone()[0]

    def add_user(self, user_id: int, username: str) -> None:
        self.cursor.execute("INSERT INTO users VALUES(%s, %s)", (user_id, username))
        self.conn.commit()

    def get_admins(self) -> list:
        self.cursor.execute("SELECT * FROM admins")
        
        admins = []
        for admin in self.cursor.fetchall():
            admins.append(Admin(*admin))

        return admins
    
    def check_admin(self, user_id: int) -> bool:
        self.cursor.execute("SELECT 1 FROM admins WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()
    
    def add_admin(self, user_id: int) -> None:
        self.cursor.execute("INSERT INTO admins VALUES(%s)", (user_id,))
        self.conn.commit()

    def close(self) -> None:
        self.cursor.close()