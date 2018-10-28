
#define trigPin 12 //output pins of ultrasonic sensors

#define upperLimit 50
#define lowerLimit 6

int echoPin[3];// receive pins of ultrasonic sensors
int count_left = 0, count_right = 0, count = 0;// counter for an object passes the sensors

double duration, distance[3];
int play, volume;

void setup() {
  //Serial Port begin
  Serial.begin (9600);
  //Define inputs and outputs
  pinMode(trigPin, OUTPUT);
  for(int Pin=9;Pin<=11;Pin++){
    pinMode(echoPin[Pin], INPUT);
  }
  
}
 
void loop() {
  // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
 
  // Read the signal from the sensor: a HIGH pulse whose
  // duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  for(int i=0; i<=2; i++){
    duration = pulseIn(echoPin[i+9], HIGH);
    // Convert the time into a distance
    distance[i] = (duration/2) / 29.1;     // Divide by 29.1 or multiply by 0.0343
  }
  //get volume converted from distance
  if(distance[0]<50 && distance[0]>6){ 
    volume = (distance[0]-5)*100/(upperLimit - lowerLimit);
  }
  
  //left/right control
  if(distance[1]<40 || distance[2]<40){
    count++;
    if(distance[1]<40) count_left++;
    if(distance[2]<40) count_right++;
  }
  else{
    count = 0;
    count_left = 0;
    count_right = 0;
  }
  
  //play next/previous
  if(count > 5 && count < 50){
    if(count_left <= count_right) play= 200;//play previous
    else play = 300;//play next
  }
  
  // play/pause
  else if(count >=50) play = 400;
  else play = volume;
  Serial.println(play);
  delay(10);
}
