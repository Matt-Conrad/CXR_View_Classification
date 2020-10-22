import os
with open('commandsToBuild.txt') as f:
    for line in f:
        os.system(line)