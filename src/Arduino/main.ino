#include <Servo.h>

String incomingData ;   
int toIntVal;  

int servo_fi1_pin = 3;
int servo_fi2_pin = 10;

Servo servo_fi1, servo_fi2;

void setup() {
  Serial.begin(9600);

  servo_fi1.attach(servo_fi1_pin);
  servo_fi2.attach(servo_fi2_pin);
  
  pinMode(LED_BUILTIN, OUTPUT);

}
void loop() {
  if (Serial.available() > 0) {
      incomingData = Serial.readStringUntil('\n');
      if(incomingData[0] == '1')
      {
        incomingData.remove(0,1);
        incomingData.toInt();
        
      }
      if(incomingData[0] == '2')
      {
        incomingData.remove(0,1);
        toIntVal = incomingData.toInt();
        servo_fi1.write(toIntVal);
      }
      if(incomingData[0] == '3')
      {
        incomingData.remove(0,1);
        toIntVal = incomingData.toInt();
        servo_fi2.write(toIntVal + 90);
      }
  }
  delay(200);
}