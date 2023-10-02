Ping And Traceroute:
-------------------
This is a Python-based tool that helps to ping and trace hops from source to destination.

Prerequisites:
---------------
1. Python version 3.10 or higher

Setup in Pycharm:
-----------------
1. Open Pycharm and navigate to the main page.
2. Click on "Open" and import the unzipped project.
3. Open Ping.java, which contains the main class.
4. Go to "Run" -> "Edit Configurations" -> Select Main class as ping.py or trace_route.py .
5. In "Parameters", add the arguments
6. Execute the program

Ping.py arguments
----------------
1. -h : prints help message with options
2. -s 100 : sends packet of size 100 bytes
3. -c 10:  10 packets should be sent
4. -i 2 :  wait for 2 seconds between successive pings
5.  -t 4 :  timeout in 4 seconds aCer which program terminates

Trace_route.py arguments
------------------------

1. -h : prints help message with options
2. -n : print numerical ip addresses
3. -q 4 : 4 probes will be done per ttl
4. -S : includes a summary of failed probes per ttl

By default 30 hops were included in the trace_route.py , we can change it according to our needs.