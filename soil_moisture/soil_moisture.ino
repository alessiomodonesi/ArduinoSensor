// Alessio Modonesi, Mattia Zanini
// Codice per il funzionamento del sensore di umidità
// Arduino MKR WAN 1310

#define WAITING_TIME 5000
#define ARRAY_SIZE(array) ((sizeof(array)) / (sizeof(array[0]))) // determina la lunghezza di un array

// media tra i vari valori
const int dry = 668;                             // 0% di umidità
const int wet = 306;                             // 100% di umidità
const byte sensori[] = {A0, A1, A2, A3, A4, A5}; // contiene tutti i pin analogici della scheda

bool stillChecking = true;
bool notConnected;
unsigned long sentMs; // timer per verificare la connessione

void setup()
{
  Serial.begin(9600); // imposta il canale di trasmissione a 9600 bts (baud)
  setupCheckUSB();
  Serial.println("Booting...");
}

void loop()
{
  checkUSB();
  if (!stillChecking)
    ReadSensors();
}

// inizializza il controllo del collegamento con lo script
void setupCheckUSB()
{
  pinMode(LED_BUILTIN, OUTPUT);
  blinkLed(1);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1500);
  sentMs = millis();
}

// verifica se l'arduino è collegato al pc (tramite lo script)
void checkUSB()
{
  if (stillChecking)
  {
    if (millis() - sentMs > WAITING_TIME)
    {
      if (!Serial.available())
      {
        // NO USB
        notConnected = true;
      }
      else
      {
        // USB CONNECTED
        digitalWrite(LED_BUILTIN, HIGH);
        notConnected = false;
      }

      stillChecking = false;
      Serial.println(!notConnected);

      if (!notConnected == true)
      {
        // USB CONNECTED
        blinkLed(3);
      }
      else
      {
        // NO USB
        blinkLed(2);
        digitalWrite(LED_BUILTIN, LOW);
      }
    }
  }
}

// legge serialmente tutti i 6 sensori connessi all'arduino
void ReadSensors()
{
  for (int i = 0; i < ARRAY_SIZE(sensori); i++)
  {
    int sensorVal = analogRead(sensori[i]);             // lettura analogica del singolo canale
    int percentuale = map(sensorVal, wet, dry, 100, 0); // converto un range di valori in percentuale
    if (!notConnected == true)
      // USB CONNECTED
      WriteArray(percentuale, i);
  }
  delay(50); // delay tra un rilevamento e l'altro
}

// Mostra nel terminale tutti e cinque i valori sotto forma di un array (visivamente)
void WriteArray(int sVal, int n)
{
  // per aprire l'array
  if (n == 0)
  {
    Serial.print("[");
  }
  // valori al centro dell'array
  Serial.print(sVal);
  if (n != ARRAY_SIZE(sensori) - 1)
  {
    Serial.print(",");
  }
  // per chiudere l'array
  if (n == ARRAY_SIZE(sensori) - 1)
  {
    Serial.println("]");
  }
}

// fa lampeggiare il led predefinito per un certo numero di volte
void blinkLed(int n)
{
  for (int i = 0; i < n; i++)
  {
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
  }
}
