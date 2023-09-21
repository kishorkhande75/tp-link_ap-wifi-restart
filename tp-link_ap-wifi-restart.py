import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time  # Import the time module

# Email Configuration
recipient_email = "YOUR_EMAIL_ID"
smtp_user = "YOUR_EMAIL_ID"
smtp_password = "YOUR_EMAIL_PASSWORD"
smtp_wifi = "smtp.gmail.com"
smtp_port = 587
sender_email = "YOUR_EMAIL_ID"

# Define the list of wifis
wifis = [
    {'wifi_ip': '192.168.1.1', 'ssh_user': 'USER_NAME', 'ssh_password': 'YOUR_DEVICE_PASSWORD'},
    {'wifi_ip': '192.168.1.2', 'ssh_user': 'USER_NAME', 'ssh_password': 'YOUR_DEVICE_PASSWORD'}
]

# Function to remove SSH keys from the Windows Registry
def remove_ssh_keys_from_registry():
    try:
        # Specify the names of the SSH keys to remove from the registry
        ssh_key_names = ["rsa2@192.168.1.1", "rsa2@22:192.168.1.2"]  # Replace with actual key names
        
        for key_name in ssh_key_names:
            # Use the 'reg delete' command to remove the SSH key from the Windows Registry
            command = f'reg delete "HKEY_CURRENT_USER\\Software\\SimonTatham\\PuTTY\\SshHostKeys" /v "{key_name}" /f'
            subprocess.run(command, shell=True, check=True)
        
        print("SSH keys removed from the Windows Registry.")
    except Exception as e:
        print(f"An error occurred while removing SSH keys: {str(e)}")

# Call the function to remove SSH keys before executing Plink command
remove_ssh_keys_from_registry()

# Function to send an email
def send_email(subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        wifi = smtplib.SMTP(smtp_wifi, smtp_port)
        wifi.starttls()
        wifi.login(smtp_user, smtp_password)
        wifi.sendmail(sender_email, recipient_email, message.as_string())
        wifi.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Email could not be sent. Error: {str(e)}")

# Define the remote command to execute
remote_command = 'restart'

# Iterate through the list of wifis and execute the Plink command for each
for wifi in wifis:
    wifi_ip = wifi['wifi_ip']
    ssh_user = wifi['ssh_user']
    ssh_password = wifi['ssh_password']
    
    # Construct the Plink command with "y" piped as input
    plink_command = f'echo y | plink -pw {ssh_password} {ssh_user}@{wifi_ip} "{remote_command}"'

    try:
        # Execute the Plink command asynchronously
        process = subprocess.Popen(plink_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait for a few seconds to allow time for the "y" response to be sent
        time.sleep(5)
        
        # Check if the process is still running
        if process.poll() is None:
            # Process is still running, which means it was able to continue after the "y" response
            print(f"Remote command execution continued for restart WiFi devices {wifi_ip} after adding host key to cache.")
            success_subject = f"IT-Alert: Automated script for restart WiFi devices {wifi_ip} Successful"
            success_message = f"Hi Team,\n \nPlease note, Automated script executed successfully to reboot the following WiFi devices:-\n \n 1. Conference \n 2. Support\n \nPurpose of this script: To clear the APR cache.\n \n--\nBest Regards,\nKishor Khande.\n------------------------------------------------------------------------------------------------------\n This is a system generated alert. We request you not reply to this message. \n------------------------------------------------------------------------------------------------------"
            send_email(success_subject, success_message)
        else:
            # Process has terminated, check the exit status
            if process.returncode == 0:
                print(f"Remote command executed successfully for restart wifi devices {wifi_ip}.")
                success_subject = f"IT-Alert: Automated script for restart WiFi devices {wifi_ip} Successful"
                success_message = f"Hi Team,\n \nPlease note, Automated script executed successfully to reboot the following WiFi devices:-\n \n 1. Conference \n 2. Support\n \nPurpose of this script: To clear the APR cache.\n \n--\nBest Regards,\nKishor Khande.\n------------------------------------------------------------------------------------------------------\n This is a system generated alert. We request you not reply to this message. \n------------------------------------------------------------------------------------------------------"
                send_email(success_subject, success_message)
            else:
                print(f"Error executing remote command for wifi device {wifi_ip}: {process.stderr}")
                error_subject = f"IT-Alert: Automated script for restart WiFi devices {wifi_ip} Failed"
                error_message = f"Hi Team,\n \nPlease note, Automated script executed failed to reboot the following WiFi devices:-\n \n 1. Conference \n 2. Support \n \n--\nBest Regards,\nKishor Khande.\n------------------------------------------------------------------------------------------------------\n This is a system generated alert. We request you not reply to this message. \n------------------------------------------------------------------------------------------------------"
                send_email(error_subject, error_message)
            
    except Exception as e:
        print(f"An error occurred for wifi device {wifi_ip}: {str(e)}")

