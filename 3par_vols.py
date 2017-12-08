#!/usr/bin/python
# parsing script for 3par
# Allan McAleavy 2017
# takes input of stavlun.out filename

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
   3par_vols.py <statvlun_file>
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
    if not key in result[vvname]:
        result[vvname][key] = 0

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
        port = data[3]     # read write or total
        rwt = data[4]     # read write or total
        cio = data[5]     # current IOPS
        aio = data[6]     # average IOPS
        mio = data[7]     # max IOPS
        ckb = data[8]     # current kb
        akb = data[9]     # average kb
        mkb = data[10]     # max kb
        csvc = data[11]    # current service time ms
        asvc = data[12]   # average service time ms
        iosz = data[13]   # io size
        aiosz = data[14]  # average iosize

        #if not result.has_key(host):
        if not vvname in result:
            result[vvname] = {}

        if re.match(b't', rwt):
            qls = data[15]
            check_key('t_curio')
            result[vvname]['t_curio'] += int(cio)

            check_key('t_curkb')
            result[vvname]['t_curkb'] += int(ckb)

            check_key('t_qlen')
            result[vvname]['t_qlen'] += int(qls)

            check_key('t_cursvc')
            if float(csvc) >= float(result[vvname]['t_cursvc']):
                result[vvname]['t_cursvc'] = float(csvc)

            check_key('t_curiosz')
            if float(iosz) > float(result[vvname]['t_curiosz']):
                result[vvname]['t_curiosz'] = float(iosz)

        if re.match(b'r', rwt):
            check_key('r_curio')
            result[vvname]['r_curio'] += int(cio)

            check_key('r_curkb')
            result[vvname]['r_curkb'] += int(ckb)

            check_key('r_cursvc')
            if float(csvc) >= float(result[vvname]['r_cursvc']):
                result[vvname]['r_cursvc'] = float(csvc)

            check_key('r_curiosz')
            if float(iosz) > float(result[vvname]['r_curiosz']):
                result[vvname]['r_curiosz'] = float(iosz)

        if re.match(b'w', rwt):
            check_key('w_curio')
            result[vvname]['w_curio'] += int(cio)

            check_key('w_curkb')
            result[vvname]['w_curkb'] += int(ckb)

            check_key('w_cursvc')
            if float(csvc) >= float(result[vvname]['w_cursvc']):
                result[vvname]['w_cursvc'] = float(csvc)

            check_key('w_curiosz')
            if float(iosz) > float(result[vvname]['w_curiosz']):
                result[vvname]['w_curiosz'] = float(iosz)

    if re.match(b'\----------------------', line):
        for k in result:
            print("VolIO,VolIO=%s,type=iops value=%s %d" %
                 (k.lower(), result[k]['t_curio'], ts))
            print("VolBW,VolBW=%s,type=mb value=%d %d" %
                 (k.lower(), int(result[k]['t_curkb']) / 1024, ts))
            print("VolRT,VolRT=%s,type=ms value=%s %d" %
                 (k.lower(), result[k]['t_cursvc'], ts))
            print("VolIOSZ,VolIOSZ=%s,type=iosz value=%s %d" %
                 (k.lower(), result[k]['t_curiosz'], ts))
            print("VolQ,VolQ=%s,type=qls value=%s %d" %
                 (k.lower(), result[k]['t_qlen'], ts))
            result[k]['t_curio'] = 0
            result[k]['t_curkb'] = 0
            result[k]['t_cursvc'] = 0
            result[k]['t_curiosz'] = 0
            result[k]['t_qlen'] = 0

            print("VolIO,VolIO=%s,type=riops value=%s %d" %
                 (k.lower(), result[k]['r_curio'], ts))
            print("VolBW,VolBW=%s,type=rmb value=%d %d" %
                 (k.lower(), int(result[k]['r_curkb']) / 1024, ts))
            print("VolRT,VolRT=%s,type=rms value=%s %d" %
                 (k.lower(), result[k]['r_cursvc'], ts))
            print("VolIOSZ,VolIOSZ=%s,type=riosz value=%s %d" %
                 (k.lower(), result[k]['r_curiosz'], ts))
            result[k]['r_curio'] = 0
            result[k]['r_curkb'] = 0
            result[k]['r_cursvc'] = 0
            result[k]['r_curiosz'] = 0

            print("VolIO,VolIO=%s,type=wiops value=%s %d" %
                 (k.lower(), result[k]['w_curio'], ts))
            print("VolBW,VolBW=%s,type=wmb value=%d %d" %
                 (k.lower(), int(result[k]['w_curkb']) / 1024, ts))
            print("VolRT,VolRT=%s,type=wms value=%s %d" %
                 (k.lower(), result[k]['w_cursvc'], ts))
            print("VolIOSZ,VolIOSZ=%s,type=wiosz value=%s %d" %
                 (k.lower(), result[k]['w_curiosz'], ts))
            result[k]['w_curio'] = 0
            result[k]['w_curkb'] = 0
            result[k]['w_cursvc'] = 0
            result[k]['w_curiosz'] = 0
file.close()
