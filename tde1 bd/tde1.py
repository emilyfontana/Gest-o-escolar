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




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.apply_styles()
        self.load_initial_data()

    def setup_ui(self):
        self.setWindowTitle("Sistema de Gestão Escolar")
        self.setGeometry(100, 100, 1000, 700)

        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        
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

        
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

       
        self.create_aluno_tab()
 


       
        self.statusBar().showMessage("Sistema de Gestão Escolar")

    def apply_styles(self):
      
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
        
        pass

    def create_aluno_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        
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

        
        self.aluno_table = QTableWidget()
        self.aluno_table.setColumnCount(7)
        self.aluno_table.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "Nascimento", "Email", "Endereço", "CEP"])
        self.aluno_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.aluno_table)

        self.tabs.addTab(tab, "Alunos")


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
    Base.metadata.create_all(engine) 
    app = QApplication(sys.argv)
    
    
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())