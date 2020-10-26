# san_socket

# Overview

This package pretends to be a bridge between ROS and Sensor Agent Node. The SAN module is a code
running on a docker container and it communicates to OPIL Server. Initially this mode is configured
to work like a button. On the ROS side, a socket is opened to talk to the docker container. It creates
a service that triggers SAN module. In this way SAN can send a signal to OPIL server.

# Instructions 

1. Launch the opil server. Check the ip address.

```
$ sudo docker-compose up
```

2. Configure san socket. In the follow directory set the ip address of the opil server

```
$ san_socket/docker/config.json
```

Change ```ip-address``` by your opil server address. Note that quotes are required.

```
{
    "contextBroker": {
        "host": "ip-address",
        "port": "1026"
    ...
...   
```

Then, start docker container in ```san_socket/docker/docker-compose.yml```

```
$ sudo docker-compose up
```

3. Launch ROS client for SAN module comunication

```
$ roslaunch san_socket client.launch 
```

4. Send a signal from ROS to OPIL server using SAN module. This package creates a ROS
service called ```san_socket/trigger ```. Use it to send a flag to OPIL Server.

```
$ rosservice call /san_socket/trigger "{}"
```
