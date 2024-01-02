# Ping And Traceroute

This is a Python-based tool that helps to ping and trace hops from source to destination.

## Prerequisites

- Python version 3.10 or higher

## Setup in Pycharm

1. Open Pycharm and navigate to the main page.
2. Click on "Open" and import the unzipped project.
3. Open `Ping.py`, which contains the main class.
4. Go to "Run" -> "Edit Configurations" -> Select Main class as `ping.py` or `trace_route.py`.
5. In "Parameters," add the arguments.
6. Execute the program.

## Ping.py Arguments

1. **-h:** Prints a help message with options.
2. **-s 100:** Sends a packet of size 100 bytes.
3. **-c 10:** Sends 10 packets.
4. **-i 2:** Waits for 2 seconds between successive pings.
5. **-t 4:** Timeout in 4 seconds after which the program terminates.

## Trace_route.py Arguments

1. **-h:** Prints a help message with options.
2. **-n:** Print numerical IP addresses.
3. **-q 4:** Four probes will be done per TTL.
4. **-S:** Includes a summary of failed probes per TTL.

By default, 30 hops were included in the `trace_route.py`; you can change it according to your needs.
