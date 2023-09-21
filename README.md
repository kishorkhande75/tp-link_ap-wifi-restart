## Automated WiFi Device Restart Script
This repository contains a Python script for automating the restart of WiFi devices by executing remote commands via SSH. The script is designed to clear the ARP cache of WiFi devices for maintenance purposes.

# Prerequisites
Before using this script, make sure you have the following prerequisites in place:

**.** Python installed on your system.
**.** The <code>subprocess</code>, <code>smtplib</code>, and <code>email</code> modules, which are used for executing commands and sending email notifications.
**.** **Plink** (PuTTY Link) installed on your system. Plink is used for SSH connections.
**.** Access to the target WiFi devices with SSH credentials.

# Configuration
Before running the script, you need to configure the following variables in the script:

**.**  <code>recipient_email</code>: The email address where you want to receive notifications about the script's execution.
**.**  <code>smtp_user</code>: Your SMTP email address.
**.**  <code>smtp_password</code>: Your SMTP email password.
**.**  <code>smtp_wifi</code>: The SMTP server address for your email service provider (e.g., smtp.gmail.com for Gmail).
**.**  <code>smtp_port</code>: The SMTP server port (587 is the default for most providers).
**.**  <code>sender_email</code>: The email address from which you want to send notifications.
Next, define the list of WiFi devices you want to restart. For each device, provide the following information:

**.**  <code> wifi_ip: The IP address of the WiFi device.
**.**  <code> ssh_user: The SSH username for connecting to the WiFi device.
**.**  <code> ssh_password: The SSH password for connecting to the WiFi device.
# Usage
1. Clone this repository to your local machine.
<code> git clone https://github.com/yourusername/automated-wifi-restart-script.git </code>
2.Navigate to the repository directory.
<code>cd automated-wifi-restart-script</code>
3. Open the <code>wifi_restart_script.py</code> file and configure the variables as described in the "Configuration" section above.

Run the script using the following command:
<code> python wifi_restart_script.py</code>

The script will execute the specified remote command (default: 'restart') on each WiFi device in the list. It will send email notifications for successful and failed executions.

## Email Notifications
The script will send email notifications to the specified recipient email address. Email subjects and messages are customized based on the execution status:

**Success**: Email subject will contain "IT-Alert: Automated script for restart WiFi devices [WiFi IP] Successful." The message will indicate that the script executed successfully.

**Failure**: Email subject will contain "IT-Alert: Automated script for restart WiFi devices [WiFi IP] Failed." The message will indicate that the script failed to execute.

## Note
This script uses Plink to execute remote commands via SSH. Ensure that Plink is correctly installed and available in your system's PATH.
Make sure to secure your SMTP email credentials and do not share them publicly.
Customize the email message and subject templates to fit your organization's needs.

**Disclaimer**: This script is provided as-is and should be used with caution. Ensure that you have proper authorization and backup measures in place before executing remote commands on WiFi devices.