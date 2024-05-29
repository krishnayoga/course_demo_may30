const int BAUD_RATE = 9600;
const char TRIGGERS[] = {'X', 'Y', 'Z'};
const int NUM_TRIGGERS = sizeof(TRIGGERS) / sizeof(TRIGGERS[0]);
const unsigned long TRIGGER_INTERVAL = 5000; // 5 seconds in milliseconds

char currentTrigger = 'X';
String cmd;
unsigned long lastResponseTime = 0;

void setup() {
  Serial.begin(BAUD_RATE);
  Serial.println(currentTrigger);
}

void loop() {
  while (Serial.available()) {
    char serialInByte = Serial.read();
    lastResponseTime = millis(); // Reset the timer

    if (serialInByte == '\n') { // Check for carriage return
      Serial.println(cmd);
      cmd = "";
      delay(1000);
      incrementTrigger();
      Serial.println(currentTrigger);
    } else {
      cmd += String(serialInByte);
    }
  }

  if (millis() - lastResponseTime >= TRIGGER_INTERVAL) {
    resetTrigger();
  }
}

void incrementTrigger() {
  for (int i = 0; i < NUM_TRIGGERS; i++) {
    if (currentTrigger == TRIGGERS[i]) {
      currentTrigger = TRIGGERS[(i + 1) % NUM_TRIGGERS];
      break;
    }
  }
}

void resetTrigger() {
  currentTrigger = TRIGGERS[0];
  Serial.println(currentTrigger);
  lastResponseTime = millis(); // Reset the timer
}
