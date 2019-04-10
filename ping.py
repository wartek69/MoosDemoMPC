#!/usr/bin/python3
from pymoos import pymoos
import time

class pingMOOS(pymoos.comms):
    def __init__(self, moos_community, moos_port):
        """Initiates MOOSComms, sets the callbacks and runs the loop"""
        super(pingMOOS, self).__init__()
        self.server = moos_community
        self.port = moos_port
        self.name = 'pingMOOS'

        self.set_on_connect_callback(self.__on_connect)
        self.run(self.server, self.port, self.name)

    def __on_connect(self):
        """OnConnect callback"""
        print("Connected to", self.server, self.port,
              "under the name ", self.name)
        return True



def main():
    pinger = pingMOOS('localhost', 9000)

    while True:
        time.sleep(1)
        pinger.notify('DESIRED_THRUST', 50, -1);
        pinger.notify('DESIRED_RUDDER', -50, -1);

if __name__ == "__main__":
    main()
