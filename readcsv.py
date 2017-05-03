# -*- coding: utf-8 -*-

def readcsv(file, delimiter=',', decimal='.', headerlines=1, strip=True, onlystr=False, nullstr=None, nullfloat=None):
    closefile = False
    if isinstance(file, basestring):
        file = open(file, 'r')
        closefile = True
    
    header = []
    data = []
    
    ncols = None
    
    for i in range(headerlines):
        row = file.readline()
        cols = row.split(delimiter)
        
        if not header:
            ncols = len(cols)
            for i in range(ncols):
                header.append([])
                data.append([])
        
        for i in range(ncols):
            if strip:
                header[i].append(cols[i].strip())
            else:
                header[i].append(cols[i])
    
    while True:
        row = file.readline()
        if not row.strip():
            break
        cols = row.split(delimiter)
        for i in range(ncols):
            if strip:
                data[i].append(cols[i].strip())
            else:
                data[i].append(cols[i])
    
    datalines = len(data[0])
    
    if not onlystr:
        for i in range(ncols):
            asfloat = []
            success = True
            for j in range(datalines):
                if data[i][j].strip() == nullstr:
                    asfloat.append(nullfloat)
                    continue
                try:
                    asfloat.append(float(data[i][j]))
                except:
                    success = False
                    break
            if success:
                data[i] = asfloat
    
    if closefile:
        file.close()
    
    return header, data
