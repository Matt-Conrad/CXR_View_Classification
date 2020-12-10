#!/bin/bash
# Move this one to run after the VM set up no matter what
username=$(<./miscellaneous/JenkinsUsername)

echo "Username"
echo $username
echo "Authorization: Basic ${username}"
echo curl 'http://127.0.0.1:8697/api/vms/0G9LFS4SVBVOVO33L6NBO3K4N9GV3F0U/ip' -X GET --header 'Accept: application/vnd.vmware.vmw.rest-v1+json' --header "Authorization: Basic ${username}"

curl 'http://127.0.0.1:8697/api/vms/0G9LFS4SVBVOVO33L6NBO3K4N9GV3F0U/power' -X PUT --header 'Content-Type: application/vnd.vmware.vmw.rest-v1+json' --header 'Accept: application/vnd.vmware.vmw.rest-v1+json' --header "Authorization: Basic ${username}" -d 'on'

IP=$(curl 'http://127.0.0.1:8697/api/vms/0G9LFS4SVBVOVO33L6NBO3K4N9GV3F0U/ip' -X GET --header 'Accept: application/vnd.vmware.vmw.rest-v1+json' --header "Authorization: Basic ${username}"| jq '.ip' | tr -d '"')

echo "IP Variable"
echo $IP

sleep 15
echo "Keygen"
ssh-keygen -R $IP

sleep 15

# endpoint=matt@$IP
echo "SSH Calls"
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $IP -l matt 'echo password | sudo -S /usr/bin/vmhgfs-fuse .host:/ /mnt/hgfs -o subtype=vmhgfs-fuse,allow_other'

sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $IP -l matt 'echo password | sudo -S chmod u+x /mnt/hgfs/SharedFolder_Guest/miscellaneous/postgresSetup.sh'
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $IP -l matt 'echo password | sudo -S /mnt/hgfs/SharedFolder_Guest/miscellaneous/postgresSetup.sh'
# sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $IP -l matt 'echo password | sudo -S chmod u+x /mnt/hgfs/SharedFolder_Guest/miscellaneous/pythonSetup.sh'
# sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $IP -l matt 'echo password | sudo -S /mnt/hgfs/SharedFolder_Guest/miscellaneous/pythonSetup.sh'
# sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $IP -l matt 'echo password | sudo -S chmod u+x /mnt/hgfs/SharedFolder_Guest/miscellaneous/cppSetup.sh'
# sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $IP -l matt 'echo password | sudo -S /mnt/hgfs/SharedFolder_Guest/miscellaneous/cppSetup.sh'
# sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $IP -l matt 'echo password | sudo -S chmod u+x /mnt/hgfs/SharedFolder_Guest/miscellaneous/combinedSetup.sh'
# sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $IP -l matt 'echo password | sudo -S /mnt/hgfs/SharedFolder_Guest/miscellaneous/combinedSetup.sh'

curl 'http://127.0.0.1:8697/api/vms/0G9LFS4SVBVOVO33L6NBO3K4N9GV3F0U/power' -X PUT --header 'Content-Type: application/vnd.vmware.vmw.rest-v1+json' --header 'Accept: application/vnd.vmware.vmw.rest-v1+json' --header "Authorization: Basic ${username}" -d 'off'