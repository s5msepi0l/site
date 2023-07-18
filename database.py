import mysql.connector

def main():
    db = sql_db("localhost", "root", "")
    db.exec()

class sql_db:
    def __init__(self, addr: str,  usr: str, pw: str):
        self.db = mysql.connector.connect(
            host=addr,
            user=usr,
            passwd=pw,
            database="webservice",
            
            auth_plugin="mysql_native_password"
        )

        self.cursor = self.db.cursor()

    def exec(self, cmd):
        self.cursor.execute(cmd)

    def com(self):
        self.db.commit()

    def fetch(self):
        return self.cursor.fetchone()

    def l_fetch(self):
        return self.cursor.fetchall()

if __name__ == "__main__":
    main()
