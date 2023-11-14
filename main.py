# Arquivo principal do aplicativo, responsável por gerenciar tudo

import sys
from PySide6.QtWidgets import (QMainWindow, QApplication, QHBoxLayout, QWidget)
from PySide6.QtCore import (Qt, QFile, QTextStream, QDir, QTimer)
from PySide6.QtGui import QFontDatabase
from src.grafico import Grafico
from src.gui import JanelaInterativa
from src.datasource import DataSource
from codigo_arduino.ponte import ArduinoUno

# É a janela pai de todas as demais
# também contém as variáveis usadas no programa todo
class JanelaPrincipal(QMainWindow):
	def __init__(self):
		super().__init__()
		self.arduino = None
		self.conectado = False
		self.timer = None
		self.build()

	def build(self):
		# carregando estilos:
		file = QFile("styles/gui.qss")
		if not file.open(QFile.ReadOnly):
			print("Erro ao abrir arquivo de estilos.")
		else:
			self.stylesheet = QTextStream(file).readAll()
			self.setStyleSheet(self.stylesheet)

		# definindo o layout / disposição de cada componente
		layout = QHBoxLayout() # na horizontal		
		# são duas seções, lado a lado
		self.secao1 = JanelaInterativa(self)
		self.secao2 = Grafico()
		layout.addWidget(self.secao1)
		layout.addWidget(self.secao2)
		layout.setAlignment(Qt.AlignTop)
		#layout.setContentsMargins(5, 0, 0, 5)

		# criando o container, para aplicar o layout
		innerWindow = QWidget(self) 
		innerWindow.setLayout(layout)
		self.setCentralWidget(innerWindow)

		# configurações da janela
		self.setWindowTitle("Sistema de monitoramento")
		self.setMinimumSize(1000, 500)
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.loop)
		self.timer.start(100)

	
	def conectar(self, porta):
		if self.conectado:
			return
		
		self.arduino = ArduinoUno(porta)
		if self.arduino.board == None:
			return
		# se chegou até aqui, conexão foi estabelecida
		self.conectado = True
	
	def loop(self):
		if self.conectado:
			valorLido, valorConvertido, OK = self.arduino.lerDados()
			self.secao1.mostrarDados(valorConvertido, OK)
			self.secao2.adicionarValor(valorConvertido)
	
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()
	
	def closeEvent(self,event):
		self.arduino.board.exit()
		event.accept()
			

# INICIO
if __name__ == '__main__':
	# criando app e janela principal onde trabalharemos
	app = QApplication(sys.argv)
	dir_ = QDir("styles")
	QFontDatabase.addApplicationFont("styles/Jost-Regular.ttf")
	window = JanelaPrincipal()
	window.show()
	sys.exit(app.exec())