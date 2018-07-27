import socket
import pickle
from threading import Thread
import time
import values
import multiprocessing

forks = []


def serialize(data):
    return pickle.dumps(data,protocol=2)

def deserialize(data):
    return pickle.loads(data)


class Monitor:
    addresses = []
    def __init__(self):
        self.isrunning=True
        self.timer = 90
        self.msocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.msocket.bind((values.MONITOR_IP,values.MONITOR_PORT2))
        p1 = Thread(target=self.backgroundprocess,args=())
        p1.start()
        t2 = Thread(target = self.decreaseTimer,args=(p1,))
        t2.start()

        pass


    def decreaseTimer(self,p1):

        global addresses
        while self.isrunning:
            time.sleep(1)
            self.timer -= 1
            print("timer = ",str(self.timer))
            if(self.timer <=0):
                for address in self.addresses:
                    print("sending kill signal ",str(address))
                    self.msocket.sendto(serialize("killsignal"),address)
                self.isrunning=False
                #p1.terminate()


    def backgroundprocess(self):
        isrunning=True
        while isrunning:
            print("server : accepting client")
            #(client,(ip,port)) = self.msocket.accept()
            message, address = self.msocket.recvfrom(values.DATA_SIZE)
            message1 = deserialize(message)
            print(message1)
            if message1[0] == "fork":
                (ip,port) = address
                if [ip,message1[1]] in forks:
                    print(str(address)+" exists in list "+str(forks))
                    self.msocket.sendto(serialize([forks.index([ip,message1[1]]),ip,message1[1]]),address)
                else:
                    self.timer=90
                    print(str(address)+" doesnot exists in list "+str(forks))
                    forks.append([ip,message1[1]])
                    self.msocket.sendto(serialize([forks.index([ip,message1[1]]),ip,message1[1]]),address)
            elif message1[0] == "displayManager":
                self.msocket.sendto(serialize(forks),address)
            elif message1[0] == "philosopher":
                self.msocket.sendto(serialize(forks),address)
                isrunning=False
            elif message1[0] == "timeout":
                self.addresses.append(address)




Monitor()



def get(i):
    return forks[i];

def get_fork_len():
    return len(forks);
