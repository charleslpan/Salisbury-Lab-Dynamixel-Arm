#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ante Qu, Charles Pan, Jason Ah Chuen

#
# *********     Dynamixel Arm Movement and Current Readings      *********
#
#
# Available Dynamixel model on this example : All models using Protocol 2.0
# This example is designed for using two Dynamixel PRO 54-200, and an USB2DYNAMIXEL.
# To use another Dynamixel model, such as X series, see their details in E-Manual(support.robotis.com) and edit below variables yourself.
# Be sure that Dynamixel PRO properties are already set as %% ID : 1 / Baudnum : 1 (Baudrate : 57600)
#
# When running the code in Terminal, the keyboard library requires to run as an administrator.
# Run the code as 'sudo python MoveButtons.py'
# Use q, a, w, s, e, d, r, f to move motors 1, 2, 3, and 4 respectively.
# Use z to quit out of program.

# Jason's update: Implemented extra controls: "h" for hello, "w" for the whip dance, "t" to go to the surface and tap it twice
# Also fixed the problem of jerky motions by using a rectangular velocity profile.

import os, ctypes, struct
import keyboard
import time

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

os.sys.path.append('../DynamixelSDK-master/python/dynamixel_functions_py')             # Path setting
os.sys.path.append('.')             # Path setting
cwd=os.getcwd()
os.chdir('../DynamixelSDK-master/python/dynamixel_functions_py')
import dynamixel_functions as dynamixel                     # Uses Dynamixel SDK library
os.chdir(cwd)
import datetime


COMM_SUCCESS                = 0                             # Communication Success result value
COMM_TX_FAIL                = -1001                         # Communication Tx Failed



