#Disclaimer: THIS CODE IS WORST THAT YOU CAN THINK. FOR EXAMPLES IT USES RANDOM NAMED GLOBAL VARIABLES AROUND... WATCH OUT! ;-)
#Authors: NOBODY 


import numpy as np
from napari.layers import Image, Labels
from magicgui import magicgui
import napari

import serial
import time
import serial.tools.list_ports
import numpy as np
import math
import base64
from napari.qt.threading import thread_worker


serialdevice = None
loop_activate = False

    

def connect_to_usb_device(manufacturer="Espressif"):
    """Connect to a USB device given its manufacturer name."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.manufacturer == manufacturer  or port.manufacturer == "Microsoft" :
            try:
                ser = serial.Serial(port.device, baudrate=2000000, timeout=1)
                print(f"Connected to device: {port.description}")
                ser.write_timeout = 1
                return ser
            except serial.SerialException:
                print(f"Failed to connect to device: {port.description}")
    print("No matching USB device found.")
    return None

def calculate_base64_length(width, height):
    """Calculate the length of a base64 string for an image of given dimensions."""
    num_bytes = width * height
    base64_length = math.ceil((num_bytes * 4) / 3)
    # ensure length is multiple of 4
    base64_length = base64_length + (4 - base64_length % 4) % 4
    return base64_length

def initCam(serialdevice):
    """Initialize the camera."""
    # adjust exposure time
    serialdevice.write(('t10\n').encode())
    while(serialdevice.read()):
          pass


def get_frame(serialdevice):
    try:
        # Command the camera to capture an image
        serialdevice.write(('\n').encode())
        time.sleep(.05)  # Allow some time for the image to be captured

        # Calculate the length of the base64 string
        base64_length = calculate_base64_length(320, 240)

        # Read the base64 string from the serial port
        lineBreakLength = 2
        base64_image_string  = serialdevice.read(base64_length+lineBreakLength)

        # Decode the base64 string into a 1D numpy array
        image_bytes = base64.b64decode(base64_image_string)
        image_1d = np.frombuffer(image_bytes, dtype=np.uint8)

        # Reshape the 1D array into a 2D image
        frame = image_1d.reshape(240, 320)
        return frame



    except Exception as e:
        print("Error")
        print(e)
        serialdevice.write(('r\n').encode())  # Reset the camera
        time.sleep(.5)

        # Clear the serial buffer
        while(serialdevice.read()):
            pass

        # Re-initialize the camera
        initCam(serialdevice)
        waitForNextFrame = True

        # Attempt a hard reset every 20 errors
        iError += 1
        if 0: #iError % 20 == 0 and iError > 1:
            try:
                # Perform a hard reset
                serialdevice.setDTR(False)
                serialdevice.setRTS(True)
                time.sleep(.1)
                serialdevice.setDTR(False)
                serialdevice.setRTS(False)
                time.sleep(.5)
            except Exception as e:
                pass

isConnected = False



# setting expsorue time: t1000\n
# setting gain: g1\n
#getting frame: \n
#restarting: r0\n */


@magicgui()
def live_camera(image_layer :Image, 
                   activated: bool,
                   exposure: int = 3,
                   gain: int = 1):
    
    pass
        
@live_camera.activated.changed.connect
def onConnect():
    global serialdevice
    global loop_activate
    if live_camera.activated.value:
        print("Try to Init")
        
        # Specify the manufacturer to connect to
        manufacturer = 'Espressif'
        
        # Connect to the USB device
        serialdevice = connect_to_usb_device(manufacturer)
        print("serialdevice", serialdevice)
        
        # Initialize the camera
        initCam(serialdevice)
        isConnected = True
        viewer.add_image(np.zeros((320,240)), contrast_limits=(0.,255.), name="ESPscope")
        #startThread(serialdevice)
        loop_activate=True
        myThread(serialdevice)
        
        
    else:
        loop_activate=False
        serialdevice = False

def update_layer(img):
        viewer.layers["ESPscope"].data = img
        viewer.layers["ESPscope"].refresh


@live_camera.gain.changed.connect
def changeGain():
    global serialdevice
    gain = live_camera.gain.value
    c="t"+str(gain)+"\n"
    serialdevice.write(c.encode())
    print(c.encode())


@live_camera.exposure.changed.connect
def changeExposure():
    global serialdevice
    exposure = live_camera.exposure.value
    c="g"+str(exposure)+"\n"
    serialdevice.write(c.encode())



@thread_worker(connect={'yielded': update_layer})
def myThread(serialdevice):
    while loop_activate:
        time.sleep(0.05)
        try:
            img=get_frame(serialdevice)
            yield img
        except:
            print("Frame lost")
    print("thread stop")

viewer = napari.Viewer()

viewer.window.add_dock_widget(live_camera,
                              name = 'Threshold widged')
napari.run()