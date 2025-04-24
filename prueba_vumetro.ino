void setup() {
  Serial.begin(9600);
  Serial.setTimeout(300);
  pinMode(3, OUTPUT); // Pin PWM
  pinMode(5, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    String input_der = Serial.readStringUntil(',');
    String input_izq = Serial.readStringUntil('\n');
    int valor_der = input_der.toInt();
    int valor_izq = input_izq.toInt();
    valor_izq = constrain(valor_izq, 0, 255);
    valor_der = constrain(valor_der, 0, 255);
    analogWrite(3, valor_der);
    analogWrite(5, valor_izq);
  }
}
