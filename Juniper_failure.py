#!/usr/bin/env python

import paramiko
import time
from datetime import datetime
import datetime



def disable_paging(remote_conn):
    '''Disable paging on a Cisco router'''

    remote_conn.send("terminal length 0\n")
    time.sleep(2)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output



if __name__ == '__main__':
    
    now = datetime.datetime.now()
    mytoday = str(now.strftime("%Y-%m-%d_%H:%M"))
    print mytoday
    
    

    # VARIABLES THAT NEED TO BE CHANGED
    ip = raw_input('FQDN or IP of device:  ')
    username = raw_input('Username:  ')
    password = raw_input('Password:  ')

    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # initiate SSH connection
    remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
    print "SSH connection established to %s" % ip

    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    print "Interactive SSH session established"

    # Strip the initial router prompt
    output = remote_conn.recv(1000)

    # See what we have
    print output

    # Now let's try to send the router a command
    remote_conn.send("\n")
    remote_conn.send("file make-directory /var/tmp/tshoot_"+mytoday+ "\n")
    
    #Gather interface description info
    remote_conn.send("show interfaces descriptions | save /var/tmp/tshoot_"+mytoday+"/description.txt\n")
    time.sleep(1)
    
    #Gather PFE statistics
    remote_conn.send("show pfe statistics error | no-more | save /var/tmp/tshoot_"+mytoday+"/pfe_stats.txt\n")
    time.sleep(1)

    #Gather LOG info
    remote_conn.send("file archive compress source /var/log/* destination /var/tmp/tshoot_"+mytoday+"/log.tgz\n")
    time.sleep(11)
    
    #Gather RSI information
    remote_conn.send("request support information | save /var/tmp/tshoot_"+mytoday+"/RSI.txt\n")
    time.sleep(10)
    
    output = remote_conn.recv(65535)
    print output
    print "Output has been saved\n"
    