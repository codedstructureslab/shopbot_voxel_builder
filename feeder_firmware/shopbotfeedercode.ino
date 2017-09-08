#include <Servo.h>
#include <stdarg.h>
#include <Arduino.h>

// Mount the servos
Servo boltservo;

////////////////////////////////////////////////////////
///////////Set all the variables and flags /////////////
////////////////////////////////////////////////////////

// Output channels from the Shopbot
int shopbot_OP9 = A0;
int shopbot_OP10 = A1;
int shopbot_OP11 = A2;
int shopbot_OP12 = A3;
float shopbot_OP9_value = 0;
float shopbot_OP10_value = 0; 
float shopbot_OP11_value = 0; 
float shopbot_OP12_value = 0;

// Flags to run the programs[

bool program_1 = false;
bool program_2 = false;
bool program_3 = false;
bool program_4 = false;

// Stepper Motor Controllers
int dirbolt = 7; // bolt direction (LOW = cclockwise(backwards))
int stumpbolt = 6; // bolt step
int dirvox = 2; // voxel direction
int stumpvox = 1; // voxel step
int dirnut = 9; // nut direction
int stumpnut = 8; // nut step
int button = 3; // dispense screw and nut
int buttonval;
int prevbuttonval;
int pos = 70; // servo starting position
int screwsleep = 5; //stepper motor low power mode

 //////////////////////////////
 ///////////Setup//////////////
 //////////////////////////////

void setup() {
  pinMode(dirbolt, OUTPUT);
  pinMode(stumpbolt, OUTPUT);
  pinMode(dirvox, OUTPUT);
  pinMode(stumpvox, OUTPUT);
  pinMode(dirnut, OUTPUT);
  pinMode(stumpnut, OUTPUT);
  pinMode(button, INPUT);
  pinMode(screwsleep, OUTPUT);  
  digitalWrite(dirbolt, LOW);
  digitalWrite(dirvox, LOW);
  digitalWrite(dirnut, HIGH);
  digitalWrite(screwsleep, LOW);
  boltservo.attach(10);
  boltservo.write(70);
  SerialUSB.begin(9600);

  SerialUSB.println("starting program...");
}

 //////////////////////////////
 ///////////Main loop//////////
 //////////////////////////////

bool isLastStateReading=false;

