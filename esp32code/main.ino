#include <WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_NeoPixel.h>

// تنظیمات وای فای
const char* ssid = "charon";
const char* password = "12121212";

// تنظیمات MQTT
const char* mqtt_broker = "broker.emqx.io";
const int mqtt_port = 1883;
const char* topic_touch_state = "esmail/touch_state";

// تنظیمات NeoPixel
#define LED_PIN    15  // پین دیتای LED RGB
#define LED_COUNT  8   // تعداد LED ها
#define TOUCH_PIN T0   // GPIO4 برای سنسور تاچ
#define THRESHOLD 40   // آستانه تشخیص لمس

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

uint32_t colors[] = {
    strip.Color(255, 0, 0),      // قرمز
    strip.Color(0, 255, 0),      // سبز
    strip.Color(0, 0, 255),      // آبی
    strip.Color(255, 255, 0),    // زرد
    strip.Color(255, 0, 255),    // بنفش
    strip.Color(0, 255, 255),    // فیروزه‌ای
    strip.Color(255, 128, 0),    // نارنجی
    strip.Color(255, 255, 255)   // سفید
};

String device_id;
WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
    Serial.println("Connecting to WiFi...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi connected");
    Serial.println("IP: ");
    Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
    String message = "";
    for (int i = 0; i < length; i++) {
        message += (char)payload[i];
    }
    
    Serial.print("Message arrived: ");
    Serial.println(message);
    
    int separator = message.indexOf(':');
    String sender_id = message.substring(0, separator);
    String touch_state = message.substring(separator + 1);
    
    if (sender_id != device_id) {
        if (touch_state == "1") {
            for(int i=0; i<LED_COUNT; i++) {
                strip.setPixelColor(i, colors[i]);
            }
            strip.show();
            Serial.println("NeoPixels ON");
        } else {
            strip.clear();
            strip.show();
            Serial.println("NeoPixels OFF");
        }
    }
}

void reconnect() {
    while (!client.connected()) {
        Serial.print("Connecting to MQTT...");
        String client_id = "esp32-neo-" + String(random(0xffff), HEX);
        if (client.connect(client_id.c_str())) {
            Serial.println("connected");
            client.subscribe(topic_touch_state);
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" retry in 5s");
            delay(5000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    
    strip.begin();
    strip.show();
    strip.setBrightness(255);
    
    touchSetCycles(0x1000, 0x1000);
    
    device_id = "ESP32_NEO_" + String((uint32_t)ESP.getEfuseMac(), HEX);
    Serial.print("Device ID: ");
    Serial.println(device_id);
    
    setup_wifi();
    client.setServer(mqtt_broker, mqtt_port);
    client.setCallback(callback);
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
    
    uint16_t touchValue = touchRead(TOUCH_PIN);
    static bool lastTouchState = false;
    bool currentTouchState = touchValue < THRESHOLD;
    
    if (currentTouchState != lastTouchState) {
        String message = device_id + ":" + (currentTouchState ? "1" : "0");
        Serial.print("Touch: ");
        Serial.println(currentTouchState ? "YES" : "NO");
        
        client.publish(topic_touch_state, message.c_str());
        lastTouchState = currentTouchState;
    }
    
    delay(100);
}
