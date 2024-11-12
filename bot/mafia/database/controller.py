import psycopg2

from mafia.database.models import Admin, User

class PostgresDatabase:

    def __init__(self, DB_URL: str) -> None:
        self.DB_URL = DB_URL
        try:
            self.conn = psycopg2.connect(DB_URL)
        except:
            print("Can't establish connection to database")

        self.cursor = self.conn.cursor()

    def reconnect(method):
        def decorator(self, *args):
            try:
                print(f"Executing DB method: '{method.__name__}' ...")
                return method(self, *args)
            except Exception as e:
                print(e)
                self.conn = psycopg2.connect(self.DB_URL)
                self.cursor = self.conn.cursor()
                print(f"Executing DB method: '{method.__name__}' ...")
                return method(self, *args)

        return decorator

    @reconnect
    def check_user(self, user_id: int) -> bool:
        self.cursor.execute("SELECT 1 FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()

    @reconnect
    def get_users(self) -> list:
        
        self.cursor.execute("SELECT * FROM users")
        
        users = []

        for user in self.cursor.fetchall():
            users.append(User(*user))
                    
        return users

    @reconnect
    def count_users(self) -> int:
        self.cursor.execute("SELECT COUNT(user_id) FROM users")

        return self.cursor.fetchone()[0]

    @reconnect
    def add_user(self, user_id: int, username: str) -> None:
        self.cursor.execute("INSERT INTO users VALUES(%s, %s)", (user_id, username))
        self.conn.commit()

    @reconnect
    def get_admins(self) -> list:
        self.cursor.execute("SELECT * FROM admins")
        
        admins = []
        for admin in self.cursor.fetchall():
            admins.append(Admin(*admin))

        return admins
    
    @reconnect
    def check_admin(self, user_id: int) -> bool:
        self.cursor.execute("SELECT 1 FROM admins WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()
    
    @reconnect
    def add_admin(self, user_id: int) -> None:
        self.cursor.execute("INSERT INTO admins VALUES(%s)", (user_id,))
        self.conn.commit()

    @reconnect
    def close(self) -> None:
        self.cursor.close()
