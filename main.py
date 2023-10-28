import sys
from gui import (JanelaInterativa, JanelaVisualizadora)
from PySide6.QtWidgets import (QMainWindow, QApplication, QHBoxLayout, QWidget)
from PySide6.QtCore import (Qt, QFile, QTextStream)

# É a janela pai de todas as demais
# também contém as variáveis usadas no programa todo
class JanelaPrincipal(QMainWindow):
	def __init__(self):
		super().__init__()
		self.build()

	def build(self):
		# carregando estilos:
		file = QFile("gui.qss")
		if not file.open(QFile.ReadOnly):
			print("Erro ao abrir arquivo de estilos.")
		else:
			self.stylesheet = QTextStream(file).readAll()
			self.setStyleSheet(self.stylesheet)

		# definindo o layout / disposição de cada componente
		layout = QHBoxLayout() # na horizontal		
		# são duas seções, lado a lado
		secao1 = JanelaInterativa()
		secao2 = JanelaVisualizadora()
		layout.addWidget(secao1)
		layout.addWidget(secao2)
		layout.setAlignment(Qt.AlignTop)
		layout.setContentsMargins(5, 0, 0, 5)

		# criando o container, para aplicar o layout
		innerWindow = QWidget(self) 
		innerWindow.setLayout(layout)
		self.setCentralWidget(innerWindow)

		# configurações da janela
		self.setWindowTitle("Sistema de monitoramento")
		self.setFixedSize(1000, 500)



# INICIO
if __name__ == '__main__':
	# criando app e janela principal onde trabalharemos
	app = QApplication(sys.argv)
	window = JanelaPrincipal()
	window.show()
	sys.exit(app.exec())