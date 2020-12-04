#!/bin/bash
# Move this one to run after the VM set up no matter what
endpoint1=matt@192.168.61.131
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint1 'echo password | sudo -S /usr/bin/vmhgfs-fuse .host:/ /mnt/hgfs -o subtype=vmhgfs-fuse,allow_other'

sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint1 'echo password | sudo -S chmod u+x /mnt/hgfs/SharedFolder_Guest/miscellaneous/postgresSetup.sh'
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint1 'echo password | sudo -S /mnt/hgfs/SharedFolder_Guest/miscellaneous/postgresSetup.sh'
# sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint1 'echo password | sudo -S chmod u+x /mnt/hgfs/SharedFolder_Guest/miscellaneous/pythonSetup.sh'
# sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint1 'echo password | sudo -S /mnt/hgfs/SharedFolder_Guest/miscellaneous/pythonSetup.sh'
# sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint1 'echo password | sudo -S chmod u+x /mnt/hgfs/SharedFolder_Guest/miscellaneous/cppSetup.sh'
# sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint1 'echo password | sudo -S /mnt/hgfs/SharedFolder_Guest/miscellaneous/cppSetup.sh'
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint1 'echo password | sudo -S chmod u+x /mnt/hgfs/SharedFolder_Guest/miscellaneous/combinedSetup.sh'
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint1 'echo password | sudo -S /mnt/hgfs/SharedFolder_Guest/miscellaneous/combinedSetup.sh'

endpoint2=matt@192.168.61.132
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint2 'echo password | sudo -S /usr/bin/vmhgfs-fuse .host:/ /mnt/hgfs -o subtype=vmhgfs-fuse,allow_other'

sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint2 'echo password | sudo -S chmod u+x /mnt/hgfs/SharedFolder_Guest/miscellaneous/postgresSetup.sh'
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint2 'echo password | sudo -S /mnt/hgfs/SharedFolder_Guest/miscellaneous/postgresSetup.sh'
# sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint2 'echo password | sudo -S chmod u+x /mnt/hgfs/SharedFolder_Guest/miscellaneous/pythonSetup.sh'
# sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint2 'echo password | sudo -S /mnt/hgfs/SharedFolder_Guest/miscellaneous/pythonSetup.sh'
# sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint2 'echo password | sudo -S chmod u+x /mnt/hgfs/SharedFolder_Guest/miscellaneous/cppSetup.sh'
# sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint2 'echo password | sudo -S /mnt/hgfs/SharedFolder_Guest/miscellaneous/cppSetup.sh'
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint2 'echo password | sudo -S chmod u+x /mnt/hgfs/SharedFolder_Guest/miscellaneous/combinedSetup.sh'
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' $endpoint2 'echo password | sudo -S /mnt/hgfs/SharedFolder_Guest/miscellaneous/combinedSetup.sh'
