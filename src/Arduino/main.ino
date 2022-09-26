String incomingByte ;    

void setup() {

  Serial.begin(9600);

  pinMode(LED_BUILTIN, OUTPUT);

}
void loop() {

  if (Serial.available() > 0) {

  incomingByte = Serial.readStringUntil('\n');

    if (incomingByte == "on") {

      digitalWrite(LED_BUILTIN, HIGH);  
    }

    else if (incomingByte == "off") {

      digitalWrite(LED_BUILTIN, LOW);
    }
  }

}