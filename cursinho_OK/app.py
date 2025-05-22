from flask import Flask, render_template, request, redirect, url_for
import db

app = Flask(__name__)

# Inicializa as tabelas do banco de dados
with app.app_context():
    db.criar_tabelas_todo()

# --------------------------
# Página inicial (login)
# --------------------------
@app.route('/')
def home():
    return render_template('index.html')

# --------------------------
# Página de login
# --------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'senha123':
            return redirect(url_for('tela_inicial'))
        else:
            return "Usuário ou senha inválidos"
    return render_template('login.html')

# --------------------------
# Tela inicial
# --------------------------
@app.route('/tela-inicial')
def tela_inicial():
    return render_template('tela_inicial.html')

# --------------------------
# Tela de cadastro de alunos
# --------------------------
@app.route('/cadastrar-aluno', methods=['GET', 'POST'])
def cadastrar_aluno():
    if request.method == 'POST':
        novo_aluno = {
            'nome': request.form['nome'],
            'datanasc': request.form['datanasc'],
            'cpf': request.form['cpf'],
            'email': request.form['email'],
            'telefone': request.form['telefone'],
            'datamatricula': request.form['datamatricula'],
            'dataconclusao': request.form['dataconclusao'],
            'curso_id': request.form['curso_id'],
            'endereco': request.form.get('endereco', ''),
            'observacoes': request.form['observacoes']
        }
        db.add_aluno(novo_aluno)
        return redirect(url_for('visualizar_alunos'))
    return render_template('cadastrar-aluno.html')

# --------------------------
# Visualizar alunos
# --------------------------
@app.route('/visualizar-alunos')
def visualizar_alunos():
    alunos = db.get_alunos()
    return render_template('visualizar_alunos.html', alunos=alunos)

# --------------------------
# Editar aluno
# --------------------------
@app.route('/editar-aluno/<int:aluno_id>', methods=['GET', 'POST'])
def editar_aluno(aluno_id):
    aluno = db.get_aluno_por_id(aluno_id)
    if aluno is None:
        return "Aluno não encontrado."

    if request.method == 'POST':
        aluno_atualizado = {
            'nome': request.form['nome'],
            'datanasc': request.form['datanasc'],
            'cpf': request.form['cpf'],
            'email': request.form['email'],
            'telefone': request.form['telefone'],
            'datamatricula': request.form['datamatricula'],
            'dataconclusao': request.form['dataconclusao'],
            'curso_id': request.form['curso_id'],
            'observacoes': request.form['observacoes'],
            'endereco': request.form['endereco']
        }
        db.update_aluno(aluno_id, aluno_atualizado)
        return redirect(url_for('visualizar_alunos'))

    return render_template('editar_aluno.html', aluno=aluno)

# --------------------------
# Excluir aluno
# --------------------------
@app.route('/excluir-aluno/<int:aluno_id>', methods=['POST', 'DELETE'])
def excluir_aluno(aluno_id):
    db.delete_aluno(aluno_id)
    return redirect(url_for('visualizar_alunos'))

@app.route('/contato')
def contato():
    return render_template('contato.html')

# --------------------------
# Rodar servidor
# --------------------------
if __name__ == '__main__':
    app.run(debug=True)