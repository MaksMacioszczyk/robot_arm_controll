#include <Servo.h>
#include <AccelStepper.h>

#define motorInterfaceType 1
#define home_switch 12

//Variables
String incomingData ;   
int toIntVal;  
const int max_stepper_range = 4000;

//Servos pins
const int servo_fi1_pin = 11;
const int servo_fi2_pin = 5;
const int servo_gripper_pin = 6;

//Stepper pins
const int dirPin = 2;
const int stepPin = 9;

//Servo and stepper init
AccelStepper myStepper(motorInterfaceType, stepPin, dirPin);
Servo servo_fi1, servo_fi2, servo_gripper;

void setup() {
  Serial.begin(9600);

  servo_fi1.attach(servo_fi1_pin);
  servo_fi2.attach(servo_fi2_pin);
  servo_gripper.attach(servo_gripper_pin);

  pinMode(home_switch, INPUT_PULLUP); //Home switch init
  home_stepper();
  set_stepper_parameters();
}
void loop() {
  if (Serial.available() > 0) {
      incomingData = Serial.readStringUntil('\n');
      if(incomingData[0] == '1')//Z-Axis
      {
        incomingData.remove(0,1);
        toIntVal = incomingData.toInt();
        move_stepper_to_possition(toIntVal);
      }
      else if(incomingData[0] == '2')//Fi1
      {
        incomingData.remove(0,1);
        toIntVal = incomingData.toInt();
        servo_fi1.write(toIntVal);
      }
      else if(incomingData[0] == '3')//Fi2
      {
        incomingData.remove(0,1);
        toIntVal = incomingData.toInt();
        servo_fi2.write(toIntVal);
      }
      else if(incomingData[0] == 'O') // Open
      {
          servo_gripper.write(80);
      }
      else if(incomingData[0] == 'C') // Close
      {
          servo_gripper.write(180);
      }
  }
  delay(200);
}

void move_stepper_to_possition(int go_to_step)
{
  if(go_to_step >= max_stepper_range)
  {
    go_to_step = max_stepper_range;
  }
  if(go_to_step <= 0)
  {
    go_to_step = 0;
  }
  
  myStepper.moveTo(-go_to_step);

  while(myStepper.distanceToGo() != 0)
  {
    myStepper.run();
  }
  
}

void set_stepper_parameters()
{
  myStepper.setMaxSpeed(2000);
  myStepper.setAcceleration(700);
  myStepper.setSpeed(1000);
}

void home_stepper()
{
    int curr_step = 0;

    //Set maxSpeed, Acceleration and Speed for homing procedure
    myStepper.setMaxSpeed(1000);
    myStepper.setAcceleration(20);
    myStepper.setSpeed(10);

    //Move down till home switch is pressed
    while(!digitalRead(home_switch))
    {
      delay(2);
      myStepper.moveTo(curr_step);
      curr_step++;
      myStepper.run();   
    }

    //Set current position to 0
    myStepper.setCurrentPosition(0);  
}