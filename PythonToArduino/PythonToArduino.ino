#define WAITING_TIME 5000

bool stillChecking = true;
bool notConnected;
unsigned long sentMs;

void setup() {
  Serial.begin(9600);
  setupCheckUSB();
  Serial.println("Booting...");
  /*xxx
    while (!Serial.available());
    x = Serial.readString().toInt();
    Serial.print(x + 1);
  */
}

void loop() {
  checkUSB();
}

void setupCheckUSB() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  sentMs = millis();
}

void checkUSB() {
  if (stillChecking) {
    //Serial.println("I'm listening");
    if (millis() - sentMs > WAITING_TIME) {
      if (!Serial.available()) {

        //NO USB

        notConnected = true;
        //Serial.println("I didn't see you.");
      } else {

        //USB CONNECTED

        digitalWrite(LED_BUILTIN, HIGH);
        notConnected = false;
        /*
          Serial.println("I see you.");

          Serial.print("You writed this: ");
          Serial.println(Serial.readString());
        */
      }
      stillChecking = false;
      Serial.println(!notConnected);

      if (!notConnected == true) {
        //USB CONNECTED
        blinkLed(3);
      }
      else {
        //NO USB
        blinkLed(2);
        digitalWrite(LED_BUILTIN, LOW);
      }
    }
  }
}

void blinkLed(int n) {
  for (int i = 0; i < n; i++) {
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
  }
}
