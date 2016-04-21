import socket
import time


HANDSHAKE_DATA = bytearray([0x49, 0x54, 0x64, 0x00, 0x00, 0x00, 0x5D, 0x00, 0x00, 0x00, 0x81, 0x85, 0xFF, 0xBD, 0x2A, 0x29, 0x5C, 0xAD, 0x67, 0x82, 0x5C, 0x57, 0xBE, 0x41, 0x03, 0xF8, 0xCA, 0xE2, 0x64, 0x30, 0xA3, 0xC1,
            0x5E, 0x40, 0xDE, 0x30, 0xF6, 0xD6, 0x95, 0xE0, 0x30, 0xB7, 0xC2, 0xE5, 0xB7, 0xD6, 0x5D, 0xA8, 0x65, 0x9E, 0xB2, 0xE2, 0xD5, 0xE0, 0xC2, 0xCB, 0x6C, 0x59, 0xCD, 0xCB, 0x66, 0x1E, 0x7E, 0x1E,
            0xB0, 0xCE, 0x8E, 0xE8, 0xDF, 0x32, 0x45, 0x6F, 0xA8, 0x42, 0xEE, 0x2E, 0x09, 0xA3, 0x9B, 0xDD, 0x05, 0xC8, 0x30, 0xA2, 0x81, 0xC8, 0x2A, 0x9E, 0xDA, 0x7F, 0xD5, 0x86, 0x0E, 0xAF, 0xAB, 0xFE,
            0xFA, 0x3C, 0x7E, 0x54, 0x4F, 0xF2, 0x8A, 0xD2, 0x93, 0xCD])

START_DRONE_DATA = bytearray([0xCC, 0x7F, 0x7F, 0x0, 0x7F, 0x0, 0x7F, 0x33])


class DroneControl(object):
    def __init__(self):
        self._ip = '172.16.10.1'
        self._tcp_port = 8888
        self._udp_port = 8895

    def connect(self):
        self.connect_tcp()
        self.connect_udp()

    def connect_tcp(self): # handshake
        print("Starting Handshake...")
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.connect((self._ip, self._tcp_port))
        self.tcp_socket.send(HANDSHAKE_DATA)
        print("Handshake done!")

    def connect_udp(self):
        print("Starting drone...")
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.connect((self._ip, self._udp_port))
        self.droneCmd = START_DRONE_DATA[:]
        self.udp_socket.send(self.droneCmd)
        print("Drone started!")

    def checksum(self, data):
        return_data = (data[1] ^ data[2] ^ data[3] ^ data[4] ^ data[5]) & 0xFF;
        return return_data

    def disconnect(self):
        print("Disconnecting...")
        self.udp_socket.close()
        self.tcp_socket.close()
        print("Disconnected!")

    def cmd(self, r=127, p=127, t=15, y=127): # roll, pitch, throttle, yaw
        time.sleep(0.05)    
        self.droneCmd[1] = r
        self.droneCmd[2] = p
        self.droneCmd[3] = t
        self.droneCmd[4] = y
        self.droneCmd[6] = self.checksum(self.droneCmd)
        self.udp_socket.send(self.droneCmd)

    def stop(self):
        time.sleep(0.05)
        self.udp_socket.send(START_DRONE_DATA)


if __name__ == "__main__":
    drone = DroneControl()
    drone.connect()

    for i in range(100):
        drone.cmd(t=50)

    drone.stop()
    drone.disconnect()
