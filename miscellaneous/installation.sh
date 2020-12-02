#!/bin/bash
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' matt@192.168.61.130 'echo password | sudo -S /usr/bin/vmhgfs-fuse .host:/ /mnt/hgfs -o subtype=vmhgfs-fuse,allow_other'
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' matt@192.168.61.130 'echo password | sudo -S chmod u+x /mnt/hgfs/SharedFolder_Guest/miscellaneous/pythonSetup.sh'
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' matt@192.168.61.130 'echo password | sudo -S /mnt/hgfs/SharedFolder_Guest/miscellaneous/pythonSetup.sh'
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' matt@192.168.61.130 'echo password | sudo -S chmod u+x /mnt/hgfs/SharedFolder_Guest/miscellaneous/postgresSetup.sh'
sshpass -p 'password' ssh -o 'StrictHostKeyChecking no' matt@192.168.61.130 'echo password | sudo -S /mnt/hgfs/SharedFolder_Guest/miscellaneous/postgresSetup.sh'