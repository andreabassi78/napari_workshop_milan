import serial
import time
import serial.tools.list_ports
import numpy as np
import cv2
import math
import base64

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

def initCam():
    """Initialize the camera."""
    # adjust exposure time
    serialdevice.write(('t10\n').encode())
    while(serialdevice.read()):
          pass

    

# Specify the manufacturer to connect to
manufacturer = 'Espressif'

# Connect to the USB device
serialdevice = connect_to_usb_device(manufacturer)

# Initialize the camera
initCam()
iError = 0
t0 = time.time()
waitForNextFrame = True
while True:
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

        # Display the image
        if waitForNextFrame:
              waitForNextFrame = False

        else:
          cv2.imshow("image", frame)

          # Calculate and print the framerate
          print("framerate: "+(str(1/(time.time()-t0))))
          t0 = time.time()

          # Break the loop if 'q' is pressed
          if cv2.waitKey(25) & 0xFF == ord('q'):
              break

    except Exception as e:
        print("Error")
        print(e)
        serialdevice.write(('r\n').encode())  # Reset the camera
        time.sleep(.5)

        # Clear the serial buffer
        while(serialdevice.read()):
            pass

        # Re-initialize the camera
        initCam()
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