void loop() {

  shopbot_OP9_value = analogRead(shopbot_OP9);
  buttonval = digitalRead(3);
  delay(10); //maybe there is a better way to clear the multiplexer?
  shopbot_OP9_value = analogRead(shopbot_OP9);


  //Serial.print("(OP9, OP10, OP11, OP12) ");
  //ardprintf("%f %f %f %f", shopbot_OP9_value, shopbot_OP10_value, shopbot_OP11_value, shopbot_OP12_value);
  //Serial.println();

  //delay(1000);
  
  // pause Arduino in loop while the Shopbot sets the outputs (as they don't all get set simultaneously
  // which can cause the Arduino to interpret them incorrectly
  
  if (shopbot_OP9_value > 950 && isLastStateReading==false) {
    isLastStateReading=true;     
    shopbot_OP9_value = analogRead(shopbot_OP9);
    shopbot_OP10_value = analogRead(shopbot_OP10);
    shopbot_OP11_value = analogRead(shopbot_OP11);
    shopbot_OP12_value = analogRead(shopbot_OP12);
  }
      
 //////////////////////////////
 ///program 1 = next screw ////
 //////////////////////////////
 
    if (shopbot_OP9_value > 950 && shopbot_OP10_value < 950 && shopbot_OP11_value > 950 && shopbot_OP12_value < 950) {
      program_1 = true;}
    else {
      program_1 = false;}
  
    if (program_1 == true){
      SerialUSB.println("Next Screw");
      for (int i=0; i < 11; i++) {
        digitalWrite(screwsleep, HIGH);
        digitalWrite(dirbolt, LOW);
        digitalWrite(stumpbolt,HIGH); 
        delayMicroseconds(6000);       
        digitalWrite(stumpbolt,LOW); 
        delayMicroseconds(6000);
        }
      digitalWrite(screwsleep, LOW);
      program_1 = false; 
      resetOutputState();
    }

//////////////////////////////
///program 2 = next voxel ////
//////////////////////////////
 
    if (shopbot_OP9_value > 950 && shopbot_OP10_value > 950 && shopbot_OP11_value < 950 && shopbot_OP12_value < 950) {
      program_2 = true;}
    else {
      program_2 = false;}
  
    if (program_2 == true){
      SerialUSB.println("Next Voxel");
      for (int i=0; i < 50; i++) {
        digitalWrite(dirvox, LOW);
        digitalWrite(stumpvox,HIGH); 
        delayMicroseconds(6000);       
        digitalWrite(stumpvox,LOW); 
        delayMicroseconds(6000);
        }
      program_2 = false; 
      resetOutputState();
    }

//////////////////////////////
///program 3 = next nut ////
//////////////////////////////
 
    if (shopbot_OP9_value > 950 && shopbot_OP10_value < 950 && shopbot_OP11_value < 950 && shopbot_OP12_value > 950) {
      program_3 = true;}
    else {
      program_3 = false;}
  
    if (program_3 == true){
      SerialUSB.println("Next Nut");
      for (int i=0; i < 350; i++) {
        digitalWrite(dirnut, HIGH);
        digitalWrite(stumpnut,HIGH); 
        delayMicroseconds(6000);       
        digitalWrite(stumpnut,LOW); 
        delayMicroseconds(6000);
        }
      program_3 = false; 
      resetOutputState();
    }

//////////////////////////////
///program 4 = servo bolt ////
//////////////////////////////
 
    if (shopbot_OP9_value > 950 && shopbot_OP10_value > 950 && shopbot_OP11_value > 950 && shopbot_OP12_value < 950) {
      program_4 = true;}
    else {
      program_4 = false;}
  
    if (program_4 == true){
      SerialUSB.println("Bolt Screw");
      for (pos = 70; pos <= 95; pos += 1) { // goes from 0 degrees to 180 degrees
                                            // in steps of 1 degree
        boltservo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(30);                       // waits 15ms for the servo to reach the position
        }
      for (pos = 95; pos >= 70; pos -= 1) { // goes from 180 degrees to 0 degrees
        boltservo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(30);                       // waits 15ms for the servo to reach the position
        }
      program_4 = false; 
      resetOutputState();
    }

//////////////////////////////
///program 5 = rewind stack ////
//////////////////////////////
 
    if (buttonval == HIGH){
      SerialUSB.println("Rewind Stack");
      for (int i=0; i < 2100; i++) {
        digitalWrite(dirnut, LOW);        
        digitalWrite(stumpnut,HIGH); 
        delayMicroseconds(6000);       
        digitalWrite(stumpnut,LOW); 
        delayMicroseconds(6000);
      }
      prevbuttonval = buttonval;
    }

///////////////////////////////////////
/////Serial monitor values /////////////
////////////////////////////////////////
   
  if(SerialUSB.available() > 0){
      char c = SerialUSB.read();
             
      //program 1
      if (c == 's'){
        Serial.println("Next Screw");
        for (int i=0; i < 11; i++) {
          digitalWrite(screwsleep, HIGH);
          digitalWrite(dirbolt, LOW);
          digitalWrite(stumpbolt,HIGH); 
          delayMicroseconds(6000);       
          digitalWrite(stumpbolt,LOW); 
          delayMicroseconds(6000);
          }
        digitalWrite(screwsleep, LOW);
      }
        
      //program 2
      if (c == 'v'){
        Serial.println("Next Voxel");
        for (int i=0; i < 50; i++) {
          digitalWrite(dirvox, LOW);
          digitalWrite(stumpvox,HIGH); 
          delayMicroseconds(6000);       
          digitalWrite(stumpvox,LOW); 
          delayMicroseconds(6000);
          }
      }
  
      //program 3
      if (c == 'n'){
        Serial.println("Next Nut");
        for (int i=0; i < 350; i++) {
          digitalWrite(dirnut, HIGH);
          digitalWrite(stumpnut,HIGH); 
          delayMicroseconds(6000);       
          digitalWrite(stumpnut,LOW); 
          delayMicroseconds(6000);
          }
      }
  
      //program 4
      if (c == 'b'){
        SerialUSB.println("Bolt Screw");
        for (pos = 70; pos <= 95; pos += 1) { // goes from 0 degrees to 180 degrees
                                              // in steps of 1 degree
          boltservo.write(pos);               // tell servo to go to position in variable 'pos'
          delay(30);                          // waits 15ms for the servo to reach the position
          }
        for (pos = 95; pos >= 70; pos -= 1) { // goes from 180 degrees to 0 degrees
          boltservo.write(pos);               // tell servo to go to position in variable 'pos'
          delay(30);                          // waits 15ms for the servo to reach the position
          }
      }
  
      //program 5
      if (c == 'r'){
        SerialUSB.println("Rewind Stack");
        for (int i=0; i < 2100; i++) {
          digitalWrite(dirnut, LOW);        
          digitalWrite(stumpnut,HIGH); 
          delayMicroseconds(6000);       
          digitalWrite(stumpnut,LOW); 
          delayMicroseconds(6000);
          }
      }
  }
}

void resetOutputState(){
		shopbot_OP9_value = 0;
		shopbot_OP10_value = 0;
		shopbot_OP11_value = 0;
		shopbot_OP12_value = 0;
		isLastStateReading=false;
}


