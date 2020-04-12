#include <ESP8266WiFi.h>
#include <Servo.h>

Servo myservo1; 
Servo myservo2;
Servo solmotor;
Servo sagmotor;
// twelve servo objects can be created on most boards

// GPIO the servo is attached to
static const int servoPin1 = 15; // Alt Servo  // D8
static const int servoPin2 = 2; // Üst Servo  // D4
static const int solmotorpin = 12;             // D6
static const int sagmotorpin = 14;             // D5


// Replace with your network credentials
const char* ssid     = "mertbaykal";
const char* password = "11370o029";

// Set web server port number to 80
WiFiServer server(80);

// Variable to store the HTTP request
String header;

// Decode HTTP GET value
String valueString1 = "70";
String valueString2 = "155";
String valueString3 = "1000";
String valueString4 = "1000";
int esit = 0;
int virgul = 0;
int ve = 0;
int tire = 0;
int yildiz = 0;

void setup() {
  Serial.begin(115200);

  myservo1.attach(servoPin1);  // attaches the servo on the servoPin to the servo object
  myservo2.attach(servoPin2);
  solmotor.attach(solmotorpin);
  sagmotor.attach(sagmotorpin);
  
  // Connect to Wi-Fi network with SSID and password
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop(){
  WiFiClient client = server.available();   // Listen for incoming clients

  if (client) {                             // If a new client connects,
    Serial.println("New Client.");          // print a message out in the serial port
    String currentLine = "";                // make a String to hold incoming data from the client
    while (client.connected()) {            // loop while the client's connected
      if (client.available()) {             // if there's bytes to read from the client,
        char c = client.read();             // read a byte, then
        Serial.write(c);                    // print it out the serial monitor
        header += c;
        if (c == '\n') {                    // if the byte is a newline character
          // if the current line is blank, you got two newline characters in a row.
          // that's the end of the client HTTP request, so send a response:
          if (currentLine.length() == 0) {
            // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
            // and a content-type so the client knows what's coming, then a blank line:
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println("Connection: close");
            client.println();

            // Display the HTML web page
            client.println("<!DOCTYPE html><html>");
            client.println("<head><meta charset=\"utf-8\" name=\"viewport\" content=\"width=device-width, initial-scale=1\">");
            client.println("<link rel=\"icon\" href=\"data:,\">");
            // CSS to style the on/off buttons 
            // Feel free to change the background-color and font-size attributes to fit your preferences
            client.println("<style>body { text-align: center; font-family: \"Trebuchet MS\", Arial; margin-left:auto; margin-right:auto;}");
            client.println(".slider { width: 300px; }</style>");
            client.println("<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js\"></script>");
                     
            // Web Page
            client.println("</head><body><h1>Hücre Operasyon Tankı</h1>");
            client.println("<p>Alt Servo Pozisyonu: <span id=\"servoPos1\"></span></p>");          
            client.println("<input type=\"range\" min=\"42\" max=\"104\" class=\"slider\" id=\"servoSlider1\" value=\""+valueString1+"\"/>");
            client.println("<p>Üst Servo Pozisyonu: <span id=\"servoPos2\"></span></p>");          
            client.println("<input type=\"range\" min=\"110\" max=\"170\" class=\"slider\" id=\"servoSlider2\" value=\""+valueString2+"\"/>");
            client.println("<p>Sol Tank Motor: <span id=\"solmotor\"></span></p>");          
            client.println("<input type=\"range\" min=\"1000\" max=\"2000\" class=\"slider\" id=\"solmotorslider\" value=\""+valueString3+"\"/>");
            client.println("<p>Sağ Tank Motor: <span id=\"sagmotor\"></span></p>");          
            client.println("<input type=\"range\" min=\"1000\" max=\"2000\" class=\"slider\" id=\"sagmotorslider\" value=\""+valueString4+"\"/>");
            client.println("<br><br><button id=\"moveservos\" onclick=\"moveservos()\">Çalıştır</button>");
            
            client.println("<script>var slider1 = document.getElementById(\"servoSlider1\");");
            client.println("var servoP1 = document.getElementById(\"servoPos1\"); servoP1.innerHTML = slider1.value;");
            client.println("slider1.oninput = function() { slider1.value = this.value; servoP1.innerHTML = this.value; }");
            client.println("var slider2 = document.getElementById(\"servoSlider2\");");
            client.println("var servoP2 = document.getElementById(\"servoPos2\"); servoP2.innerHTML = slider2.value;");
            client.println("slider2.oninput = function() { slider2.value = this.value; servoP2.innerHTML = this.value; }");
            client.println("var solslider = document.getElementById(\"solmotorslider\");");
            client.println("var solmotor = document.getElementById(\"solmotor\"); solmotor.innerHTML = solslider.value;");
            client.println("solslider.oninput = function() { solslider.value = this.value; solmotor.innerHTML = this.value; }");
            client.println("var sagslider = document.getElementById(\"sagmotorslider\");");
            client.println("var sagmotor = document.getElementById(\"sagmotor\"); sagmotor.innerHTML = sagslider.value;");
            client.println("sagslider.oninput = function() { sagslider.value = this.value; sagmotor.innerHTML = this.value; }");
            client.println("$.ajaxSetup({timeout:1000}); function moveservos() { ");
            client.println("");
            client.println("$.get(\"/?value=\" + slider1.value + \",\" + slider2.value + \"&\" + solslider.value + \"-\" + sagslider.value + \"*\"); {Connection: close};}</script>");
           
            client.println("</body></html>");     
            
            //GET /?value=180& HTTP/1.1
            if(header.indexOf("GET /?value=")>=0) {
              esit = header.indexOf('=');
              virgul = header.indexOf(',');
              ve = header.indexOf('&');
              tire = header.indexOf('-');
              yildiz = header.indexOf('*');
              valueString1 = header.substring(esit+1, virgul);
              valueString2 = header.substring(virgul+1, ve);
              valueString3 = header.substring(ve+1, tire);
              valueString4 = header.substring(tire+1, yildiz);
              //Rotate the servo
              myservo1.write(valueString1.toInt());
              myservo2.write(valueString2.toInt()); 
              solmotor.writeMicroseconds(valueString3.toInt());
              sagmotor.writeMicroseconds(valueString4.toInt());
            }         
            // The HTTP response ends with another blank line
            client.println();
            // Break out of the while loop
            break;
          } else { // if you got a newline, then clear currentLine
            currentLine = "";
          }
        } else if (c != '\r') {  // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }
      }
    }
    // Clear the header variable
    header = "";
    // Close the connection
    client.stop();
    Serial.println("Client disconnected.");
    Serial.println("");
  }
}
