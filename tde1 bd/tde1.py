from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QStackedWidget, QWidget, 
                             QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QFormLayout,
                             QTabWidget, QGroupBox, QMessageBox, QTableWidget, QTableWidgetItem,
                             QHeaderView, QDateEdit, QTextEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
import sys

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

    def create(self, session, data):
        self.nome = data['nome']
        self.cpf = data['cpf']
        self.data_nascimento = data['data_nascimento']
        self.email = data['email']
        self.endereco = data['endereco']
        self.cep = data['cep']
        session.add(self)
        session.commit()
        return True

    def read(self, session, aluno_id=None):
        if aluno_id is None:
            return session.query(Aluno).all()
        return session.query(Aluno).filter_by(id_aluno=aluno_id).first()

    def update(self, session, data):
        if data['nome']:
            self.nome = data['nome']
        if data['cpf']:
            self.cpf = data['cpf']
        if data['data_nascimento']:
            self.data_nascimento = data['data_nascimento']
        if data['email']:
            self.email = data['email']
        if data['endereco']:
            self.endereco = data['endereco']
        if data['cep']:
            self.cep = data['cep']
        session.commit()
        return True

    def delete(self, session, aluno_id):
        aluno = session.query(Aluno).filter_by(id_aluno=aluno_id).first()
        if aluno:
            session.delete(aluno)
            session.commit()
            return True
        return False

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

    def create(self, session, data):
        self.nome = data['nome']
        self.cpf = data['cpf']
        self.data_nascimento = data['data_nascimento']
        self.email = data['email']
        self.endereco = data['endereco']
        self.cep = data['cep']
        self.cargo = data['cargo']
        self.formacao = data['formacao']
        self.horas_aulas = data['horas_aulas']
        session.add(self)
        session.commit()
        return True

    def read(self, session, docente_id=None):
        if docente_id is None:
            return session.query(Docente).all()
        return session.query(Docente).filter_by(id_professor=docente_id).first()

    def update(self, session, data):
        if data['nome']:
            self.nome = data['nome']
        if data['cpf']:
            self.cpf = data['cpf']
        if data['data_nascimento']:
            self.data_nascimento = data['data_nascimento']
        if data['email']:
            self.email = data['email']
        if data['endereco']:
            self.endereco = data['endereco']
        if data['cep']:
            self.cep = data['cep']
        if data['cargo']:
            self.cargo = data['cargo']
        if data['formacao']:
            self.formacao = data['formacao']
        if data['horas_aulas']:
            self.horas_aulas = data['horas_aulas']
        session.commit()
        return True

    def delete(self, session, docente_id):
        docente = session.query(Docente).filter_by(id_professor=docente_id).first()
        if docente:
            session.delete(docente)
            session.commit()
            return True
        return False

class Materia(Base):
    __tablename__ = 'materia'

    id_materia = Column(Integer, primary_key=True)
    nome = Column(String)
    qtd_materias = Column(Integer)
    turmas = relationship("Turma", secondary=turma_materia, back_populates="materias")

    def create(self, session, data):
        self.nome = data['nome']
        self.qtd_materias = data['qtd_materias']
        session.add(self)
        session.commit()
        return True

    def read(self, session, materia_id=None):
        if materia_id is None:
            return session.query(Materia).all()
        return session.query(Materia).filter_by(id_materia=materia_id).first()

    def update(self, session, data):
        if data['nome']:
            self.nome = data['nome']
        if data['qtd_materias']:
            self.qtd_materias = data['qtd_materias']
        session.commit()
        return True

    def delete(self, session, materia_id):
        materia = session.query(Materia).filter_by(id_materia=materia_id).first()
        if materia:
            session.delete(materia)
            session.commit()
            return True
        return False

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
    matriculas = relationship("Matricula", back_populates="turma")

    def create(self, session, data):
        self.n_sala = data['n_sala']
        self.qtd_alunos = data['qtd_alunos']
        self.serie = data['serie']
        self.grade_horaria = data['grade_horaria']
        self.docente_id = data['docente_id']
        session.add(self)
        session.commit()
        return True

    def read(self, session, turma_id=None):
        if turma_id is None:
            return session.query(Turma).all()
        return session.query(Turma).filter_by(id_turma=turma_id).first()

    def update(self, session, data):
        if data['n_sala']:
            self.n_sala = data['n_sala']
        if data['qtd_alunos']:
            self.qtd_alunos = data['qtd_alunos']
        if data['serie']:
            self.serie = data['serie']
        if data['grade_horaria']:
            self.grade_horaria = data['grade_horaria']
        if data['docente_id']:
            self.docente_id = data['docente_id']
        session.commit()
        return True

    def delete(self, session, turma_id):
        turma = session.query(Turma).filter_by(id_turma=turma_id).first()
        if turma:
            session.delete(turma)
            session.commit()
            return True
        return False

