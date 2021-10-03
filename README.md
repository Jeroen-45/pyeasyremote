# pyeasyremote
pyeasyremote can be used to control buttons, sliders, pan tilt controls and colorwheels of DMX lighting control software that supports the Easy Remote app. This library was only tested using the Daslight DVC4 software, but should work for other software too. Please let me know if you have tested the library with other software.

**NOTE: I am not affiliated with LIGHTINGSOFT, Daslight, Nicolaudie Group or any other related companies. This is an unofficial piece of software just for tinkering with Easy Remote using python.**

# Usage
````python
from pyeasyremote import EasyRemote

# Initialize an EasyRemote
er = EasyRemote("192.168.1.100")

# Turn on a button named "My Button" in your lighting software
er.objects["My Button"].set_state(True)
# Set a slider named "My Slider" to 255
er.objects["My Slider"].set_value(255)
# Set a pan tilt control named "My PanTilt" to the top right corner
er.objects["My PanTilt"].set_pan_tilt(65535, 65535)
# Set a colorwheel named "My Colorwheel" to red using RGB
er.objects["My Colorwheel"].set_rgb(255, 0, 0)
# Set a colorwheel named "My Colorwheel" to red using HSV
er.objects["My Colorwheel"].set_hsv(0.0, 1.0, 1.0)
````
In the case that initialization fails due to a timeout on the response from
your lighting software, the objects dict will be empty.