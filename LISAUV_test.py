from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
import time
import logging

FORMAT = ('%(threadName)-15s ''%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')

#Comment this if DEBUG unnecessary
logging.basicConfig(format=FORMAT)


log = logging.getLogger()
log.setLevel(logging.DEBUG)
hex_file = open('outhex.txt', 'w')


#Client setting
client = ModbusSerialClient(method='rtu', port='COM3', timeout=1, baudrate=9600)

#Slave Adress
UNIT = 2


#======== Addresses TriOS LISA UV ============

#CALIBRATION ADDRESSES
add_COD_Offset = 104		#float
add_COD_Scaling = 106		#float
add_BOD_Offset = 108		#float
add_BOD_Scaling = 110		#float
add_TOC_Offset = 108		#float
add_TOC_Scaling = 110		#float

#VALUE ADDRESSES
add_SAC = 1000				#float
add_COD = 1002				#float
add_BOD = 1004				#float
add_TOC = 1006				#float
add_TransUV = 1008			#float
add_TransCorr = 1010		#float
add_Turbid = 1012			#float
add_absorb254 = 1034		#float
add_absorb530 = 1036		#float
add_SQI = 1038				#float
add_absorb254AU = 1040		#float
add_absorb530AU = 1042		#float

def reportID(address):
		result = client.report_slave_id(address)
		decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
		result = str(decoder.decode_string())
		return result
  
  
def read_reg_float(address, length):
		log.debug("Reading registers..")

		# (Target register, read length, device id)
		# read holding register is command 0x03
		result = client.read_holding_registers(address, length, unit=UNIT)
		decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
		result = str(decoder.decode_32bit_float())

		log.debug(result)
		time.sleep(0.2)
		return result

def read_reg_32uint(address, length):
		log.debug("Reading registers..")

		# (Target register, read length, device id)
		# read holding register is command 0x03
		result = client.read_holding_registers(address, length, unit=UNIT)
		decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
		intresult = str(decoder.decode_32bit_uint())

		log.debug(result)
		time.sleep(0.2)
		return intresult

def read_reg_16uint(address, length):
		log.debug("Reading registers..")

		# (Target register, read length, device id)
		# read holding register is command 0x03
		result = client.read_holding_registers(address, length, unit=UNIT)
		decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
		intresult = str(decoder.decode_16bit_uint())

		log.debug(result)
		time.sleep(0.2)
		return intresult

def initClient():
	connected = client.connect()

	log.debug("Connected: " + str(connected))
	return connected
 

if __name__ == "__main__":
    connected = initClient()
    while connected:
        #input command
        
        #Trigger measurement before reading
        client.write_coil(1, True, UNIT)
        
        print("COD: ", read_reg_float(add_COD, 2), "mg/L")
        time.sleep(1)
