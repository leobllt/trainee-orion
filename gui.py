import time
from PySide6.QtWidgets import *
from PySide6.QtCore import (Qt, QSize)
#from PySide6.QtGui import QValidator


# Janela com interação: botões, inputs...
class JanelaInterativa(QWidget):
    def __init__(self):
        super().__init__()
        self.build()
    
    def build(self):
        # definindo o layout / disposição de cada componente
        layout = QVBoxLayout() # na vertical
        # COMPONENTES:
        # combo 1 {
        label1 = QLabel("PORTA: ")
        input1 = QLineEdit()
        input1.setPlaceholderText("COM")
        self.button1 = QPushButton("CONECTAR")
        self.button1.clicked.connect(self.buttonAction)
        combo1 = Combo([label1, input1, self.button1])
        layout.addWidget(combo1)
        layout.addSpacing(15)
        # }

        # combo 2 {
        label2 = QLabel("STATUS:")
        label2.setFixedHeight(20)
        self.status = QLabel()
        self.status.setObjectName("status")
        self.status.setProperty("class", "statusDesligado")
        self.status.setFixedSize(QSize(50,20))
        combo2 = Combo([label2, self.status])
        temp = combo2.layout()
        temp.setSpacing(15)
        combo2.setLayout(temp)
        layout.addWidget(combo2)
        layout.addSpacing(20)
        # }
    
        # {
        label3 = QLabel("LOGS:")
        layout.addWidget(label3)
        self.logger = logsViewer()
        layout.addWidget(self.logger)
        # }

        # {
        self.button2 = QPushButton("⚠ EMERGÊNCIA")
        self.button2.setObjectName("botao2")
        self.button2.clicked.connect(self.buttonAction2)
        #self.button3 = QPushButton("LIMPAR LOGS")
        #self.button3.clicked.connect(self.buttonAction3)
        combo3 = Combo([self.button2])
        layout.addWidget(combo3)
        # }
        
        # demais configurações
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        self.setFixedSize(300, 500)
    
    # ação do botão 1
    def buttonAction(self):
        self.status.setProperty("class", "statusOK")
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)
        self.logger.alert("Conectado com sucesso!")
        self.logger.alert("Lendo dados...")
    
    # ação do botão 2
    def buttonAction2(self):
        self.status.setProperty("class", "statusEmergencia")
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)
        self.logger.alert("<b>ATENÇÃO: coloque água.</b>")
    
    # ação do botão 3
    def buttonAction3(self):
        self.logger.setText("")


# Janela para visualização: gráfico, logs...
class JanelaVisualizadora(QWidget):
    def __init__(self):
        super().__init__()
        self.build()
    
    def build(self):
        self.setFixedSize(700, 500)


# Widget que reúne 'subwidgets'/compenentes tal como num combo horizontal
class Combo(QWidget):
    def __init__(self, componentes):
        super().__init__()
        self.componentes = componentes
        self.build()

    def build(self):
        if self.componentes is None:
            return
        
        layout = QHBoxLayout()
        for componente in self.componentes:
            layout.addWidget(componente)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignLeft)
        self.setLayout(layout)
        

class logsViewer(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
    
    def alert(self, msg):
        t = time.localtime() # obtendo tempo real
        self.append(f'{time.strftime("%H:%M:%S", t)}: {msg}')