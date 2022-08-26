//Alessio Modonesi, Mattia Zanini
//Righe di codice per il funzionamento del sensore di umidità

#define ARRAY_SIZE(array) ((sizeof(array))/(sizeof(array[0]))) // determina la lunghezza di un array

// valori da ricalibrare per per ogni board e in ogni condizione del sensore
/*
  Sensore A0, wet = 197;
  Sensore A0, dry = 503;

  Sensore A1, wet = 207;
  Sensore A1, dry = 516;

  Sensore A2, wet = 195;
  Sensore A2, dry = 502;

  Sensore A3, wet = 207;
  Sensore A3, dry = 515;

  Sensore A4, wet = 208;
  Sensore A4, dry = 515;

  Sensore A5, wet = 202;
  Sensore A5, dry = 511;
*/

//media tra i vari valori
const int dry = 510; // 0% di umidità
const int wet = 203; // 100% di umidità
const byte sensori[] = {A0, A1, A2, A3, A4, A5}; //contiene tutti i pin analogici della scheda

void setup() {
  Serial.begin(9600); // imposta il canale di trasmissione a 9600 bts (baud)
}

void loop() {
  writeSensorValJson();
}

// legge serialmente tutti i 6 sensori connessi all'arduino
void readMultiSensors() {
  for (int i = 0; i < ARRAY_SIZE(sensori); i++) {
    int sensorVal = analogRead(sensori[i]); //lettura analogica del singolo canale

    /*
      Serial.print("Sensore ");
      Serial.print(i);
      Serial.print(" : ");
      Serial.println(sensorVal);
    */

    //
    int percentuale = map(sensorVal, wet, dry, 100, 0); // converto un range di valori in percentuale
    Serial.print("Sensore ");
    Serial.print(i);
    Serial.print(" : ");
    Serial.print(percentuale);
    Serial.println("%");
    //
    writeArray(percentuale, i);
  }
  Serial.println(); // per staccare i vecchi valori da quelli nuovi
  delay(2500); // delay tra un rilevamento e l'altro
}

void writeSensorValJson() {
  for (int i = 0; i < ARRAY_SIZE(sensori); i++) {
    int sensorVal = analogRead(sensori[i]); //lettura analogica del singolo canale
    //int percentuale = map(sensorVal, wet, dry, 100, 0); // converto un range di valori in percentuale
    writeArray(sensorVal, i);
  }
  delay(100); // delay tra un rilevamento e l'altro
}

//write the value as an array in the terminal
void writeArray(int sVal, int n) {
  if (n == 0) {
    Serial.print("[");
  }
  Serial.print(sVal);
  if (n != ARRAY_SIZE(sensori) - 1) {
    Serial.print(",");
  }
  if (n == ARRAY_SIZE(sensori) - 1) {
    Serial.println("]");// per staccare i vecchi valori da quelli nuovi
  }
}
