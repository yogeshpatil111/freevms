# freevms

## To run this, first create simulated data using,

python simulation.py [vm count: default(10)]

## Simulated files vms.txt and <vmid>.txt will get generated in "sim/" folder in the same place

python vmutilization.py [run count: default(60)]

## utlization configurations are in vm.config files. Those can be tweaked before every execution

## It will run for 1 minute till run count reaches 0. It will analyze and store data in /var/tmp directory and cleans it up.
## Result will look like,

VM ID : c5itqqcg is unused for a while
....



