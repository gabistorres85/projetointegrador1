import enum
import hashlib
import sqlite3
from sqlite3.dbapi2 import Timestamp
from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Date, DateTime, Enum
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

# conecta ao banco de dados 'curso.db'
# caso o banco não exista ele será criado
# Criar conexão com SQLite (arquivo local chamado banco.db)
engine = create_engine("sqlite:///banco.db", echo=True)

# Base para os modelos
Base = declarative_base()

# Criar tabelas hash
def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id_Usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    login = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    senha_hash = Column(String, nullable=False)
    criado_em = Column(DateTime, default=func.now())


    
    # Métodos para definir e verificar senha - usando hash

    def set_senha(self, senha: str):
        self.senha_hash = hash_senha(senha)

    def checa_senha(self, senha: str) -> bool:
        return self.senha_hash == hash_senha(senha)

class StatusPresenca(enum.Enum):
    presente = "presente"
    falta = "falta"
    falta_justificada = "falta_justificada"


class Genero(Base):
    __tablename__ = 'generos'
    id_Genero = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String, nullable=False, unique=True)
    alunos = relationship("Aluno", back_populates="genero")

class Pcd(Base):
    __tablename__ = 'pcds'
    id_Pcd = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String, nullable=False, unique=True)
    alunos = relationship("Aluno", back_populates="pcd", uselist=False) # Relação um-para-um

class Raca(Base):
    __tablename__ = 'racas'
    id_Raca = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String, nullable=False, unique=True)
    alunos = relationship("Aluno", back_populates="raca", uselist=False) # Relação um-para-um

class Aluno(Base):
    __tablename__ = 'alunos'
    id_Aluno = Column(Integer, primary_key=True, autoincrement=True)
    id_Genero = Column(Integer, ForeignKey('generos.id_Genero'))
    id_Pcd = Column(Integer, ForeignKey('pcds.id_Pcd'))
    id_Raca = Column(Integer, ForeignKey('racas.id_Raca'))
    nomeAluno = Column(String, nullable=False)
    datanasc = Column(String)
    cpf = Column(String(11))
    email = Column(String, nullable=False, unique=True)
    telefone = Column(String(11)) #11999999999
    datamatricula = Column(Date)
    dataconclusao = Column(Date)
    observacoes = Column(String)
    curso_id = Column(Integer)
    endereco = Column(String)
    presenca = Column(Enum(StatusPresenca), default=StatusPresenca.falta)
    e_faltoso = Column(Integer, default=0)
    genero = relationship("Genero", back_populates="alunos")    
    pcd = relationship("Pcd", back_populates="alunos", uselist=False) # Relação um-para-um
    raca = relationship("Raca", back_populates="alunos", uselist=False) # Relação um-para-um
    cursos = relationship("Turma", secondary="curso_aluno", back_populates="alunos") # Relação muitos-para-muitos

class Curso(Base):
    __tablename__ = 'cursos'
    id_Curso = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False, unique=True)
    descricao = Column(String)
    turno = Column(String)
    id_Professor = Column(Integer, ForeignKey('professores.id_Professor'))
    professor = relationship("Professor", back_populates="cursos", uselist=False) # Relação um-para-um

class Professor(Base):
    __tablename__ = 'professores'
    id_Professor = Column(Integer, primary_key=True, autoincrement=True)
    id_Genero = Column(Integer, ForeignKey('generos.id_Genero'))
    id_Pcd = Column(Integer, ForeignKey('pcds.id_Pcd'))
    id_Raca = Column(Integer, ForeignKey('racas.id_Raca'))
    nomeProfessor = Column(String, nullable=False)
    cpf = Column(String(11))
    email = Column(String, nullable=False, unique=True)
    telefone = Column(String(11)) #11999999999
    cursos = relationship("Curso", back_populates="professor") # Relação um-para-muitos
    professores = relationship("Professor", back_populates="genero") 
    pcd = relationship("Pcd", back_populates="alunos", uselist=False) # Relação n:1
    raca = relationship("Raca", back_populates="alunos", uselist=False) # Relação m-para-um
    genero = relationship("Genero", back_populates="professores")

class Turma(Base):
    __tablename__ = 'turmas'
    id_Turma = Column(Integer, primary_key=True, autoincrement=True)
    nomeTurma = Column(String, nullable=False, unique=True)
    descricao = Column(String)
    turno = Column(String)
    curso_id = Column(Integer, ForeignKey('cursos.id_Curso'))
    id_Aluno = Column(Integer, ForeignKey('alunos.id_Aluno'))
    alunos = relationship("Aluno", secondary="curso_aluno", back_populates="cursos") #Relação muitos-para-muitos
    curso = relationship("Curso", back_populates="turmas") # Relação um-para-muitosu

class Matricula(Base):
    __tablename__ = 'curso_aluno'
    id_Matricula = Column(Integer, primary_key=True, autoincrement=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id_Aluno'))
    turma_id = Column(Integer, ForeignKey('turmas.id_Turma'))
    aluno = relationship("Aluno", back_populates="cursos", uselist=False) # Relação um-para-um
    turma = relationship("Turma", back_populates="alunos") # Relação um-para-um
    data_matricula = Column(DateTime)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")
    

'''def criar_tabelas_todo():
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
    print("Tabelas criadas (se não existiam).")'''