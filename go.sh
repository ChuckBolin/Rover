# changes diretory
cd ~/rover

# Starts gpsd, gps server
sudo gpsd -F /var/run/gpsd.sock /dev/ttyUSB0

# Starts data logger
python data_logger5.py

