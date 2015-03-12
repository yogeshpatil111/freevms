import sys
import os
import random
import string

def main(argv):
    if not os.path.exists("sim"):
        os.mkdir("sim")
    vm_list = "sim/vms.txt"
    vmfile = open(vm_list,"w")
    vmcount = 10
    if len(argv) > 1:
        try:
            vmcount = int(argv[1])
        except:
            print "vmcount should be a valid integer"
            os._exit(1)
    for i in xrange(vmcount):
        vmid = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        vmfile.write(vmid+"\n")
        vm_stat = open("sim/"+vmid+".txt","w")
        utilrand = random.random() * 85
        cpuutil = str(utilrand + 5 + random.random())
        memutil = str(utilrand + 15 - random.random())
        diskutil = str(utilrand + 7 + random.random())
        
        vm_stat.write(cpuutil + "," + memutil + "," + diskutil + "\n")
        vm_stat.close()
    vmfile.close()

    

if __name__ == "__main__":
    main(sys.argv)
    
