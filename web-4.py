#!/usr/bin/python
# from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import paho.mqtt.client as mqtt
import datetime
now =datetime.date.today()
from http.server import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 8080

#def on_message(client, userdata, message):
#    print (message.payload)
#    return True
value1data = now.strftime('%Y-%m-%d')
value = "Waage ohne Funktion"
def on_message(client, userdata, message):
    global value
    value = str(message.payload.decode("utf-8"))
topics = ["huhn"]
client = mqtt.Client()
client.on_message=on_message
client.connect("127.0.0.1", 1883, 60)
client.loop_start()
for huhn in topics:
        client.subscribe("huhn/#")
        client.loop_start()

class myHandler(BaseHTTPRequestHandler):
        def do_GET(self):
                global value
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.end_headers()
                # Send the html message
                self.wfile.write(bytes("<html><head><title>Web View Waage</title></head>", "utf-8"))
                self.wfile.write(bytes("<body><p>Nester Uebersicht</p>", "utf-8"))
                self.wfile.write(bytes("<p>Datum: "+str (value1data)+"</p></body>", 'utf8'))
                self.wfile.write(bytes("<table style=background-color: #fffff height: 301px; width=397 border=2 ><tbody><tr><td style=width: 123px;>&nbsp;</td><td style=width: 126px;>&nbsp;</td><td style=width: 126px;>&nbsp;</td></tr><tr><td style=width: 123px;>Nest1</td><td style=width: 126px;>Gewicht in Gramm: "+str (value)+"</td><td style=width:126px;>Huhn</td></tr><tr><td style=width: 123px;>Nest2</td> <td style=width: 126px;>Gewicht</td> <td style=width: 126px;>Huhn</td> </tr>  <tr>  <td style=width: 123px;>Nest3</td> <td style=width: 126px;>Gewicht&nbsp;</td><td style=width: 126px;>Huhn</td> </tr></tbody></table>", 'utf8'))
                return

try:
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print ('Started httpserver on port ' , PORT_NUMBER)

    server.serve_forever()

except KeyboardInterrupt:
    print ('^C received, shutting down the web server')
    server.socket.close()
