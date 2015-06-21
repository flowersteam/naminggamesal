#!/usr/bin/python
# -*- coding: latin-1 -*-

import os
import subprocess
import time
import datetime
        
path = '/home/sforestier/software/explaupoppydiva/scripts/arm/'

start_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_dir = '/home/sforestier/software/explaupoppydiva/logs/' + start_date + '-CompetentExplo'



def write_pbs(config_name, iter):
    pbs =   """
#!/bin/sh

#PBS -l nodes=1:ppn=2
#PBS -l walltime=04:00:00
#PBS -N {}-{}
#PBS -o {}/logs/log-{}.output
#PBS -e {}/logs/log-{}.error

cd {}
python xps.py {} {} {}

""".format(nb_nodes,nb_cores,walltime,config_name, iter, log_dir, iter, log_dir, iter, path, log_dir, config_name, iter)
    filename = '{}-{}.pbs'.format(config_name, iter)
    print log_dir + "/pbs/" + filename
    with open(log_dir + "/pbs/" + filename, 'wb') as f:
        f.write(pbs)



config_list = [
               "MB",
               "MS2",
               "TOP-DOWN-CMA-Tree"
               ]

iter_list = range(1,10 + 1) 



os.mkdir(log_dir)
os.mkdir(log_dir + "/pbs")
os.mkdir(log_dir + "/logs")
    






for config_name in config_list:
    for i in iter_list:
        print config_name, i
        write_pbs(config_name, i)   
        filename = '{}-{}.pbs'.format(config_name, i)
        
        print "Run qsub", config_name, i
        print "qsub " + log_dir + "/pbs/" + filename
        process = subprocess.Popen("qsub " + log_dir + "/pbs/" + filename, shell=True, stdout=subprocess.PIPE)
        time.sleep(0.1)