class Matricula(Base):
    __tablename__ = 'matricula'

    id_matricula = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey('aluno.id_aluno'))
    aluno = relationship("Aluno", back_populates="matriculas")
    turma_id = Column(Integer, ForeignKey('turma.id_turma'))
    turma = relationship("Turma", back_populates="matriculas")
    boletos = relationship("Boleto", back_populates="matricula")

    def create(self, session, data):
        self.aluno_id = data['aluno_id']
        self.turma_id = data['turma_id']
        session.add(self)
        session.commit()
        return True

    def read(self, session, matricula_id=None):
        if matricula_id is None:
            return session.query(Matricula).all()
        return session.query(Matricula).filter_by(id_matricula=matricula_id).first()

    def update(self, session, data):
        if data['aluno_id']:
            self.aluno_id = data['aluno_id']
        if data['turma_id']:
            self.turma_id = data['turma_id']
        session.commit()
        return True

    def delete(self, session, matricula_id):
        matricula = session.query(Matricula).filter_by(id_matricula=matricula_id).first()
        if matricula:
            session.delete(matricula)
            session.commit()
            return True
        return False

class Boleto(Base):
    __tablename__ = 'boleto'

    id_boleto = Column(Integer, primary_key=True)
    matricula_id = Column(Integer, ForeignKey('matricula.id_matricula'))
    valor = Column(Float)
    data_vencimento = Column(Date)
    data_emissao = Column(Date)
    desconto = Column(Integer)
    matricula = relationship("Matricula", back_populates="boletos")
    forma_pagamento = relationship("FormaPagamento", back_populates="boleto")

    def create(self, session, data):
        self.matricula_id = data['matricula_id']
        self.valor = data['valor']
        self.data_vencimento = data['data_vencimento']
        self.data_emissao = data['data_emissao']
        self.desconto = data['desconto']
        session.add(self)
        session.commit()
        return True

    def read(self, session, boleto_id=None):
        if boleto_id is None:
            return session.query(Boleto).all()
        return session.query(Boleto).filter_by(id_boleto=boleto_id).first()

    def update(self, session, data):
        if data['valor']:
            self.valor = data['valor']
        if data['data_vencimento']:
            self.data_vencimento = data['data_vencimento']
        if data['data_emissao']:
            self.data_emissao = data['data_emissao']
        if data['desconto']:
            self.desconto = data['desconto']
        session.commit()
        return True

    def delete(self, session, boleto_id):
        boleto = session.query(Boleto).filter_by(id_boleto=boleto_id).first()
        if boleto:
            session.delete(boleto)
            session.commit()
            return True
        return False

class Salario(Base):
    __tablename__ = 'salario'

    id_salario = Column(Integer, primary_key=True)
    docente_id = Column(Integer, ForeignKey('docente.id_professor'))
    valor = Column(Float)
    data_pagamento = Column(Date)
    docente = relationship("Docente", back_populates="salarios")

    def create(self, session, data):
        self.docente_id = data['docente_id']
        self.valor = data['valor']
        self.data_pagamento = data['data_pagamento']
        session.add(self)
        session.commit()
        return True

    def read(self, session, salario_id=None):
        if salario_id is None:
            return session.query(Salario).all()
        return session.query(Salario).filter_by(id_salario=salario_id).first()

    def update(self, session, data):
        if data['valor']:
            self.valor = data['valor']
        if data['data_pagamento']:
            self.data_pagamento = data['data_pagamento']
        session.commit()
        return True

    def delete(self, session, salario_id):
        salario = session.query(Salario).filter_by(id_salario=salario_id).first()
        if salario:
            session.delete(salario)
            session.commit()
            return True
        return False