class DynamixelReader:
    def __init__(self,
                 # Check which port is being used on your controller
                 device_name = "COM5".encode('utf-8'),
                 # baud rate
                 baud_rate = 1000000,
                 # motor ids
                 m1id = 100,
                 m2id = 101,
                 m3id = 102,
                 m4id = 103,
                 #protocol ver
                 proto_ver = 2,
                 #SyncRead Addr
                 read_addr = 126,
                 #SyncRead Len
                 read_len = 2):
        self.baud_rate = baud_rate
        self.device_name = device_name
        self.m1id = m1id
        self.m2id = m2id
        self.m3id = m3id
        self.m4id = m4id
        self.proto_ver = proto_ver
        self.read_addr = read_addr
        self.read_len = read_len

        # Initialize PortHandler Structs
        # Set the port path
        # Get methods and members of PortHandlerLinux or PortHandlerWindows
        self.port_num = dynamixel.portHandler(device_name)
        dynamixel.setPacketTimeoutMSec(1)
        # Initialize PacketHandler Structs
        dynamixel.packetHandler()
        # Initialize Groupsyncread Structs for Current
        self.groupread_num = dynamixel.groupSyncRead(self.port_num, proto_ver, read_addr,read_len) #0, 148
        dt = datetime.datetime.now()
        self.timestamp0 = dt.minute * 60000000 + dt.second * 1000000 + dt.microsecond
        self.Init_Port_And_Motors()
        self.Init_Param_Storage()

    def __del__(self):
        self.Disable_Torque_Close_Port()

    def Init_Port_And_Motors(self):
        # Open port
        if dynamixel.openPort(self.port_num):
            print("Successfully opened the port!")
        else:
            print("Failed to open the port!")
            print("Press any key to terminate...")
            getch()
            quit()
        # Set port baudrate
        if dynamixel.setBaudRate(self.port_num, self.baud_rate):
            print("Successfully set the baudrate!")
        else:
            print("Failed to change the baudrate!")
            print("Press any key to terminate...")
            getch()
            quit()
        ADDR_PRO_TORQUE_ENABLE = 64
        TORQUE_ENABLE = 1
        dxl_comm_result = COMM_TX_FAIL
        # Enable Dynamixel#1 Torque
        dynamixel.write1ByteTxRx(self.port_num, self.proto_ver, self.m1id, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))
        else:
            print("Dynamixel#1 has been successfully connected")
        # Enable Dynamixel#2 Torque
        dynamixel.write1ByteTxRx(self.port_num, self.proto_ver, self.m2id, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))
        else:
            print("Dynamixel#2 has been successfully connected")
        # Enable Dynamixel#3 Torque
        dynamixel.write1ByteTxRx(self.port_num, self.proto_ver, self.m3id, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))
        else:
            print("Dynamixel#3 has been successfully connected")
        # Enable Dynamixel#4 Torque
        dynamixel.write1ByteTxRx(self.port_num, self.proto_ver, self.m4id, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))
        else:
            print("Dynamixel#4 has been successfully connected")

    def Init_Param_Storage(self):
        groupread_num = self.groupread_num
        # Add parameter storage for Dynamixel#1 current
        dxl_addparam_result = ctypes.c_ubyte(dynamixel.groupSyncReadAddParam(groupread_num, self.m1id)).value
        if dxl_addparam_result != 1:
            print("[ID:%03d] groupSyncRead addparam failed" % (self.m1id))
            quit()

        # Add parameter storage for Dynamixel#2 current
        dxl_addparam_result = ctypes.c_ubyte(dynamixel.groupSyncReadAddParam(groupread_num, self.m2id)).value
        if dxl_addparam_result != 1:
            print("[ID:%03d] groupSyncRead addparam failed" % (self.m2id))
            quit()

        # Add parameter storage for Dynamixel#2 current
        dxl_addparam_result = ctypes.c_ubyte(dynamixel.groupSyncReadAddParam(groupread_num, self.m3id)).value
        if dxl_addparam_result != 1:
            print("[ID:%03d] groupSyncRead addparam failed" % (self.m3id))
            quit()

        # Add parameter storage for Dynamixel#4 current
        dxl_addparam_result = ctypes.c_ubyte(dynamixel.groupSyncReadAddParam(groupread_num, self.m4id)).value
        if dxl_addparam_result != 1:
            print("[ID:%03d] groupSyncRead addparam failed" % (self.m4id))
            quit()

    def Set_Value(self, motorId, set_addr, set_len, value):
        if(set_len == 4):
            dynamixel.write4ByteTxRx(self.port_num, self.proto_ver, motorId, set_addr, value)
        elif(set_len == 2):
            dynamixel.write2ByteTxRx(self.port_num, self.proto_ver, motorId, set_addr, value)
        elif(set_len == 1):
            dynamixel.write1ByteTxRx(self.port_num, self.proto_ver, motorId, set_addr, value)
        else:
            print('[ID:%03d]: invalid set length %d' %(motorId, set_len))
            return
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))

    def Disable_Torque_Close_Port(self):
        ADDR_PRO_TORQUE_ENABLE = 64
        TORQUE_DISABLE = 0
        dxl_comm_result = COMM_TX_FAIL
        # Enable Dynamixel#1 Torque
        dynamixel.write1ByteTxRx(self.port_num, self.proto_ver, self.m1id, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))
        else:
            print("Dynamixel#1 has been successfully freed")
        # Enable Dynamixel#2 Torque
        dynamixel.write1ByteTxRx(self.port_num, self.proto_ver, self.m2id, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))
        else:
            print("Dynamixel#2 has been successfully freed")
        # Enable Dynamixel#3 Torque
        dynamixel.write1ByteTxRx(self.port_num, self.proto_ver, self.m3id, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))
        else:
            print("Dynamixel#3 has been successfully freed")
        # Enable Dynamixel#4 Torque
        dynamixel.write1ByteTxRx(self.port_num, self.proto_ver, self.m4id, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))
        else:
            print("Dynamixel#4 has been successfully freed")

        #close port
        dynamixel.closePort(self.port_num)
        
    def Read_Value(self, motorId, read_addr, read_len):
        # Read value
        dxl_result = -1
        if(read_len == 4):
            dxl_result = dynamixel.read4ByteTxRx(self.port_num, self.proto_ver, motorId, read_addr)
        elif(read_len == 2):
            dxl_result = dynamixel.read2ByteTxRx(self.port_num, self.proto_ver, motorId, read_addr)
        elif(read_len == 1):
            dxl_result = dynamixel.read1ByteTxRx(self.port_num, self.proto_ver, motorId, read_addr)
        else:
            print('[ID:%03d]: invalid read length %d' %(motorId, read_len))
            return dxl_result
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))
        return dxl_result

