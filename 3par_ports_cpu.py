#!/usr/bin/python
# parsing script for 3par
# Allan McAleavy 2017
# Parses cpu, cache and port data

import re
import time
from sys import argv

port=0
rwt='n'
cio=0
aio=0
mio=0
ckb=0
akb=0
mkb=0
csvc=0
asvc=0
iosz=0
aiosz=0
queue=0
ts=0
pattern='%H:%M:%S %m/%d/%Y'
npluscpu=0
util=0
nodecount=0

# Gather Delayed ACK details
file=open('statcmp.out', 'rb', 0)
for line in file:
    data=line.split()
    if re.search(b'^[0-9][0-9]:',line):
       dte=line.split()
       tsp = data[0] + " " + data[1]
       ts=int(time.mktime(time.strptime(tsp,pattern)))

    if re.search(b'RPM',line):
       nodecount=1

    if nodecount >=1 and re.search(b'^   [0-3]',line):
           print("Cache,Cache=%s,type=delack value=%s %d" % ( data[0],data[12],ts))
           nodecount = nodecount + 1

    if nodecount == 5:
       nodecount=0
file.close()

#Gather CPU details

file=open('statcpu.out', 'rb', 0)
for line in file:
    data=line.split()
    if re.search(b'^[0-9][0-9]:',line):
       dte=line.split()
       tsp = data[0] + " " + data[1]
       ts=int(time.mktime(time.strptime(tsp,pattern)))

    if re.search(b'[0-9],[0-9]',line):
       npluscpu=data[0].split(',')
       util = 100 - int(data[3])
       print("Cpu,Cpu=%s:%s,type=util value=%s %d" % (npluscpu[0],npluscpu[1],util,ts))
       print("UsrCpu,UsrCpu=%s:%s,type=util value=%s %d" % (npluscpu[0],npluscpu[1],data[1],ts))
       print("SysCpu,SysCpu=%s:%s,type=util value=%s %d" % (npluscpu[0],npluscpu[1],data[2],ts))
    if re.search(b'[0-3],total',line):
       npluscpu=data[0].split(',')
       print("Cpu,Cpu=%s,type=intr value=%s %d" % (npluscpu[0],data[4],ts))
       print("Cpu,Cpu=%s,type=ctx value=%s %d" % (npluscpu[0],data[5],ts))
file.close()

# Gather host port details
file=open('statport-host.out', 'rb', 0)
for line in file:
    data=line.split()
    if re.search(b'KBytes',line):
       dte=line.split()
       tsp = data[0] + " " + data[1]
       ts=int(time.mktime(time.strptime(tsp,pattern)))

    if re.search(b'[0-9]:[0-9]:[0-9]',line):
       if re.search(b'Data',line):
          port=data[0]    # port
          cord=data[1]    # Ctrl or Data
          rwt=data[2]     # read write or total
          cio=data[3]     # current IOPS
          aio=data[4]     # average IOPS
          mio=data[5]     # max IOPS
          ckb=data[6]     # current kb
          akb=data[7]     # average kb
          mkb=data[8]     # max kb
          csvc=data[9]    # current service time ms
          asvc=data[10]   # average service time ms
          iosz=data[11]   # io size
          aiosz=data[12]  # average iosize

          if re.match(b't',rwt):
             queue=data[13]
             print("PortIO,PortIO=%s,type=tiops value=%s %d" %(port,cio,ts))
             print("PortQ,PortQ=%s,type=qls value=%s %d" %(port,queue,ts))
             print("PortBW,PortBW=%s,type=tkb value=%s %d" %(port,ckb,ts))
             print("PortRT,PortRT=%s,type=tms value=%s %d" %(port,csvc,ts))
          if re.match(b'r',rwt):
             print("PortIO,PortIO=%s,type=riops value=%s %d" %(port,cio,ts))
             print("PortBW,PortBW=%s,type=rkb value=%s %d" %(port,ckb,ts))
             print("PortRT,PortRT=%s,type=rms value=%s %d" %(port,csvc,ts))
          if re.match(b'w',rwt):
             print("PortIO,PortIO=%s,type=wiops value=%s %d" %(port,cio,ts))
             print("PortBW,PortBW=%s,type=wkb value=%s %d" %(port,ckb,ts))
             print("PortRT,PortRT=%s,type=wms value=%s %d" %(port,csvc,ts))

file.close()
