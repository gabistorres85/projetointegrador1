from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import db

app = Flask(__name__)

# Inicializa as tabelas do banco de dados
'''with app.app_context():
    db.criar_tabelas_todo()'''

#---------------------------
# Função Helpers
#--------------------------

#--------------------------
# Conversão de dados
#---------------------------

def to_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value,'%Y-%m-%d').date()
    except ValueError:
        return None
    
def to_int(value):
    if value in (None, "", "null"):
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None
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
@app.route('/cadastrar-aluno', methods=['POST'])
def cadastrar_aluno():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({'erro':'Ausência de dados'}),400
                       
    # Definição dos campos obrigatórios
    obrigatorios = ['nome', 'dt_nasc','id_Genero','id_Pcd','id_Raca',
                    'cpf','telefone','endereco']
    faltando = [campo for campo in obrigatorios if campo not in data or not data[campo]]

    if faltando:
        return jsonify({"erro": f"Campos obrigatórios ausentes: {faltando}"}), 400
    
    #Tratamento dos dados
    for k in ['id_Genero','id_Pcd','id_Raca']:
        data[k] = to_int(k)

    for k in ['dt_nasc','dt_matricula','dt_conclusao']:
      data[k] = to_date(k)

    # Campos opcionais
    novo_aluno = db.Aluno(**data)
   
    with Session(db.engine) as s:
        # Tratamento para casos de cadastro de mesmo CPF
        try: 
            s.add(novo_aluno)
            s.commit()
            s.refresh(novo_aluno)

        except IntegrityError as e:
            print(e)
            s.rollback()
            if 'cpf' in str(e.orig).lower():
                return jsonify({'erro': 'Já existe um aluno com esse CPF.'}), 409
            else:
                return jsonify({'erro': 'Erro de integridade no banco.'}), 400
    
    return jsonify({
        'mensagem': 'Aluno cadastrado com sucesso.',
        'id': novo_aluno.id_Aluno
    }), 201
# --------------------------
# Visualizar alunos
# --------------------------
'''@app.route('/visualizar-alunos')
def visualizar_alunos():
    alunos = Session(db.session).query(db.Aluno).all()
    return render_template('visualizar_alunos.html', alunos=alunos)

# --------------------------
# Editar aluno
# --------------------------
@app.route('/editar-aluno/<int:aluno_id>', methods=['GET', 'POST'])
def editar_aluno(aluno_id):
    with Session(db.engine) as session: 
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

#---------------------------
# Cadastrar professor
#---------------------------
app.route('/cadastrar-professor', methods=['GET', 'POST'])
def cadastrar_professor():
    if request.method == 'POST':
        novo_professor = {
            'nome': request.form['nome'],
            'id_Genero': request.form['id_Genero'],
            'id_Raca': request.form['id_Raca'],
            'id_Pcd': request.form['id_Pcd'],
            'cpf': request.form['cpf'],
            'email': request.form['email'],
            'telefone': request.form['telefone'],
            'endereco': request.form.get('endereco', ''),
        }
        db.add_professor(novo_professor)
        return redirect(url_for('visualizar_professores'))
    return render_template('cadastrar-professor.html')

#---------------------------
# Visualizar professores
#--------------------------
@app.rote('/visualizar-professores')
def visualizar_professores():
    professores = db.get_professores()
    return render_template('visualizar_professores.html', professores=professores)

'''

# --------------------------
# Rodar servidor
# --------------------------
if __name__ == '__main__':
    app.run(debug=True)
