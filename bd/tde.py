from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///escola.db', echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

turma_materia = Table(
    'turma_materia', Base.metadata,
    Column('id_turma', Integer, ForeignKey('turma.id_turma')),
    Column('id_materia', Integer, ForeignKey('materia.id_materia'))
)
class Aluno(Base):
    __tablename__ = 'aluno'

    id_aluno = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String, unique=True)
    data_nascimento = Column(Date)
    email = Column(String)
    endereco = Column(String)
    cep = Column(String)
    matriculas = relationship("Matricula", back_populates="aluno")

    def create(self, session):
        self.nome = input("Nome do aluno: ")
        self.cpf = input("CPF do aluno: ")
        self.email = input("Email do aluno: ")
        self.endereco = input("Endereço do aluno: ")
        self.cep = input("CEP do aluno: ")
        
        session.add(self)
        session.commit()
        print("Aluno criado com sucesso!")

    @staticmethod
    def read(session):
        aluno_id = int(input("ID do aluno: "))
        aluno = session.query(Aluno).filter_by(id_aluno=aluno_id).first()
        if aluno:
            print(f"Aluno encontrado: {aluno.nome}, CPF: {aluno.cpf}, Email: {aluno.email}")
        else:
            print("Aluno não encontrado!")

    def update(self, session):
        nome = input("Novo nome")
        if nome:
            self.nome = nome
        cpf = input("Novo CPF")
        if cpf:
            self.cpf = cpf

        email = input("Novo email ")
        if email:
            self.email = email
        endereco = input("Novo endereço")
        if endereco:
            self.endereco = endereco
        cep = input("Novo CEP")
        if cep:
            self.cep = cep
        session.commit()

    def delete(self, session):
        aluno_id = int(input("ID do aluno a ser excluído: "))
        aluno = session.query(Aluno).filter_by(id_aluno=aluno_id).first()
        if aluno:
            session.delete(aluno)
            session.commit()
            print("Aluno excluído com sucesso!")
        else:
            print("Aluno não encontrado!")

def menu_aluno(session):
    while True:
        print("\n1. Criar aluno")
        print("2. Ler aluno")
        print("3. Atualizar aluno")
        print("4. Deletar aluno")
        print("5. Sair")
        escolha = input("Escolha uma opção (1-5): ")

        if escolha == '1':
            aluno = Aluno() 
            aluno.create(session)
        elif escolha == '2':
            Aluno.read(session)  
        elif escolha == '3':
            aluno_id = int(input("ID do aluno a ser atualizado: "))
            aluno = session.query(Aluno).filter_by(id_aluno=aluno_id).first()
            if aluno:
                aluno.update(session)
            else:
                print("Aluno não encontrado!")
        elif escolha == '4':
            aluno_id = int(input("ID do aluno a ser excluído: "))
            aluno = session.query(Aluno).filter_by(id_aluno=aluno_id).first()
            if aluno:
                aluno.delete(session)
            else:
                print("Aluno não encontrado!")
        elif escolha == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


class Docente(Base):
    __tablename__ = 'docente'

    id_professor = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String, unique=True)
    data_nascimento = Column(Date)
    email = Column(String)
    endereco = Column(String)
    cep = Column(String)
    cargo = Column(String)
    formacao = Column(String)
    horas_aulas = Column(Float)
    salarios = relationship("Salario", back_populates="docente")
    turmas = relationship("Turma", back_populates="docente")

    def create(self, session):
        self.nome = input("Nome do docente: ")
        self.cpf = input("CPF do docente: ")
        self.data_nascimento = input("Data de nascimento (YYYY-MM-DD): ")
        self.email = input("Email do docente: ")
        self.endereco = input("Endereço do docente: ")
        self.cep = input("CEP do docente: ")
        self.cargo = input("Cargo do docente: ")
        self.formacao = input("Formação do docente: ")
        self.horas_aulas = float(input("Horas de aulas do docente: "))
        session.add(self)
        session.commit()

    def read(self, session):
        docente_id = int(input("ID do docente: "))
        return session.query(Docente).filter_by(id_professor=docente_id).first()

    def update(self, session):
        nome = input("Novo nome: ")
        if nome:
            self.nome = nome
        cpf = input("Novo CPF: ")
        if cpf:
            self.cpf = cpf
        data_nascimento = input("Nova data de nascimento: ")
        if data_nascimento:
            self.data_nascimento = data_nascimento
        email = input("Novo email: ")
        if email:
            self.email = email
        endereco = input("Novo endereço: ")
        if endereco:
            self.endereco = endereco
        cep = input("Novo CEP: ")
        if cep:
            self.cep = cep
        cargo = input("Novo cargo: ")
        if cargo:
            self.cargo = cargo
        formacao = input("Nova formação: ")
        if formacao:
            self.formacao = formacao
        horas_aulas = input("Novas horas de aulas: ")
        if horas_aulas:
            self.horas_aulas = float(horas_aulas)
        session.commit()

    def delete(self, session):
        docente_id = int(input("ID do docente a ser excluído: "))
        docente = session.query(Docente).filter_by(id_professor=docente_id).first()
        if docente:
            session.delete(docente)
            session.commit()

