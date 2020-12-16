#!/bin/bash
# Move this one to run after the VM set up no matter what

# Must set up credentials in Jenkins
auth=$(echo -n ${VMREST_CREDS} | base64)

id=null
while [ $id == null ]
do 
    vmList=$(curl 'http://127.0.0.1:8697/api/vms' -X GET --header 'Accept: application/vnd.vmware.vmw.rest-v1+json' --header "Authorization: Basic ${auth}")
 
    id=$(echo $vmList | jq --arg VM_DESTINATION "$VM_DESTINATION" '.[] | select(.path | contains($VM_DESTINATION)) | .id')
done

id=$(echo $id | tr -d '"')
curl "http://127.0.0.1:8697/api/vms/${id}/power" -X PUT --header 'Content-Type: application/vnd.vmware.vmw.rest-v1+json' --header 'Accept: application/vnd.vmware.vmw.rest-v1+json' --header "Authorization: Basic ${auth}" -d 'on'

online=null
while [ $online == null ]
do 
    online=$(curl "http://127.0.0.1:8697/api/vms/${id}/ip" -X GET --header 'Accept: application/vnd.vmware.vmw.rest-v1+json' --header "Authorization: Basic ${auth}" | jq '.ip' )
    sleep 1
done

IP=$(echo ${online} | tr -d '"')
ssh-keygen -R $IP

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