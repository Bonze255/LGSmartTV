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
    	host = xxx.xxx.xxx.xxx
	port = 3000
	tvid = 1
	
</pre>

### Attributes
  * `host`: specifies the ip address of your SmartTV device.
  * `port`: if you want to use a nonstandard port.
  * `tvid`: Not Used at the moment
## items.conf
<pre>

</pre>
### LGSmartTv
There are two possibilities to use this attribute. 
  * Define it on a string item and set it to `true`: With this configuration, every string you set to this item will be send to the SmartTV device.
  * Define it on a boolean item and set it to a key value: With this configuration, the specified key value is sent whenever you set the item to `true` (if the item is only for sending a specific command to the tv then you should consider using the `enforce_updates` attribute, too).
  * for functions witch have more than one variable, they must been seperated with an "|"; shown by the examples 


## Possible Functions
KEYWORD | Webos2| Webos3|Value| Description
--- |---|---| ---| ---
|KEY_POWEROFF|-|-|-|-|	 	        	
|KEY_MUTE|-|-|-|-|	 			
|KEY_SHOWPIC|-|-|-|-|	       		
|KEY_SHOWMEDIA|-|-|-|-|	     		
|KEY_OPENMEDIAPL|-|-|-|-|	   		
|KEY_PLAY|-|-|-|-|	 			
|KEY_STOP|-|-|-|-|	 			
|KEY_REWIND|-|-|-|-|	 
|KEY_FORWARD|-|-|-|-|	 
|KEY_CHANNELUP|-|-|-|-|	 
|KEY_CHANNELDOWN|-|-|-|-|	 
|KEY_3DON|-|-|-|-|	 
|KEY_3DOFF|-|-|-|-|	 
|KEY_VOLUP|-|-|-|-|	 
|KEY_VOLDOWN|-|-|-|-|	 
|SET_MSG|-|-|-|-|	 
|SET_MSG2|-|-|-|-|	 
|SET_VOL|-|-|-|-|	 
|SET_INPUTSOURCE|-|-|-|-|	 
|SET_CHANNEL|-|-|-|-|	 
|GET_SYSTEMINFO|-|-|-|-|	 
|GET_SWINFO|-|-|-|-|	 
|GET_SERVICES|-|-|-|-|	 
|GET_CHANNELLIST|-|-|-|-|	 
|GET_CHANNELINFO|-|-|-|-|	 
|GET_INPUTLIST|-|-|-|-|	 
|GET_AUDIOSTATUS|-|-|-|-|	 
|GET_PROGRAMMINFO|-|-|-|-|

### Function Values


## logic.conf

Currently there is no logic configuration for this plugin.

# Functions

Currently there are no functions offered from this plugin.


