import napari
from qtpy.QtWidgets import QWidget
from qtpy.QtWidgets import QVBoxLayout
import numpy
import serial
import serial.tools.list_ports
from magicgui.widgets import SpinBox, PushButton, Container
from napari.qt.threading import thread_worker
import math
import base64
import time

class CameraWidget(QWidget):
    def __init__(self, viewer: napari.Viewer):
        self.viewer = viewer
        super().__init__()
        self.serial=self.connect_to_usb_device('Espressif')
        self.base64_length=self.calculate_base64_length(320,240)
        self.lineBreakLength = 2
        self.worker=None
        self.gain_sbox=None
        self.exposure_sbox=None
        self.working=False
        self.create_ui()
        self.image = viewer.add_image(data=numpy.random.randint(255, size=(240,320),dtype="uint8"))
        self.initCam()

    def connect_to_usb_device(self, manufacturer="Espressif"):
        """Connect to a USB device given its manufacturer name."""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.manufacturer == manufacturer or port.manufacturer == "Microsoft":
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
        """Calculate the length of a base64 string for an image of given dimensions."""
        num_bytes = width * height
        base64_length = math.ceil((num_bytes * 4) / 3)
        # ensure length is multiple of 4
        base64_length = base64_length + (4 - base64_length % 4) % 4
        return base64_length

    def set_gain(self):
        print("setting gain")
        self.serial.write(('g'+str(self.gain_sbox.value)+'\n').encode())
        while (self.serial.read()):
            pass

    def set_exposure(self):
        print("setting exposure")
        self.serial.write(('t' + str(self.exposure_sbox.value) + '\n').encode())
        while (self.serial.read()):
            pass

    def initCam(self):
        """Initialize the camera."""
        # adjust exposure time
        self.serial.write(('t' + str(self.exposure_sbox.value) + '\n').encode())
        while (self.serial.read()):
            pass

    @thread_worker
    def camera_loop(self):
        while(self.working):
            self.serial.write(('\n').encode())
            time.sleep(.05)
            try:
                base64_image_string = self.serial.read(self.base64_length + self.lineBreakLength)

                # Decode the base64 string into a 1D numpy array
                image_bytes = base64.b64decode(base64_image_string)
                image_1d = numpy.frombuffer(image_bytes, dtype=numpy.uint8)

                # Reshape the 1D array into a 2D image
                self.image.data=image_1d.reshape(240, 320)
            except:
                self.serial.write(('r\n').encode())  # Reset the camera
                time.sleep(.5)
                while (self.serial.read()):
                    pass
                self.initCam()
        self.serial.write(('r\n').encode())


    def create_ui(self):
        # initialize layout
        layout = QVBoxLayout()
        self.setLayout(layout)


        # create button
        start_btn = PushButton(text='Start')
        start_btn.clicked.connect(self.start)

        exposure_sbox = SpinBox(value=10, label="Exposure ", max=1200, min=1)
        set_exp_button = PushButton(label="Apply")
        set_exp_button.clicked.connect(self.set_exposure)
        self.exposure_sbox = exposure_sbox

        gain_sbox = SpinBox(value=1, label="gain", max=30,min=1)
        set_gain_button = PushButton(label="Apply")
        set_gain_button.clicked.connect(self.set_gain)
        self.gain_sbox = gain_sbox

        widgets_container = Container(widgets=[exposure_sbox,
                                               set_exp_button,
                                               gain_sbox,
                                               set_gain_button,
                                               start_btn])

        layout.addWidget(widgets_container.native)  # NOTE that we need to use the "native" attribute with magicgui objects
        self.widgets_container = widgets_container

    def start(self):
        if not self.working:
            self.working=True
            self.worker = self.camera_loop()
            self.worker.start()
        else:
            self.working=False


if __name__ == '__main__':
    viewer = napari.Viewer()
    mywidget = CameraWidget(viewer)
    viewer.window.add_dock_widget(mywidget, name='my QT widget with magicgui widgets')
    napari.run()