import multiprocessing
import values
import datetime
import socket
from threading import Thread
import time

class Display1:
    def __init__(self, host=values.MONITOR_IP, port=values.MONITOR_PORT):
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

    def print_header(self):
        initialstate = [datetime.datetime.now().strftime(values.DISPLAY_TIME_FORMAT)]
        headers = [values.CURRENT_TIME_STRING]
        line = '-'*values.DISPLAY_COLUMN_OFFSET
        for i in range(len(values.forks)):
            headers.append(values.PHILOSOPHER_HEADER_STRING + str(i))
            initialstate.append(values.STATE_THINKING_STRING)
            line += "-"*values.DISPLAY_COLUMN_OFFSET

        string1=""
        string2=""

        for i in headers:
            string1 += " " * values.DISPLAY_COLUMN_OFFSET + i

        for j in initialstate:
            string2 += " "*values.DISPLAY_COLUMN_OFFSET + j


        print(string1)
        print(line)
        print(string2)


    def start(self):
        self.run = True
        while self.run:
            try:
                d = self.receive()
                Thread(target=self.display_philosopher_states, args=(d,)).start()
            except Exception as e:
                print("Exception :",e)

    def stop(self):
        self.run = False

    def send(self, data, remote_address):
        self.socket.sendto(data, remote_address)

    def receive(self, size=1024):
        try:
            data = self.socket.recvfrom(size)
            return data
        except Exception as e:
            print("receive exception ",e)

    def close(self):
        self.socket.close()


    def display_philosopher_states(self, data):
        display_state = []
        action = values.unserialize(data[0]) #[philosopher_id, action]
        philosopher_id = action[0]
        state = action[1]

        state_string = ""
        if state == values.STATE_THINKING:
            state_string = values.STATE_THINKING_STRING
        elif state == values.STATE_WAITING:
            state_string = values.STATE_WAITING_STRING
        elif state == values.STATE_EATING:
            state_string = values.STATE_EATING_STRING

        current_time = datetime.datetime.now().strftime(values.DISPLAY_TIME_FORMAT)
        display_state.append(current_time)

        for i in range(len(values.forks)):
            if i == philosopher_id:
                display_state.append(state_string)
            else:
                display_state.append("-"* len(values.forks))

        string1= ""
        for i in display_state:
            string1 += " "*values.DISPLAY_COLUMN_OFFSET + str(i)

        print(string1)


def run_in_background(length):
    try:
        display_module = Display1(values.MONITOR_IP,values.MONITOR_PORT)
        display_module.print_header()
        display_module.start()
    except Exception as e:
        print("run_in_background :",str(e))


def get_all_forks():
    global forks
    port = 4001
    try:
        msocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msocket.sendto(values.serialize(["displayManager",port]),(values.MONITOR_IP,values.MONITOR_PORT2))
    except socket.error as e:
        print("Connection error 0: "+str(e))
    try:
        #this is test
        data, server = msocket.recvfrom(2048)
        forks = values.unserialize(data)
        values.forks = forks
        print(forks)
    except socket.error as e:
        print("Connection error 1: "+str(e))

def display():
    get_all_forks()
    display_ = multiprocessing.Process(target=run_in_background, args=(5,))
    display_.start()

    time.sleep(120)
    display_.terminate()


if __name__ == "__main__":
    display()
