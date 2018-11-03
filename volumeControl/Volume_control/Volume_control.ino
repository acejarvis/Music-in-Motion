
#define trig_1 2//output pins of ultrasonic sensors
#define echo_1 3
#define trig_2 4
#define echo_2 5
#define trig_3 6
#define echo_3 7
// define the detect-range
#define upperLimit 27
#define lowerLimit 6

int count_left = 0, count_right = 0, count = 0;// counter for an object passes the sensors

int volume, volume_memory = 0;
float dist_1,dist_2,dist_3;

float getDist(int trigPin, int echoPin)
{
  float dist,duration;
  // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
 
  // Read the signal from the sensor: a HIGH pulse whose
  // duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  
    duration = pulseIn(echoPin, HIGH);
    // Convert the time into a distance
    dist = (duration/2) / 29.1;
    //if (dist>60) dist = 60;
    return dist;
}

void setup() {
  //Serial Port begin
  Serial.begin (9600);
  //Define inputs and outputs
  pinMode(trig_1, OUTPUT);
  pinMode(echo_1, INPUT);
  pinMode(trig_2, OUTPUT);
  pinMode(echo_2, INPUT);
  pinMode(trig_3, OUTPUT);
  pinMode(echo_3, INPUT);
}
 
void loop() {
  //get distance
  dist_1 = getDist(trig_1, echo_1);
  dist_2 = getDist(trig_2, echo_2);
  dist_3 = getDist(trig_3, echo_3);

  //get volume converted from distance
  if(dist_1 >= lowerLimit - 0.2 && dist_1 <= upperLimit){ 
    volume = (dist_1-5.8)*100/(upperLimit - lowerLimit);
    Serial.println(volume);
  }
  //range detect for the other two sensors
  else{
    if(dist_2 >= lowerLimit - 0.2 && dist_2 <= upperLimit){
      Serial.print('2');
    }
    else Serial.print('3');
    Serial.print('0');
    if(dist_3 >= lowerLimit - 0.2 && dist_3 <= upperLimit){
      Serial.println('2');
    }
    else Serial.println('3');
  }
  
  delay(10);
}
