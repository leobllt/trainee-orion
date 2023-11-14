# Arquivo com a classe para gerar o gráfico de linhas

from PySide6.QtGui import (QPainter, QColor, QBrush, QFont, QPen)
from PySide6.QtCharts import (QChart, QChartView, QValueAxis, QLineSeries)
from PySide6.QtCore import Qt

# Line plot
class Grafico(QChartView):
    def __init__(self):
        super().__init__()
        self.qtdMax = 20 # qt max de valores na tela no momento
        self.actual_min = 0 # min valor do eixo x
        self.x = 0 # inicio
        self.build()

    def build(self):
        # criando série
        self.series = QLineSeries()
        # customizando série
        pen = QPen(QColor.fromRgb(253, 177, 87))
        pen.setWidth(3)
        self.series.setPen(pen)

        # criando gráfico
        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.series)

        # Personalizando
        fonte = QFont()
        fonte.setFamily("Jost")
        fonte.setPixelSize(16)
        fonte.setBold(True)
        self.chart.setTitleFont(fonte)
        self.chart.setTitle("Concentração de gás CH4")
        self.chart.setTitleBrush(QBrush(Qt.white))
        self.chart.setBackgroundBrush(QBrush(QColor().fromRgb(34, 34, 34)))
        
        # Eixo x:
        eixoX = QValueAxis()
        eixoX.setTitleText("Tempo")
        eixoX.setTitleBrush(QBrush(Qt.white))
        eixoX.setLabelsBrush(QBrush(Qt.white))
        eixoX.setGridLineVisible(False)
        eixoX.setVisible(False)
        self.chart.addAxis(eixoX, Qt.AlignBottom)
        self.series.attachAxis(eixoX)

        # Eixo y:
        eixoY = QValueAxis()
        eixoY.setTitleText("PPM")
        fonte2 = QFont()
        fonte2.setFamily("Jost")
        eixoY.setTitleFont(fonte2)
        eixoY.setTitleBrush(QBrush(Qt.white))
        eixoY.setLabelsBrush(QBrush(Qt.white))
        eixoY.setRange(200, 10000)
        eixoY.setTickCount(10)
        #eixoY.setTickInterval()
        eixoY.setLabelFormat("%.2f")
        self.chart.addAxis(eixoY, Qt.AlignLeft)
        self.series.attachAxis(eixoY)

        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(QBrush(QColor().fromRgb(34, 34, 34)))

    def adicionarValor(self, y):
        self.x += 1
        self.series.append(self.x, y)

        if self.series.count() > self.qtdMax:
            self.series.remove(0)
            self.actual_min = self.series.at(0).x()

        self.chart.axisX().setRange(self.actual_min, self.series.count() + self.actual_min)
        #self.repaint()