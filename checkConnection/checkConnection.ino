void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(13,  OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int portV = (analogRead(Serial) / 1023.0) * (5.0 * 4.7);
  if (portV > 6) {
    digitalWrite(13, HIGH);
    Serial.println("Linked");
  } else {
    digitalWrite(13, LOW);
    Serial.println("No Link");
  }
  Serial.println(portV);
  delay(1000);
}
