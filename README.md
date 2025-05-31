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

```bash
sudo apt update && sudo apt install lm-sensors sendmail curl python3-pip
pip install psutil
