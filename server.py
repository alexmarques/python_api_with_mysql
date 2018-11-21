from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/contatos'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(250), unique=False)
    telefone = db.Column(db.String(30), unique=False)

    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone

class ContatoSchema(ma.Schema):
    class Meta:
        fields = ('nome', 'telefone')

contato_schema = ContatoSchema()        
contatos_schema = ContatoSchema(many=True)

@app.route('/contatos', methods=['GET'])
def get_contatos():
    contatos = Contato.query.all()
    result = contatos_schema.dump(contatos)
    return jsonify(result.data)

@app.route('/contatos/<id>', methods=['GET'])    
def contato_detail(id):
    contato = Contato.query.get(id)
    return contato_schema.jsonify(contato)

if __name__ == '__main__':
   app.run(debug=True)