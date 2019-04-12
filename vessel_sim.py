#!/usr/bin/python3
from pymoos import pymoos
import time
import math

secondsPerMin = 60


class Vessel(pymoos.comms):
    # x and y in meters!
    # speed m/s
    # rot_change in degree/s/s
    def __init__(self, x, y, rot, heading, speed, rot_change, rot_max, rot_min):
        self.x = x
        self.y = y
        self.rot = rot
        self.heading = heading
        self.speed = speed
        self.rot_change = rot_change
        self.rot_max = rot_max
        self.rot_min = rot_min

    def __clamp(self, rot):
        if rot > self.rot_max:
            return self.rot_max
        elif rot < self.rot_min:
            return self.rot_min
        else:
            return rot

    def simulate(self, rrot, delta_t = 1):
        rrot = self.__clamp(rrot)
        self.x = self.x + math.sin(self.heading / 180 * math.pi) * self.speed * delta_t
        self.y = self.y + math.cos(self.heading / 180 * math.pi) * self.speed * delta_t
        self.heading = (self.heading + self.rot / secondsPerMin * delta_t) % 360
        if self.rot < rrot:
            self.rot = self.rot + self.rot_change * delta_t
            if self.rot > rrot:
                self.rot = rrot
        elif self.rot > rrot:
            self.rot = self.rot - self.rot_change * delta_t
            if self.rot < rrot:
                self.rot = rrot
        else:
            self.rot = self.rot

class MoosPub(pymoos.comms):
    def __init__(self, moos_community, moos_port):
        """Initiates MOOSComms, sets the callbacks and runs the loop"""
        super(MoosPub, self).__init__()
        self.server = moos_community
        self.port = moos_port
        self.name = 'MoosPub'

        self.set_on_connect_callback(self.__on_connect)
        self.run(self.server, self.port, self.name)

    def __on_connect(self):
        """OnConnect callback"""
        print("Connected to", self.server, self.port,
              "under the name ", self.name)
        return True



def main():
    vessel = Vessel(0, -20, 0, 180, 1, 0.1, 180, -180)
    pinger = MoosPub('localhost', 9000)

    while True:
        time.sleep(0.1)
        vessel.simulate(0)
        pinger.notify('NAV_X', vessel.x, -1);
        pinger.notify('NAV_Y', vessel.y, -1);
        pinger.notify('NAV_SPEED', vessel.speed, -1);

        pinger.notify('NAV_HEADING', vessel.heading, -1);

if __name__ == "__main__":
    main()
