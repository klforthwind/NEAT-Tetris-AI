import serial
import time
import math

# --------------------------------------------------------

# Switch Button Values
BTN_NONE         = 0x0000000000000000
BTN_Y            = 0x0000000000000001
BTN_B            = 0x0000000000000002
BTN_A            = 0x0000000000000004
BTN_X            = 0x0000000000000008
BTN_L            = 0x0000000000000010

# Actual Switch DPAD Values
A_DPAD_CENTER    = 0x08
A_DPAD_U         = 0x00
A_DPAD_U_R       = 0x01
A_DPAD_R         = 0x02
A_DPAD_D_R       = 0x03
A_DPAD_D         = 0x04
A_DPAD_D_L       = 0x05
A_DPAD_L         = 0x06
A_DPAD_U_L       = 0x07

# Enum DIR Values
DIR_CENTER    = 0x00
DIR_U         = 0x01
DIR_R         = 0x02
DIR_D         = 0x04
DIR_L         = 0x08
DIR_U_R       = DIR_U + DIR_R
DIR_D_R       = DIR_D + DIR_R
DIR_U_L       = DIR_U + DIR_L
DIR_D_L       = DIR_D + DIR_L

DPAD_CENTER      = 0x0000000000000000
DPAD_U           = 0x0000000000010000
DPAD_R           = 0x0000000000020000
DPAD_D           = 0x0000000000040000
DPAD_L           = 0x0000000000080000
DPAD_U_R         = DPAD_U + DPAD_R
DPAD_D_R         = DPAD_D + DPAD_R
DPAD_U_L         = DPAD_U + DPAD_L
DPAD_D_L         = DPAD_D + DPAD_L

RSTICK_CENTER    = 0x0000000000000000
RSTICK_R         = 0x000FF00000000000 #   0 (000)
RSTICK_U_R       = 0x02DFF00000000000 #  45 (02D)
RSTICK_U         = 0x05AFF00000000000 #  90 (05A)
RSTICK_U_L       = 0x087FF00000000000 # 135 (087)
RSTICK_L         = 0x0B4FF00000000000 # 180 (0B4)
RSTICK_D_L       = 0x0E1FF00000000000 # 225 (0E1)
RSTICK_D         = 0x10EFF00000000000 # 270 (10E)
RSTICK_D_R       = 0x13BFF00000000000 # 315 (13B)

NO_INPUT         = BTN_NONE + DPAD_CENTER + RSTICK_CENTER

# Commands to send to MCU
COMMAND_NOP        = 0x00
COMMAND_SYNC_1     = 0x33
COMMAND_SYNC_2     = 0xCC
COMMAND_SYNC_START = 0xFF

# Responses from MCU
RESP_USB_ACK       = 0x90
RESP_UPDATE_ACK    = 0x91
RESP_UPDATE_NACK   = 0x92
RESP_SYNC_START    = 0xFF
RESP_SYNC_1        = 0xCC
RESP_SYNC_OK       = 0x33

# --------------------------------------------------------

class Emulator:

    def __init__(self, serialPort):
        # Create the serial connection to the arduino pro micro
        self.ser = serial.Serial(port=serialPort, baudrate=19200,timeout=1)

        # Attempt to sync with the MCU
        if not self.sync():
            print('Could not sync!')
            exit()
    
        # Successfully connected if we've reached this line
        print('Successful Connection!')

    def nextGenome(self):
        tt = time.time()
        while(time.time() - tt < 3):
            self.send_input(BTN_A)

    def runButton(self, outputNode, cmd):
        if int(outputNode) == 1:
            # print(cmd)
            self.send_input(cmd)

    def emulateTetris(self, arr):
        self.send_input(DPAD_CENTER)
        self.send_input(NO_INPUT)
        self.runButton(arr[0], DPAD_U)
        self.runButton(arr[1], DPAD_R)
        self.runButton(arr[2], DPAD_D)
        self.runButton(arr[3], DPAD_L)
        self.runButton(arr[4], BTN_L)
        self.runButton(arr[5], BTN_Y)
        self.runButton(arr[6], BTN_B)
        # self.runButton(arr[7], self.rstick_angle(0, 0xFF))
        # self.runButton(arr[8], self.rstick_angle(90, 0xFF))
        # self.runButton(arr[9], self.rstick_angle(180, 0xFF))
        # self.runButton(arr[10], self.rstick_angle(270, 0xFF))
    
    def close(self):
        self.ser.close

