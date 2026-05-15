class CANparser:
    def __init__(self, filename):
        self.filename = filename
        self.results = []
        self.pass_count = 0
        self.fail_count = 0 

    def read_asc_file(self):
        lines = []
        with open(self.filepath,'r') as f:
            for line in f: # for item in collection
                lines.append(line.strip()) # remove \n from a line
        return lines    

    def parse_line(self, line):
        parts = line.split()
        timestamp = parts[0]
        msg_id = parts[2]
        data_bytes = parts[6:]
        return timestamp, msg_id, data_bytes # extracted timestamp, message ID and

    def decode_signal(self,msg_id,data_bytes): 
        byte0 = int(data_bytes[0],16)
        # dictionary for IDs taken from data that mean something 
        signals = {
            "0C8": ("Engine Speed", byte0 * 30, "RPM"),
            "0A0": ("Vehicle Speed", byte0 * 1, "km/h"),
            "1B0": ("Engine Temp", byte0 - 40, "C")
    }
        if msg_id in signals:
            name,value,unit = signals[msg_id]
            return name,value,unit
        return None,None,None

    