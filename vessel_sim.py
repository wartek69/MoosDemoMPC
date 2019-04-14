#!/usr/bin/python3
from pymoos import pymoos
import time
import math
import threading


secondsPerMin = 60


class Vessel():
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

class VesselMoosPub(pymoos.comms):
    def __init__(self, moos_community, moos_port):
        """Initiates MOOSComms, sets the callbacks and runs the loop"""
        self.vessel = Vessel(-500, -1600, 0, 0, 1, 0.1, 180, -180)
        super(VesselMoosPub, self).__init__()
        self.server = moos_community
        self.port = moos_port
        self.name = 'VesselMoosPub'

        self.lock = threading.Lock()
        self.add_active_queue('rrot_queue', self.__on_vessel_rrot)
        self.add_message_route_to_active_queue('rrot_queue', 'RROT')

        self.set_on_connect_callback(self.__on_connect)
        self.run(self.server, self.port, self.name)

    def __on_connect(self):
        """OnConnect callback"""
        print("Connected to", self.server, self.port,
              "under the name ", self.name)
        self.register('RROT', 0)


        return True

    def __on_vessel_rrot(self, msg):
        self.lock.acquire()
        print('new control action received')
        try:
            if msg.key() == 'RROT':
                self.vessel.simulate(msg.double())
                states = '{},{},{},{},{}'.format(self.vessel.x,
                                                 self.vessel.y,
                                                 self.vessel.speed,
                                                 self.vessel.heading,
                                                 self.vessel.rot)
                self.notify('VESSEL_STATE', states, -1)
        finally:
            self.lock.release()
        return True



def main():
    time.sleep(1)
    vesselMoos = VesselMoosPub('localhost', 9000)
    # all the states in one message to make sure everything arrives at the mpc
    states = '{},{},{},{},{}'.format(vesselMoos.vessel.x,
                                     vesselMoos.vessel.y,
                                     vesselMoos.vessel.speed,
                                     vesselMoos.vessel.heading,
                                     vesselMoos.vessel.rot)
    time.sleep(1)
    print('notifying...')
    vesselMoos.notify('VESSEL_STATE', states, -1);

    while True:
        time.sleep(0.01)
        vesselMoos.lock.acquire()
        try:
            vesselMoos.notify('NAV_X', vesselMoos.vessel.x, -1);
            vesselMoos.notify('NAV_Y', vesselMoos.vessel.y, -1);
            vesselMoos.notify('NAV_SPEED', vesselMoos.vessel.speed, -1);
            vesselMoos.notify('NAV_HEADING', vesselMoos.vessel.heading, -1);
            # depth used in marine viewer to check the rot
            vesselMoos.notify('NAV_DEPTH', vesselMoos.vessel.rot, -1);
        finally:
            vesselMoos.lock.release()







if __name__ == "__main__":
    main()
