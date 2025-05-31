#!/usr/bin/env python3
import os
import time
import psutil
import subprocess
import smtplib
import signal
from email.mime.text import MIMEText
import sys

PID_FILE = "/tmp/lms_monitor.pid"
CHECK_INTERVAL = 5  # seconds

# Alert configuration (customize as needed)
EMAIL_TO = "windowsorgy@gmail.com"
SMS_TO = "+17205893383@tmomail.com"
EMAIL_FROM = "yourserver@example.com"  # Change to an appropriate sender

# Global threshold variables (set via user input)
PAUSE_TEMP = None
RESUME_TEMP = None

def signal_handler(sig, frame):
    print("\nSignal received, terminating monitoring...\n")
    resume_processes()  # try to resume any processes
    try:
        os.remove(PID_FILE)
    except Exception as e:
        print("Error removing PID file:", e, "\n")
    sys.exit(0)

# Attach interruption signals
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

def get_cpu_temp():
    """
    Reads the CPU temperature using lm-sensors.
    It searches for a line containing "Core" and extracts the value.
    """
    try:
        result = subprocess.run(["sensors"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "Core" in line:
                try:
                    # Expected format: "Core 0:       +45.0°C ..."
                    temp_str = line.split("+")[1].split("°")[0]
                    temp = float(temp_str)
                    return temp
                except Exception as e:
                    print("Error parsing temperature:", e, "\n")
    except Exception as e:
        print("Error running sensors command:", e, "\n")
    return None

def freeze_processes():
    """
    Suspends non-kernel processes by sending them the STOP signal.
    Adjust the list of critical processes as needed.
    """
    paused = []
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            # Exclude processes that are considered critical (customize as needed)
            if proc.info["name"] not in ["systemd", "init", "bash"]:
                os.system(f"kill -STOP {proc.info['pid']}")
                paused.append(f"{proc.info['name']} (PID {proc.info['pid']})")
        except Exception as e:
            print("Error freezing process", proc.info["name"], ":", e, "\n")
    print("Processes frozen:\n" + "\n".join(paused) + "\n")
    return paused

def resume_processes():
    """
    Resumes the processes by sending them the CONT signal.
    """
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            os.system(f"kill -CONT {proc.info['pid']}")
        except Exception as e:
            print("Error resuming process", proc.info["name"], ":", e, "\n")
    print("Resumed processes\n")

def send_alert(paused_programs):
    """
    Sends an email and an SMS alert containing details of the paused programs.
    """
    message = "CPU Overheated!\nPaused programs:\n" + "\n".join(paused_programs)
    
    # Send email alert
    msg = MIMEText(message)
    msg["Subject"] = "CPU Overheat Warning"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        smtp = smtplib.SMTP("localhost")
        smtp.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        smtp.quit()
        print("Sent email alert\n")
    except Exception as e:
        print("Email error:", e, "\n")

    # Send SMS alert using sendmail (this leverages the carrier's email-to-SMS gateway)
    try:
        os.system(f'echo "{message}" | sendmail {SMS_TO}')
        print("Sent SMS alert\n")
    except Exception as e:
        print("SMS error:", e, "\n")

def main():
    global PAUSE_TEMP, RESUME_TEMP

    # Ask user for threshold temperatures.
    try:
        PAUSE_TEMP = float(input("Whats the temp you want non-kernal programs to pause? "))
        RESUME_TEMP = float(input("Whats the temp you want non kernal programs to resume at? "))
    except Exception as e:
        print("Invalid input. Exiting.")
        sys.exit(1)

    print("\nMonitoring starting with pause threshold:", PAUSE_TEMP, "°C and resume threshold:", RESUME_TEMP, "°C\n")

    # Write our PID to the PID file so that we can stop the process later.
    try:
        with open(PID_FILE, "w") as f:
            f.write(str(os.getpid()))
    except Exception as e:
        print("Error writing PID file:", e, "\n")

    while True:
        temp = get_cpu_temp()
        if temp is None:
            print("Could not read temperature, retrying...\n")
        else:
            print(f"Current CPU Temp: {temp:.1f}°C\n")
            if temp > PAUSE_TEMP:
                print("Temperature exceeded pause threshold. Freezing processes...\n")
                paused_programs = freeze_processes()
                send_alert(paused_programs)
                while True:
                    temp = get_cpu_temp()
                    if temp is not None:
                        print(f"Waiting... CPU Temp: {temp:.1f}°C\n")
                        if temp < RESUME_TEMP:
                            break
                    time.sleep(CHECK_INTERVAL)
                resume_processes()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
