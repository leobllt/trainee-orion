# Arquivo com as classes do GUI

import time
from PySide6.QtWidgets import *
from PySide6.QtCore import (Qt, QSize)
#from PySide6.QtGui import QValidator
from src.grafico import Grafico


# Janela com interação: botões, inputs...
class JanelaInterativa(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.emergencia = False
        self.build()
    
    def build(self):
        # definindo o layout / disposição de cada componente
        layout = QVBoxLayout() # na vertical
        # COMPONENTES:
        # combo 1 {
        label1 = QLabel("PORTA: ")
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("COM")
        self.button1 = QPushButton("CONECTAR")
        self.button1.setObjectName("button1")
        self.button1.clicked.connect(self.buttonAction)
        combo1 = Combo([label1, self.input1, self.button1])
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

         # combo 3 {
        label3 = QLabel("CONCENTRAÇÃO HC4:")
        #label3.setFixedHeight(20)
        self.concentracao = QLabel('-')
        self.concentracao.setObjectName("concentracao")
        combo3 = Combo([label3, self.concentracao])
        temp = combo3.layout()
        temp.setSpacing(15)
        combo3.setLayout(temp)
        layout.addWidget(combo3)
        layout.addSpacing(20)
        # }
    
        # {
        label4 = QLabel("LOGS:")
        layout.addWidget(label4)
        self.logger = logsViewer()
        layout.addWidget(self.logger)
        layout.addSpacing(10)
        # }

        # {
        self.button2 = QPushButton("⚠ EMERGÊNCIA")
        self.button2.setObjectName("button2")
        self.button2.clicked.connect(self.buttonAction2)
        self.button2.setEnabled(False)
        #self.button3 = QPushButton("LIMPAR LOGS")
        #self.button3.clicked.connect(self.buttonAction3)
        combo3 = Combo([self.button2])
        layout.addWidget(combo3)
        # }
        
        # demais configurações
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        self.setFixedWidth(300)
    
    def setOK(self):
        self.status.setProperty("class", "statusOK")
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)

    def setEmergencia(self):
        self.status.setProperty("class", "statusEmergencia")
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)

    def unset(self):
        self.status.setProperty("class", "statusDesligado")
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)
    
    def setAlerta(self):
        self.status.setProperty("class", "statusAlerta")
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)

    # ação do botão 1
    def buttonAction(self):
        self.parent.conectar(self.input1.text())
        if self.parent.conectado:
            self.logger.alert("Conectado com sucesso!")
            self.logger.alert("Lendo dados...")  
            self.button1.setEnabled(False)
            self.button2.setEnabled(True)
        else:
            self.logger.alert("Erro ao se conectar.")  
    
    # ação do botão 2
    def buttonAction2(self):
        if self.parent.conectado:
            self.emergencia = not self.emergencia
            self.parent.arduino.alternarEmergencia()
            if(self.emergencia):
                self.setEmergencia()
                self.logger.alert('<b><span style="color:red;">ATENÇÃO: coloque água.</span></b>')
            else:
                self.unset()

    # ação do botão 3
    def buttonAction3(self):
        self.logger.setText("")

    def mostrarDados(self, valorConvertido, OK):
        self.concentracao.setText(f'{valorConvertido} PPM')
        if not self.emergencia:
            if OK:
                self.setOK()
            else:
                self.setAlerta()


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
        

# Widget de visualização de logs
class logsViewer(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
    
    def alert(self, msg):
        t = time.localtime() # obtendo tempo real
        self.append(f'<b>{time.strftime("%H:%M:%S", t)}:</b> {msg}')