class Materia(Base):
    __tablename__ = 'materia'

    id_materia = Column(Integer, primary_key=True)
    nome = Column(String)
    qtd_materias = Column(Integer)
    turmas = relationship("Turma", secondary=turma_materia, back_populates="materias")

    def create(self, session):
        self.nome = input("Nome da matéria: ")
        self.qtd_materias = int(input("Quantidade de matérias: "))
        session.add(self)
        session.commit()

    def read(self, session):
        materia_id = int(input("ID da matéria: "))
        return session.query(Materia).filter_by(id_materia=materia_id).first()

    def update(self, session):
        nome = input("Novo nome: ")
        if nome:
            self.nome = nome
        qtd_materias = input("Nova quantidade de matérias: ")
        if qtd_materias:
            self.qtd_materias = int(qtd_materias)
        session.commit()

    def delete(self, session):
        materia_id = int(input("ID da matéria a ser excluída: "))
        materia = session.query(Materia).filter_by(id_materia=materia_id).first()
        if materia:
            session.delete(materia)
            session.commit()

class Turma(Base):
    __tablename__ = 'turma'

    id_turma = Column(Integer, primary_key=True)
    n_sala = Column(Integer)
    qtd_alunos = Column(Integer)
    serie = Column(String)
    grade_horaria = Column(String)
    docente_id = Column(Integer, ForeignKey('docente.id_professor'))
    docente = relationship("Docente", back_populates="turmas")
    materias = relationship("Materia", secondary=turma_materia, back_populates="turmas")

    def create(self, session):
        self.n_sala = int(input("Número da sala: "))
        self.qtd_alunos = int(input("Quantidade de alunos: "))
        self.serie = input("Série: ")
        self.grade_horaria = input("Grade horária: ")
        self.docente_id = int(input("ID do docente: "))
        session.add(self)
        session.commit()

    def read(self, session):
        turma_id = int(input("ID da turma: "))
        return session.query(Turma).filter_by(id_turma=turma_id).first()

    def update(self, session):
        n_sala = input("Novo número da sala: ")
        if n_sala:
            self.n_sala = int(n_sala)
        qtd_alunos = input("Nova quantidade de alunos: ")
        if qtd_alunos:
            self.qtd_alunos = int(qtd_alunos)
        serie = input("Nova série: ")
        if serie:
            self.serie = serie
        grade_horaria = input("Nova grade horária: ")
        if grade_horaria:
            self.grade_horaria = grade_horaria
        session.commit()

    def delete(self, session):
        turma_id = int(input("ID da turma a ser excluída: "))
        turma = session.query(Turma).filter_by(id_turma=turma_id).first()
        if turma:
            session.delete(turma)
            session.commit()

class Matricula(Base):
    __tablename__ = 'matricula'

    id_matricula = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey('aluno.id_aluno'))
    aluno = relationship("Aluno", back_populates="matriculas")
    turma_id = Column(Integer, ForeignKey('turma.id_turma'))
    turma = relationship("Turma")

    def create(self, session):
        self.aluno_id = int(input("ID do aluno: "))
        self.turma_id = int(input("ID da turma: "))
        session.add(self)
        session.commit()

    def read(self, session):
        matricula_id = int(input("ID da matrícula: "))
        return session.query(Matricula).filter_by(id_matricula=matricula_id).first()

    def delete(self, session):
        matricula_id = int(input("ID da matrícula a ser excluída: "))
        matricula = session.query(Matricula).filter_by(id_matricula=matricula_id).first()
        if matricula:
            session.delete(matricula)
            session.commit()


class Salario(Base):
    __tablename__ = 'salario'

    id_salario = Column(Integer, primary_key=True)
    valor = Column(Float)
    docente_id = Column(Integer, ForeignKey('docente.id_professor'))
    docente = relationship("Docente", back_populates="salarios")

    def create(self, session):
        self.valor = float(input("Valor do salário: "))
        self.docente_id = int(input("ID do docente: "))
        session.add(self)
        session.commit()

    def read(self, session):
        salario_id = int(input("ID do salário: "))
        return session.query(Salario).filter_by(id_salario=salario_id).first()

    def update(self, session):
        valor = input("Novo valor do salário: ")
        if valor:
            self.valor = float(valor)
        session.commit()

    def delete(self, session):
        salario_id = int(input("ID do salário a ser excluído: "))
        salario = session.query(Salario).filter_by(id_salario=salario_id).first()
        if salario:
            session.delete(salario)
            session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    menu_aluno(session)
