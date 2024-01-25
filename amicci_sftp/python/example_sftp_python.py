#
# AUTHOR: Marcus Siqueira
# This PHP example send the data via post request to one of the APIs avaiable by Amicci. 
# It's a generic code, and simulates a large number of data to be sent.
# It iterated over a bunch of data and sent a maximum number of data each time. 
# The number of the requests to the API will depend on the ammount of data, because it's not fully sent at once, but in parts.
# 
# Requirements:
#   - Python 3.9.2 or later
#       - paramiko 3.3.1 
import paramiko

#Enable if you want log transaction
#paramiko_log = "paramiko.log"
#paramiko.util.log_to_file("paramiko_log")

#Must only use hostname and not http or https
host = "hostname"
#SFTP username
username = "sftp-user"
#The private key file path, either use full file path or the file name is the file in the same folder of that script
private_key_file_path = 'sftp_rsa'
#port, by default use 22 (default SFTP port)
port = 22

#local file path, either use full file path or the file name is the file in the same folder of that script
local_file_path = 'file.txt'

#remote file path, either use full file path or the file name is the file in the same folder of that script
remote_file_path = 'file.txt'

#if the key pair was generated in other format than RSAKey, that line must use another lib like DSSKey for example
private_key = paramiko.RSAKey.from_private_key_file(private_key_file_path)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#Try/Catch, if connection fails, an exception will be raised
try:
    #Open SFTP Connection using paramiko SSHClient
    ssh.connect(hostname=host, port=port, username=username, pkey=private_key)
    sftp = ssh.open_sftp()
    #Execute a Put command that will upload a local file to a remote path in SFTP
    files = sftp.put(local_file_path, remote_file_path)
    #Closes SFTP and Connection
    sftp.close()
    ssh.close()
except Exception as e:
    print(e, ' - Exception Raised!')