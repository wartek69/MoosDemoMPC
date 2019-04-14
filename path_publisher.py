#!/usr/bin/python3
from pymoos import pymoos
from scipy.interpolate import CubicSpline
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
        self.register('PATH_X', 0)
        self.register('PATH_Y', 0)
        return True

def create_path_small(length):
    px = []
    py = []
    #x = [0, 500, 2000, 4000, 6000]
    #y = [-1500, -800, -1800, 2000, -500]
    x = [0, 20, 80, 100, 200]
    y = [-100, -80, -60, -80, -100]

    cs = CubicSpline(x, y)
    for k in range(length):
        px.append(k)
        py.append(cs(k))
    return px, py

def create_path(length):
    px = []
    py = []
    x = [0, 500, 2000, 4000, 6000]
    y = [-1500, -800, -1800, 2000, -500]
    cs = CubicSpline(x, y)
    for k in range(length):
        px.append(k)
        py.append(cs(k))
    return px, py


def main():
    pinger = pingMOOS('localhost', 9000)
    px, py = create_path(4001)
    time.sleep(1)
    pinger.notify('PATH_X', str(px), -1)
    pinger.notify('PATH_Y', str(py), -1)
    j = 0;
    while j < 20:
        time.sleep(1)

        j = j + 1
        for i in range(len(px)):
            coords = '{},{}'.format(px[i], py[i])
            pinger.notify('VIEW_POINT', coords, -1);

if __name__ == "__main__":
    main()
