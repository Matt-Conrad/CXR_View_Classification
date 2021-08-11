#!/bin/bash

# Start up vmrest API
nohup vmrest &

# Must set up credentials in Jenkins
auth=$(echo -n ${VMREST_CREDS} | base64)

vmrest_ip=127.0.0.1
vmrest_port=8697
vmrest_url=http://${vmrest_ip}:${vmrest_port}/api/vms
vmSource="/home/matt/vmwareSnapshots/Ubuntu"
vmDestination="/home/matt/vmware/Ubuntu/"

if [ -z "$vmDestination" ] # TODO: Checking can maybe be removed if sudo is removed from installation.sh call in Jenkinsfile
then
    echo "ERROR: vmDestination is empty. This can result in deleted system files with rm -rf"
    exit 1    
fi

# Wait for vmrest to start up
while ! echo exit | nc $vmrest_ip $vmrest_port; do sleep 1; done

declare -a curlArgs=('-H' "Authorization: Basic ${auth}" '-H' 'Accept: application/vnd.vmware.vmw.rest-v1+json' '-H' 'Content-Type: application/vnd.vmware.vmw.rest-v1+json')

vmList=$(curl "${vmrest_url}" -X GET "${curlArgs[@]}")
numVMs=$(echo $vmList | jq '. | length')

if [ $numVMs -gt 0 ]
then
    # Get VM ID
    # Minor Bug: If the destination isn't there, this comes up as null and the VM doesn't get turned off
    id=$(echo $vmList | jq --arg vmDestination "${vmDestination}" '.[] | select(.path | contains($vmDestination)) | .id') 
    id=$(echo $id | tr -d '"')
    # Turn off VM
    curl "${vmrest_url}/${id}/power" -X PUT "${curlArgs[@]}" -d 'off'
    # Remove VM
    rm -rf ${vmDestination}
fi

cp -r ${vmSource} ${vmDestination}
chmod -R a+rwx ${vmDestination}

# Get VM ID
vmList=$(curl "${vmrest_url}" -X GET "${curlArgs[@]}")
id=$(echo $vmList | jq --arg vmDestination "${vmDestination}" '.[] | select(.path | contains($vmDestination)) | .id')
id=$(echo $id | tr -d '"')

# Get Shared Folders information
sharedFolderInfo=$(curl "${vmrest_url}/${id}/sharedfolders" -X GET "${curlArgs[@]}")
sharedFolderGuestName=$(echo $sharedFolderInfo | jq '.[0].folder_id' | tr -d '"')
sharedFolderHostPath=$(echo $sharedFolderInfo | jq '.[0].host_path' | tr -d '"')

if [ -z "$sharedFolderHostPath" ]
then
    echo "ERROR: sharedFolderHostPath is empty. This can result in deleted system files with rm -rf"
    exit 1
else
    # Replace shared folder contents with most recent build
    rm -rf ${sharedFolderHostPath}/*
    cp -r `ls --ignore=.*` ${sharedFolderHostPath}
    chmod -R a+rwx ${sharedFolderHostPath}
fi

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

endpoint=${VM_UBUNTU_CREDS_USR}@${IP}

declare -a sshpassArgs=('-p' "${VM_UBUNTU_CREDS_PSW}")
declare -a sshArgs=('-o' 'StrictHostKeyChecking no')
sshCommandPrefix="echo ${VM_UBUNTU_CREDS_PSW} | sudo -S" # Take out sudo at some point
sharedFolderMountLocation="/mnt/hgfs"
miscFolder="${sharedFolderMountLocation}/${sharedFolderGuestName}/miscellaneous"

sshpass "${sshpassArgs[@]}" ssh $endpoint "${sshArgs[@]}" "${sshCommandPrefix} /usr/bin/vmhgfs-fuse .host:/ ${sharedFolderMountLocation} -o subtype=vmhgfs-fuse,allow_other,uid=1000,gid=1000" #IDs are IDs of matt user on VM

if [ $setupPostgresOnGuest == true ] 
then
    sshpass "${sshpassArgs[@]}" ssh $endpoint "${sshArgs[@]}" "${sshCommandPrefix} ${miscFolder}/postgresSetup.sh"
fi

if [ $setupPythonOnGuest == true ] 
then
    sshpass "${sshpassArgs[@]}" ssh $endpoint "${sshArgs[@]}" "${sshCommandPrefix} ${miscFolder}/pythonSetup.sh source"
fi

if [ $setupCppOnGuest == true ] 
then
    sshpass "${sshpassArgs[@]}" ssh $endpoint "${sshArgs[@]}" "${sshCommandPrefix} ${miscFolder}/cppSetup.sh prebuilt"
fi

if [ $setupCombinedOnGuest == true ] 
then
    sshpass "${sshpassArgs[@]}" ssh $endpoint "${sshArgs[@]}" "${sshCommandPrefix} ${miscFolder}/combinedBuild.sh download"
fi

if [ $setupToBuildCppOnGuest == true ] 
then
    sshpass "${sshpassArgs[@]}" ssh $endpoint "${sshArgs[@]}" "${sshCommandPrefix} ${miscFolder}/cppSetup.sh build"
fi

if [ $setupEngineOnGuest == true ] 
then
    sshpass "${sshpassArgs[@]}" ssh $endpoint "${sshArgs[@]}" "${sshCommandPrefix} ${miscFolder}/engineSetup.sh nginx network"
fi