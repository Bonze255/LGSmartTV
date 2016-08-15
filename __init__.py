#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#
# Copyright 2012 KNX-User-Forum e.V.            http://knx-user-forum.de/
#
#  This file is part of SmartHome.py.    http://mknx.github.io/smarthome/
#
#  SmartHome.py is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHome.py is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHome.py.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
import socket
import time
import base64

from uuid import getnode as getmac

logger = logging.getLogger('')


class LGSmartTV():

    def __init__(self, smarthome, host, port=55000):
        self._sh = smarthome
        self._host = host
        self._port = port
        self._tvid = int(tvid)
        
        
    def parse_item(self, item):
        if 'smarttv' in item.conf:
            logger.debug("Smart TV Item {0} with value {1} for TV found!".format(
                item, item.conf['smarttv']))
            return self.update_item
        else:
            return None

    def update_item(self, item, caller=None, source=None, dest=None):
        val = item()
        if isinstance(val, str):
            if val.startswith('KEY_'):
                self.push(val)
            return
        if val:
            keys = item.conf['smarttv']
            if isinstance(keys, str):
                keys = [keys]
            for key in keys:
                if isinstance(key, str) and key.startswith('KEY_'):
                    self.push(key)

    def parse_logic(self, logic):
        pass

    def run(self):
        self.alive = True
        return None

    def stop(self):
        self.alive = False
        return None
        
    #Creates a Websocket Connection    
    def connect(self):
        ws_handshake_cmd = "GET "+str(self._path)+" HTTP/1.1\r\n"
        ws_handshake_cmd += "Upgrade: websocket\r\n"
        ws_handshake_cmd += "Connection: Upgrade\r\n"
        ws_handshake_cmd += "Sec-WebSocket-Version: 13\r\n"
        ws_handshake_cmd += "Sec-WebSocket-Key: "+ str(self._wskey) + "\r\n"
        ws_handshake_cmd += "Host: "+ str(self._host)+":"+str(self._port)+"\r\n\r\n"
    
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self._host, self._port))
            self._sock.settimeout(5)
        except:
            print("Verbindung zu ", str(self._host), "nicht möglich!")
    
        print("Sending WS handshake", ws_handshake_cmd)
        response = self.send(ws_handshake_cmd)
        #print ("debug-ausgabe von response", response)
    
        if response != '':
            print("WS Handshake Response:", response)
        else:
            print("ERROR during WS handshake!")
    
        matches = re.search(b'Sec-WebSocket-Accept:\s*(.*=)', response)
        #print("ergebnis ",matches)
    
        keyAccept = matches.group().strip()
        print("keyaccept ",keyAccept)
        #try:
        #print("WSKEY", self._wskey)
        expectedResonse = base64.b64encode(hashlib.sha1(self._wskey + b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11').digest())
        print("expected response",expectedResonse)
        if keyAccept == expectedResonse:
            self._connected = True
            print("Key Akzeptiert")
        else:
            self._connected = False
            print("Key nicht Akzeptiert")
        #except:
        #    print('Fehler!')
        #else:
        #    self._connected = False
    
        if self._connected:
            print( "Sucessfull WS connection to", self._host, ": ", self._port)
        return self._connected

        
    def disconnect(self):
        self._connected = False
        self._sock.close()
        print("Connection closed to ",self._host)
        return None
        
    #Creates a Handshake with the TV (Pairing)
    def lg_handshake(self):
        if self._connected == False:
            self.connect()
        if self._connected:
            handshake ='{"type":"register","id":"register_0","payload":{"forcePairing":False,"pairingType":"PROMPT","client-key":"'+str(self._handshakecode)+'manifest":{"manifestVersion":1,"appVersion":"1.1","signed":{"created":"20140509","appId":"com.lge.test","vendorId":"com.lge","localizedAppNames":{"":"LG Remote App","ko-KR":"ë¦¬ëª¨ì»¨ ì•±","zxx-XX":"Ð›Ð“ RÑ?Ð¼otÑ? AÐŸÐŸ"},"localizedVendorNames":{"":"LG Electronics"},"permissions":["TEST_SECURE","CONTROL_INPUT_TEXT","CONTROL_MOUSE_and_KEYBOARD","READ_INSTALLED_APPS","READ_LGE_SDX","READ_NOTIFICATIONS","SEARCH","WRITE_SETTINGS","WRITE_NOTIFICATION_ALERT","CONTROL_POWER","READ_CURRENT_CHANNEL","READ_RUNNING_APPS","READ_UPDATE_INFO","UPDATE_FROM_REMOTE_APP","READ_LGE_TV_INPUT_EVENTS","READ_TV_CURRENT_TIME"],"serial":"2f930e2d2cfe083771f68e4fe7bb07"},"permissions":["LAUNCH","LAUNCH_WEBAPP","APP_TO_APP","CLOSE","TEST_OPEN","TEST_PROTECTED","CONTROL_AUDIO","CONTROL_DISPLAY","CONTROL_INPUT_JOYSTICK","CONTROL_INPUT_MEDIA_RECORDING","CONTROL_INPUT_MEDIA_PLAYBACK","CONTROL_INPUT_TV","CONTROL_POWER","READ_APP_STATUS","READ_CURRENT_CHANNEL","READ_INPUT_DEVICE_LIST","READ_NETWORK_STATE","READ_RUNNING_APPS","READ_TV_CHANNEL_LIST","WRITE_NOTIFICATION_TOAST","READ_POWER_STATE","READ_COUNTRY_INFO"],"signatures":[{"signatureVersion":1,"signature":"eyJhbGdvcml0aG0iOiJSU0EtU0hBMjU2Iiwia2V5SWQiOiJ0ZXN0LXNpZ25pbmctY2VydCIsInNpZ25hdHVyZVZlcnNpb24iOjF9.hrVRgjCwXVvE2OOSpDZ58hR+59aFNwYDyjQgKk3auukd7pcegmE2CzPCa0bJ0ZsRAcKkCTJrWo5iDzNhMBWRyaMOv5zWSrthlf7G128qvIlpMT0YNY+n/FaOHE73uLrS/g7swl3/qH/BGFG2Hu4RlL48eb3lLKqTt2xKHdCs6Cd4RMfJPYnzgvI4BNrFUKsjkcu+WD4OO2A27Pq1n50cMchmcaXadJhGrOqH5YmHdOCj5NSHzJYrsW0HPlpuAx/ECMeIZYDh6RMqaFM2DXzdKX9NmmyqzJ3o/0lkk/N97gfVRLW5hA29yeAwaCViZNCP8iC9aO0q9fQojoa7NQnAtw=="}]}}}'
            if self._lg_key != '':
                handshake = str.replace(self._handshakecode,self._lg_key)
            else:
                handshake = '{"type":"register","id":"register_0","payload":{"forcePairing":False,"pairingType":"PROMPT","manifest":{"manifestVersion":1,"appVersion":"1.1","signed":{"created":"20140509","appId":"com.lge.test","vendorId":"com.lge","localizedAppNames":{"":"LG Remote App","ko-KR":"ë¦¬ëª¨ì»¨ ì•±","zxx-XX":"Ð›Ð“ RÑ?Ð¼otÑ? AÐŸÐŸ"},"localizedVendorNames":{"":"LG Electronics"},"permissions":["TEST_SECURE","CONTROL_INPUT_TEXT","CONTROL_MOUSE_and_KEYBOARD","READ_INSTALLED_APPS","READ_LGE_SDX","READ_NOTIFICATIONS","SEARCH","WRITE_SETTINGS","WRITE_NOTIFICATION_ALERT","CONTROL_POWER","READ_CURRENT_CHANNEL","READ_RUNNING_APPS","READ_UPDATE_INFO","UPDATE_FROM_REMOTE_APP","READ_LGE_TV_INPUT_EVENTS","READ_TV_CURRENT_TIME"],"serial":"2f930e2d2cfe083771f68e4fe7bb07"},"permissions":["LAUNCH","LAUNCH_WEBAPP","APP_TO_APP","CLOSE","TEST_OPEN","TEST_PROTECTED","CONTROL_AUDIO","CONTROL_DISPLAY","CONTROL_INPUT_JOYSTICK","CONTROL_INPUT_MEDIA_RECORDING","CONTROL_INPUT_MEDIA_PLAYBACK","CONTROL_INPUT_TV","CONTROL_POWER","READ_APP_STATUS","READ_CURRENT_CHANNEL","READ_INPUT_DEVICE_LIST","READ_NETWORK_STATE","READ_RUNNING_APPS","READ_TV_CHANNEL_LIST","WRITE_NOTIFICATION_TOAST","READ_POWER_STATE","READ_COUNTRY_INFO"],"signatures":[{"signatureVersion":1,"signature":"eyJhbGdvcml0aG0iOiJSU0EtU0hBMjU2Iiwia2V5SWQiOiJ0ZXN0LXNpZ25pbmctY2VydCIsInNpZ25hdHVyZVZlcnNpb24iOjF9.hrVRgjCwXVvE2OOSpDZ58hR+59aFNwYDyjQgKk3auukd7pcegmE2CzPCa0bJ0ZsRAcKkCTJrWo5iDzNhMBWRyaMOv5zWSrthlf7G128qvIlpMT0YNY+n/FaOHE73uLrS/g7swl3/qH/BGFG2Hu4RlL48eb3lLKqTt2xKHdCs6Cd4RMfJPYnzgvI4BNrFUKsjkcu+WD4OO2A27Pq1n50cMchmcaXadJhGrOqH5YmHdOCj5NSHzJYrsW0HPlpuAx/ECMeIZYDh6RMqaFM2DXzdKX9NmmyqzJ3o/0lkk/N97gfVRLW5hA29yeAwaCViZNCP8iC9aO0q9fQojoa7NQnAtw=="}]}}}'
                print("Sending LG handshake",handshake)
            response = self.send(hybi10Encode(handshake))
            if response == True:
                print("LG Handshake Response",json_string(response))
                result = json_array(response)
                if result and ('id' in result) and  result['id']=='result_0' and ('client-key' in result['payload']):
                    #// LG client-key received: COMPARE!!!
                    if self._lg_key == result['payload']['client-key']:
                        print("LG Client-Key successfully approved")
                    else:
                        if result and ('id'in result) and  result['id']=='register_0' and ('pairingType' in result['payload']) and ('returnValue' in result['payload']):
                            #// LG TV is prompting for access rights
                            if (result['payload']['pairingType'] == 'PROMPT') and (result['payload']['returnValue'] == 'True'):
                                starttime = time.time()
                                lg_key_received = False
                                error_received = False
                                while (time-starttime<60 and not lg_key_received and not error_received):
                                    response = read(self._sock, 8192)
                                    result = json_array(response)
                                    if result == True and ('id' in result) and  result['id']=='register_0' and is_array(result['payload']) and ('client-key' in result['payload']):
                                        lg_key_received = True
                                        self._lg_key = result['payload']['client-key']
                                        print("LG Client-Key successfully received:",self._lg_key)
                                    elif result and ('id' in result) and  result['id']=='register_0' and ('error' in result):
                                        error_received = True
                                        print("ERROR: ",result['error'])
                                    time.sleep(200000 / 1000000.0)#usleep(200000)
                                    time = time.time()
            else:
                print("ERROR during LG handshake:")
        else:
            return False
        
    #Send Websocket Messages to the TV
    def send(self, msg):
        print("Send Funktion message", msg )
        self._sock.send(msg.encode())
        #write(self._sock, msg)
        time.sleep(2500 / 1000000.0)#usleep(250000)
        response = self._sock.recv(8192)
        print("Send Response", response)
        return response
        
    #Sends Commands to the TV
    def send_command(self, cmd):
        if (self._connected == False):
            self.connect()
        if (self._connected == True):
            print("Sending command:", cmd)
            response = self._send(self.hybi10Encode(cmd))
            if (response):
                print("Command response:",self.json_string(response))
            else:
                print("Error sending command:",cmd)
            return response
    #Encode the Packets wich are send to the TV    
    def hybi10Encode(self,payload, type = 'text', masked = True):
    frameHead = []
    frame = ''
    payloadLength = len(payload)

    if type == 'text':
        #// first byte indicates FIN, Text-Frame (10000001):
        frameHead[0] = 129
    elif type == 'close':
        #// first byte indicates FIN, Close Frame(10001000):
        frameHead[0] = 136
    elif type == 'ping':
        #// first byte indicates FIN, Ping frame (10001001):
        frameHead[0] = 137
    elif type == 'pong':
        #// first byte indicates FIN, Pong frame (10001010):
        frameHead[0] = 138

    #// set mask and payload length (using 1, 3 or 9 bytes)
    if (payloadLength > 65535):
        payloadLengthBin = str_split(sprintf('%064b', payloadLength), 8)
        if masked == True:
            frameHead[1] = 255
        else:
            frameHead[1] =  127

        for i in  range(0,8):
            frameHead[i + 2] = bindec(payloadLengthBin[i])

        #// most significant bit MUST be 0 (close connection if frame too big)
        if (frameHead[2] > 127):
            self.close(1004)
            return False
    elif payloadLength > 125:
        ##payloadLengthBin = str_split(sprintf('%016b', $payloadLength), 8)

        if masked == True:
            frameHead[1] = 254
        else:
            frameHead[1] = 126
        frameHead[2] = bindec(payloadLengthBin[0])
        frameHead[3] = bindec(payloadLengthBin[1])
    else:
        if masked ==  True:
            frameHead[1] = payloadLength + 128
        else:
            frameHead[1] = payloadLength

    #// convert frame-head to string:
    for i in frameHead.iterkeys():
        frameHead[i] = chr(frameHead[i])

    if masked == True:
        #// generate a random mask:
        mask = []
        for i in range(0,4):
            mask[i] = chr(rand(0, 255))
        frameHead = array_merge(frameHead, mask)
    frame = implode('', frameHead)
    #// append payload to frame:
    for i in range(i, payloadLength):
        if masked == True:
            frame += payload[i] ^ mask[i % 4]
        else:
            frame += payload[i]
    return frame
    
    #Generates a Random String for Websocket Connection
    def generateRandomString(self, length = 10, addSpaces = True, addNumbers = True):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"Â§$%&/()=[]{}'
    useChars = []
    #// select some random chars:
    for i in range(0, length):
        useChars.append( characters[random.randint (0, len(characters)-1)])

    #// add spaces and numbers:
    if(addSpaces == True):
        useChars.append(' ', ' ', ' ', ' ', ' ', ' ')

    if(addNumbers == True):

        useChars.append(random.randint(0,9))
        useChars.append(random.randint(0,9))
        useChars.append(random.randint(0,9))
    random.shuffle(useChars)
    randomString = ''.join([str(i) for i in useChars])
    randomString = randomString.strip(' \t\n\r')
    randomString = randomString[0:length]
    print("RandomString", randomString)
    return randomString
    
    #Return a Json-Conform String    
    def json_string(self,str):
    start = strpos(str,"{")
    end = strripos(str,"}")
    len = end-start+1
    result = substr(str,start,len)
    return result

