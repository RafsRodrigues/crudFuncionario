from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from conexao import obter_conexao
from datetime import datetime

class Funcionario:
    def __init__(self, id, nome, endereco, telefone, data_nascimento):
        self.id = id
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.data_nascimento = data_nascimento
     
lista = []

app = Flask(__name__)

#  todas as datas de nascimento aparecerão no formato brasileiro
@app.template_filter('data_br')
def data_br(data):
    if isinstance(data, str):
        data = datetime.strptime(data, '%Y-%m-%d')
    return data.strftime('%d/%m/%Y')

@app.route('/')
def index():
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, endereco, telefone, data_nascimento FROM Funcionarios_py")
    funcionarios = cursor.fetchall()
    cursor.close()
    conexao.close()

    # Cria objetos Funcionario a partir do resultado
    lista = [Funcionario(id, nome, endereco, telefone, data_nascimento) for id, nome, endereco, telefone, data_nascimento in funcionarios]

    return render_template('lista.html', titulo='Funcionários', funcionarios=lista)


@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Funcionário')

    
@app.route('/criar', methods=['POST'])
def criar():
    dados = request.get_json()
    funcionario = dados[0]

    nome = funcionario['nome']
    endereco = funcionario['endereco']
    telefone = funcionario['telefone']
    data_nascimento = funcionario['data_nascimento']

    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO Funcionarios_py (nome, endereco, telefone, data_nascimento) VALUES (?, ?, ?, ?)",
        (nome, endereco, telefone, data_nascimento)
    )
    conexao.commit()
    cursor.close()
    conexao.close()

    return jsonify({"mensagem": "Salvo com sucesso"})

@app.route('/deletar/<int:id>')
def deletar(id):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM Funcionarios_py WHERE id = ?", id)
    conexao.commit()
    cursor.close()
    conexao.close()

    flash('Funcionário deletado com sucesso!')
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, endereco, telefone, data_nascimento FROM Funcionarios_py WHERE id = ?", id)
    funcionario = cursor.fetchone()
    cursor.close()
    conexao.close()

    if funcionario:
        nome, endereco, telefone, data_nascimento = funcionario
        return render_template('editar.html', titulo='Editar Funcionário', id=id, nome=nome, endereco=endereco, telefone=telefone, data_nascimento=data_nascimento)
    else:
        flash("Funcionário não encontrado.")
        return redirect(url_for('index'))     
        
@app.route('/atualizar', methods=['POST'])
def atualizar():
    dados = request.get_json()
    id = dados['id']
    nome = dados['nome']
    data_nascimento = dados['data_nascimento']
    endereco = dados['endereco']
    telefone = dados['telefone']

    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE Funcionarios_py 
        SET nome = ?, data_nascimento = ?, endereco = ?, telefone = ?
        WHERE id = ?
    """, (nome, data_nascimento, endereco, telefone, id))
    conexao.commit()
    cursor.close()
    conexao.close()

    return jsonify({"mensagem": "Atualizado com sucesso!"})


app.run(debug=True)
