import values
import time
import random
import multiprocessing
import socket
import pickle
from connection import UDPClient
from connection import TCPClient

class Philosopher:

    def __init__(self,id,fork_left,fork_right):
        self.philosopher_id= id
        self.left_fork = fork_left
        self.right_fork = fork_right


    def enable(self):
        self.is_running = True
        while self.is_running:
            self.display(values.serialize([self.philosopher_id, values.STATE_THINKING]))
            time.sleep(random.randint(1, 3))
            self.sitOnTable()

    def get_fork2(self, fork):
        client = TCPClient(fork[0], fork[1])
        client.connect()
        client.send(values.serialize([self.philosopher_id, values.ACTION_PICK_FORK]))
        data = client.receive()
        if data:
            data_from_fork = pickle.loads(data)
            if \
                    data_from_fork[1] == self.philosopher_id \
                    and data_from_fork[2] == values.ACTION_PICK_FORK \
                    and data_from_fork[3] == values.ACTION_SUCCESS:
                return [values.ACTION_SUCCESS, client]
        client.close()
        return [values.ACTION_FAIL, client]



    def sitOnTable(self):
        forkl,forkr = self.left_fork,self.right_fork
        while self.is_running:
            self.display(values.serialize([self.philosopher_id, values.STATE_WAITING]))
            fork1 = self.get_fork1(forkl)
            state_fork2 = self.get_fork2(forkr)

            fork2 = state_fork2[1]
            #If you cant get the second fork, just drop the first fork
            # wait for some time and try again to pick up the second fork
            if state_fork2[0] == values.ACTION_FAIL:
                self.dropfork(fork1)
                forkl, forkr = forkr, forkl
            else:
                break

        if self.is_running:
            #
            self.display(values.serialize([self.philosopher_id, values.STATE_EATING]))  # IS EATING
            time.sleep(random.randint(2, 6))
            # Release both forks after done eating
            self.dropfork(fork1)
            self.dropfork(fork2)
        else:
            if fork1:
                fork1.close()
            if fork2:
                fork2.close()



    def dropfork(self, client):
        # Tell fork that this philosopher wants to drop the fork and make it
        # available to other who are trying to access it
        client.send(values.serialize([self.philosopher_id, values.ACTION_DROP_FORK]))
        data = client.receive()
        if data:
            response = pickle.loads(data)
            if \
                    response[1] == self.philosopher_id \
                    and response[2] == values.ACTION_DROP_FORK \
                    and response[3] == values.ACTION_SUCCESS:
                client.close()
            else:
                pass



    def get_fork1(self,forkl):
        while self.is_running:
            try:
                time.sleep(1)
                try:
                    lfork = TCPClient(forkl[0],forkl[1])
                    lfork.connect()
                except socket.error as e:
                    print("socekt error lf =",e)
                lfork.send(values.serialize([self.philosopher_id, values.ACTION_PICK_FORK]))
                data = lfork.receive(1024)
                print(str(values.unserialize(data)))
                if data:
                    data_from_fork = values.unserialize(data)
                    if \
                            data_from_fork[1] == self.philosopher_id \
                            and data_from_fork[2] == values.ACTION_PICK_FORK \
                            and data_from_fork[3] == values.ACTION_SUCCESS:
                        return lfork
                lfork.close()
            except Exception as e:
                pass





    @staticmethod
    def display(msg):
        client = UDPClient()
        client.send(values.MONITOR_IP, values.MONITOR_PORT, msg)
        client.close()


#---------------------------- END CLASS ---------------------------------


background_philosophers = []

def philosopher_process(identifier, fork1, fork2):
    philosopher = Philosopher(identifier, fork1, fork2)
    philosopher.enable()


def create_philosophers():
    global background_philosophers

    for i in range(len(values.forks)):
        print("running "+str(i))
        process = multiprocessing.Process(target=philosopher_process,args=(i,values.get_fork1(i),values.get_fork2(i),))
        background_philosophers.append(process)
        process.start()

    time.sleep(90)
    #ask_forks_to_terminate()
    for f in background_philosophers:
            f.terminate()


def get_all_forks():
    global forks
    port = 4001
    try:
        msocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msocket.sendto(values.serialize(["philosopher",port]),(values.MONITOR_IP,values.MONITOR_PORT2))
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


if __name__ == "__main__":
    try:
        get_all_forks()
        create_philosophers()
    except KeyboardInterrupt:
        for f in background_philosophers:
            f.terminate()
