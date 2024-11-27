import mysql.connector
import hashlib

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
    def connect(self):
        mydb = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
            )
        return mydb

    def readAll(self):
        conn = self.connect()
        cursor = conn.cursor()
        req = "SELECT * FROM etudiant"
        cursor.execute(req)
        #print(req)
        data = cursor.fetchall()
        conn.close()
        return data
    
    def readOne(self,id):
        conn = self.connect()
        cursor = conn.cursor()
        req = f"SELECT * FROM etudiant WHERE idetudiant = {id}"
        cursor.execute(req)
        #print(req)
        data = cursor.fetchone()
        conn.close()
        return data

    def authorized(self, request):
        auth = request.authorization
        username = auth.username
        password = auth.password
        password = (hashlib.sha256(password.encode('utf-8')).hexdigest())

        conn = self.connect()
        cursor = conn.cursor()
        req = f"SELECT password FROM user WHERE login = '{username}'"
        #print(req)
        cursor.execute(req)
        data = cursor.fetchone()
        conn.close()
        if data and (data[0] == password):
            return True
        else:
            return False
        
    def create(self, nom, prenom, email, telephone):
            conn = self.connect()
            cursor = conn.cursor()
            req = f"INSERT INTO etudiant (nom, prenom, email, telephone) VALUES (%s, %s, %s, %s)"
            cursor.execute(req, (nom, prenom, email, telephone))
            conn.commit()
            conn.close()
            return cursor.lastrowid
        
    def update(self, id, nom, prenom, email, telephone):
            conn = self.connect()
            cursor = conn.cursor()
            req = f"""
                UPDATE etudiant 
                SET nom = %s, prenom = %s, email = %s, telephone = %s
                WHERE idetudiant = %s
            """
            cursor.execute(req, (nom, prenom, email, telephone, id))
            conn.commit()
            conn.close()
            return cursor.rowcount
        
    def delete(self, id):
            conn = self.connect()
            cursor = conn.cursor()
            req = f"DELETE FROM etudiant WHERE idetudiant = %s"
            cursor.execute(req, (id,))
            conn.commit()
            conn.close()
            return cursor.rowcount

    def log(self, request):
        try:
            auth = request.authorization
            username = auth.username
            password = auth.password 
            password = (hashlib.sha256(password.encode('utf-8')).hexdigest())
        except:
            return 401
        try:
            conn = self.connect()
            curs = conn.cursor()
        except:
            return 500
        try:
            curs.execute(f"SELECT * FROM user WHERE login = '{username}' AND password = '{password}'")
            data = curs.fetchone()
            if data:
                return data 
            else:
                return 401
        except:
            return(401)
        finally:
            conn.close()
                 
