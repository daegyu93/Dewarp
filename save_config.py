from time import sleep
from smbus2 import SMBus, i2c_msg
import struct
import numpy as np

class I2cDevice:
    def __init__(self, bus, dev_addr):
        self.__bus = bus
        self.dev_addr = dev_addr
        
    # def read(self, reg_addr):
    #     with SMBus(self.__bus) as bus:
    #         data = bus.read_i2c_block_data(self.dev_addr, reg_addr, 8)
    #         float_data = value = struct.unpack('>d', bytes(data))[0]
    #         return float_data
        
    def read(self, reg_addr):
        reg_lsb = reg_addr & 0xff
        reg_msb = (reg_addr>>8) & 0xff
        wr = i2c_msg.write(self.dev_addr , [reg_msb, reg_lsb] )
        rd = i2c_msg.read(self.dev_addr , 8)
        with SMBus(self.__bus) as bus: 
            bus.i2c_rdwr(wr, rd)
            int_value = int.from_bytes(rd, 'little')
            value = np.uint64(int_value).view('float64')
            return value
            
def main(args):
    camera_number = args[1]
    
    if camera_number == '0':
        bus = 10
        addr = 0x51
    elif camera_number == '1':
        bus = 10
        addr = 0x52
    elif camera_number == '2':
        bus = 11
        addr = 0x51
    elif camera_number == '3':
        bus = 11
        addr = 0x52
    elif camera_number == '4':
        bus = 12
        addr = 0x51
    elif camera_number == '5':
        bus = 12
        addr = 0x52
        
    
    fx_addr = 0x0144
    fy_addr = 0x014c
    cx_addr = 0x0154
    cy_addr = 0x015c
    k1_addr = 0x0164
    k2_addr = 0x016c
    k3_addr = 0x0174
    p1_addr = 0x0194
    p2_addr = 0x019c
    
    sleep(1)

    des = I2cDevice(bus=bus, dev_addr=addr)
    fx = des.read(fx_addr)
    fy = des.read(fy_addr)
    cx = f"{des.read(cx_addr):.6f}"
    cy = f"{des.read(cy_addr):.6f}"
    k1 = f"{des.read(k1_addr):.6f}"
    k2 = f"{des.read(k2_addr):.6f}"
    k3 = f"{des.read(k3_addr):.6f}"
    p1 = f"{des.read(p1_addr):.6f}"
    p2 = f"{des.read(p2_addr):.6f}"
    
    print(f'fx: {fx}', f'fy: {fy}', f'cx: {cx}', f'cy: {cy}', f'k1: {k1}', f'k2: {k2}', f'k3: {k3}', f'p1: {p1}', f'p2: {p2}')
    
    focal_length = f"{(fx + fy)/2:.6f}"

    #save dewarper_config.txt
    config_file_name = 'config/dewarper_config_' + str(camera_number) + '.txt'
    f = open(config_file_name, 'w')
    # [property]
    # output-width=1920
    # output-height=1080
    # num-batch-buffers=1
    f.write('[property]\n')
    f.write('output-width=1920\n')
    f.write('output-height=1080\n')
    f.write('num-batch-buffers=1\n')
    f.write('\n')

    # [surface0]
    # projection-type=3
    # width=1920
    # height=1080
    # focal-length=733.1000
    # distortion= -0.2725762476997752;0.06077245841636788;-0.0055581754220842446;-0.0005782749923515222;0.000701124461693587
    # src-x0=936.337
    # src-y0=580.864
    f.write('[surface0]\n')
    f.write('projection-type=3\n')
    f.write('width=1920\n')
    f.write('height=1080\n')
    f.write('focal-length=' + focal_length + '\n')
    f.write('distortion=' + k1 + ';' + k2 + ';' + k3 + ';' + p1 + ';' + p2 + '\n')
    f.write('src-x0=' + cx + '\n')
    f.write('src-y0=' + cy + '\n')
    f.close()


import sys

if __name__ == "__main__":
    main(sys.argv)
    