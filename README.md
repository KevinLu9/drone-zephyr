# drone-zephyr
The Zehphyr is a drone that I am making from scratch. It is a personal project that I work on in my time off.

## Hardware
### Rpi Pico + Rpi Zero 2 W + Wifi
The Zephyr utilises a Raspberry Pi Pico W at its core. It interfaces with various sensors to track of the drone's surroundings and predict its external state.
* MPU6050 - Is a 3 Axis Gyroscope and Accelerometer Sensor used to predict pitch and roll (might change in the future to include magnometer for yaw).
* BME280 - An Atmospheric Sensor that allows measurements of Temperature, Humidity, and Barometric Pressure to estimate alititude.

The drone also is equiped with a Raspberry Pi Zero 2 W which will run more advanced functionality such as driving a GUI that enables the user to control and see real-time data.

Most communication to the drone is currently only planned to use WIFI 2.4Ghz, which greatly limits its range. Future plans to change this may happen. i.e. ExpressLRS for greater ranges and some sort of different technology for FPV feeds at longer ranges.

## Graphical User Interface
### Vite + NodeJS + React + TailwindCSS + Daisyui
Is a frontend Graphical User Interface to display real-time data to the drone. The application can also send commands and control the drone based on mobile phone inertial sensors and button presses.

This is the current state of the gui as of 27/07/2024.
![Photo of GUI](https://github.com/KevinLu9/drone-zephyr/blob/images/gui-27-07-2024.JPG)

#### Development Setup
1. Clone the Repository.
2. Install dependencies with `npm install`.
3. Start the application with `npm run dev`.
4. Go to `http://localhost:5173` in your browser.

#### Production Setup
1. Clone the Repository.
2. Install dependencies with `npm install`.
3. Build the application with `npm run build`.
4. Install *Nginx* onto the target device (Raspberry Pi Zero 2 W with Rasbian Installed).
5. Configure *Nginx* to serve the application from the /var/www/html directory.
6. Copy all files built in `/dist/` into /var/www/html