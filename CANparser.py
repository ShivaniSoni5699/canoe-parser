def read_asc_file(filepath):
    lines = []
    with open(filepath,'r') as f:
        for line in f:
            lines.append(line.strip()) # remove \n from a line
    return lines
    
def parse_line(line):
    parts = line.split()
    timestamp = parts[0]
    msg_id = parts[2]
    data_bytes = parts[6:]
    return timestamp, msg_id, data_bytes # extracted timestamp, message ID and data bytes from CAN frame 

def decode_signal(msg_id,data_bytes): 
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


def validate(name,value,unit):
    limits = {
        "Engine Speed": 6000,
        "Vehicle Speed": 200,
        "Engine Temp": 120
    }
    if name in limits:
        if value > limits[name]:
            return "FAIL"
        else:
            return "PASS"
    return "UNKNOWN"

def generate_report(results):
    print("-" * 40)
    pass_count = 0
    fail_count = 0
    for name, value, unit, result in results:
        if result == "PASS":
            pass_count += 1
        else:
            fail_count += 1
        print(f"{result} | {name}: {value} {unit}")
    print("-" * 40)
    print(f"Total: {pass_count + fail_count} checked | {pass_count} PASS | {fail_count} FAIL")

    with open("report.txt", "w") as f:
        f.write("CAN Bus Validation Report\n")
        f.write("-" * 40 + "\n")
        for name, value, unit, result in results:
            f.write(f"{result} | {name}: {value} {unit}\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total: {pass_count + fail_count} checked | {pass_count} PASS | {fail_count} FAIL\n")

lines = read_asc_file("can_log.asc")

results = []

for line in lines:
    timestamp, msg_id, data_bytes = parse_line(line)
    name, value, unit = decode_signal(msg_id, data_bytes)
    if name is not None:
        result = validate(name, value, unit)
        results.append((name, value, unit, result))

generate_report(results)