if __name__ == '__main__':

    reader = DynamixelReader(device_name = "/dev/tty.usbserial-FT2N0DM5".encode('utf-8'),
                             # baud rate
                             baud_rate = 115200,
                             # motor ids
                             m1id = 100, m2id = 101, m3id = 102, m4id = 103,
                             # protocol ver
                             proto_ver = 2,
                             # Motor Current Addr and Len
                             read_addr = 126, read_len = 2)

    N_QUERIES = 4000

    ADDR_PRO_GOAL_POSITION = 116  # address of the goal position and present position
    ADDR_PRO_PRESENT_POSITION = 132
    LEN_PRO_GOAL_POSITION = 4  # length of size of goal and present position
    LEN_PRO_PRESENT_POSITION = 4
    
    
    ADDR_PRO_GOAL_VELOCITY = 104  # address of the goal velocity and present velocity
    ADDR_PRO_PRESENT_VELOCITY = 128

    ADDR_PRO_ACCELERATION = 108  # acceleration value of profile
    ADDR_PRO_VELOCITY = 112 # velocity value of profile


    # for j in range(N_QUERIES):
    #     oldtimestamp = timestamp
    #
    #     # read all current
    #     [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()
    #
    #     #filter
    #
    #
    #     #set goal position example
    #     skip = 20  # skip represents the interval
    #     if j % skip == 0:
    #         reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, current_position - int(j))
    #
    #     difft = timestamp - oldtimestamp
    #     print(
    #         "%09d,%05d,%05d,%05d,%05d, %d" % (timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current, difft))
    #     print("%09d,%05d,%05d,%05d,%05d" % (timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current),
    #           file=fout)

    curr1 = reader.Read_Value(reader.m1id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    curr2 = reader.Read_Value(reader.m2id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    curr3 = reader.Read_Value(reader.m3id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    curr4 = reader.Read_Value(reader.m4id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    
    # Determining type of profile to use (step, rectangular or trapezoidal)
    
    reader.Set_Value(reader.m1id, ADDR_PRO_VELOCITY, LEN_PRO_GOAL_POSITION, 1)
    #reader.Set_Value(reader.m1id, ADDR_PRO_ACCELERATION, LEN_PRO_GOAL_POSITION, 1)
    reader.Set_Value(reader.m2id, ADDR_PRO_VELOCITY, LEN_PRO_GOAL_POSITION, 1)
    #reader.Set_Value(reader.m2id, ADDR_PRO_ACCELERATION, LEN_PRO_GOAL_POSITION, 1)
    reader.Set_Value(reader.m3id, ADDR_PRO_VELOCITY, LEN_PRO_GOAL_POSITION, 1)
    #reader.Set_Value(reader.m3id, ADDR_PRO_ACCELERATION, LEN_PRO_GOAL_POSITION, 1)
    reader.Set_Value(reader.m4id, ADDR_PRO_VELOCITY, LEN_PRO_GOAL_POSITION, 1)
    #reader.Set_Value(reader.m4id, ADDR_PRO_ACCELERATION, LEN_PRO_GOAL_POSITION, 1)
    
    
    # Setting goal velocity
    reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_VELOCITY, LEN_PRO_GOAL_POSITION, 1)
    reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_VELOCITY, LEN_PRO_GOAL_POSITION, 1)
    reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_VELOCITY, LEN_PRO_GOAL_POSITION, 1)
    reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_VELOCITY, LEN_PRO_GOAL_POSITION, 1)
    
    while True:  # making a loop


        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('q'):
                reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr1 + 20)
                curr1 += 20
                print('You Pressed Motor 1 UP Key!')
            if keyboard.is_pressed('a'):
                reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr1 - 20)
                curr1 -= 20
                print('You Pressed Motor 1 DOWN Key!')
            if keyboard.is_pressed('w'):
                reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2 + 20)
                curr2 += 20
                print('You Pressed Motor 2 UP Key!')
            if keyboard.is_pressed('s'):
                reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2 - 20)
                curr2 -= 20
                print('You Pressed Motor 2 DOWN Key!')
            if keyboard.is_pressed('e'):
                reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr3 + 20)
                curr3 += 20
                print('You Pressed Motor 3 UP Key!')
            if keyboard.is_pressed('d'):
                reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr3 - 20)
                curr3 -= 20
                print('You Pressed Motor 3 DOWN Key!')
            if keyboard.is_pressed('r'):  # if key 'q' is pressed
                reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4 + 20)
                curr4 += 20
                print('You Pressed Motor 4 UP Key!')
            if keyboard.is_pressed('f'):
                reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4 - 20)
                curr4 -= 20
                print('You Pressed Motor 4 DOWN Key!')
            
            # Hello World movement
            if keyboard.is_pressed('h'):
                reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 3901)
                reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 950)
                reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 288)
                reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 2100)
                
                #delay
                time.sleep(1)
                
                #reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 3901)
                #reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 950)
                #reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 288)
                reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 780)
                
                #delay
                time.sleep(1)
                
                for x in range(5):
                    #reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 3901)
                    #reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 950)
                    reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, -732)
                    #reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 780)
                    
                    #delay
                    time.sleep(0.5)
                    #reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 3901)
                    #reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 950)
                    reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 1148)
                    #reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 780)
                    
                    #delay
                    time.sleep(0.5)
            
                print('hello!')
            
            # Tapping movement on horizontal surface
            if keyboard.is_pressed('t'):
                
                # end effector on horizontal table
                reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 193)
                reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 1450)
                reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 307)
                reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 2274)
                time.sleep(1)
                
                for x in range(2):
                    # move up
                    reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 1400)    
                    time.sleep(1)
                    
                    # move down
                    reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 1450)    
                    time.sleep(0.5)
            
            # Whip dance move
            if keyboard.is_pressed('m'):
                
                reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 3500)
                reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 1710)
                reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 2100)
                reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 2050)
                time.sleep(0.1)
                
                reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 1960)
                time.sleep(0.1)
                reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 2600)
                time.sleep(0.1)
                
                reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 4400)
                
                time.sleep(0.1)

                reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 1410)
                time.sleep(0.1)
                reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 1360)
                
                time.sleep(0.1)
                
                reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 4430)
                time.sleep(0.1)
                reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 1420)
                time.sleep(0.1)
                reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 1364)
                time.sleep(0.1)
                reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 1940)
                
            if keyboard.is_pressed('z'):
                break  # finishing the loop
            else:
                pass
        except:
            break  # if user pressed a key other than the given key the loop will break
        
        #print(curr1, end = " ")
        #print(curr2, end = " ")
        #print(curr3, end = " ")
        #print(curr4)

    del reader
    fout.close()
    print("Reading done!")

#miscellaneous
# Control table address
ADDR_PRO_TORQUE_ENABLE = 64  # Control table address is different in Dynamixel model
ADDR_PRO_GOAL_POSITION = 116
ADDR_PRO_REALTIME_TICK = 120
ADDR_PRO_PRESENT_POSITION = 132
ADDR_PRO_LED_RED = 65
ADDR_PRO_CURRENT = 126

# Data Byte Length
LEN_PRO_GOAL_POSITION = 4
LEN_PRO_PRESENT_POSITION = 4
LEN_PRO_REALTIME_TICK = 2
LEN_PRO_LED_RED = 1
LEN_PRO_CURRENT = 2

# Protocol version
PROTOCOL_VERSION = 2  # See which protocol version is used in the Dynamixel

# Default setting
DXL1_ID = 100  # Dynamixel ID: 1
DXL2_ID = 101  # Dynamixel ID: 2
DXL3_ID = 102  # Dynamixel ID: 3
DXL4_ID = 103  # Dynamixel ID: 4
BAUDRATE = 1000000
DEVICENAME = "COM5".encode('utf-8')  # Check which port is being used on your controller