# **CAN Bus Log Parser**

A Python tool that parses .asc log files, decodes CAN signals, and generates automated pass/fail validation reports.









**Signals supported:**



|**Message ID**|**Signal**|**Formula**|**Unit**|**Limit**|
|-|-|-|-|-|
|0x0C8|Engine Speed|byte0 × 30|RPM|6000|
|0x0A0|Vehicle Speed|byte0 × 1|km/h|200|
|0x1B0|Engine Temp|byte0 - 40|°C|120|





**What it does:**



* Reads a .asc log file
* Extracts timestamp, message ID, and payload bytes from each CAN frame
* Decodes raw hex bytes into real engineering values (RPM, km/h, °C)
* Validates values against safe thresholds
* Generates a pass/fail report in the terminal and saves it to report.txt





**Example Output:**



CAN Bus Validation Report

\----------------------------------------

FAIL | Engine Speed: 7200 RPM

PASS | Vehicle Speed: 0 km/h

FAIL | Engine Speed: 7200 RPM

PASS | Vehicle Speed: 16 km/h

\----------------------------------------

Total: 4 checked | 2 PASS | 2 FAIL



