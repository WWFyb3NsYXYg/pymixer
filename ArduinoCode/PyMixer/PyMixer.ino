#define PIN_POT_1     A2
#define PIN_POT_2     A1
int val1, val2;
void setup() {
  Serial.begin(115200);
  pinMode(PIN_POT_1, INPUT);
  pinMode(PIN_POT_2, INPUT);
}
void loop() {
  if (val1 != float(map(analogRead(PIN_POT_1), 60, 850, 0, 100)) || val2 != float(map(analogRead(PIN_POT_2), 35, 1013, 0, 100))) {  
    val1 = float(map(analogRead(PIN_POT_1), 60, 850, 0, 100));
    val2 = float(map(analogRead(PIN_POT_2), 35, 1013, 0, 100));
    val1 = float(constrain(val1, 0, 100));
    val2 = float(constrain(val2, 0, 100));
    Serial.print(val1);
    Serial.print(',');
    Serial.print(val2);
    Serial.print('\n');
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(15);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delay(15);
  }}