class FormaPagamento(Base):
    __tablename__ = 'forma_pagamento'

    id_forma_pagamento = Column(Integer, primary_key=True)
    boleto_id = Column(Integer, ForeignKey('boleto.id_boleto'))
    descricao = Column(String)
    parcela = Column(Integer)
    boleto = relationship("Boleto", back_populates="forma_pagamento")

    def create(self, session, data):
        self.boleto_id = data['boleto_id']
        self.descricao = data['descricao']
        self.parcela = data['parcela']
        session.add(self)
        session.commit()
        return True

    def read(self, session, forma_pagamento_id=None):
        if forma_pagamento_id is None:
            return session.query(FormaPagamento).all()
        return session.query(FormaPagamento).filter_by(id_forma_pagamento=forma_pagamento_id).first()

    def update(self, session, data):
        if data['descricao']:
            self.descricao = data['descricao']
        if data['parcela']:
            self.parcela = data['parcela']
        session.commit()
        return True

    def delete(self, session, forma_pagamento_id):
        forma_pagamento = session.query(FormaPagamento).filter_by(id_forma_pagamento=forma_pagamento_id).first()
        if forma_pagamento:
            session.delete(forma_pagamento)
            session.commit()
            return True
        return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.apply_styles()
        self.load_initial_data()

    def setup_ui(self):
        self.setWindowTitle("Sistema de Gestão Escolar")
        self.setGeometry(100, 100, 1000, 700)

        # Widget central e layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Cabeçalho
        header = QLabel("Sistema de Gestão Escolar")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                background-color: #2c3e50;
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 15px;
                border-radius: 5px;
            }
        """)
        main_layout.addWidget(header)

        # Widget de abas
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Criar as abas
        self.create_aluno_tab()
        self.create_docente_tab()


        # Status bar
        self.statusBar().showMessage("Sistema de Gestão Escolar")

    def apply_styles(self):
        # Aplicar estilo geral
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                background: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #95a5a6;
                color: white;
                padding: 8px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #3498db;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QLineEdit, QDateEdit, QComboBox, QTextEdit {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QTableWidget {
                gridline-color: #bdc3c7;
                background-color: white;
                alternate-background-color: #f5f5f5;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 5px;
                border: none;
            }
        """)

    def load_initial_data(self):
        # Carregar dados iniciais se necessário
        pass

    def create_aluno_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Formulário de aluno
        form_group = QGroupBox("Cadastro de Aluno")
        form_layout = QFormLayout()

        self.aluno_id = QLineEdit()
        self.aluno_id.setPlaceholderText("Deixe em branco para novo cadastro")
        self.aluno_nome = QLineEdit()
        self.aluno_cpf = QLineEdit()
        self.aluno_data_nasc = QDateEdit()
        self.aluno_data_nasc.setDate(QDate.currentDate())
        self.aluno_email = QLineEdit()
        self.aluno_endereco = QTextEdit()
        self.aluno_endereco.setMaximumHeight(80)
        self.aluno_cep = QLineEdit()

        form_layout.addRow("ID:", self.aluno_id)
        form_layout.addRow("Nome*:", self.aluno_nome)
        form_layout.addRow("CPF*:", self.aluno_cpf)
        form_layout.addRow("Data Nascimento:", self.aluno_data_nasc)
        form_layout.addRow("Email:", self.aluno_email)
        form_layout.addRow("Endereço:", self.aluno_endereco)
        form_layout.addRow("CEP:", self.aluno_cep)

        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        # Botões de ação
        button_layout = QHBoxLayout()
        self.btn_salvar_aluno = QPushButton("Salvar")
        self.btn_ler_aluno = QPushButton("Buscar")
        self.btn_atualizar_aluno = QPushButton("Atualizar")
        self.btn_deletar_aluno = QPushButton("Deletar")
        self.btn_limpar_aluno = QPushButton("Limpar")

        self.btn_salvar_aluno.clicked.connect(self.save_aluno)
        self.btn_ler_aluno.clicked.connect(self.read_aluno)
        self.btn_atualizar_aluno.clicked.connect(self.update_aluno)
        self.btn_deletar_aluno.clicked.connect(self.delete_aluno)
        self.btn_limpar_aluno.clicked.connect(self.clear_aluno_fields)

        button_layout.addWidget(self.btn_salvar_aluno)
        button_layout.addWidget(self.btn_ler_aluno)
        button_layout.addWidget(self.btn_atualizar_aluno)
        button_layout.addWidget(self.btn_deletar_aluno)
        button_layout.addWidget(self.btn_limpar_aluno)

        layout.addLayout(button_layout)

        # Tabela de alunos
        self.aluno_table = QTableWidget()
        self.aluno_table.setColumnCount(7)
        self.aluno_table.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "Nascimento", "Email", "Endereço", "CEP"])
        self.aluno_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.aluno_table)

        self.tabs.addTab(tab, "Alunos")

    def create_docente_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Formulário de docente (similar ao de aluno)
        form_group = QGroupBox("Cadastro de Docente")
        form_layout = QFormLayout()
        
        # Adicione campos para docente aqui
        self.docente_id = QLineEdit()
        self.docente_nome = QLineEdit()
        self.docente_cpf = QLineEdit()
        self.docente_data_nasc = QDateEdit()
        self.docente_data_nasc.setDate(QDate.currentDate())
        self.docente_email = QLineEdit()
        self.docente_endereco = QTextEdit()
        self.docente_endereco.setMaximumHeight(80)
        self.docente_cep = QLineEdit()
        self.docente_cargo = QLineEdit()
        self.docente_formacao = QLineEdit()
        self.docente_horas_aulas = QLineEdit()
        
        form_layout.addRow("ID:", self.docente_id)
        form_layout.addRow("Nome*:", self.docente_nome)
        form_layout.addRow("CPF*:", self.docente_cpf)
        form_layout.addRow("Data Nascimento:", self.docente_data_nasc)
        form_layout.addRow("Email:", self.docente_email)
        form_layout.addRow("Endereço:", self.docente_endereco)
        form_layout.addRow("CEP:", self.docente_cep)
        form_layout.addRow("Cargo:", self.docente_cargo)
        form_layout.addRow("Formação:", self.docente_formacao)
        form_layout.addRow("Horas/Aula:", self.docente_horas_aulas)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Botões de ação
        button_layout = QHBoxLayout()
        self.btn_salvar_docente = QPushButton("Salvar")
        self.btn_ler_docente = QPushButton("Buscar")
        self.btn_atualizar_docente = QPushButton("Atualizar")
        self.btn_deletar_docente = QPushButton("Deletar")
        self.btn_limpar_docente = QPushButton("Limpar")
        
        button_layout.addWidget(self.btn_salvar_docente)
        button_layout.addWidget(self.btn_ler_docente)
        button_layout.addWidget(self.btn_atualizar_docente)
        button_layout.addWidget(self.btn_deletar_docente)
        button_layout.addWidget(self.btn_limpar_docente)
        
        layout.addLayout(button_layout)
        
        # Tabela de docentes
        self.docente_table = QTableWidget()
        self.docente_table.setColumnCount(9)
        self.docente_table.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "Nascimento", "Email", "Cargo", "Formação", "Horas/Aula", "Endereço"])
        self.docente_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.docente_table)
        
        self.tabs.addTab(tab, "Docentes")

    def create_materia_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Formulário de matéria
        form_group = QGroupBox("Cadastro de Matéria")
        form_layout = QFormLayout()
        
        self.materia_id = QLineEdit()
        self.materia_nome = QLineEdit()
        self.materia_qtd = QLineEdit()
        
        form_layout.addRow("ID:", self.materia_id)
        form_layout.addRow("Nome*:", self.materia_nome)
        form_layout.addRow("Quantidade:", self.materia_qtd)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Botões de ação
        button_layout = QHBoxLayout()
        self.btn_salvar_materia = QPushButton("Salvar")
        self.btn_ler_materia = QPushButton("Buscar")
        self.btn_atualizar_materia = QPushButton("Atualizar")
        self.btn_deletar_materia = QPushButton("Deletar")
        self.btn_limpar_materia = QPushButton("Limpar")
        
        button_layout.addWidget(self.btn_salvar_materia)
        button_layout.addWidget(self.btn_ler_materia)
        button_layout.addWidget(self.btn_atualizar_materia)
        button_layout.addWidget(self.btn_deletar_materia)
        button_layout.addWidget(self.btn_limpar_materia)
        
        layout.addLayout(button_layout)
        

    def save_aluno(self):
        try:
            data = {
                'nome': self.aluno_nome.text(),
                'cpf': self.aluno_cpf.text(),
                'data_nascimento': self.aluno_data_nasc.date().toPyDate(),
                'email': self.aluno_email.text(),
                'endereco': self.aluno_endereco.toPlainText(),
                'cep': self.aluno_cep.text()
            }
            
            if not data['nome'] or not data['cpf']:
                QMessageBox.warning(self, "Aviso", "Nome e CPF são obrigatórios!")
                return
                
            aluno = Aluno()
            if aluno.create(session, data):
                QMessageBox.information(self, "Sucesso", "Aluno cadastrado com sucesso!")
                self.clear_aluno_fields()
                self.load_alunos_table()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar aluno: {str(e)}")

    def read_aluno(self):
        try:
            if not self.aluno_id.text():
                QMessageBox.warning(self, "Aviso", "Informe o ID do aluno para buscar!")
                return
        
            aluno_id = self.aluno_id.text()
            if aluno_id:
                aluno = Aluno().read(session, int(aluno_id))
                if aluno:
                    self.aluno_nome.setText(aluno.nome or "")
                    self.aluno_cpf.setText(aluno.cpf or "")
                    if aluno.data_nascimento:
                        self.aluno_data_nasc.setDate(QDate.fromString(aluno.data_nascimento.strftime("%Y-%m-%d"), "yyyy-MM-dd"))
                    self.aluno_email.setText(aluno.email or "")
                    self.aluno_endereco.setPlainText(aluno.endereco or "")
                    self.aluno_cep.setText(aluno.cep or "")
                else:
                    QMessageBox.warning(self, "Aviso", "Aluno não encontrado!")
            else:
                self.load_alunos_table()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao buscar aluno: {str(e)}")

    def update_aluno(self):
        try:
            if not self.aluno_id.text():
                QMessageBox.warning(self, "Aviso", "Informe o ID do aluno para atualizar!")
                return
                
            data = {
                'nome': self.aluno_nome.text(),
                'cpf': self.aluno_cpf.text(),
                'data_nascimento': self.aluno_data_nasc.date().toPyDate(),
                'email': self.aluno_email.text(),
                'endereco': self.aluno_endereco.toPlainText(),
                'cep': self.aluno_cep.text()
            }
            
            aluno = Aluno().read(session, int(self.aluno_id.text()))
            if aluno and aluno.update(session, data):
                QMessageBox.information(self, "Sucesso", "Aluno atualizado com sucesso!")
                self.clear_aluno_fields()
                self.load_alunos_table()
            else:
                QMessageBox.warning(self, "Aviso", "Aluno não encontrado!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar aluno: {str(e)}")

    def delete_aluno(self):
        try:
            if not self.aluno_id.text():
                QMessageBox.warning(self, "Aviso", "Informe o ID do aluno para excluir!")
                return
                
            reply = QMessageBox.question(self, "Confirmação", 
                                        "Tem certeza que deseja excluir este aluno?",
                                        QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                if Aluno().delete(session, int(self.aluno_id.text())):
                    QMessageBox.information(self, "Sucesso", "Aluno excluído com sucesso!")
                    self.clear_aluno_fields()
                    self.load_alunos_table()
                else:
                    QMessageBox.warning(self, "Aviso", "Aluno não encontrado!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao excluir aluno: {str(e)}")

    def clear_aluno_fields(self):
        self.aluno_id.clear()
        self.aluno_nome.clear()
        self.aluno_cpf.clear()
        self.aluno_data_nasc.setDate(QDate.currentDate())
        self.aluno_email.clear()
        self.aluno_endereco.clear()
        self.aluno_cep.clear()

    def load_alunos_table(self):
        try:
            alunos = Aluno().read(session)
            self.aluno_table.setRowCount(len(alunos))
            
            for row, aluno in enumerate(alunos):
                self.aluno_table.setItem(row, 0, QTableWidgetItem(str(aluno.id_aluno)))
                self.aluno_table.setItem(row, 1, QTableWidgetItem(aluno.nome or ""))
                self.aluno_table.setItem(row, 2, QTableWidgetItem(aluno.cpf or ""))
                self.aluno_table.setItem(row, 3, QTableWidgetItem(
                    aluno.data_nascimento.strftime("%d/%m/%Y") if aluno.data_nascimento else ""))
                self.aluno_table.setItem(row, 4, QTableWidgetItem(aluno.email or ""))
                self.aluno_table.setItem(row, 5, QTableWidgetItem(aluno.endereco or ""))
                self.aluno_table.setItem(row, 6, QTableWidgetItem(aluno.cep or ""))
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar tabela: {str(e)}")


if __name__ == "__main__":
    Base.metadata.create_all(engine)  # cria as tabelas no SQLite
    app = QApplication(sys.argv)
    
    # Definir estilo da aplicação
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())