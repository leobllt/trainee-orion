#define pinoSensorGas A0 // sensor MQ4
#define pinoLedVerde 13
#define pinoLedAmarelo 12
#define pinoLedVermelho 11
#define limiar 5000 // ppm, valor recomendado no datasheet
#define sensorMin 200 // ppm
#define sensorMax 10000 // ppm

unsigned int valorLido = 0;
unsigned int valorConvertido = 0;
// Estado de emergência depende da interação com usuário
bool emergencia = false;

void setup()
{
  Serial.begin(9600);
  pinMode(pinoSensorGas, INPUT);
  pinMode(pinoLedVerde, OUTPUT);
  pinMode(pinoLedAmarelo, OUTPUT);
  pinMode(pinoLedVermelho, OUTPUT); 
  
  Serial.println("Lendo do sensor...");
  delay(1000);
}

void loop()
{
  valorLido = analogRead(pinoSensorGas);
  /* 
    De acordo com o datasheet, a corrente lida cresce
    linearmente em relação à concentração de CH4.
  */
  valorConvertido = map(valorLido, 0, 1023, sensorMin, sensorMax);
  Serial.println(String(valorLido) + " | " + String(valorConvertido) + " ppm");

  if(emergencia){
    digitalWrite(pinoLedAmarelo, HIGH);
    digitalWrite(pinoLedVerde, LOW);
    digitalWrite(pinoLedVermelho, LOW);
    //Serial.println("Adicione água!");
  }
  else if(valorConvertido > limiar)
  {
    digitalWrite(pinoLedVermelho, HIGH);
    digitalWrite(pinoLedVerde, LOW);
    digitalWrite(pinoLedAmarelo, LOW);
  }
  else
  {
    digitalWrite(pinoLedVerde, HIGH);
    digitalWrite(pinoLedVermelho, LOW);
    digitalWrite(pinoLedAmarelo, LOW);
  }

}
