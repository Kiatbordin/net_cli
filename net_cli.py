import paramiko
from datetime import datetime

def run_cli_command(hostname, username, password, command):
    # Create SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the device
        client.connect(hostname, username=username, password=password)

        # Execute the command
        stdin, stdout, stderr = client.exec_command(command)

        # Read the output
        output = stdout.read().decode()

        # Generate the output filename
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_filename = f"{hostname}_{current_datetime}.txt"

        # Write the output to the file
        with open(output_filename, 'w') as file:
            file.write(output)

        print(f"Output saved to file: {output_filename}")

    except paramiko.AuthenticationException:
        print(f"Authentication failed for {hostname}. Please check the credentials.")
    except paramiko.SSHException as e:
        print(f"SSH connection failed: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the SSH connection
        client.close()

# Read the hosts file and store the hostnames in an array
hosts_file = 'hosts.txt'
with open(hosts_file, 'r') as file:
    hostnames = file.read().splitlines()

# Read the credentials file
credentials_file = 'credentials.txt'
with open(credentials_file, 'r') as file:
    credentials = file.read().splitlines()

# Extract the username and password from credentials
username = credentials[0]
password = credentials[1]

# Set the common command for all hosts
command = 'show version'

# Iterate over each hostname and run the CLI command
for hostname in hostnames:
    print(f"Running command on {hostname}:")
    run_cli_command(hostname, username, password, command)
    print('-' * 50)
