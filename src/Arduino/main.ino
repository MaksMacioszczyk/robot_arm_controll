#include <Servo.h>

String incomingData ;   
int toIntVal;  

int servo_fi1_pin = 3;
int servo_fi2_pin = 10;
int servo_gripper_pin = 9;

Servo servo_fi1, servo_fi2, servo_gripper;

void setup() {
  Serial.begin(9600);

  servo_fi1.attach(servo_fi1_pin);
  servo_fi2.attach(servo_fi2_pin);
  servo_gripper.attach(servo_gripper_pin);

  pinMode(LED_BUILTIN, OUTPUT);

}
void loop() {
  if (Serial.available() > 0) {
      incomingData = Serial.readStringUntil('\n');
      if(incomingData[0] == '1')
      {
        incomingData.remove(0,1);
        incomingData.toInt();
        //Place to make 
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
        servo_fi2.write(toIntVal);
      }
      if(incomingData[0] == 'O') //Open
      {
          servo_gripper.write(80);
      }
      if(incomingData[0] == 'C') // Close
      {
          servo_gripper.write(180);
      }
  }
  delay(200);
}