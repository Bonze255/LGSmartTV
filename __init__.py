__author__ = 'Marni'
#IMplementierung for Python and SMarthomeNG.py
#by Manuel Holländer

import logging
import socket
import time
import datetime
import base64
from base64 import urlsafe_b64encode as encode
from base64 import urlsafe_b64decode as decode
import hmac
import json
import binascii
import hashlib
from  urllib import request
import sys
import random
import re
from os import *
from mimetypes import MimeTypes
import struct

logger = logging.getLogger('')


class WebOsTv:
    def __init__(self, host='127.0.0.1', port=3000, lgkey='', path="/"):
        # self._sh = smarthome
        self._host = host
        self._port = port
        self._wskey = encode(self.generateRandomString(16, False, True))  # Websocket Handshake Code
        self._tvkey = lgkey  # LG Webos Handshae COde
        self._path = str(path)
        self._handshake = False
        self._handshakecode = ''  ##CODE des HANDSHAKES!
        self._connected = False
        self.connect()  # //
        self.lg_handshake()
        self._keyfile = "key.txt"
        self.message("SmarthomeNG.py"+" YEAH, it works!!!")
        self.message2("YEAH, it works!!!")
        self.set_mute()
        self.open_browser_at("smarthome.local")
        self.debug = False
        self.channellist()
        self.get_channel()
        #self.get_SW_info()
        #self.get_services()
        self.get_systemInfo()
        self.show_image("http://findicons.com/files/icons/1188/somatic_rebirth_system/128/home.png", "test", "test")
        self.show_media("http://www.groemitz.de/webcam/pics/aktuell_webcam.jpg", "test", "test", 1 )
        # print("YEAH, it works!!!")
        #time.sleep(5)
        #self.set_volume(75)
        #time.sleep(10)
        #self.disconnect()
        ##prog


    # //Websocket Connect
    def connect(self):
        ws_handshake_cmd = "GET {0} HTTP/1.1\r\n".format(self._path)
        ws_handshake_cmd += "Upgrade: websocket\r\n"
        ws_handshake_cmd += "Connection: Upgrade\r\n"
        ws_handshake_cmd += "Sec-WebSocket-Version: 13\r\n"
        ws_handshake_cmd += "Sec-WebSocket-Key: {0}\r\n".format(self._wskey)
        ws_handshake_cmd += "Host: {0}: {1}\r\n\r\n".format(self._host, self._port)

        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self._host, self._port))
            self._sock.settimeout(20)
        except:
            print("Verbindung zu ", self._host, " nicht möglich!")

        print("Sending WS handshake", ws_handshake_cmd)
        response = self.send(ws_handshake_cmd, "ws")

        # Empfangenes prüfen und Key suchen
        if response == '':
            print("ERROR during WS handshake!")
            returnkey = ''
        else:
            print("WS Handshake Response:", response.decode('ascii'))
            matches = re.search('Sec-WebSocket-Accept:\s*(.*=)', response.decode('utf-8'))
            returnkey = matches.groups()
            returnkey = returnkey[0]
            #print("Match in response ",returnkey)

        #// Vergleich ob empfangener Key und generierter Key gleich sind
        key = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        keys = str("%s%s" % (self._wskey, key)).encode('utf-8')
        nonce = base64.b64encode(keys)
        pdigest = base64.b64encode(hashlib.sha1(keys).digest())
        pdigest = pdigest.decode('UTF-8')

        # print('return', returnkey, ' = ', pdigest)
        if returnkey != pdigest:
            self._connected = False
            #print("Key nicht Akzeptiert")
        else:
            self._connected = True
            #print("Key Akzeptiert")
            print("Sucessfull WS connection to", self._host, ": ", self._port)
        return self._connected
    # // LG TV Connect
    def lg_handshake(self):
        if self._connected == False:
            self.connect()
        else:
            handshake = "{\"type\":\"register\",\"id\":\"register_0\",\"payload\":{\"forcePairing\":false,\"pairingType\":\"PROMT\",\"manifest\":{\"manifestVersion\":1,\"appVersion\":\"1.1\",\"signed\":{\"created\":\"20140509\",\"appId\":\"com.lge.test\",\"vendorId\":\"com.lge\",\"localizedAppNames\":{\"\":\"LG Remote App\",\"ko-KR\":\"리모컨 앱\",\"zxx-XX\":\"ЛГ Rэмotэ AПП\"},\"localizedVendorNames\":{\"\":\"LG Electronics\"},\"permissions\":[\"TEST_SECURE\",\"CONTROL_INPUT_TEXT\",\"CONTROL_MOUSE_AND_KEYBOARD\",\"READ_INSTALLED_APPS\",\"READ_LGE_SDX\",\"READ_NOTIFICATIONS\",\"SEARCH\",\"WRITE_SETTINGS\",\"WRITE_NOTIFICATION_ALERT\",\"CONTROL_POWER\",\"READ_CURRENT_CHANNEL\",\"READ_RUNNING_APPS\",\"READ_UPDATE_INFO\",\"UPDATE_FROM_REMOTE_APP\",\"READ_LGE_TV_INPUT_EVENTS\",\"READ_TV_CURRENT_TIME\"],\"serial\":\"2f930e2d2cfe083771f68e4fe7bb07\"},\"permissions\":[\"LAUNCH\",\"LAUNCH_WEBAPP\",\"APP_TO_APP\",\"CLOSE\",\"TEST_OPEN\",\"TEST_PROTECTED\",\"CONTROL_AUDIO\",\"CONTROL_DISPLAY\",\"CONTROL_INPUT_JOYSTICK\",\"CONTROL_INPUT_MEDIA_RECORDING\",\"CONTROL_INPUT_MEDIA_PLAYBACK\",\"CONTROL_INPUT_TV\",\"CONTROL_POWER\",\"READ_APP_STATUS\",\"READ_CURRENT_CHANNEL\",\"READ_INPUT_DEVICE_LIST\",\"READ_NETWORK_STATE\",\"READ_RUNNING_APPS\",\"READ_TV_CHANNEL_LIST\",\"WRITE_NOTIFICATION_TOAST\",\"READ_POWER_STATE\",\"READ_COUNTRY_INFO\"],\"signatures\":[{\"signatureVersion\":1,\"signature\":\"eyJhbGdvcml0aG0iOiJSU0EtU0hBMjU2Iiwia2V5SWQiOiJ0ZXN0LXNpZ25pbmctY2VydCIsInNpZ25hdHVyZVZlcnNpb24iOjF9.hrVRgjCwXVvE2OOSpDZ58hR+59aFNwYDyjQgKk3auukd7pcegmE2CzPCa0bJ0ZsRAcKkCTJrWo5iDzNhMBWRyaMOv5zWSrthlf7G128qvIlpMT0YNY+n/FaOHE73uLrS/g7swl3/qH/BGFG2Hu4RlL48eb3lLKqTt2xKHdCs6Cd4RMfJPYnzgvI4BNrFUKsjkcu+WD4OO2A27Pq1n50cMchmcaXadJhGrOqH5YmHdOCj5NSHzJYrsW0HPlpuAx/ECMeIZYDh6RMqaFM2DXzdKX9NmmyqzJ3o/0lkk/N97gfVRLW5hA29yeAwaCViZNCP8iC9aO0q9fQojoa7NQnAtw==\"}]}}}"
            if self._tvkey != '':  #handshakecode vorhanden
                handshake = handshake.replace('HANDSHAKECODE', self._tvkey)
            else:  #handshakecode nicht vorhanden
                handshake = "{\"type\":\"register\",\"id\":\"register_0\",\"payload\":{\"forcePairing\":false,\"pairingType\":\"PROMT\",\"manifest\":{\"manifestVersion\":1,\"appVersion\":\"1.1\",\"signed\":{\"created\":\"20140509\",\"appId\":\"com.lge.test\",\"vendorId\":\"com.lge\",\"localizedAppNames\":{\"\":\"LG Remote App\",\"ko-KR\":\"리모컨 앱\",\"zxx-XX\":\"ЛГ Rэмotэ AПП\"},\"localizedVendorNames\":{\"\":\"LG Electronics\"},\"permissions\":[\"TEST_SECURE\",\"CONTROL_INPUT_TEXT\",\"CONTROL_MOUSE_AND_KEYBOARD\",\"READ_INSTALLED_APPS\",\"READ_LGE_SDX\",\"READ_NOTIFICATIONS\",\"SEARCH\",\"WRITE_SETTINGS\",\"WRITE_NOTIFICATION_ALERT\",\"CONTROL_POWER\",\"READ_CURRENT_CHANNEL\",\"READ_RUNNING_APPS\",\"READ_UPDATE_INFO\",\"UPDATE_FROM_REMOTE_APP\",\"READ_LGE_TV_INPUT_EVENTS\",\"READ_TV_CURRENT_TIME\"],\"serial\":\"2f930e2d2cfe083771f68e4fe7bb07\"},\"permissions\":[\"LAUNCH\",\"LAUNCH_WEBAPP\",\"APP_TO_APP\",\"CLOSE\",\"TEST_OPEN\",\"TEST_PROTECTED\",\"CONTROL_AUDIO\",\"CONTROL_DISPLAY\",\"CONTROL_INPUT_JOYSTICK\",\"CONTROL_INPUT_MEDIA_RECORDING\",\"CONTROL_INPUT_MEDIA_PLAYBACK\",\"CONTROL_INPUT_TV\",\"CONTROL_POWER\",\"READ_APP_STATUS\",\"READ_CURRENT_CHANNEL\",\"READ_INPUT_DEVICE_LIST\",\"READ_NETWORK_STATE\",\"READ_RUNNING_APPS\",\"READ_TV_CHANNEL_LIST\",\"WRITE_NOTIFICATION_TOAST\",\"READ_POWER_STATE\",\"READ_COUNTRY_INFO\"],\"signatures\":[{\"signatureVersion\":1,\"signature\":\"eyJhbGdvcml0aG0iOiJSU0EtU0hBMjU2Iiwia2V5SWQiOiJ0ZXN0LXNpZ25pbmctY2VydCIsInNpZ25hdHVyZVZlcnNpb24iOjF9.hrVRgjCwXVvE2OOSpDZ58hR+59aFNwYDyjQgKk3auukd7pcegmE2CzPCa0bJ0ZsRAcKkCTJrWo5iDzNhMBWRyaMOv5zWSrthlf7G128qvIlpMT0YNY+n/FaOHE73uLrS/g7swl3/qH/BGFG2Hu4RlL48eb3lLKqTt2xKHdCs6Cd4RMfJPYnzgvI4BNrFUKsjkcu+WD4OO2A27Pq1n50cMchmcaXadJhGrOqH5YmHdOCj5NSHzJYrsW0HPlpuAx/ECMeIZYDh6RMqaFM2DXzdKX9NmmyqzJ3o/0lkk/N97gfVRLW5hA29yeAwaCViZNCP8iC9aO0q9fQojoa7NQnAtw==\"}]}}}"
                print("Sending LG handshake", handshake)

            response = self.send(handshake, '')
            print('RAW response nach handshake', response)

            if response != '':
                result = self.json_string(response)
                print("LG Handshake Response", result)
                if 'id' in result.keys() and result['id'] == 'result_0' and 'client-key' in result['payload'].keys():
                    #// LG client-key received: COMPARE!!!
                    if self._lg_key == result['payload']['client-key']:
                        print("LG Client-Key successfully approved")
                elif result and 'id' in result.keys() and result['id'] == 'register_0' and 'pairingType' in result['payload'].keys() and 'returnValue' in result['payload'].keys():
                    start = self.timestopp()
                    lg_key_received = False
                    error_received = False

                    while (self.timestopp()- start < 60 and not lg_key_received and not error_received):

                        response = self._sock.recv(8192)
                        print('HANDSHAKE RESPONSE ', response)
                        result = self.json_string(response)
                        if 'id' in result and result['id'] == 'register_0' and ('client-key' in result['payload']):
                            lg_key_received = True
                            self._lg_key = result['payload']['client-key']
                            print("LG Client-Key successfully received:", self._lg_key)
                        elif ('id' in result) and result['id'] == 'register_0' and ('error' in result):
                            error_received = True
                            print("ERROR: ", result['error'])
                       # time.sleep(2)
            else:
                print("ERROR during LG handshake:")
    # Disconnect
    def disconnect(self):
        self._connected = False
        self._sock.close()
        print("Connection closed to ", self._host)
    #Nachricht an TV senden
    def send(self, msg, funktion):
        msg = msg.encode()
        if funktion != "ws":
            msg = self.hybi10Encode(msg)
        #print("Send Funktion message", msg)
        self._sock.send(msg)
        response = self._sock.recv(8192)  #.encode('ascii').strip()
        return response
    #Erzeuge zufälligen String
    def generateRandomString(self, length=10, addSpaces=True, addNumbers=True):
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"Â§$%&/()=[]{}'
        useChars = []
        #// select some random chars:
        for i in range(0, length):
            useChars.append(characters[random.randint(0, len(characters) - 1)])

        #// add spaces and numbers:
        if (addSpaces == True):
            useChars.append(' ', ' ', ' ', ' ', ' ', ' ')

        if (addNumbers == True):
            useChars.append(random.randint(0, 9))
            useChars.append(random.randint(0, 9))
            useChars.append(random.randint(0, 9))

        random.shuffle(useChars)
        randomString = ''.join([str(i) for i in useChars])
        randomString = randomString.strip(' \t\n\r')
        randomString = randomString[0:length]

        return str(randomString).encode('utf-8')
    #Nachricht zu TV encoden
    def hybi10Encode(self, payload, type='text', masked=True):  # masked = True):
        frameHead = []
        payloadLength = len(payload)
        #payload = str(payload).encode('utf-8')

        #FRAMEHEAD
        ##Fin + RSV + TYPE
        if type == 'text':
            #// first byte indicates FIN, Text-Frame (10000001):
            frameHead.append(129)  #struct.pack('>B', 129)#129
        elif type == 'close':
            #// first byte indicates FIN, Close Frame(10001000):
            frameHead.append(136)  #struct.pack('>B', 136)#136
        elif type == 'ping':
            #// first byte indicates FIN, Ping frame (10001001):
            frameHead.append(137)  #struct.pack('>B', 137)
        elif type == 'pong':
            #// first byte indicates FIN, Pong frame (10001010):
            frameHead.append(138)  #struct.pack('>B', 138) #138

        ##set masking and payload length (using 1, 3 or 9 bytes)
        ###
        if (payloadLength > 65535):
            payloadLengthBin = struct.pack('>H', payloadLength)

            #1
            if masked == True:
                frameHead.append(255)  #struct.pack('>B', 255)
            else:
                frameHead.append(127)  #struct.pack('>B', 127)

            frameHead.append(int(payloadLengthBin[0]))  #2
            frameHead.append(int(payloadLengthBin[1]))  #3

            #// most significant bit MUST be 0 (close connection if frame too big)
            if (frameHead[2] > 127):
                self.close(1004)
                return False

        elif payloadLength > 125 and payloadLength < 65536:
            payloadLengthBin = struct.pack('>H', payloadLength)
            #print('mittlerer payloadfall', payloadLengthBin,payloadLengthBin[0], payloadLengthBin[1])

            if masked == True:
                frameHead.append(254)  #struct.pack('>B', 254)
            else:
                frameHead.append(126)  #struct.pack('>B', 126)
                #
            frameHead.append(int(payloadLengthBin[0]))  #struct.pack('>B', payloadLengthBin[0]) #2
            frameHead.append(int(payloadLengthBin[1]))  #struct.pack('>B', payloadLengthBin[1]) #3

        else:  #<=125
            if masked == True:
                frameHead.append(int(payloadLength + 128))#1
            else:
                frameHead.append(int(payloadLength))


        ##// Masking the framehead
        if masked == True:
            #// generate a random mask:
            mask = []
            for i in range(0, 4):
                mask.append(int(random.randint(0, 255)))

        ##//PAYLOADDATA
        payloaddata = []
        #print(payloadLength)
        for i in range(0, payloadLength):
            if masked == True:
                #print(chr(payload[i]), i)
                payloaddata.append(int(payload[i]) ^ int(mask[i % 4]))
            else:
                payloaddata.append(int(payload[i]))

        #|framehead|maskstr|payload^mask[i%4]
        frame = []
        frame.extend(frameHead)
        frame.extend(mask)
        frame.extend(payloaddata)

        #if self.debug == True:
        #print('framehead', frameHead)
        #print('mask', mask)
        #print('payloaddata', payloaddata)
         #   print('alle daten ', frame)

        # #// convert frame-head to string:###########################################################################
        #framehead+lenght+masking+data
        return bytes(frame)
    #Anweisung zu TV senden
    def send_command(self, cmd):
        if self._connected == False:
            self.connect()
        else:
            print("Sending command:", cmd)
            cmd = str(cmd).encode()
            cmd = self.hybi10Encode(cmd)
            #print('response von hyb10 encoder', cmd)
            self._sock.send(cmd)
            #print('response von send command', response)
            response = self._sock.recv(8192)
            if (response):
                responsedict = self.json_string(response)
                if "error" in responsedict.keys():
                    print("ERROR:" ,responsedict['error'], ", by id", responsedict['id'])
                    print("by this Command:", cmd)
                    #print("Command response:", response.decode('latin-1'))
            else:
                print("No Data Recieved! Error sending command:", cmd)
            return response
    def json_string(self, str):
        matches = re.search('({.*})', str.decode('latin-1'))
        str = matches.groups()
        print('JSON String ', str)
        result = json.loads(str[0])
        return result

