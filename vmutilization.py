import multiprocessing
import time
import os
import ConfigParser
import datetime
import random
import sys
import glob

pool_size = multiprocessing.cpu_count() * 2
config_path = "vm.config"
vm_list = "sim/vms.txt"
stat_path="/var/tmp/"
low_cpu_util=10
low_memory_util=20
low_disk_util=10

def get_config():
    global low_cpu_util
    global low_memory_util
    global low_disk_util
    
    if os.path.exists(config_path):
        config = ConfigParser.ConfigParser()
        config.read(config_path)
        
        if config.has_section("underutilized"):
            for option in config.options("underutilized"):
                if "cpu" == option:
                    low_cpu_util = config.getfloat("underutilized", "cpu")
                if "memory" == option:
                    low_memory_util = config.getfloat("underutilized", "memory")
                if "disk" == option:
                    low_disk_util = config.getfloat("underutilized", "disk")

def get_vm_list():
    if not os.path.exists(vm_list):
        print "File " + vm_list +" does not exists. It provides VM list for the program"
    vmfile = open(vm_list,"r")
    return [x.strip() for x in vmfile.readlines()]

def change_stat(stat):
    value  = 10
    try:
        value = float(stat)
    except:
        pass
    variation = value / 10
    variation *=  random.random()
    if (random.random() > 0.5):
        value += variation
    else:
        value -= variation
    return str(value)
    

"""
Mock Function to get simulated data
"""
def get_vm_stat(vmid):
    stat_line = open("sim/"+vmid+".txt","r").readline()
    stats = stat_line.split(",")
    mod_stat = []
    for stat in stats:
        mod_stat.append(change_stat(stat))
    return ','.join(mod_stat)
    

def collect_vm_data(vmid):
    line = get_vm_stat(vmid)+"\n"
    
    data_file = open(stat_path+"/"+vmid+".csv","a")
    data_file.write(line)
    data_file.close()

def process_vm_data(vmid):
    data_file_name = stat_path+"/"+vmid+".csv"
    data_file = open(data_file_name,"r")
    count = 0
    cpu_util = 0
    memory_util = 0
    disk_util = 0
    for line in data_file.readlines():
        count += 1
        try:
            tokens = line.split(",")
            cpu_util += float(tokens[0])
            memory_util += float(tokens[1])
            disk_util += float(tokens[2])
        except:
            pass
    data_file.close()

    cpu_util_avg = cpu_util / count
    memory_util_avg = memory_util / count
    disk_util_avg = disk_util / count

    if cpu_util_avg < low_cpu_util and \
       memory_util_avg < low_memory_util and \
       disk_util_avg < low_disk_util:
        open(stat_path+"/"+vmid+".unused", 'a').close()
    os.remove(data_file_name)
        

def collectdata(vm_list):
    global pool_size
    
    pool = multiprocessing.Pool(processes=pool_size)
    pool.map(collect_vm_data, vm_list,5)
    pool.close()
    pool.join()

def processdata(vm_list):
    global pool_size
    
    pool = multiprocessing.Pool(processes=pool_size)
    pool.map(process_vm_data, vm_list,5)
    pool.close()
    pool.join()

def printvms():
    unused_reg = stat_path+'/*.unused'
    for unused in glob.iglob(unused_reg):
        vmid = unused.strip().rsplit('/',1)[1].split(".")[0]
        print "VM ID : " + vmid + " is unused for a while"
        os.remove(unused)
    

def main(argv):
    global pool_size
    global stat_path
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H_%M_%S')
    stat_path += st
    if not os.path.exists(stat_path):
        os.makedirs(stat_path)

    interval = 60
    
    run_count = 60
    if len(argv) > 1:
        try:
            run_count = int(argv[1])
        except:
            print "runcount should be a valid integer"
            os._exit(1)

    vm_list = get_vm_list()
    vm_count = len(vm_list)
    if vm_count < pool_size:
        pool_size = vm_count
    
    execution_count = 0
    while(execution_count < run_count):
        before_collect = datetime.datetime.now()
        collectdata(vm_list)
        after_collect = datetime.datetime.now()
        execution_count += 1
        delta = after_collect - before_collect
        if delta.seconds > interval:
            print "Stat collections taking more than a minute. Please tune your program"
        else:
            if (execution_count < run_count):
                time.sleep(interval - delta.seconds)
    processdata(vm_list)
    printvms()
    os.rmdir(stat_path)
    

if __name__ == "__main__":
    main(sys.argv)
