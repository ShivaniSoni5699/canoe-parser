class CANparser:
    def __init__(self, filename):
        self.filename = filename
        self.results = []
        self.pass_count = 0
        self.fail_count = 0 

    def read_asc_file(self):
        lines = []
        with open(self.filename,'r') as f:
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

   # show pass fail validation
    def validate(self,name,value):
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

    def run(self):
        lines = self.read_asc_file()
        for line in lines:
            timestamp, msg_id, data_bytes = self.parse_line(line)
            name, value, unit = self.decode_signal(msg_id, data_bytes)
            if name is not None:
                result = self.validate(name, value)
                self.results.append((name, value, unit, result))
                if result == "PASS":
                    self.pass_count += 1
                else:
                    self.fail_count += 1
        self.generate_html_report()
    
    def generate_html_report(self):
        with open("reports/report.html", "w") as f:
            f.write("""
<html>
<head>
<style>
    body { font-family: Arial; padding: 20px; }
    table { border-collapse: collapse; width: 100%; }
    th { background: #333; color: white; padding: 8px; }
    td { padding: 8px; border: 1px solid #ccc; }
    .PASS { background: #d4edda; }
    .FAIL { background: #f8d7da; }
</style>
</head>
<body>
<h2>CAN Bus Validation Report</h2>
""")
            f.write("<table><tr><th>Signal</th><th>Value</th><th>Unit</th><th>Result</th></tr>")
            for name, value, unit, result in self.results:
                f.write(f'<tr class="{result}"><td>{name}</td><td>{value}</td><td>{unit}</td><td>{result}</td></tr>')
            f.write("</table>")
            f.write(f"<p>Total: {self.pass_count + self.fail_count} | {self.pass_count} PASS | {self.fail_count} FAIL</p>")
            f.write("</body></html>")
        print("Report saved: report.html")

parser = CANparser("can_log.asc")
parser.run()