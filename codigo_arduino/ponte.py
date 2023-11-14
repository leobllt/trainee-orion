from pyfirmata import Arduino, util
import time

class ArduinoUno:
    def __init__(self, porta):
        # dados fixos
        self.limiar = 5000 # ppm, valor recomendado no datasheet
        self.sensorMin = 200 # ppm
        self.sensorMax = 10000 # ppm
        # atributos
        self.porta = porta
        self.board = None
        self.pinoSensorGas = None
        self.pinoLedVerde = None
        self.pinoLedAmarelo = None
        self.pinoLedVermelho = None 
        self.emergencia = False
        self.it = None
        self.config()
    
    def config(self):
        # iniciando microcontrolador
        try:
            self.board = Arduino(self.porta)
            # obtendo portas
            self.pinoSensorGas = self.board.get_pin('a:0:i')
            if self.pinoSensorGas == None:
                raise RuntimeError("Porta A0")
            self.pinoLedVerde = self.board.get_pin('d:13:o')
            if self.pinoLedVerde == None:
                raise RuntimeError("Porta 13")
            self.pinoLedAmarelo = self.board.get_pin('d:12:o')
            if self.pinoLedAmarelo == None:
                raise RuntimeError("Porta 12")
            self.pinoLedVermelho = self.board.get_pin('d:11:o')
            if self.pinoLedVermelho == None:
                raise RuntimeError("Porta 11")
            print("Arduino carregado.")
        except Exception as e:
            self.board = None
            print("Erro " + str(e))
            return
        
        self.it = util.Iterator(self.board)
        self.it.start()
        self.pinoSensorGas.enable_reporting()

    # método para ligar/desligar amarelo
    def alternarEmergencia(self):
        self.emergencia = not self.emergencia
        if(self.emergencia):
            self.pinoLedAmarelo.write(1)
            self.pinoLedVerde.write(0)
            self.pinoLedVermelho.write(0)
        else:
            self.pinoLedAmarelo.write(0)
    
    # método que retorna um dado lido
    def lerDados(self):    
        if self.emergencia:
            return    
        valorLido = self.pinoSensorGas.read()
        if valorLido == None:
            print('nao leu do analogico')

        ''' De acordo com o datasheet, a corrente lida cresce
            linearmente em relação à concentração de CH4. '''
        valorConvertido = Calc.map_range(valorLido, 0, 1, self.sensorMin, self.sensorMax)

        OK = valorConvertido < self.limiar
        self.pinoLedVerde.write(OK)
        self.pinoLedVermelho.write(not OK)
        
        return (valorLido, valorConvertido, OK)


class Calc:
    @staticmethod
    def map_range(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min