#!/usr/bin/python
# parsing script for 3par
# Allan McAleavy 2917
# takes input of statvlun.out file

import re
import time
import argparse
from sys import argv

lun = 0
host = ''
port = 0
rwt = 'n'
cio = 0
aio = 0
mio = 0
ckb = 0
akb = 0
mkb = 0
csvc = 0
asvc = 0
iosz = 0
aiosz = 0
queue = 0
ts = 0
pattern = '%H:%M:%S %m/%d/%Y'
npluscpu = 0
util = 0
result = {}

examples = """examples:
   3par_host.py <statvlun_file>
"""
# arguments
parser = argparse.ArgumentParser(
    description="Gather performance data from 3par Arrays",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=examples)
parser.add_argument("vlun", help="Path to vlun file")
args = parser.parse_args()

if str(args.vlun):
    csvfile = args.vlun
if not str(args.vlun):
    exit

def check_key(key):
    if not key in result[host]:
        result[host][key] = 0

try:
    file = open(args.vlun, 'rb', 0)
except:
    print ("Could not open file %s" % (args.vlun))
    exit()

for line in file:
    data = line.split()
    if re.search(b'KBytes', line):
        dte = line.split()
        tsp = data[0] + " " + data[1]
        ts = int(time.mktime(time.strptime(tsp, pattern)))

    if re.search(b'[0-9]:[0-9]:[0-9]', line):
        lun = data[0]     # lun number
        vvname = data[1]  # vv name
        host = data[2]    # hostname
        port = data[3]    # read write or total
        rwt = data[4]     # read write or total
        cio = data[5]     # current IOPS
        aio = data[6]     # average IOPS
        mio = data[7]     # max IOPS
        ckb = data[8]     # current kb
        akb = data[9]     # average kb
        mkb = data[10]    # max kb
        csvc = data[11]   # current service time ms
        asvc = data[12]   # average service time ms
        iosz = data[13]   # io size
        aiosz = data[14]  # average iosize

        if not host in result:
            result[host] = {}

        if re.match(b't', rwt):
            qls = data[15]
            check_key('t_curio')
            result[host]['t_curio'] += int(cio)

            check_key('t_curkb')
            result[host]['t_curkb'] += int(ckb)

            check_key('t_qlen')
            result[host]['t_qlen'] += int(qls)

            check_key('t_cursvc')
            if float(csvc) >= float(result[host]['t_cursvc']):
                result[host]['t_cursvc'] = float(csvc)

            check_key('t_curiosz')
            if float(iosz) > float(result[host]['t_curiosz']):
                result[host]['t_curiosz'] = float(iosz)

        if re.match(b'r', rwt):
            check_key('r_curio')
            result[host]['r_curio'] += int(cio)

            check_key('r_curkb')
            result[host]['r_curkb'] += int(ckb)

            check_key('r_cursvc')
            if float(csvc) >= float(result[host]['r_cursvc']):
                result[host]['r_cursvc'] = float(csvc)

            check_key('r_curiosz')
            if float(iosz) > float(result[host]['r_curiosz']):
                result[host]['r_curiosz'] = float(iosz)

        if re.match(b'w', rwt):
            check_key('w_curio')
            result[host]['w_curio'] += int(cio)

            check_key('w_curkb')
            result[host]['w_curkb'] += int(ckb)

            check_key('w_cursvc')
            if float(csvc) >= float(result[host]['w_cursvc']):
                result[host]['w_cursvc'] = float(csvc)

            check_key('w_curiosz')
            if float(iosz) > float(result[host]['w_curiosz']):
                result[host]['w_curiosz'] = float(iosz)

    if re.match(b'\----------------------', line):
        for k in result:
            print("HostIO,HostIO=%s,type=iops value=%s %d" %
                 (k.lower(), result[k]['t_curio'], ts))
            print("HostBW,HostBW=%s,type=mb value=%d %d" %
                 (k.lower(), int(result[k]['t_curkb']) / 1024, ts))
            print("HostRT,HostRT=%s,type=ms value=%s %d" %
                 (k.lower(), result[k]['t_cursvc'], ts))
            print("HostIOSZ,HostIOSZ=%s,type=iosz value=%s %d" %
                 (k.lower(), result[k]['t_curiosz'], ts))
            print("HostQ,HostQ=%s,type=qls value=%s %d" %
                 (k.lower(), result[k]['t_qlen'], ts))
            result[k]['t_curio'] = 0
            result[k]['t_curkb'] = 0
            result[k]['t_cursvc'] = 0
            result[k]['t_curiosz'] = 0
            result[k]['t_qlen'] = 0

            print("HostIO,HostIO=%s,type=riops value=%s %d" %
                 (k.lower(), result[k]['r_curio'], ts))
            print("HostBW,HostBW=%s,type=rmb value=%d %d" %
                 (k.lower(), int(result[k]['r_curkb']) / 1024, ts))
            print("HostRT,HostRT=%s,type=rms value=%s %d" %
                 (k.lower(), result[k]['r_cursvc'], ts))
            print("HostIOSZ,HostIOSZ=%s,type=riosz value=%s %d" %
                 (k.lower(), result[k]['r_curiosz'], ts))
            result[k]['r_curio'] = 0
            result[k]['r_curkb'] = 0
            result[k]['r_cursvc'] = 0
            result[k]['r_curiosz'] = 0

            print("HostIO,HostIO=%s,type=wiops value=%s %d" %
                 (k.lower(), result[k]['w_curio'], ts))
            print("HostBW,HostBW=%s,type=wmb value=%d %d" %
                 (k.lower(), int(result[k]['w_curkb']) / 1024, ts))
            print("HostRT,HostRT=%s,type=wms value=%s %d" %
                 (k.lower(), result[k]['w_cursvc'], ts))
            print("HostIOSZ,HostIOSZ=%s,type=wiosz value=%s %d" %
                 (k.lower(), result[k]['w_curiosz'], ts))
            result[k]['w_curio'] = 0
            result[k]['w_curkb'] = 0
            result[k]['w_cursvc'] = 0
            result[k]['w_curiosz'] = 0
file.close()
