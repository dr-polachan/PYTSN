import simpy


class packet(object):
    """ A class that represents a packet.

        Parameters
        ----------
        time : float
            the time the packet is created
        size : float
            the packet size in bytes
        id : int
            packet ID
        src, dst : int
            source and destination terminal ID's
        flow_id : int
            stream ID
    """
    def __init__(self, time=None, size=None, id=None, src=None, dst=None, flow_id=-1,\
    priority=None, type=None, data=None):
        
        self.time = time 
        self.id = id 
        self.flow_id = flow_id
        self.priority = priority
        self.src = src
        self.dst = dst
        self.size = size # bytes
        self.type = type
        self.data = data

    def __repr__(self):
        return "flow: {}, msg: {}, prio: {}, snd-time: {},  size(B): {}, src: {}, dst: {}, type: {}".\
            format(self.flow_id, self.id, self.priority, self.time, self.size, self.src, self.dst, self.type)

