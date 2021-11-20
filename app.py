############Glogle#########
import wordcloud
import numpy as np
from matplotlib import pyplot as plt
from IPython.display import display
import fileupload
import io
import sys
##############Ocean###########
import sqlite3
from flask import Flask, g, render_template, request
######Configure_OCEAN#########
DATABASE = "./flasker.db"
SECRET_KEY = "pudim"
USERNAME = "admin"
PASSWORD = "admin"
######Aplicação OCEAN#########
app = Flask(__name__)
app.config.from_object(__name__)
#######Conectando ao Banco de dados######
def connect_db():
    return sqlite3.connect(DATABASE)
###Abrindo conexão#####
@app.before_request
def before():
    g.db = connect_db()
###Fechando conexão####
@app.teardown_request
def after(exception):
    g.db.close()
#####Criando rota para aplição#######
@app.route('/')
def index():
    #leitura=open("./arqText.txt", "r")
    #print (leitura.read())
    #leitura.close()
    sql = 'SELECT titulo, texto from entradas order by id desc'
    cur = g.db.execute(sql)
    entradas = [dict(titulo=titulo, texto=texto) for titulo, texto in cur.fetchall()]
    return render_template("index.html", entradas=entradas)
@app.route('/inserir', methods=['POST'])
def inserir():
    sql = 'INSERT INTO entradas (titulo, texto) values(?,?)'
    g.db.execute(sql, [request.form['titulo'], request.form['texto']])
    g.db.commit()
    return render_template('index.html')