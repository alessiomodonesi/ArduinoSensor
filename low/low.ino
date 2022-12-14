#include <avr/power.h>
#include <SoftwareSerial.h>

#define TIME(n) (n / 16)
void setup()
{
  Serial.begin(9600);
  Serial.println(F_CPU); //                        16000000
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  clock_prescale_set(clock_div_16);
  /*
    if (F_CPU == 8000000) clock_prescale_set(clock_div_2);
    if (F_CPU == 4000000) clock_prescale_set(clock_div_4);
    if (F_CPU == 2000000) clock_prescale_set(clock_div_8);
    if (F_CPU == 1000000) clock_prescale_set(clock_div_16);
  */
  Serial.begin(19200);
}

void loop() {
  //Serial.println(F_CPU);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.println("Spento");
  delay(TIME(1000));
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.println("Acceso");
  delay(TIME(1000));
}
