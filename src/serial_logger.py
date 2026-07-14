# realtime detection
import datetime
import os
# sample data cause we use simulationn / test driven development
sample_data = [
    "1015,102,OK",
    "2015,25.00,TEMP",
    "3017,650,ALERT",
    "4015,30.00,TEMP",
    "WATCHDOG,0,FAULT",
    "5018,200,OK"
]

# function 
def process_line(line):
    parts = line.split(",")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if parts[2] == "FAULT" :
      print(f"FAULT detected at {timestamp}" )
      return f"{timestamp} | Watchdog fault\n "

    elif parts[2] == "ALERT" :
       print(f"ALERT at {timestamp} , value: {parts[1]} ")
       return f"{timestamp} | ALERT | value: {parts[1]}\n"

    elif parts[2] == "TEMP":
        return f"{timestamp} | TEMP | {parts[1]} C\n"
    
    else:
        return f"{timestamp} | SPEED | {parts[1]} | {parts[2]}\n"
    
def run_logger() :
   os.makedirs("reports_2", exist_ok = True)
   log_entries = []
   for line in sample_data:
      entry = process_line(line)
      log_entries.append(entry)

   with open("reports_2/serial_log.txt","w") as f:
      f.writelines(log_entries)
    
   print("\nLog saved : reports_2/serial_log.txt")


run_logger()