import sqlite3

# conecta ao banco de dados 'curso.db'
# caso o banco não exista ele será criado
conn = sqlite3.connect("curso.db", check_same_thread=False)
conn.row_factory = sqlite3.Row

def criar_tabelas_todo():
    """ cria a tabela 'tarefa' caso ela não exista """
    cursor = conn.cursor()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS cursos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        descricao TEXT,
        turno TEXT
        )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        datanasc DATE,
        cpf CHAR(11),
        email TEXT NOT NULL UNIQUE,
        telefone TEXT,
        datamatricula DATE,
        dataconclusao DATE,
        observacoes TEXT,
        curso_id INTEGER,
        endereco TEXT,
        FOREIGN KEY (curso_id) REFERENCES cursos(id)
        )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        login TEXT NOT NULL UNIQUE,
        senha_hash TEXT NOT NULL,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

def add_aluno(aluno):
    """ adiciona uma novo aluno """
    print ("inserir")
    print (aluno['nome'])
    conn.execute("INSERT INTO alunos (nome, datanasc, cpf, email, telefone, datamatricula, dataconclusao,observacoes, curso_id, endereco) VALUES (?, ?, ?, ?, ?, ?, NULL, ?, ?, ?)", (aluno['nome'], aluno['datanasc'], aluno['cpf'], aluno['email'], aluno['telefone'], aluno['datamatricula'], aluno['observacoes'], aluno['curso_id'], aluno['endereco']))
    conn.commit()

def get_alunos(): # retorna um cursor
    """ retorna a lista de alunos cadastras """
    cursor = conn.execute("select id, nome, datanasc, cpf, email, telefone, datamatricula, dataconclusao, curso_id, endereco, observacoes from alunos")
    return [dict(row) for row in cursor.fetchall()]

def get_aluno_por_id(aluno_id):
    """ Retorna os dados de um aluno específico pelo ID """
    cursor = conn.execute("SELECT * FROM alunos WHERE id = ?", (aluno_id,))
    result = cursor.fetchone()
    return dict(result) if result else None

def update_aluno(id, aluno):
    """ Atualiza os dados de um aluno pelo ID """
    conn.execute("""
        UPDATE alunos
        SET nome = ?, datanasc = ?, cpf = ?, email = ?, telefone = ?, datamatricula = ?, dataconclusao = ?, observacoes = ?, curso_id = ?, endereco = ?
        WHERE id = ?
    """, (aluno['nome'], aluno['datanasc'], aluno['cpf'], aluno['email'], aluno['telefone'], aluno['datamatricula'], aluno['dataconclusao'], aluno['observacoes'], aluno['curso_id'], aluno['endereco'], id))
    conn.commit()

def delete_aluno(id):
    """ Remove um aluno pelo ID """
    conn.execute("DELETE FROM alunos WHERE id = ?", (id,))
    conn.commit()

if __name__ == "__main__":
    criar_tabelas_todo()
    print("Tabelas criadas (se não existiam).")