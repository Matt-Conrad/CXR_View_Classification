#!/bin/bash +x

# Start up vmrest API
nohup vmrest &

# Must set up credentials in Jenkins
auth=$(echo -n ${VMREST_CREDS} | base64)

vmrest_ip=127.0.0.1
vmrest_port=8697
vmrest_url=http://${vmrest_ip}:${vmrest_port}/api/vms

declare -a curlArgs=('-H' "Authorization: Basic ${auth}" '-H' 'Accept: application/vnd.vmware.vmw.rest-v1+json' '-H' 'Content-Type: application/vnd.vmware.vmw.rest-v1+json')

# Wait for vmrest to start up
while ! echo exit | nc $vmrest_ip $vmrest_port; do sleep 1; done

# Get VM ID
id=null
while [ $id == null ]
do 
    vmList=$(curl "${vmrest_url}" -X GET "${curlArgs[@]}")
 
    id=$(echo $vmList | jq --arg VM_DESTINATION "$VM_DESTINATION" '.[] | select(.path | contains($VM_DESTINATION)) | .id')
done
id=$(echo $id | tr -d '"')

# Turn off VM
curl "${vmrest_url}/${id}/power" -X PUT "${curlArgs[@]}" -d 'off'

# Get Shared Folders information
# sharedFolderInfo=$(curl "${vmrest_url}/${id}/sharedfolders" -X GET)

# Copy snapshot VM
rm -rf ${VM_DESTINATION}
cp -r ${VM_SOURCE} ${VM_DESTINATION}

# Replace shared folder contents with most recent build
rm -rf ${SHARED_FOLDER_HOST_PATH}/*
cp -r `ls --ignore=.*` ${SHARED_FOLDER_HOST_PATH}

# Turn on VM
curl "${vmrest_url}/${id}/power" -X PUT "${curlArgs[@]}" -d 'on'

# Get IP of VM
IP=null
while [ $IP == null ]
do 
    IP=$(curl "${vmrest_url}/${id}/ip" -X GET "${curlArgs[@]}" | jq '.ip' )
    sleep 1
done
IP=$(echo ${IP} | tr -d '"')

# Update ssh key
ssh-keygen -R $IP

# Run scripts on VM using SSH
endpoint=matt@$IP

declare -a sshpassArgs=('-p' 'password')
declare -a sshArgs=('-o' 'StrictHostKeyChecking no')
sshCommandPrefix='echo password | sudo -S'
miscFolder='/mnt/hgfs/SharedFolder_Guest/miscellaneous'

sshpass "${sshpassArgs[@]}" ssh $endpoint "${sshArgs[@]}" "${sshCommandPrefix} /usr/bin/vmhgfs-fuse .host:/ /mnt/hgfs -o subtype=vmhgfs-fuse,allow_other"

sshpass "${sshpassArgs[@]}" ssh $endpoint "${sshArgs[@]}" "${sshCommandPrefix} chmod u+x ${miscFolder}/postgresSetup.sh && ${miscFolder}/postgresSetup.sh"
sshpass "${sshpassArgs[@]}" ssh $endpoint "${sshArgs[@]}" "${sshCommandPrefix} chmod u+x ${miscFolder}/pythonSetup.sh && ${miscFolder}/pythonSetup.sh"
sshpass "${sshpassArgs[@]}" ssh $endpoint "${sshArgs[@]}" "${sshCommandPrefix} chmod u+x ${miscFolder}/pythonSetup.sh && ${miscFolder}/cppSetup.sh"
sshpass "${sshpassArgs[@]}" ssh $endpoint "${sshArgs[@]}" "${sshCommandPrefix} chmod u+x ${miscFolder}/pythonSetup.sh && ${miscFolder}/combinedSetup.sh"

# curl 'http://127.0.0.1:8697/api/vms/0G9LFS4SVBVOVO33L6NBO3K4N9GV3F0U/power' -X PUT --header 'Content-Type: application/vnd.vmware.vmw.rest-v1+json' --header 'Accept: application/vnd.vmware.vmw.rest-v1+json' --header "Authorization: Basic ${auth}" -d 'off'