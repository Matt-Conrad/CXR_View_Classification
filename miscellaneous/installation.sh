#!/bin/bash

# Start up vmrest API
nohup vmrest &

# Wait for vmrest to start up
while ! echo exit | nc 127.0.0.1 8697; do sleep 1; done

# Must set up credentials in Jenkins
auth=$(echo -n ${VMREST_CREDS} | base64)

# Get VM ID
id=null
while [ $id == null ]
do 
    vmList=$(curl 'http://127.0.0.1:8697/api/vms' -X GET --header 'Accept: application/vnd.vmware.vmw.rest-v1+json' --header "Authorization: Basic ${auth}")
 
    id=$(echo $vmList | jq --arg VM_DESTINATION "$VM_DESTINATION" '.[] | select(.path | contains($VM_DESTINATION)) | .id')
done
id=$(echo $id | tr -d '"')

# Turn off VM
curl "http://127.0.0.1:8697/api/vms/${id}/power" -X PUT --header 'Content-Type: application/vnd.vmware.vmw.rest-v1+json' --header 'Accept: application/vnd.vmware.vmw.rest-v1+json' --header "Authorization: Basic ${auth}" -d 'off'

# Copy snapshot VM
rm -rf ${VM_DESTINATION}
cp -r ${VM_SOURCE} ${VM_DESTINATION}

# Replace shared folder contents with most recent build
rm -rf ${SHARED_FOLDER_HOST_PATH}/*
cp -r `ls --ignore=.*` ${SHARED_FOLDER_HOST_PATH}

# Turn on VM
curl "http://127.0.0.1:8697/api/vms/${id}/power" -X PUT --header 'Content-Type: application/vnd.vmware.vmw.rest-v1+json' --header 'Accept: application/vnd.vmware.vmw.rest-v1+json' --header "Authorization: Basic ${auth}" -d 'on'

# Get IP of VM
IP=null
while [ $IP == null ]
do 
    IP=$(curl "http://127.0.0.1:8697/api/vms/${id}/ip" -X GET --header 'Accept: application/vnd.vmware.vmw.rest-v1+json' --header "Authorization: Basic ${auth}" | jq '.ip' )
    sleep 1
done
IP=$(echo ${IP} | tr -d '"')

# Update ssh key
ssh-keygen -R $IP

# Run scripts on VM using SSH
endpoint=matt@$IP
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint 'echo password | sudo -S /usr/bin/vmhgfs-fuse .host:/ /mnt/hgfs -o subtype=vmhgfs-fuse,allow_other'

sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint 'echo password | sudo -S chmod u+x /mnt/hgfs/SharedFolder_Guest/miscellaneous/postgresSetup.sh'
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint 'echo password | sudo -S /mnt/hgfs/SharedFolder_Guest/miscellaneous/postgresSetup.sh'
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint 'echo password | sudo -S chmod u+x /mnt/hgfs/SharedFolder_Guest/miscellaneous/pythonSetup.sh'
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint 'echo password | sudo -S /mnt/hgfs/SharedFolder_Guest/miscellaneous/pythonSetup.sh'
# sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint 'echo password | sudo -S chmod u+x /mnt/hgfs/SharedFolder_Guest/miscellaneous/cppSetup.sh'
# sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint 'echo password | sudo -S /mnt/hgfs/SharedFolder_Guest/miscellaneous/cppSetup.sh'
# sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint 'echo password | sudo -S chmod u+x /mnt/hgfs/SharedFolder_Guest/miscellaneous/combinedSetup.sh'
# sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint 'echo password | sudo -S /mnt/hgfs/SharedFolder_Guest/miscellaneous/combinedSetup.sh'

# curl 'http://127.0.0.1:8697/api/vms/0G9LFS4SVBVOVO33L6NBO3K4N9GV3F0U/power' -X PUT --header 'Content-Type: application/vnd.vmware.vmw.rest-v1+json' --header 'Accept: application/vnd.vmware.vmw.rest-v1+json' --header "Authorization: Basic ${auth}" -d 'off'