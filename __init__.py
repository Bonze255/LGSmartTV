import logging
import socket
import time
import base64

from uuid import getnode as getmac

logger = logging.getLogger('')


class webOSTV:

    def __init__(self, smarthome, host, port=3000, lgKey="NOKEY", path="/"):
        self._sh = smarthome
        self._host = host
        self._port = port
        self._wskey = key = base64_encode(generateRandomString(16, false, true))
        self._tvkey = lgkey
        self._path = str(path)
        self._handshake = false
        self._connected = false
        if self._tvkey == "NOKEY":
            unset(self._tvkey)

    def connect(self):
        ws_handshake_cmd = "GET "+self._path+" HTTP/1.1\r\n"
        ws_handshake_cmd += "Upgrade: websocket\r\n"
        ws_handshake_cmd += "Connection: Upgrade\r\n"
        ws_handshake_cmd += "Sec-WebSocket-Version: 13\r\n"
        ws_handshake_cmd += "Sec-WebSocket-Key: "+ self._wskey + "\r\n"
        ws_handshake_cmd += "Host: "+self._host+":"+self._port+"\r\n\r\n"
        #self._sock = fsockopen(self._host, self._port, errn, errstr, 2)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self._host, self._port))
        self._sock.settimeout(10000)

        print("Sending WS handshake", ws_handshake_cmd)
        response = self.send(ws_handshake_cmd)
        print ("debug-ausgabe", response)

        if response == True:
            print("WS Handshake Response:", response)
        else:
            print("ERROR during WS handshake!")
        matches = re.match('#Sec-WebSocket-Accept:\s(.*)$#mU', response)
        try:
            keyAccept = trim(matches[1])
            #expectedResonse = base64_encode(pack('H*', sha1(self._wskey . '258EAFA5-E914-47DA-95CA-C5AB0DC85B11')))
            if keyAccept == expectedResonse:
                self._connected = True
            else:
                self._connected = False
        except:
            print('Fehler!')
        else:
            self._connected = False

        if self._connected:
            print( "Sucessfull WS connection to", self._host, ": ", self._port)
        return self._connected

    def lg_handshake():
        if self._connected == False:
            self.connect()
        if self._connected:
        	#handshake ="{"type":"register","id":"register_0","payload":{"forcePairing":false,"pairingType":"PROMPT","client-key":"HandSHAKEKEYGOESHERE","manifest":{"manifestVersion":1,"appVersion":"1.1","signed":{"created":"20140509","appId":"com.lge.test","vendorId":"com.lge","localizedAppNames":{"":"LG Remote App","ko-KR":"ë¦¬ëª¨ì»¨ ì•±","zxx-XX":"Ð›Ð“ RÑ?Ð¼otÑ? AÐŸÐŸ"},"localizedVendorNames":{"":"LG Electronics"},"permissions":["TEST_SECURE","CONTROL_INPUT_TEXT","CONTROL_MOUSE_and_KEYBOARD","READ_INSTALLED_APPS","READ_LGE_SDX","READ_NOTIFICATIONS","SEARCH","WRITE_SETTINGS","WRITE_NOTIFICATION_ALERT","CONTROL_POWER","READ_CURRENT_CHANNEL","READ_RUNNING_APPS","READ_UPDATE_INFO","UPDATE_FROM_REMOTE_APP","READ_LGE_TV_INPUT_EVENTS","READ_TV_CURRENT_TIME"],"serial":"2f930e2d2cfe083771f68e4fe7bb07"},"permissions":["LAUNCH","LAUNCH_WEBAPP","APP_TO_APP","CLOSE","TEST_OPEN","TEST_PROTECTED","CONTROL_AUDIO","CONTROL_DISPLAY","CONTROL_INPUT_JOYSTICK","CONTROL_INPUT_MEDIA_RECORDING","CONTROL_INPUT_MEDIA_PLAYBACK","CONTROL_INPUT_TV","CONTROL_POWER","READ_APP_STATUS","READ_CURRENT_CHANNEL","READ_INPUT_DEVICE_LIST","READ_NETWORK_STATE","READ_RUNNING_APPS","READ_TV_CHANNEL_LIST","WRITE_NOTIFICATION_TOAST","READ_POWER_STATE","READ_COUNTRY_INFO"],"signatures":[{"signatureVersion":1,"signature":"eyJhbGdvcml0aG0iOiJSU0EtU0hBMjU2Iiwia2V5SWQiOiJ0ZXN0LXNpZ25pbmctY2VydCIsInNpZ25hdHVyZVZlcnNpb24iOjF9.hrVRgjCwXVvE2OOSpDZ58hR+59aFNwYDyjQgKk3auukd7pcegmE2CzPCa0bJ0ZsRAcKkCTJrWo5iDzNhMBWRyaMOv5zWSrthlf7G128qvIlpMT0YNY+n/FaOHE73uLrS/g7swl3/qH/BGFG2Hu4RlL48eb3lLKqTt2xKHdCs6Cd4RMfJPYnzgvI4BNrFUKsjkcu+WD4OO2A27Pq1n50cMchmcaXadJhGrOqH5YmHdOCj5NSHzJYrsW0HPlpuAx/ECMeIZYDh6RMqaFM2DXzdKX9NmmyqzJ3o/0lkk/N97gfVRLW5hA29yeAwaCViZNCP8iC9aO0q9fQojoa7NQnAtw=="}]}}}"
            if self._lg_key != '':
                handshake = str.replace('HandSHAKEKEYGOESHERE',self._lg_key)
            else:
               # handshake = "{"type":"register","id":"register_0","payload":{"forcePairing":false,"pairingType":"PROMPT","manifest":{"manifestVersion":1,"appVersion":"1.1","signed":{"created":"20140509","appId":"com.lge.test","vendorId":"com.lge","localizedAppNames":{"":"LG Remote App","ko-KR":"ë¦¬ëª¨ì»¨ ì•±","zxx-XX":"Ð›Ð“ RÑ?Ð¼otÑ? AÐŸÐŸ"},"localizedVendorNames":{"":"LG Electronics"},"permissions":["TEST_SECURE","CONTROL_INPUT_TEXT","CONTROL_MOUSE_and_KEYBOARD","READ_INSTALLED_APPS","READ_LGE_SDX","READ_NOTIFICATIONS","SEARCH","WRITE_SETTINGS","WRITE_NOTIFICATION_ALERT","CONTROL_POWER","READ_CURRENT_CHANNEL","READ_RUNNING_APPS","READ_UPDATE_INFO","UPDATE_FROM_REMOTE_APP","READ_LGE_TV_INPUT_EVENTS","READ_TV_CURRENT_TIME"],"serial":"2f930e2d2cfe083771f68e4fe7bb07"},"permissions":["LAUNCH","LAUNCH_WEBAPP","APP_TO_APP","CLOSE","TEST_OPEN","TEST_PROTECTED","CONTROL_AUDIO","CONTROL_DISPLAY","CONTROL_INPUT_JOYSTICK","CONTROL_INPUT_MEDIA_RECORDING","CONTROL_INPUT_MEDIA_PLAYBACK","CONTROL_INPUT_TV","CONTROL_POWER","READ_APP_STATUS","READ_CURRENT_CHANNEL","READ_INPUT_DEVICE_LIST","READ_NETWORK_STATE","READ_RUNNING_APPS","READ_TV_CHANNEL_LIST","WRITE_NOTIFICATION_TOAST","READ_POWER_STATE","READ_COUNTRY_INFO"],"signatures":[{"signatureVersion":1,"signature":"eyJhbGdvcml0aG0iOiJSU0EtU0hBMjU2Iiwia2V5SWQiOiJ0ZXN0LXNpZ25pbmctY2VydCIsInNpZ25hdHVyZVZlcnNpb24iOjF9.hrVRgjCwXVvE2OOSpDZ58hR+59aFNwYDyjQgKk3auukd7pcegmE2CzPCa0bJ0ZsRAcKkCTJrWo5iDzNhMBWRyaMOv5zWSrthlf7G128qvIlpMT0YNY+n/FaOHE73uLrS/g7swl3/qH/BGFG2Hu4RlL48eb3lLKqTt2xKHdCs6Cd4RMfJPYnzgvI4BNrFUKsjkcu+WD4OO2A27Pq1n50cMchmcaXadJhGrOqH5YmHdOCj5NSHzJYrsW0HPlpuAx/ECMeIZYDh6RMqaFM2DXzdKX9NmmyqzJ3o/0lkk/N97gfVRLW5hA29yeAwaCViZNCP8iC9aO0q9fQojoa7NQnAtw=="}]}}}"
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
                    if (result['payload']['pairingType'] == "PROMPT") and (result['payload']['returnValue'] == 'true'):
                    	starttime = microtime(1)
                        lg_key_received = false
                        error_received = false
                        while (time-starttime<60 and not lg_key_received and not error_received):
                            response = @fread(self._sock, 8192)
                            result = json_array(response)
                            if result == True and ('id' in result) and  result['id']=='register_0' and is_array(result['payload']) and ('client-key' in result['payload']):
                                lg_key_received = true
                                self._lg_key = result['payload']['client-key']
                                print("LG Client-Key successfully received:",self._lg_key)
                            elif result and ('id' in result) and  result['id']=='register_0' and ('error' in result):
                                error_received = true
                                print("ERROR: ",result['error'])
                            usleep(200000)
                            time = microtime(1)

            else:
                print("ERROR during LG handshake:")
        else:
            return False

    def disconnect(self):
        self._connected = False
        @fclose(self._sock)
        print("Connection closed to ",self._host)

    def send(self, msg):
        @fwrite(self._sock, msg)
        usleep(250000)
        response = @fread(self._sock, 8192)
        return response

    def send_command(self, cmd)
        if (self._connected == False):
            self.connect()
        if (self._connected == True):
            print("Sending command:", cmd)
            response = self._send(hybi10Encode(cmd))
            if (response):
                print("Command response:",json_string(response))
            else:
                print("Error sending command:",cmd)
            return response

    def message(msg):
        command = "{"id":"message","type":"request","uri":"ssap://system.notifications/createToast","payload":{"message": "msg"}}"
        self._send_command(command)

    def power_off():
        command = "{"id":"power_off","type":"request","uri":"ssap://system/turnOff"}"
        self._send_command(command)

    def set_volume(vol):
        command = "{"id":"set_volume","type":"request","uri":"ssap://audio/setVolume","payload":{"volume":".vol."}}"
        self._send_command(command)

    def hybi10Encode(payload, type = 'text', masked = true):
        frameHead = []
        frame = ''
        payloadLength = strlen(payload)

        switch (type) {
            case 'text':
                #// first byte indicates FIN, Text-Frame (10000001):
                frameHead[0] = 129
                break

            case 'close':
                #// first byte indicates FIN, Close Frame(10001000):
                frameHead[0] = 136
                break

            case 'ping':
                #// first byte indicates FIN, Ping frame (10001001):
                frameHead[0] = 137
                break

            case 'pong':
                #// first byte indicates FIN, Pong frame (10001010):
                frameHead[0] = 138
                break
        }

        #// set mask and payload length (using 1, 3 or 9 bytes)
        if (payloadLength > 65535):
            payloadLengthBin = str_split(sprintf('%064b', payloadLength), 8)
            frameHead[1] = (masked == true) ? 255 : 127
            for (i = 0 i < 8 i++):
                frameHead[i + 2] = bindec(payloadLengthBin[i])

            #// most significant bit MUST be 0 (close connection if frame too big)
            if (frameHead[2] > 127):
                self.close(1004)
                return false
        elif (payloadLength > 125):
            payloadLengthBin = str_split(sprintf('%016b', $payloadLength), 8)
            frameHead[1] = (masked == true) ? 254 : 126
            frameHead[2] = bindec($payloadLengthBin[0])
            frameHead[3] = bindec($payloadLengthBin[1])
        else:
            frameHead[1] = (masked == true) ? payloadLength + 128 : payloadLength


        #// convert frame-head to string:
        for(array_keys(frameHead) as i):
            frameHead[i] = chr(frameHead[i])

        if (masked === true):
            #// generate a random mask:
            mask = []
            for (i = 0 i < 4 i++):
                mask[i] = chr(rand(0, 255))
            frameHead = array_merge(frameHead, mask)
        frame = implode('', frameHead)
        #// append payload to frame:
        for (i = 0 i < payloadLength i++):
            frame += (masked === true) ? payload[i] ^ mask[i % 4] : payload[i]
        return frame

    def generateRandomString(length = 10, addSpaces = true, addNumbers = true)
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"Â§$%&/()=[]{}'
        useChars = []
        #// select some random chars:
        for(i = 0 i < length i++):
            useChars[] = characters[mt_rand(0, strlen(characters)-1)]

        #// add spaces and numbers:
        if(addSpaces == True):
            #array_push(useChars, ' ', ' ', ' ', ' ', ' ', ' ')
            useChars.append( ' ', ' ', ' ', ' ', ' ', ' ')

        if(addNumbers == True):
            #array_push(useChars, rand(0,9), rand(0,9), rand(0,9))
            useChars.append(useChars, rand(0,9), rand(0,9), rand(0,9))
        shuffle(useChars)
        randomString = trim(implode('', useChars))
        randomString = substr(randomString, 0, length)
        return randomString


    def json_array(str):
        result = json_decode(json_string(str),true)
        return result

    def json_string(str):
        from = strpos(str,"{")
        to = strripos(str,"}")
        len = to-from+1
        result = substr(str,from,len)
        return result

    def run(self):
        tv = new webOSTV("192.168.0.200",3000,"785cff4fef58555ef82188b83cda579e")
        self.connect()                     //
        self._lg_handshake()
        self._message("YEAH, it works!!!")
        sleep (5)
        self._set_volume(75)
        sleep(10)
        self._disconnect()
