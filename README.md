# **CPU Temperature Monitor for Ubuntu Server**
This script monitors CPU temperatures using `lm-sensors` and suspends non-kernel processes when a specified temperature threshold is exceeded. Processes are resumed when the temperature drops below the resume threshold. **Email and SMS alerts** are sent when overheating occurs.

## **Features**
- **Temperature-based process control** (pauses non-kernel processes when overheating, resumes them afterward).
- **Customizable temperature thresholds** (set at startup).
- **Email and SMS alerts** when overheating occurs.
- **Start & stop commands** (`lms-start` and `lms-stop`).
- **Easy customization** for email & SMS notifications.

---

## **Installation Guide**

### **Step 1: Install Dependencies**
Run the following commands to install required packages:


sudo apt update && sudo apt install lm-sensors sendmail curl python3-pip
pip install psutil
Step 2: Enable lm-sensors
bash
sudo sensors-detect
Follow the prompts to detect CPU temperature sensors.

Step 3: Download the Script
Clone this repository and copy lms_monitor.py to the /usr/local/bin/ directory:

``bash
git clone https://github.com/YOUR_GITHUB_REPO_NAME.git
cd YOUR_GITHUB_REPO_NAME
sudo cp lms_monitor.py /usr/local/bin/lms_monitor.py
sudo chmod +x /usr/local/bin/lms_monitor.py``
Step 4: Create the Start Command
Make a simple command called lms-start to launch the monitor:

``bash
echo -e '#!/bin/bash\n/usr/bin/env python3 /usr/local/bin/lms_monitor.py' | sudo tee /usr/local/bin/lms-start
sudo chmod +x /usr/local/bin/lms-start``
Step 5: Create the Stop Command
Make a command called lms-stop to stop the monitor:

``bash
echo -e '#!/bin/bash\nif [ -f /tmp/lms_monitor.pid ]; then\n  PID=$(cat /tmp/lms_monitor.pid)\n  echo "Stopping lms_monitor process with PID $PID"\n  kill $PID\n  sleep 2\n  rm -f /tmp/lms_monitor.pid\nelse\n  echo "lms_monitor is not running."\nfi' | sudo tee /usr/local/bin/lms-stop
sudo chmod +x /usr/local/bin/lms-stop``
Customization Guide
Changing Email and SMS Recipient
Edit the following variables in lms_monitor.py:

``python
EMAIL_TO = "your_email@example.com"  # Change this to your alert email
SMS_TO = "your_phone_number@carrier_email.com"  # Change this to your SMS gateway address
EMAIL_FROM = "yourserver@example.com"  # Sender email (modify if necessary)``
Where do I find my SMS-to-email address? Each carrier has an SMS-to-email gateway that lets you send text messages via email. Use the format:

``plaintext
[YourPhoneNumber]@[CarrierEmailDomain]``
Here are common gateways for major U.S. carriers:

Carrier	SMS-to-Email Address Format
AT&T	{YourPhoneNumber}@txt.att.net
Verizon	{YourPhoneNumber}@vtext.com
T-Mobile	{YourPhoneNumber}@tmomail.net
Sprint	{YourPhoneNumber}@messaging.sprintpcs.com
MetroPCS	{YourPhoneNumber}@mymetropcs.com
Boost Mobile	{YourPhoneNumber}@sms.myboostmobile.com
For other carriers, check their official documentation.

Usage
Starting the Monitor
Run:

``bash
lms-start``
You'll be prompted with two questions:

"Whats the temp you want non-kernal programs to pause?"

"Whats the temp you want non kernal programs to resume at?"

Stopping the Monitor
Run:

``bash
lms-stop``
Testing
To test:

Run lms-start with a low threshold (e.g., 10°C) so it triggers quickly.

Check that processes freeze (ps -eo pid,stat,comm | grep 'T').

Monitor log output for temperature readings.

Verify alerts via email & SMS.
