# Tutorial: Building and Setting Up ESPressoScope for GitHub Workshop

Welcome to the tutorial on how to build the ESPressoScope and set it up for the upcoming workshop. Please follow the guidelines and steps provided to ensure a smooth experience during the workshop.

## Pre-hackathon (Day One, After 5pm)

### Overview:
This session is optional and meant for those interested in getting a head start on the main workshop.

### Steps:

1. **Build the ESPresosocpoe**
    - Based on the instructions provided on [this page](https://matchboxscope.github.io/docs/Variants/ESPressoScope).
    - Specifically, look for the **XIAO variation** and follow [those instructions](https://matchboxscope.github.io/docs/Variants/ESPressoScope/#variation-seeed-studio-xiao-camera)
    
2. **More about Seeed Studio Xiao Camera**
    - Additional information about the camera can be found [here](https://matchboxscope.github.io/docs/Hardware/SeeedXiao).
    - Learn how to adapt the Xiao camera to the traditional ESPressoscope design.

3. **Sample Collection** (Optional)
    - If interested, you can also collect samples using off-the-shelf coverslips or sticky tape for later testing.

---

## During Workshop (27th of September) 

### STEP 1 – 10:00 am to 10:30 am: Setting up computers and ESP32s

- Quick Overview of the course:
  -> ImSwitch (https://github.com/openUC2/ImSwitch)
  -> the Camera
  -> the ESPressoscope Universe
  -> UC2 + Camera + ImSwitch: https://github.com/openUC2/openUC2-SEEED-XIAO-Camera/tree/seeed
- **Flashing the XIAO**
    - Comprehensive guide on how to flash the XIAO is available [here](https://matchboxscope.github.io/docs/Tutorials/ESP32RawUSBFrame#quickstart).
    - Visit [this website](https://matchboxscope.github.io/firmware/FLASH.html) to initiate the flash process.
    
- **Python Setup**
    - Ensure you have the following Python pre-requisites:
        - pyserial
        - numpy
        - cv2
        
- **Understanding the Firmware** (Optional)
    - If curious, take a peek at what the ESP32 firmware is up to [here](https://matchboxscope.github.io/docs/Tutorials/ESP32RawUSBFrame#esp32-code).
    
- **Testing the Camera**
    - Once the camera is set up, connect it via USB to your computer.
    - Visit [this website](https://matchboxscope.github.io/cameraserial/index.html) and select the port in the browser.
    - If everything is set up correctly, a live stream should show up.
    
- **Serial Commands to Control the Camera:**
  These commands can either be sent via a serial monitor (e.g. Arduino) or Pyserial at 2000000 BAUD, no lineeneding. 
    ```bash
    setting exposure time: t1000\n
    setting gain: g1\n
    getting frame: \n
    restarting: r0\n */
    ```

### STEP 2 – 10:30 am to 11:00 am: Introduction
- **Topics to Cover:**
    - Introduction to threading in napari.
    - Basics of threads.
    - Introduction to GUI programming with emphasis on key elements.

### STEP 3 – 11:00 am to 12:30 pm: Hackathon

Participants will collaborate on code related tasks.

- **Python Adapter for Frame Reception**
    - Understand the Python adapter mechanism for receiving frames and converting them to numpy objects. The guide can be found [here](https://matchboxscope.github.io/docs/Tutorials/ESP32RawUSBFrame#python-code).
    
- **Tasks**
    - Acquire images from the camera.
    - Record and display the number of frames.
    - Develop a live view feature.
    - Implement controls for camera settings.
    
- **Advanced Task**
    - Learn and integrate the HTTP interface using the Napari plugin provided. Follow the instructions [here](https://github.com/Matchboxscope/omniscope-viewer/tree/main/src/omniscopeViewer).

### STEP 4 – 12:30 pm to 1:00 pm: Wrap-up

- **Showcasing Work**
    - Participants present their napari plugins developed for data acquisition.
    - Appreciate and learn from the plugins developed by peers.

### STEP 5 – 2:00 pm to 3:00 pm: Discussion on Acquisition Software

- **Discussion Topics:**
    - Jacopo's plugin for multiarray camera microscopes.
    - Imswitch software.
    - Acquire CZI.

---

We hope you find this guide informative and are looking forward to the workshop. If you have any queries or issues, feel free to reach out to the coordinators. Happy building!