# --------------------------------------------------------

        # Compute x and y based on angle and intensity
    def angle(self, angle, intensity):
        # y is negative because on the Y input, UP = 0 and DOWN = 255
        x =  int((math.cos(math.radians(angle)) * 0x7F) * intensity / 0xFF) + 0x80
        y = -int((math.sin(math.radians(angle)) * 0x7F) * intensity / 0xFF) + 0x80
        return x, y

    def lstick_angle(self, angle, intensity):
        return (intensity + (angle << 8)) << 24

    def rstick_angle(self, angle, intensity):
        return (intensity + (angle << 8)) << 44

    # Precision wait
    def wait(self, waitTime):
        t0 = time.perf_counter()
        t1 = t0
        while (t1 - t0 < waitTime):
            t1 = time.perf_counter()

    # Read X bytes from the serial port (returns list)
    def read_bytes(self, size):
        bytes_in = self.ser.read(size)
        return list(bytes_in)

    # Read 1 byte from the serial port (returns int)
    def read_byte(self):
        bytes_in = self.read_bytes(1)
        if len(bytes_in) != 0:
            byte_in = bytes_in[0]
        else:
            byte_in = 0
        return byte_in

    # Discard all incoming bytes and read the last (latest) (returns int)
    def read_byte_latest(self):
        inWaiting = self.ser.in_waiting
        if inWaiting == 0:
            inWaiting = 1
        bytes_in = self.read_bytes(inWaiting)
        if len(bytes_in) != 0:
            byte_in = bytes_in[0]
        else:
            byte_in = 0
        return byte_in

    # Write bytes to the serial port
    def write_bytes(self, bytes_out):
        self.ser.write(bytearray(bytes_out))
        return

    # Write byte to the serial port
    def write_byte(self, byte_out):
        self.write_bytes([byte_out])
        return

    # Compute CRC8
    # https://www.microchip.com/webdoc/AVRLibcReferenceManual/group__util__crc_1gab27eaaef6d7fd096bd7d57bf3f9ba083.html
    def crc8_ccitt(self, old_crc, new_data):
        data = old_crc ^ new_data

        for i in range(8):
            if (data & 0x80) != 0:
                data = data << 1
                data = data ^ 0x07
            else:
                data = data << 1
            data = data & 0xff
        return data

    # Send a raw packet and wait for a response (CRC will be added automatically)
    def send_packet(self, packet=[0x00,0x00,0x08,0x80,0x80,0x80,0x80,0x00], debug=False):
        if not debug:
            bytes_out = []
            bytes_out.extend(packet)

            # Compute CRC
            crc = 0
            for d in packet:
                crc = self.crc8_ccitt(crc, d)
            bytes_out.append(crc)
            self.write_bytes(bytes_out)
            # print(bytes_out)

            # Wait for USB ACK or UPDATE NACK
            byte_in = self.read_byte()
            commandSuccess = (byte_in == RESP_USB_ACK)
        else:
            commandSuccess = True
        return commandSuccess

    # Convert DPAD value to actual DPAD value used by Switch
    def decrypt_dpad(self, dpad):
        if dpad == DIR_U:
            dpadDecrypt = A_DPAD_U
        elif dpad == DIR_R:
            dpadDecrypt = A_DPAD_R
        elif dpad == DIR_D:
            dpadDecrypt = A_DPAD_D
        elif dpad == DIR_L:
            dpadDecrypt = A_DPAD_L
        elif dpad == DIR_U_R:
            dpadDecrypt = A_DPAD_U_R
        elif dpad == DIR_U_L:
            dpadDecrypt = A_DPAD_U_L
        elif dpad == DIR_D_R:
            dpadDecrypt = A_DPAD_D_R
        elif dpad == DIR_D_L:
            dpadDecrypt = A_DPAD_D_L
        else:
            dpadDecrypt = A_DPAD_CENTER
        return dpadDecrypt

    # Convert CMD to a packet
    def cmd_to_packet(self, command):
        cmdCopy = command
        low              =  (cmdCopy & 0xFF)  ; cmdCopy = cmdCopy >>  8
        high             =  (cmdCopy & 0xFF)  ; cmdCopy = cmdCopy >>  8
        dpad             =  (cmdCopy & 0xFF)  ; cmdCopy = cmdCopy >>  8
        lstick_intensity =  (cmdCopy & 0xFF)  ; cmdCopy = cmdCopy >>  8
        lstick_angle     =  (cmdCopy & 0xFFF) ; cmdCopy = cmdCopy >> 12
        rstick_intensity =  (cmdCopy & 0xFF)  ; cmdCopy = cmdCopy >>  8
        rstick_angle     =  (cmdCopy & 0xFFF)
        dpad = self.decrypt_dpad(dpad)
        left_x, left_y   = self.angle(lstick_angle, lstick_intensity)
        right_x, right_y = self.angle(rstick_angle, rstick_intensity)

        packet = [high, low, dpad, left_x, left_y, right_x, right_y, 0x00]
        # print (hex(command), packet, lstick_angle, lstick_intensity, rstick_angle, rstick_intensity)
        return packet

    # Send a formatted controller command to the MCU
    def send_cmd(self, command=NO_INPUT):
        commandSuccess = self.send_packet(self.cmd_to_packet(command))
        return commandSuccess

    # Wait for data to be available on the serial port
    def wait_for_data(self, timeout = 1.0, sleepTime = 0.1):
        t0 = time.perf_counter()
        t1 = t0
        inWaiting = self.ser.in_waiting
        while ((t1 - t0 < sleepTime) or (inWaiting == 0)):
            time.sleep(sleepTime)
            inWaiting = self.ser.in_waiting
            t1 = time.perf_counter()

    # Force MCU to sync
    def force_sync(self):
        # Send 9x 0xFF's to fully flush out buffer on device
        # Device will send back 0xFF (RESP_SYNC_START) when it is ready to sync
        self.write_bytes([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF])

        # Wait for serial data and read the last byte sent
        self.wait_for_data()
        byte_in = self.read_byte_latest()

        # Begin sync...
        inSync = False
        if byte_in == RESP_SYNC_START:
            self.write_byte(COMMAND_SYNC_1)
            byte_in = self.read_byte()
            if byte_in == RESP_SYNC_1:
                self.write_byte(COMMAND_SYNC_2)
                byte_in = self.read_byte()
                if byte_in == RESP_SYNC_OK:
                    inSync = True
        return inSync

    # Start MCU syncing process
    def sync(self):
        inSync = False

        # Try sending a packet
        inSync = self.send_packet()
        if not inSync:
            # Not in sync: force resync and send a packet
            inSync = self.force_sync()
            if inSync:
                inSync = self.send_packet()
        return inSync

    def send_input(self, command=NO_INPUT):
        if not self.send_cmd(command):
            print('Packet Error!')