#gibt aktuelle Zeit zurpck
    def timestopp(self):
        return time.time()

#------------------------------------------------------------------------------------------------------------------------
    ##Funktionen des TVS
    ##FB Emulation
    def set_volume(self, vol):
        #@ int volume
        command = '{"id":"set_volume","type":"request","uri":"ssap://audio/setVolume","payload":{"volume":"'+ str(vol) +'"}}'
        self.send_command(command)
    def set_poweroff(self):
        command = '{"id":"power_off","type":"request","uri":"ssap://system/turnOff"}'
        self.send_command(command)
    def set_mute(self):
        response = self.send_command('{"id":"status_","type":"request","uri":"ssap://audio/getVolume"}')
        #// {"type":"response","id":"status_1","payload":{"muted":false,"scenario":"mastervolume_tv_speaker","active":false,"action":"requested","volume":7,"returnValue":true,"subscribed":true}}
        return None
    def input_media_play(self):
        command = '{"id":"set_play","type":"request","uri":"ssap://media.controls/play"}'
        self.send_command(command)
    def input_media_stop(self):
        command = '{"id":"set_stop","type":"request","uri":"ssap://media.controls/stop"}'
        self.send_command(command)
    def input_media_pause(self):
        command = '{"id":"set_pause","type":"request","uri":"ssap://media.controls/pause"}'
        self.send_command(command)
    def input_media_rewind(self):
        command = '{"id":"set_rewind","type":"request","uri":"ssap://media.controls/rewind"}'
        self.send_command(command)
    def input_media_forward(self):
        command = '{"id":"set_fastForward","type":"request","uri":"ssap://media.controls/fastForward"}'
        self.send_command(command)
    def input_channel_up(self):
        command = '{"id":"set_channelUp","type":"request","uri":"ssap://tv/channelUp"}'
        self.send_command(command)
    def input_channel_down(self):
        command = '{"id":"set_channelDown","type":"request","uri":"ssap://tv/channelDown"}'
        self.send_command(command)
    def get_channel_info(self, id, channelnr):
        payload = {
            "channelId": id,
            "channelNumber":channelnr}
        command = '{"id":"channelinfo","type":"request","uri":"ssap://tv/openChannel","payload":'+ json.dumps(payload)+'}'
        self.send_command(command)

    def input_3d_on(self):
        command = '{"id":"set_3Don","type":"request","uri":"ssap://com.webos.service.tv.display/set3DOn"}'
        self.send_command(command)
    def input_3d_off(self):
        command = '{"id":"set_3Doff","type":"request","uri":"ssap://com.webos.service.tv.display/set3DOff"}'
        self.send_command(command)
    def get_audio_status(self):
        command = '{"id":"get_status","type":"request","uri":"ssap://audio/getStatus"}'
        #// send_command("status_", "subscribe", "ssap://audio/getStatus", null, fn);
        self.send_command(command)

    ##Zusatzfunktionen
    # Message auf TV
    def message(self, msg):
        payload = {
           "message": msg,
        }
        command = '{"id":"message","type":"request","uri":"ssap://system.notifications/createToast","payload":'+ json.dumps(payload)+'}'
        self.send_command(command)
        return None

    def message2(self,msg):# not working!°
        #@ message 	string 		Message to display (upto 60 characters)
        #@icon 	string 	<optional>
	    #@->Icon url for the notification (80x80 png format)
        #@appId 	string 	<optional>
	    #@->AppID of app to launch when toast is clicked. Only needed to specific a different appID than current app.
        #@appParams 	object 	<optional>
	    #@->Launch parameters to send when clicked.
        #@target 	string 	<optional>
	    #@->A target filepath to open; must be a valid webOS mimetype. An alternative to appId and params.
        #@noaction 	boolean 	<optional>
	    #@->If clicking the toast should do nothing.
        #@stale 	boolean 	<optional>
	    #@->If true, it's not actively displayed as a new notification.
        iconData = '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'

        payload = {
           "message": msg,
           "iconData" : iconData,
           "iconExtension" : "png",
           "noaction": "1",
           "target": "_blank"
        }
        command = '{"id":"message","type":"request","uri":"palm://system.notifications/createToast","payload":'+ json.dumps(payload)+'}'
        self.send_command(command)

    def  open_browser_at(self, url):
        #@url url with http/https
    #// response: {"type":"response","id":"0","payload":{"returnValue":true,"id":"com.webos.app.browser","sessionId":"Y29tLndlYm9zLmFwcC5icm93c2VyOnVuZGVmaW5lZA=="}}
        print('opening browser at:', url)
        protocol = url[0:7]
        if (protocol != 'http://' and protocol != 'https:/'):
            url = "http://" + url
            command = '{"id":"open_browser","type":"request","uri":"ssap://system.launcher/open", "payload":{"target":"' + url +'"}}'
            self.send_command(command)

    def channellist(self):
        command = '{"id":"channels_","type":"request","uri":"ssap://tv/getChannelList"}'
      #// send_command("channels_", "subscribe", "ssap://tv/getChannelList", null, function(err, resp) {
        self.send_command(command)
          #  var channellistarray = resp.payload.channelList;
          #  var retlist = {channels : []};
          #  for (var i = channellistarray.length - 1; i >= 0; i--) {
          #    var ch = {id: channellistarray[i].channelId,
          #              name: channellistarray[i].channelName,
          #              number: channellistarray[i].channelNumber};
          #    // console.log(channellistarray[i]);
          #    console.log(ch);
          #    retlist.channels.push(ch);
           # }
    def get_channel(self):
        command = '{"id":"channels_","type":"request","uri":"ssap://tv/getCurrentChannel"}'
        self.send_command(command)
    def set_channel(self,channel):
        #/* set the active channel; use channelId as from the channellist, such as eg 0_13_7_0_0_1307_0 */
        command = '{"id":"channels_","type":"request","uri":"ssap://tv/openChannel", "payload":{"channelId":"' + channel +'"}}'
        self.send_command(command)

    def set_input_source(self):
        command = '{"id":"","type":"request","uri":"ssap://tv/switchInput", "payload":{"inputId:":"' + input +'"}}'
        response = self.send_command(command)
        if "features" in response.keys():
            print(response[features])
    def get_input_list(self):
        #// <--- received: {"type":"response","id":"input_1","payload": {"devices":[{"id":"SCART_1","label":"AV1","port":1,"appId":"com.webos.app.externalinput.scart","icon":"http://lgsmarttv.lan:3000/resources/f84946f3119c23cda549bdcf6ad02a89c73f7682/scart.png","modified":false,"autoav":false,"currentTVStatus":"","subList":[],"subCount":0,"connected":false,"favorite":false},{...}, {...}],"returnValue":true}}
        command = '{"id":"input_","type":"request","uri":"ssap://tv/getExternalInputList"}'
        self.send_command(command)
    def media_player_open(self, url):
        command = '{"id":"myVideo","type":"WIDEVINE","uri":"ssap://media.viewer/open", "payload":{"dataURL":"' + url +'"}}'
        self.send_command(command)

    def get_SW_info(self):
         command = '{"id":"sw_info","type":"request","uri":"ssap://com.webos.service.update/getCurrentSWInformation"}'
         self.send_command(command)
    def get_services(self):

        command = '{"id":"services_","type":"request","uri":"ssap://api/getServiceList"}'
        self.send_command(command)
    def get_systemInfo(self):
        #luna://com.webos.service.tv.systemproperty", {
        command = '{"id":"system_info","type":"request","uri":"ssap://com.webos.service.tv.systemproperty"}'
        self.send_command(command)

    def show_image(self, url, title = "", desc =""):
        mime = MimeTypes()
        mime_type = mime.guess_type(url)

        payload = {
            "target": url,
            "title":title,
            "description":desc,
            "mimeType":mime_type[0],
            "iconSrc":url}
        command = '{"id":"images","type":"request","uri":"ssap://media.viewer/open","payload":'+ json.dumps(payload)+'}'
        self.send_command(command)

    def show_media(self, url, title = "", desc ="", loop = 0):
        mime = MimeTypes()
        mime_type = mime.guess_type(url)
        payload = {
            "target": url,
            "title":title,
            "description":desc,
            "mimeType": mime_type[0],
            "iconSrc":"",
            "loop":loop}
        command = '{"id":"images","type":"request","uri":"ssap://media.viewer/open","payload":'+ json.dumps(payload)+'}'
        self.send_command(command)


tv = WebOsTv('192.168.178.57', 3000)
