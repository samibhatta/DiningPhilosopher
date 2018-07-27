import constants
import socket
import pickle
import datetime
from threading import Thread

class TCPClient:
    _socket=None
    def __init__(self,remote_host=socket.gethostname(), remote_port=5000):
        self.remote_host = self.remote_port = None
        self.remote_host, self.remote_port = remote_host, remote_port
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as exp:
            print('Failed creating TCP connection', exp)

def connect(self ):
    try:
        self._socket.connect((self.remote_host, self.remote_port))
        except socket.error as e:
            pass
                
                def send(self, data):
                    self._socket.send(data)

def receive(self, size=1024):
    data = None
        try:
            data =  self._socket.recv(size)
            return data
    except socket.error as e:
        print("error=",e)
        return data

def close(self):
    if self._socket:
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
                self._socket.close()
            except Exception as e:
                print("Error closing socket :",e)




class UDPSocket(object):
    def __init__(self, host=None, port=constants.MONITOR_PORT):
        self.host, self.port = host, port
        self.run = False
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as exp:
            print('Failed to create server UDP socket object!!', exp)
        try:
            self.socket.bind((self.host, self.port))
        except socket.error as exp:
            print('Cannot bind server to ' + str(self.host) + ' on port ' + str(self.port), exp)

def start(self):
    self.run = True
        while self.run:
            d = self.receive()
            Thread(target=self.handle_data, args=(d,)).start()
                
                def stop(self):
                    self.run = False

def send(self, data, remote_address):
    self.socket.sendto(data, remote_address)
    
    def receive(self, size=1024):
        return self.socket.recvfrom(size)
    
    def close(self):
        self.socket.close()
    
    
    def handle_data(self, data):
        state = []
        
        response = pickle.loads(data[0])
        process_id = response[0]
        status_type = response[1]
        
        status = ""
        if status_type == 0:
            status = "Thinking"
        elif status_type == 1:
            status = "Waiting"
        elif status_type == 2:
            status = "Eating"
    
        current_time = datetime.datetime.now().strftime('%B %d %H:%M:%S')
        state.append(current_time)
        
        for i in range(self.num):
            if i == process_id:
                state.append(status)
            else:
                state.append("--------")

print(self.display_format.format(*state))


class UDPClient:
    def __init__(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as exp:
            print('Failed to create client UDP socket object!!', exp)

def send(self, remote_host=constants.MONITOR_IP, remote_port=constants.MONITOR_PORT, data=""):
    self.socket.sendto(data, (remote_host, remote_port))
    
    def receive(self, size=1024):
        return self.socket.recvfrom(size)[0]
    
    def close(self):
        self.socket.close()


class Display(UDPSocket):
    def __init__(self, number_of_philosophers):
        self.num = number_of_philosophers
        self.headers = ['Current Time']
        self.divider_line = '----------------------'
        self.display_format = '{: >20} '
        self.initialstate = [datetime.datetime.now().strftime('%B %d %H:%M:%S')]
        for i in range(number_of_philosophers):
            self.headers.append("Philosopher " + str(i))
            self.initialstate.append("Thinking")
            if i != (number_of_philosophers - 1):
                self.display_format += "{: >20} "
            else:
                self.display_format += "{: >20}"
            self.divider_line += "----------------------"
        
        print(self.display_format.format(*self.headers))
        print(self.divider_line)
        print(self.display_format.format(*self.initialstate))
        
    super(Display, self).__init__(constants.MONITOR_IP, constants.MONITOR_PORT)


def start(self):
    super(Display, self).start()
    
    def stop(self):
        super(Display, self).stop()
        super(Display, self).close()


