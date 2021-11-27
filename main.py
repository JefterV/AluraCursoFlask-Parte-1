from flask import Flask, render_template, request, redirect, session, url_for
from flask.helpers import flash

app = Flask(__name__)
app.secret_key = "xyz"

# Class de cadastros. 
class CadastraJogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class CadastraUsuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++ INSERINDO DADOS LOCAIS

# Jogos
jogo01 = CadastraJogo('Fortnite', 'BattleRoyale', 'Epic Games')
jogo02 = CadastraJogo('CS:GO', 'FPS', 'STEAM')
lista = [jogo01, jogo02]

# Usuarios
usuario1 = CadastraUsuario('Jefter', 'Jefter Viana', "1234")
dictUsers = {usuario1.id: usuario1}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# INICIANDO ROTAS 
@app.route("/")
def index():   
    return render_template('lista.html', titulo='Lista de jogos', jogos =lista)


@app.route("/novo")
def novo():
    StringUser = 'usuario_logado'

    if StringUser not in session or session[StringUser] == None:
        return redirect(url_for('login', proxima=url_for('novo')))

    return render_template('novo.html', titulo='Novo Jogo')


@app.route('/criar', methods =["POST",])
def criar():
    nome      = request.form['nome']
    categoria = request.form['categoria']
    console   = request.form['console']

    jogo      = CadastraJogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima   = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=["POST",])
def autenticar():
    UsuarioID     = request.form["usuario"]
    ProximaPagina = request.form['proxima']
    StringUser    = "usuario_logado"
    
    if UsuarioID in dictUsers.keys():
        if dictUsers[UsuarioID].senha == request.form['senha']:
            session[StringUser] = request.form["usuario"]

            flash('Olá, ' + request.form["usuario"] + '! Bem vindo, login efetado com sucesso.')
            return redirect(ProximaPagina)
        
    flash('Usuario ou senha incorretos.')
    return redirect(url_for("login"))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash("Logout concluido.")
    return redirect(url_for("index"))

# END ROTAS 

# EXECUTANDO SERVIÇO 
app.run(debug=True)