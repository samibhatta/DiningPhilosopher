 # The Dining Philosopher Problem 

Problem Description:
The Dining Philosopher Problem states that K philosophers seated around a circular table with one fork between each pair of philosophers. There is one fork between each philosopher. A philosopher may eat if he can pick up the two forks adjacent to him. One fork may be picked up by any one of its adjacent followers but not both.  [source: geeksforgeeks.org ] 

Each philosopher is represented by the following pseudocode:
```   
 While true do
       {  
    THINK;
      	    PICKUP(CHOPSTICK[i], CHOPSTICK[i+1 mod 5]);
      	    EAT;
      	    PUTDOWN(CHOPSTICK[i], CHOPSTICK[i+1 mod 5])
       }   

 ```

When we are solving the Dining Philosopher Problem in distributed system, things get little complicated because we have to take into consideration the  network and the issues with network communication. Since there is no shared memory, message passing is the only way to communicate between forks, philosophers and monitors and DisplayManager

Requirement
1. python 2.6 or greater
2. Any Unix or Windows system

## HOW TO RUN THE PROGRAM
1. At first, change the name of host computer on which you will run the monitor in ```values.py``` file under the variable name of **MONITOR_IP**

   ```	MONITOR_IP = socket.gethostbyname("sigma27")```

2.	And then, run monitor.py in one computer

    ```	$ python monitor.py```

3.	After you do that, run mfork.py in five different machines

    ```	$ python mfork.py```

4.	Once all forks are running, run the displayManager.py in another machine or you can choose the same machine that is running monitor

    ```	$ python displayManager.py```

5.	Once displayManger is active, run mphilospher.py in another machine

    ```	$ python mphilosopher.py```

Connection in the system

![IMAGE](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1" )

Fig  :  Block diagram showing all UDP and TCP connection in the system

## Modules
There are 5 main modules in our program
1.	Values
2.	Forks
3.	Philosopher
4.	Monitor
5.	DisplayManager

	
**_Values_**

This module contains all the main variables and constants that are used in the program, values like display format, monitors ip and port, timer etc.


**_Forks_**

This module is responsible to create fork. This will create separate processes to run forks in background. This module will also register forks to monitor and communicate with philosopher. Communication with monitor is through UDP and communication with philosophers in through TCP.

**_Philosopher_**

This module is responsible to create philosopher and communicate with forks with TCP connection.. Each philosopher will send its status (thinking, waiting, eating) to the DisplayManager with UDP communication.

 ![IMAGE](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")
 
 Fig : Block diagram showing the request response message and connection type between different processes

**_Monitor_**

This module will keep track of all the forks running in different machines. When philosopher want to know the address and port of forks, it will send a message to monitor through UDP and monitor will send a list of registered forks. Monitor is also responsible to send a kill signal to all the forks after certain timeout period.

**_DisplayManager_**

This module is responsible to Display the states of philosopher. Each Philosopher will sent its status in a random interval of time to the DisplayManager through UDP. 
	
Program Flow
1.	The modules , values, stores the ip and port of the monitor. The IP address of monitor is get by doing **socket.gethostbyname()** function. 
At first we run Monitor in one machine. It will serve as a UDP server and start accepting connection. It will serve to forks and philosophers. The monitor will keep running in background throughout the program life cycle

2.	After running Monitor, we need to run forks in N different machines. When fork.py is run, it will create a socket to communicate with Monitor in same port and IP.  The fork will then send its ip and port to the monitor, which on receiving by monitor is stored in a list. You can run as many client forks as you like in different machines, the monitor will keep track of all. On running the fork module, it will create child processes for each fork. As the forks are added to monitors list, the monitor will run a timer in a separate thread. The function of the timer is to send a kill signal to the forks after "timer" duration of time. The forks will terminate all their background processes on receiving the kill signal sent by Monitor. It's like an hourglass.Monitor also serves philosophers on providing the forks details. When philosopher process first runs, it will send a request to  monitor to get the list of registered forks. After getting the fork detail, it will establish TCP connection with fork and then start   sending and receiving messages to and from the nearest two forks.

    ![IMAGE](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")
    
    Fig : UDP client server communication where Monitor is server and fork/philosopher are clients

3.	All forks are initially clean. So at first each fork can be grabbed by any philosopher. After the forks are created, it just waits for the philosopher to send message. 

4.	After philosopher are created, each philosopher will find its nearest two forks. This is done with the help of fork id. The fork id is the index of the fork that was maintained by the monitor. Each philosopher will have access to its nearest two forks. Philosopher 'n' will have access to fork 'n-1' and n. For example philosopher 5 will have access to fork 4 and fork 5. 
	At first all philosophers will pick the n-1 th fork. After that it will try to access nth fork. 
If the second fork is not available , it will put down the first fork, wait for a random time and try again. This works because the wait time of different philosopher are not same. So if a philosopher puts down fork and waits 3 second, other philosopher might just wait two second and grab the clean fork before the first philosopher grabs it. The first and second forks are swapped in when the philosopher cannot access any of the fork, so that in next iteration it will try to pick up the second fork first.
Throughout the program, the philosopher can be in any of the following three states:
     - When the philosopher has no fork in its any hand, it is in *THINKING* state.
     - When the philosopher has 1 fork in iots hand and waiting for another fork, it is in *WAITING* state
     - When the philosopher has both fork in its hands, it is in *EATING* state.

    When philosophe gets both fork1 and fork2, it will start eating for a random duration of time and then clean the fork and put it down.Philosopher will know if the fork is dirty or clean by sending it a message and checking the response.

5.   When philosopher requests pick up or drop a fork, it will send a message to fork. The fork will check the message to see it is for the pick request or drop request.
     - If it is for pick request, it reads the status if it is currently dirty or clean. If dirty , it replies with a message which contains the flag 'pickup_fail' and the id of philosopher which is currently using it.

     - If it is a drop request, it change the status from dirty to clean and sets fork_user to None. and sends the response to philosopher which contains the message 'drop_success'

6.	After program runs for 90 seconds, all background processes are terminated. Monitor will send kill signal to all forks simultaneously to let them know that time is over. The philosophers and DisplayManager have their own timers so they all will terminate.

 ![IMAGE](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")
 
Fig: Message passing between monitor and fork and philosopher and monitor


Program Output:

