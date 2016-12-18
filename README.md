# LGSmartTV
WebOS Plugin for SarthomeNG.py
(https://github.com/ConnectSDK/Connect-SDK-Android-Core/blob/master/src/com/connectsdk/service/WebOSTVService.java)
Its possible to show Pictues or Messages on the Screen.
Remote Emulation is also possible.

Example:
The Doorbell rings -> Webcam shows a picture from the Visitor

or

A New Mail is recieved, a Message is shown on the TV.

# Requirements
This plugin has no requirements or dependencies.

# Configuration

## plugin.conf
<pre>
[LgSmartTv]
    class_name = LGSmartTV
    class_path = plugins.lgsmarttv
    host = 192.168.178.56
	port = 3000
	tvid = 1
</pre>

### Attributes
  * `host`: specifies the ip address of your SmartTV device.
  * `port`: if you want to use a nonstandard port.

## items.conf
<pre>
[smarttv]
	type = str
    smarttv = true
    smarttv_id = 1
    enforce_updates = true
	[[handshake]]
	    name = "Activate Handshake"
		type = bool
        smarttv = "HANDSHAKE"
		visu_acl = rw
    [[handshakekey]]
		name = Handshakekey
		type = str
        smarttv = true
        smarttv_handshake = 1
        sql = True
		cache = True
		visu_acl = rw
    [[message]]
        name = Hellomessage
        type = bool
        visu_acl = rw
        enforce_updates = true
		smarttv_id = 1
		smarttv = KEY_msg                                   #Befehl
        smarttv_value = "Herzlich Willkommen by SmarthomeNG"#value
        knx_dpt = 1
        knx_listen = 0/0/7

</pre>
### LGSmartTv
There are two possibilities to use this attribute. 
  * Define it on a string item and set it to `true`: With this configuration, every string you set to this item will be send to the SmartTV device.
  * Define it on a boolean item and set it to a key value: With this configuration, the specified key value is sent whenever you set the item to `true` (if the item is only for sending a specific command to the tv then you should consider using the `enforce_updates` attribute, too).
  * for functions witch have more than one variable, they must been seperated with an ","; shown by the examples 


## Possible Functions
Funktion | Key | Webos2| Webos3|Value| Beschreibung
--- | --- |---|---| ---| ---
Nachricht anzeigen | KEY_MSG ||| "Nachricht" |maximal 160 Zeichen "Nachricht"
Bild anzeigen | KEY_PIC ||| "URL" |Zeigt im Media Player ein Bild an, "URL oder Speicherort muss übergaben werden"
POP-UP anzeigen | KEY_POP ||| "URL"  "text" |Zeigt ein Popup, mit Icon an 
Lautstärke erhöhen | KEY_VOL+ ||| -- | Volume +
Lautstärke verringern | KEY_VOL- ||| -- | Volume -
Lautstärke setzen (Absolut) | KEY_SETVOL ||| -- | 
Button Play     | KEY_PlAY ||| -- | Button Play
Button FOrward  | KEY_FORWARD ||| -- |
Button Rewind   | KEY_REWIND ||| -- |
                | KEY_OPENURL ||| "URL" |Öffnet im MEdia Player eine URL , diese muss übergaben werden 
Button Mute     | KEY_Mute| --|||
Button Set3DOn  | KEY_Set3DOn ||| --|
Button Set3DOff | KEY_Set3DOff||| --|
3d Status       | KEY_GET3DSTATUS||| --|

### Function Values
Not Implementet GetChannelList, GetChannelinfo, SetChannel, GetChannelCurrentProgramInfo, getExternalInputList,setExternalInput,getServiceInfo,getSystemInfo

## logic.conf

Currently there is no logic configuration for this plugin.

# Functions

Currently there are no functions offered from this plugin.


