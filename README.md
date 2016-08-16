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
[lgsmarttv]
    class_name = LGSmartTV
    class_path = plugins.lgsmarttv
    host = 192.168.0.45
    port = 3000

</pre>

### Attributes
  * `host`: specifies the ip address of your SmartTV device.
  * `port`: if you want to use a nonstandard port.

## items.conf

### smarttv
There are two possibilities to use this attribute. 
  * Define it on a string item and set it to `true`: With this configuration, every string you set to this item will be send to the SmartTV device.
  * Define it on a boolean item and set it to a key value: With this configuration, the specified key value is sent whenever you set the item to `true` (if the item is only for sending a specific command to the tv then you should consider using the `enforce_updates` attribute, too).
  * for functions witch have more than one variable, they must been seperated with an ","; shown by the examples 

<pre>
[tv]
    type = str
    smarttv = true
    smarttv_id = 1
    enforce_updates = true

    [[mute]]
        type = bool
        smarttv = true
        smartfunc = mute
        enforce_updates = true

    [[notification]]
        name = notification
        type = String
        visu_acl = rw
        smarttvfunc = message , "Hallo"
        enforce_updates = true
        knx_dpt = 1
        knx_listen = 0/0/7
</pre>
## Possible Functions
### Key Values
Play, Pause, Stop, Forward, Rewind, ChannelUp, ChannelDown, Vol+, Vol-, Mute, Set3DOn, Set3DOff, Get3DStatus

### Function Values
ShowMessage, SetVol, OpenPicture, GetVol, OpenApp, OpenUrl 
Not Implementet GetChannelList, GetChannelinfo, SetChannel, GetChannelCurrentProgramInfo, getExternalInputList,setExternalInput,getServiceInfo,getSystemInfo

## logic.conf

Currently there is no logic configuration for this plugin.

# Functions

Currently there are no functions offered from this plugin.


