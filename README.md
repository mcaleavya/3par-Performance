# 3par-Performance
Performance Scripts for parsing 3par statistics 

## 3par_hosts.py 
Script to parse statvlun aggregate host data into influx batch format.
```

./3par_hosts.py statvlun.out > batch
/usr/bin/curl -i -XPOST 'http://<influx_db>:8086/write?db=<3PAR DBNAME>&precision=s' --data-binary @batch

## Eaxample data.. 
$ grep -i SERVERA batch
HostIO,HostIO=servera,type=iops value=1990 1505502061
HostBW,HostBW=servera,type=mb value=48 1505502061
HostRT,HostRT=servera,type=ms value=3.34 1505502061
HostIOSZ,HostIOSZ=servera,type=iosz value=228.0 1505502061
HostQ,HostQ=servera,type=qls value=32 1505502061
HostIO,HostIO=servera,type=riops value=1856 1505502061
HostBW,HostBW=servera,type=rmb value=40 1505502061
HostRT,HostRT=servera,type=rms value=2.94 1505502061
HostIOSZ,HostIOSZ=servera,type=riosz value=228.1 1505502061
HostIO,HostIO=servera,type=wiops value=134 1505502061
HostBW,HostBW=servera,type=wmb value=8 1505502061
HostRT,HostRT=servera,type=wms value=4.13 1505502061
HostIOSZ,HostIOSZ=servera,type=wiosz value=67.3 1505502061
```

## 3par_vols.py 
Script to parse statvlun aggregate volume data into influx batch format.
```

./3par_vols.py statvlun.out > batch
/usr/bin/curl -i -XPOST 'http://<influx_db>:8086/write?db=<3PAR DBNAME>&precision=s' --data-binary @batch

## Eaxample data.. 
$ grep -i VOLA batch
VolIO,VolIO=vola,type=iops value=150 1505502061
VolBW,VolBW=vola,type=mb value=6 1505502061
VolRT,VolRT=vola,type=ms value=11.94 1505502061
VolIOSZ,VolIOSZ=vola,type=iosz value=308.1 1505502061
VolQ,VolQ=vola,type=qls value=0 1505502061
VolIO,VolIO=vola,type=riops value=6 1505502061
VolBW,VolBW=vola,type=rmb value=1 1505502061
VolRT,VolRT=vola,type=rms value=4.96 1505502061
VolIOSZ,VolIOSZ=vola,type=riosz value=430.5 1505502061
VolIO,VolIO=vola,type=wiops value=140 1505502061
VolBW,VolBW=vola,type=wmb value=4 1505502061
VolRT,VolRT=vola,type=wms value=11.94 1505502061
VolIOSZ,VolIOSZ=vola,type=wiosz value=38.2 1505502061
```
