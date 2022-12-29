#include <Arduino.h>
#include <Servo.h>

// create servo obj array
Servo hand[5];

String s = "";

//time calc
unsigned long last_serial_in = 0;
unsigned long last_standby = 0;

//standby
#define STANDBY_TIME 15000
#define SERVO_DELAY 15

//default state
String last_state = "rock";

//FSM
#define BUTTON_PIN 2
#define FSM_STANDBY_ON_PIN 8
#define FSM_STANDBY_OFF_PIN 7
#define STANDBY_ON 0
#define STANDBY_OFF 1
#define FSM_MAX 2
uint8_t fsm_counter = 0;
unsigned long last_press = 0;

void initHand()
{
    hand[0].attach(5);  //Servo 1 (食指)
    hand[1].attach(6);  //Servo 2 (中指)
    hand[2].attach(9);  //Servo 3 (拇指)
    hand[3].attach(10); //Servo 4 (無名指)
    hand[4].attach(11); //Servo 5 (尾指)
}

void paper()
{
    hand[0].write(50);
    hand[1].write(50);
    hand[2].write(130);
    hand[3].write(50);
    hand[4].write(50);
}

void rock()
{
    hand[0].write(130);
    hand[1].write(130);
    hand[2].write(30);
    hand[3].write(130);
    hand[4].write(130);
}

void scissors()
{
    hand[0].write(50);
    hand[1].write(50);
    hand[2].write(30);
    hand[3].write(130);
    hand[4].write(130);
}

void yo()
{
    hand[0].write(30);
    hand[1].write(130);
    hand[2].write(130);
    hand[3].write(130);
    hand[4].write(30);
}

uint8_t count = 1;
uint8_t finger = 0;
uint8_t sign = 1;
uint8_t finger_arr[] = {2, 0, 3, 4};
void standby()
{
    hand[0].write(150 - count);
    hand[1].write(150 - count);
    hand[2].write(30 + count);
    hand[3].write(150 - count);
    hand[4].write(150 - count);

    if (count == 0)
    {
        sign = 1;
    }
    else if (count == 90)
    {
        sign = -1;
    }
    // Serial.println(count);
    count += sign;

    last_standby = millis();

    //
    // hand[1].write(130);

    // uint8_t angle = 130 - count;
    // if (finger == 0)
    // {
    //     angle = 30 + count;
    // }
    // hand[finger_arr[finger]].write(angle);

    // if (count == 0)
    // {
    //     sign = 1;
    //     if (finger < 3)
    //     {
    //         finger += 1;
    //     }
    //     else
    //     {
    //         finger = 0;
    //     }
    // }
    // else if (count == 80)
    // {
    //     sign = -1;
    // }
    // Serial.println(count);
    // count += sign;

    // last_standby = millis();
}

void button_interrupt()
{
    if ((millis() - last_press) > 200)
    {
        if (fsm_counter < FSM_MAX - 1)
        {
            fsm_counter += 1;
        }
        else
        {
            fsm_counter = 0;
        }
        // Serial.println(fsm_counter);
        last_press = millis();
    }
}

void setup()
{
    Serial.begin(9600);
    pinMode(13, OUTPUT);
    initHand();
    rock();

    // while (1)
    // {
    //     rock();
    //     delay(3000);
    //     paper();
    //     delay(3000);
    //     scissors();
    //     delay(3000);
    // }

    pinMode(BUTTON_PIN, INPUT);
    attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), button_interrupt, RISING);

    pinMode(FSM_STANDBY_ON_PIN, OUTPUT);
    pinMode(FSM_STANDBY_OFF_PIN, OUTPUT);

    last_serial_in = millis();
}

char c;
void loop()
{
    s = "";
    while (Serial.available())
    {
        c = Serial.read();
        if (c != '\n')
        {
            s += c;
        }
        delay(5);
    }

    if (s != "")
    {
        // Serial.println(s);
        if (last_state != s)
        {
            last_serial_in = millis();
        }

        if (s == "serial_init")
        {
            digitalWrite(13, HIGH);
        }
        else if (s == "paper")
        {
            paper();
            last_state = s;
        }
        else if (s == "rock")
        {
            rock();
            last_state = s;
        }
        else if (s == "scissors")
        {
            scissors();
            last_state = s;
        }
    }

    if (fsm_counter == STANDBY_ON)
    {
        digitalWrite(FSM_STANDBY_ON_PIN, HIGH);
        digitalWrite(FSM_STANDBY_OFF_PIN, LOW);
    }
    else if (fsm_counter == STANDBY_OFF)
    {
        digitalWrite(FSM_STANDBY_ON_PIN, LOW);
        digitalWrite(FSM_STANDBY_OFF_PIN, HIGH);
    }

    if (millis() - last_serial_in > STANDBY_TIME)
    {
        if (millis() - last_standby > SERVO_DELAY && fsm_counter == STANDBY_ON)
        {
            standby();
        }

        // last_state = "yo";
    }
    // rock();
}