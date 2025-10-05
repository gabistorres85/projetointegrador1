import enum
import hashlib
from sqlalchemy import ForeignKey, Table, create_engine, Column, Integer, String, Date, DateTime, Enum
from sqlalchemy.orm import declarative_base, relationship, Session, Mapped, mapped_column
from sqlalchemy.sql import func

# conecta ao banco de dados 'curso.db'
# caso o banco não exista ele será criado
# Criar conexão com SQLite (arquivo local chamado banco.db)
engine = create_engine("sqlite:///banco.db", echo=True)

# Base para os modelos
Base = declarative_base()

# Tabela associativa para relação muitos-para-muitos entre Curso e Turma    
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
    usuario = Column(String, nullable=False)
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
    cursos = relationship("Curso", secondary=curso_turma, back_populates="turmas") # Relação N:N
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
    alunos = relationship("Aluno", backref="pcd") #Relação N:1
    professores = relationship("Professor", backref="pcd") #Relação N:1

    

class Raca(Base):
    __tablename__ = 'racas'
    id_Raca = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String, nullable=False, unique=True)
    alunos = relationship("Aluno", backref="raca") #Relação N:1
    professores = relationship("Professor", backref="raca") #Relação N:1

class Aluno(Base):
    __tablename__ = 'alunos'
    id_Aluno = Column(Integer, primary_key=True, autoincrement=True)
    id_Genero = Column(Integer, ForeignKey('generos.id_Genero'))
    id_Pcd = Column(Integer, ForeignKey('pcds.id_Pcd'))
    id_Raca = Column(Integer, ForeignKey('racas.id_Raca'))
    id_Turma = Column(Integer, ForeignKey('turmas.id_Turma'))
    nome = Column(String, nullable=False)
    dt_nasc = Column(Date)
    cpf = Column(String(11),unique=True, nullable=False)
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
    turmas = relationship("Turma", secondary=curso_turma, back_populates="cursos") # Relação N:N

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

    with Session(engine) as session:
        # criando as tabelas de gênero, raça e pcd
        branco = Raca(descricao="branco")
        pardo = Raca(descricao="pardo")
        preto = Raca(descricao="preto")
        amarelo = Raca(descricao="amarelo")
        indigena = Raca(descricao="indigena")
    
        nao_declarado_raca = Raca(descricao="nao declarado")
        homem_cis = Genero(descricao="homem-cis")
        mulher_cis = Genero(descricao="mulher-cis")
        homem_trans = Genero(descricao="homem-trans")
        mulher_trans = Genero(descricao="mulher-trans")
        nao_binario = Genero(descricao="não-binario")
        nao_declarado_genero = Genero(descricao="nao declarado")
        
        deficiencia_fisica = Pcd(descricao="deficiencia fisica")
        deficiencia_auditiva = Pcd(descricao="deficiencia auditiva")
        deficiencia_visual = Pcd(descricao="deficiencia visual")   
        deficiencia_intelectual = Pcd(descricao="deficiencia intelectual")
        neurodivergencia = Pcd(descricao="neurodivergencia")
        nao_declarado_pcd = Pcd(descricao="nao declarado")  

    session.add_all([branco, pardo, preto, amarelo, indigena, nao_declarado_raca,
                    homem_cis, mulher_cis, homem_trans, mulher_trans, nao_binario, nao_declarado_genero,
                    deficiencia_fisica, deficiencia_intelectual, deficiencia_auditiva, deficiencia_visual, nao_declarado_pcd])

    session.commit()
    print("Dados iniciais inseridos com sucesso!")

