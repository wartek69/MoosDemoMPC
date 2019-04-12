#!/usr/bin/python3
from pymoos import pymoos
from scipy.interpolate import CubicSpline
import time
import threading


class mpcMOOS(pymoos.comms):
    def __init__(self, moos_community, moos_port):
        """Initiates MOOSComms, sets the callbacks and runs the loop"""
        super(mpcMOOS, self).__init__()
        self.server = moos_community
        self.port = moos_port
        self.name = 'mpcMOOS'

        self.lock = threading.Lock()

        self.set_on_connect_callback(self.__on_connect)
        self.set_on_mail_callback(self.__on_new_mail)

        self.add_active_queue('path_queue', self.on_path)
        self.add_message_route_to_active_queue('path_queue', 'PATH_X')
        self.add_message_route_to_active_queue('path_queue', 'PATH_Y')



        self.run(self.server, self.port, self.name)

    def __on_connect(self):
        """OnConnect callback"""
        print("Connected to", self.server, self.port,
              "under the name ", self.name)
        self.register('PATH_X', 0)
        self.register('PATH_Y', 0)
        return True

    def __on_new_mail(self):
        """OnNewMail callback"""

        print("on_mail activated by")

        return True


    def on_path(self, msg):
        """Special callback for path"""
        self.lock.acquire()
        try:
            # print("on_path activated by", msg.key(), "with value", msg.string())
            if msg.key() == 'PATH_X':
                # parse the path x coords
                self.path_x = msg.string().replace('[', '')
                self.path_x = self.path_x.replace(']', '')
                self.path_x = self.path_x.replace(' ', '')
                self.path_x = self.path_x.split(',')
                self.path_x = [float(i) for i in self.path_x]
                print('Received {} x coordinates'.format(len(self.path_x)))
            elif msg.key() == 'PATH_Y':
                # parse the path y coords
                self.path_y = msg.string().replace('[', '')
                self.path_y = self.path_y.replace(']', '')
                self.path_y = self.path_y.replace('array(', '')
                self.path_y = self.path_y.replace(')', '')
                self.path_y = self.path_y.replace(' ', '')
                self.path_y = self.path_y.split(',')
                self.path_y = [float(i) for i in self.path_y]
                print('Received {} y coordinates'.format(len(self.path_y)))
        finally:
            self.lock.release()
        return True

def main():
    pinger = mpcMOOS('localhost', 9000)
    while True:
        time.sleep(1)
        print('sleeping')


if __name__ == "__main__":
    main()
