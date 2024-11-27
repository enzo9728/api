import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)


mydb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password = "",
    database = "ciel2025"
)


cursor = mydb.cursor()

@app.route('/v1/etudiants/',methods=['GET'])
def getetudiants():
    etudiants = []
    req = f"SELECT * FROM etudiant"
    cursor.execute(req)
    result = cursor.fetchall()
    for row in result:
        etudiant = {
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
            }
        etudiants.append(etudiant)
    return jsonify(etudiants), 200

@app.route('/v1/etudiants/<int:id>',methods=['GET'])
def getEtudiants(id):
    req = f"SELECT *FROM etudiant WHERE idetudiant = " + str(id)
    print (req)
    cursor.execute(req)
    row = cursor.fetchone()
    etudiant = {
        "idetudiant": row[0],
        "nom": row[1],
        "prenom": row[2],
        "email": row[3],
        "telephone": row[4]
    }
    return jsonify(etudiant), 200

@app.route('/v1/etudiants/',methods=['POST'])
def addEtudiants():
    nom = request.json['nom']
    prenom = request.json['prenom']
    email = request.json['email']
    telephone = request.json['telephone']
    req = f"INSERT INTO etudiant (nom, prenom, email, telephone)\
        VALUES ('{nom}','{prenom}','{email}','{telephone}')"
    cursor.execute(req)
    mydb.commit()
    return jsonify({'message':'Ajout OK'}), 201
    #return req

@app.route('/v1/etudiants/<int:id>',methods=['PUT'])
def updateEtudiants(id):
    nom = request.json['nom']
    prenom = request.json['prenom']
    email = request.json['email']
    telephone = request.json['telephone']
    req = f"""
    UPDATE etudiant
    SET nom = %s, prenom = %s, email = %s, telephone = %s
    WHERE idetudiant = %s;
    """
    cursor.execute(req, (nom, prenom, email, telephone, id))
    mydb.commit()
    return jsonify({'message':'Ajout OK'}), 200
    #return req

@app.route('/v1/etudiants/<int:id>',methods=['DELETE'])
def deleteEtudiants(id):
    nom = request.json['nom']
    prenom = request.json['prenom']
    email = request.json['email']
    telephone = request.json['telephone']
    req = req = f"DELETE FROM etudiant WHERE idetudiant = %s;"    
    cursor.execute(req, (id,))
    mydb.commit()
    return jsonify({'message':'Ajout OK'}), 200

if __name__ == '__main__':
    app.run(debug=True)
