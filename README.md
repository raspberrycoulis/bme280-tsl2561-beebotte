# bme280-tsl2561-beebotte
## Using the BME280 and TSL2561 sensors to measure temperature, humidity, pressure and luminosity data then sending to Beebotte for data visualisation purposes.

This Python script is based on Beebotte's example to use a DHT11 temperature and humidity sensor on the Raspberry Pi and feed data to a dashboard. The example script can be found [here](https://beebotte.com/tutorials/monitor_humidity_and_temperature_with_raspberrypi) and requires a Beebotte account.

### Install the Beebotte files

You'll need to install the relevant Beebotte files, which is done by:

    sudo pip install beebotte

If you get a warning, you may need to install PIP first, which is done by:

    sudo apt-get install python-pip

### Clone and use my script

Simply clone this script by running:

    cd ~
    git clone https://github.com/raspberrycoulis/bme280-tsl2561-beebotte.git

Then you will need to provide your channel token and set your channel name to match the new channel you create in Beebotte:

    # Replace CHANNEL_TOKEN with that of your Beebotte channel and YOUR_CHANNEL_NAME with the name you give your Beebotte channel
    bbt = BBT(token = 'CHANNEL_TOKEN')
    chanName = "YOUR_CHANNEL_NAME"

You can use your preferred text editor, but Nano works just fine:

    sudo nano /home/pi/bme280-tsl2561-beebotte/dashboard.py

Be sure to save when exiting:

    ctrl + x
    y

Make the script executable:

    sudo chmod +x dashboard.py

And then finally test it by running:

    ./dashboard.py

If done correctly, you should see data in your Beebotte channel. Stop the script by pressing `ctrl + c`.

## Making the script run automatically on boot

I followed the excellent guide found on [Raspberry Pi Spy](http://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/) to make my `dashboard.py` script run on boot. To recap, this is what I did:

### 1. Create a Unit file

This is what will tell the Pi to run your script on boot:

    sudo nano /lib/systemd/system/beebotte.service

Then add the following text to your file (you may need to adjust the path for your `dashboard.py` script depending on where it is located (the part `/home/pi/bme280-tsl2561-beebotte/dashboard.py`):

    [Unit]
    Description=Send BME280 and TSL2561 sensor data to Beebotte
    After=multi-user.target
    
    [Service]
    Type=idle
    ExecStart=/usr/bin/python /home/pi/bme280-tsl2561-beebotte/dashboard.py
    
    [Install]
    WantedBy=multi-user.target

Exit, `ctrl + x`, and save `y`to create the service unit file.

### 2. Set the relevant permissions

Make sure that the permissions are set correctly:

    sudo chmod 644 /lib/systemd/system/beebotte.service

### 3. Configure systemd

Make sure that systemd can use your newly created unit file:

    sudo systemctl daemon-reload
    sudo systemctl enable beebotte.service

Reboot the Pi to test via `sudo reboot`.

### 4. Check on the status of your service

Check that the service has started by running:

    sudo systemctl status beebotte.service

If done correctly, you should see that your `dashboard.py` script is now running!