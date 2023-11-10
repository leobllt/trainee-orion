# Arquivo principal do aplicativo, responsável por gerenciar tudo

import sys
import time
from PySide6.QtWidgets import (QMainWindow, QApplication, QHBoxLayout, QWidget)
from PySide6.QtCore import (Qt, QFile, QTextStream, QDir)
from PySide6.QtGui import QFontDatabase
from src.grafico import Grafico
from src.gui import JanelaInterativa
from src.datasource import DataSource

# É a janela pai de todas as demais
# também contém as variáveis usadas no programa todo
class JanelaPrincipal(QMainWindow):
	def __init__(self):
		super().__init__()
		self.conexao = False
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

		# teste
		self.dados = enumerate(DataSource.dadosTeste())
	
	def conectar(self):
		#...
		if not self.conexao:
			self.conexao = True
			return True
		else:
			return False
	
	def teste(self):
		try:
			x, y = next(self.dados)
			self.secao2.adicionarValor(x, float(y))
			self.secao1.concentracao.setText(y + " ppm")
			if(float(y) >= 5000):
				self.secao1.setAlerta()
			else:
				self.secao1.setOK()
		except StopIteration:
			print('fim dados teste')
	
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()
		elif event.key() == Qt.Key_T and self.conexao:
			self.teste()
			

# INICIO
if __name__ == '__main__':
	# criando app e janela principal onde trabalharemos
	app = QApplication(sys.argv)
	dir_ = QDir("styles")
	QFontDatabase.addApplicationFont("styles/Jost-Regular.ttf")
	window = JanelaPrincipal()
	window.show()
	sys.exit(app.exec())