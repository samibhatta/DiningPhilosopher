import pickle
import socket

#------------------------------ Variables -------------------------------
forks = [] #just a placeholder. Its values are set from other files

#------------------------------ Constants -------------------------------
FORK_PORT = 6541
MONITOR_IP = "192.168.0.3" #socket.gethostbyname("sigma27")
DATA_SIZE = 2048
MONITOR_PORT = 6444
MONITOR_PORT2 = 6555

STATE_THINKING = 0
STATE_WAITING = 1
STATE_EATING = 2

STATE_THINKING_STRING = "Thinking"
STATE_WAITING_STRING = "Waiting"
STATE_EATING_STRING = "Eating"

CURRENT_TIME_STRING = "Current Time"
PHILOSOPHER_HEADER_STRING = "Philo# "
DISPLAY_TIME_FORMAT = "%B %d %H:%M:%S" #month_short day hour:minute:second
DISPLAY_COLUMN_OFFSET = 20
DISPLAY_COLUMN_SPACE = "{: <"+str(DISPLAY_COLUMN_OFFSET)+"s}"


ACTION_PICK_FORK = 1
ACTION_DROP_FORK = 0

ACTION_SUCCESS = 1
ACTION_FAIL = 0

#-------------------------------- Helper methods --------------------------
def fork_count():
    return len(forks)


def get_fork(index):
    return forks[index]


def get_fork1(index):
    fork = get_fork(index % len(forks))
    return fork if fork else get_fork(len(forks)-1)
    # if fork:
    #     return fork
    # else:
    #     return get_fork(len(forks) - 1)


def get_fork2(index):
    fork = get_fork((index + 1) % len(forks))
    return fork if fork else get_fork(len(forks) - 1)
    # if fork:
    #     return fork
    # else:
    #     return get_fork(len(forks) - 1)

def unserialize(data):
    return pickle.loads(data)

def serialize(data):
    return pickle.dumps(data,protocol=2)

