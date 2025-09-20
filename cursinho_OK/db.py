import enum
import hashlib
import sqlite3
from sqlite3.dbapi2 import Timestamp
from sqlalchemy import ForeignKey, Table, create_engine, Column, Integer, String, Date, DateTime, Enum
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy.sql import func

# conecta ao banco de dados 'curso.db'
# caso o banco não exista ele será criado
# Criar conexão com SQLite (arquivo local chamado banco.db)
engine = create_engine("sqlite:///banco.db", echo=True)

# Base para os modelos
Base = declarative_base()

curso_turma = Table(
    "curso_turma",
    Base.metadata,
    Column("curso_id", Integer, ForeignKey("cursos.id_Curso"), primary_key=True),
    Column("turma_id", Integer, ForeignKey("turmas.id_Turma"), primary_key=True)
)
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

class StatusArea(enum.Enum):
    humanas = "humanas"
    exatas = "exatas"
    biologicas = "biologicas"

class StatusTurno(enum.Enum):
    matutino = "matutino"
    vespertino = "vespertino"
    noturno = "noturno"

class Turma(Base):
    __tablename__ = 'turmas'
    id_Turma = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False, unique=True)
    turmas = relationship("Cursos", secondary=curso_turma, back_populates="turmas") # Relação N:N
    alunos = relationship("Aluno", backref="turma") # Relação 1:N


class Genero(Base):
    __tablename__ = 'generos'
    id_Genero = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String, nullable=False, unique=True)
    alunos = relationship("Aluno", backref="genero") #Relação N:1
    professores = relationship("Professor", backref="genero") #Relação N:1

class Pcd(Base):
    __tablename__ = 'pcds'
    id_Pcd = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String, nullable=False, unique=True)
    alunos = relationship("Aluno", backref="genero") #Relação N:1
    professores = relationship("Professor", backref="genero") #Relação N:1

    

class Raca(Base):
    __tablename__ = 'racas'
    id_Raca = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String, nullable=False, unique=True)
    alunos = relationship("Aluno", backref="genero") #Relação N:1
    professores = relationship("Professor", backref="genero") #Relação N:1

class Aluno(Base):
    __tablename__ = 'alunos'
    id_Aluno = Column(Integer, primary_key=True, autoincrement=True)
    id_Genero = Column(Integer, ForeignKey('generos.id_Genero'))
    id_Pcd = Column(Integer, ForeignKey('pcds.id_Pcd'))
    id_Raca = Column(Integer, ForeignKey('racas.id_Raca'))
    id_Turma = Column(Integer, ForeignKey('turmas.id_Turma'))
    nome = Column(String, nullable=False)
    datanasc = Column(String)
    cpf = Column(String(11))
    email = Column(String, nullable=False, unique=True)
    telefone = Column(String(11)) #11999999999
    endereco = Column(String)
    dt_matricula = Column(Date)
    dt_conclusao = Column(Date)
    observacoes = Column(String)
    presenca = Column(Enum(StatusPresenca), default=StatusPresenca.falta)
    e_faltoso = Column(Integer, default=0)
    

class Curso(Base):
    __tablename__ = 'cursos'
    id_Curso = Column(Integer, primary_key=True, autoincrement=True)
    id_Professor = Column(Integer, ForeignKey('professores.id_Professor'))
    nome = Column(String, nullable=False, unique=True)
    area = Column(Enum(StatusArea), nullable=False)
    turno = Column(Enum(StatusTurno))
    professor = relationship("Professor", backref="cursos") # Relação N:1

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
    endereco = Column(String)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")


