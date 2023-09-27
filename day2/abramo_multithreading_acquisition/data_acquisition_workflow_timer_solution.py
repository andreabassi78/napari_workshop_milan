import napari
from qtpy.QtWidgets import QWidget, QPushButton, QSpinBox
from qtpy.QtWidgets import QVBoxLayout, QFormLayout
from qtpy.QtCore import QTimer
from napari.qt.threading import thread_worker
import serial.tools.list_ports
import numpy as np
import serial, math
import time
import base64

class MyAcquisitionWidget(QWidget):
    
    def __init__(self, viewer:napari.Viewer):
        super().__init__()
        self.viewer = viewer
        self.create_ui()
        self.serial = self.open_serial()
        self.init_cam()
        self.live_started = False
        self.live_timer = QTimer()
        self.live_timer.setInterval(50)
        self.live_timer.timeout.connect(self.update_layer)
        
    def create_ui(self):
        
        # initialize layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # create exposure time spinbox
        self.exp_time_spinbox = QSpinBox()
        self.exp_time_spinbox.setMinimum(1)
        self.exp_time_spinbox.setMaximum(1200)
        self.exp_time_spinbox.setValue(10)
        NLayout = QFormLayout()
        NLayout.addRow('Exposure time (ms)', self.exp_time_spinbox   )
        layout.addLayout(NLayout)

        # create gain control spinbox
        self.gain_spinbox = QSpinBox()
        self.gain_spinbox.setMinimum(1)
        self.gain_spinbox.setMaximum(30)
        self.gain_spinbox.setValue(5)
        NLayout = QFormLayout()
        NLayout.addRow('Gain control', self.gain_spinbox)
        layout.addLayout(NLayout)
        
        # create live button button
        self.live_button = QPushButton('Start live')
        layout.addWidget(self.live_button)
        
        # connect signals
        self.live_button.clicked.connect(self.toggle_live)
        self.exp_time_spinbox.valueChanged.connect(self.request_exp_time)
        self.gain_spinbox.valueChanged.connect(self.request_gain)
        
    
    def request_exp_time(self, value):
        self.serial.write((f't{value}\n').encode())
        while self.serial.read():
            pass
    
    def request_gain(self, value):
        self.serial.write((f'g{value}\n').encode())
        while self.serial.read():
            pass
    
    def update_layer(self):
    
        # Command the camera to capture an image
        self.serial.write(('\n').encode())
        time.sleep(.05)  # Allow some time for the image to be captured
        
        # Calculate the length of the base64 string
        base64_length = self.calculate_base64_length(320, 240)

        # Read the base64 string from the serial port
        lineBreakLength = 2
        base64_image_string  = self.serial.read(base64_length+lineBreakLength)

        try:
            # Decode the base64 string into a 1D numpy array
            image_bytes = base64.b64decode(base64_image_string)
            image_1d = np.frombuffer(image_bytes, dtype=np.uint8)

            # Reshape the 1D array into a 2D image
            frame = image_1d.reshape(240, 320)
            self.viewer.layers['camera_data'].data = frame
        except ValueError:
            print("Error: frame dropped")
        except KeyError: 
            self.viewer.add_image(frame, name="camera_data")

    
    def toggle_live(self):
        if not self.live_started:
            self.live_started = True
            print("Starting live")
            self.live_timer.start()
            self.live_button.setText('Stop live')
        else:
            self.live_started = False
            print("Stopping live")
            self.live_timer.stop()
            self.live_button.setText('Start live')
    
    def init_cam(self):
        """Initialize the camera."""
        # adjust exposure time
        self.serial.write(('t10\n').encode())
        while(self.serial.read()):
            pass
    
    def open_serial(self, manufacturer="Espressif", port=None):
        if port is not None:
            try:
                ser = serial.Serial(port, baudrate=2000000, timeout=1)
                print(f"Connected to device: {port}")
                ser.write_timeout = 1
                return ser
            except Exception as e:
                print(e)
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

    def calculate_base64_length(self, width, height):
        """ Calculate the length of a base64 string for an image of given dimensions. """
        num_bytes = width * height
        base64_length = math.ceil((num_bytes * 4) / 3)
        # ensure length is multiple of 4
        base64_length = base64_length + (4 - base64_length % 4) % 4
        return base64_length
            
if __name__ == '__main__':
   
    viewer = napari.Viewer()
    mywidget = MyAcquisitionWidget(viewer)
    viewer.window.add_dock_widget(mywidget, name = 'my first QT widget')
    napari.run()