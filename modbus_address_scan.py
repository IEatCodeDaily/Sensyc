from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
import time
import logging

FORMAT = ('%(threadName)-15s '
		  '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
#logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(0) # 0 = NONE ; 10 = DEBUG

def scanAddress():
	client = ModbusSerialClient(method='rtu', port='COM3', timeout=1, baudrate=9600)
	connected = client.connect()

	log.debug("Connected: " + str(connected))

	if connected:
		log.debug("Reading registers..")
		available = []
		# (Target register, read length, device id)
		# read holding register is command 0x03
  
		#Change range to check more addresses
		for i in range(0xffff):
			result = client.read_holding_registers(4, 2, unit=i)		#just put in random addresses. it'll answer with illegal addresses if found
			
			if result != 0:
				available.append(i)
			#log.debug(result)
			print(i)
			print(result)
			time.sleep(.25)
	return available
    
if __name__ == "__main__":
	slaves = scanAddress()
	print(slaves)
