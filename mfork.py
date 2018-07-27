import socket
import pickle
from threading import Thread
import multiprocessing
import values

class Fork:
    def __init__(self,index,host,port):

        #ID of each fork process so that philosopher can address it by its index and
        # it is easy to pass int message
        self.id=index

        #Assume that initially all forks are clean
        self.is_dirty=False

        #forks ip and port
        self.host=host
        self.port = port

        #Each fork process is running at first
        self.is_running=True

#-------------------------------METHODS----------------------------------------------

    # Consider each fork as a thread. It will run in background
    # Create TCP Socket connection. Each fork will act as a socket server
    # Forks will receive message from Philosophers (TCP client)
    # and send message about fork availability to philosophers

    def enable(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as exp:
            print("Connection establishment problem " + str(exp))

        try:
            self.socket.bind((self.host, self.port))
        except socket.error as exp:
            print("socket bind problem " + str(exp))

        self.socket.listen(0)
        while self.is_running:
            self.server,self.host = self.socket.accept()
            Thread(target = self.receive_data,args=(self.server,)).start()



    def pickfork(self,philosopher_request,connection):
        if self.is_dirty:
            sent_data = values.serialize([self.id, philosopher_request[0], values.ACTION_PICK_FORK, values.ACTION_FAIL])
            connection.send(sent_data)
            print("data received at philosopher : ",str(values.unserialize(sent_data)))
            return False
        else:  # If fork is clean/not being used
            self.is_dirty = True
            self.current_philosopher = philosopher_request[0]
            sent_data = self.serialize([self.id, self.current_philosopher, values.ACTION_PICK_FORK, values.ACTION_SUCCESS])
            connection.send(sent_data)
            print("data received at philosopher : ",str(values.unserialize(sent_data)))
            return True


    def dropfork(self,philosopher_request,connection):
        # philosopher that was using the fork want to clean the dirty fork and put it down
        # only the owner can put this fork down
        if self.is_dirty and self.current_philosopher == philosopher_request[0]:
            last_user = self.current_philosopher
            self.is_dirty = False #celan the fork
            self.current_philosopher = None #now the fork belongs to no one and any one of two adjascent philosopher can pick it
            connection.send(values.serialize([self.id, last_user, 0, 1])) # let philosophers know the status of this fork
        else:
            connection.send(values.serialize([self.id, philosopher_request[0], 0, 0]))


    def receive_data(self,connection):
        while self.is_running:
            try:
                data = connection.recv(values.DATA_SIZE)
                if data:
                    print("data from philosopher : "+str(values.unserialize(data)))
                    philosopher_request = values.unserialize(data)
                    if philosopher_request[1] == values.ACTION_PICK_FORK:
                        is_successful = self.pickfork(philosopher_request,connection)
                        if not is_successful:
                            break
                    elif philosopher_request[1] == values.ACTION_DROP_FORK:
                        self.dropfork(philosopher_request,connection)
                        break

            except socket.error as e:
                print("error getting data : " + str(e))
                #connection.close()
        connection.close()


    def disable(self):
        self.is_running = False


    def deserialize(self,data):
        return pickle.loads(data)

    def serialize(self,data):
        return pickle.dumps(data,protocol=2)

#--------------End Class --------------------------

def register_forks():
    host = "localhost"
    port = 4446
    try:
        msocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msocket.sendto(values.serialize(["fork",port]),(values.MONITOR_IP,values.MONITOR_PORT2))
    except socket.error as e:
        print("Connection error 0: "+str(e))
    try:
        #this is test
        data, server = msocket.recvfrom(values.DATA_SIZE)
        data_array = values.unserialize(data)
        print(str(data_array))
        return data_array
    except socket.error as e:
        print("Connection error 1: "+str(e))
    finally:
        msocket.close()

background_forks = []

def timeout(background_forks):
    running = True

    host = "localhost"
    port = 4446
    try:
        msocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msocket.sendto(values.serialize(["timeout",port]),(values.MONITOR_IP,values.MONITOR_PORT2))
    except socket.error as e:
        print("Connection error 0: "+str(e))
    while running:
        try:
            data, server = msocket.recvfrom(values.DATA_SIZE)
            data_array = values.unserialize(data)
            for p in background_forks:
                print("background forks terminated",p)
                p.terminate()
            running=False
        except socket.error as e:
            print("Connection error 1: "+str(e))
            running=False
        pass



def create_forks(data_array):
    global background_forks

    fork = Fork(data_array[0],data_array[1],data_array[2])
    print(fork)
    process = multiprocessing.Process(target=fork.enable,args=())
    process.start()
    background_forks.append(process)

    process1 = multiprocessing.Process(target=timeout,args=(background_forks,))
    process1.start()


if __name__ == "__main__":
    try:
        data_array = register_forks()
        create_forks(data_array)
    except KeyboardInterrupt:
        for f in background_forks:
            f.terminate()



