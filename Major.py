import RPi.GPIO as GPIO
import time
import urllib2
import sys
import serial
from hx711 import HX711

GPIO.setmode(GPIO.BCM)

port = "/dev/ttyAMA0"  # Raspberry Pi serial communication pin 8, 10(14,15)
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)

myAPI = 'O130VPN7NMYQPVNW' 	# API key of thinkspeek

# URL where we will send the data
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 

PIROUT = 4		#Output pin of PIR Sensor associate with pin 7
MCTRL = 27		#Control pin of servo motor associate with pin 13
TRIG = 17       #Triger pin of ultrasonic sensor associate with pin 11
ECHO = 18		#Echo pin of ultrasonic sensor associate with pin 12
DT = 2			#DT pin of hx711 associate with pin 3
SCK = 3			#SCK pin of hx711 associate with pin 5


GPIO.setup(PIROUT, GPIO.IN) #PIR
GPIO.setup(MCTRL, GPIO.OUT) #motor
GPIO.setup(TRIG,GPIO.OUT)   #ultrasonic sensor               
GPIO.setup(ECHO,GPIO.IN)    #ultrasonic sensor               

while True:
	status_pir=pir()
	st_dist = dist()
	st_weight = weight()
	gps()


def pir()
	try:
		time.sleep(2) # to stabilize sensor
			if GPIO.input(PIROUT):
				GPIO.output(MCTRL, True)
				time.sleep(0.5) #Motor turns on for 0.5 sec
				print("Door Opened")
				return 1
			elif	
				GPIO.output(MCTRL, False)
				print("Door Closed")
				return 0
	except:

def dist()
	GPIO.output(TRIG, False)                 #Set TRIG as LOW
	print "Waitng For Sensor To Settle"
	time.sleep(2)                            #Delay of 2 seconds
	GPIO.output(TRIG, True)                  #Set TRIG as HIGH
	time.sleep(0.00001)                      #Delay of 0.00001 seconds
	GPIO.output(TRIG, False)                 #Set TRIG as LOW

	while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
		pulse_start = time.time()              #Saves the last known time of LOW pulse

	while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
		pulse_end = time.time()                #Saves the last known time of HIGH pulse 

	pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

	distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
	distance = round(distance, 2)            #Round to two decimal points
	
	if distance > 2 and distance < 400:      #Check whether the distance is within range
		print "Distance:",distance,"cm"  #Print distance with 0.5 cm calibration
		return distance
	else:
		print "Out Of Range"                   #display out of range

def weight()
	hx = HX711(DT,SCK )
	hx.set_reading_format("LSB", "MSB")
	hx.set_reference_unit(92)
	hx.reset()
	hx.tare()
	try:
		val = hx.get_weight(SCK)
        print val
		return val
		hx.power_down()
        hx.power_up()
        time.sleep(1)
	except:

def gps()
	data = ser.readline()
    parseGPS(data)	
	
def parseGPS(data):
    if data[0:6] == "$GPGGA":
        s = data.split(",")
        if s[7] == '0':
            print "no satellite data available"
            return        
        time = s[1][0:2] + ":" + s[1][2:4] + ":" + s[1][4:6]
        lat = decode(s[2])
        dirLat = s[3]
        lon = decode(s[4])
        dirLon = s[5]
        alt = s[9] + " m"
        sat = s[7]
        print "Time(UTC): %s-- Latitude: %s(%s)-- Longitude:%s(%s)\-- Altitude:%s--(%s satellites)" %(time, lat, dirLat, lon, dirLon, alt, sat) 

def decode(coord):
    # DDDMM.MMMMM -> DD deg MM.MMMMM min
    v = coord.split(".")
    head = v[0]
    tail =  v[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"