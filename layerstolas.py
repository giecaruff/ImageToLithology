import numpy as np
import argparse

import Utils
import readcsv
import LAS

parser = argparse.ArgumentParser()

parser.add_argument('--layersfilename', '-l')
parser.add_argument('--layerscodecolumn', type=int, default=1)
parser.add_argument('--layerstopcolumn', type=int, default=2)
parser.add_argument('--layersbottomcolumn', type=int, default=3)
parser.add_argument('--layersskiplines', type=int, default=1)
parser.add_argument('--csvfilename', '-c', default='')
parser.add_argument('--csvcode1column', type=int, default=1)
parser.add_argument('--csvcode2column', type=int, default=2)
parser.add_argument('--csvskiplines', type=int, default=1)
parser.add_argument('--csvcolumnseparator', default=',')
parser.add_argument('--csvemptycell', default='')
parser.add_argument('--topshift', type=float, default=0.0)
parser.add_argument('--bottomshift', type=float, default=0.0)
parser.add_argument('--wellfilename', '-w')
parser.add_argument('--depthmnem', default='')
parser.add_argument('--mnem', default='')
parser.add_argument('--unit', default='')
parser.add_argument('--nullcode', default=-1)
parser.add_argument('--interpolate', action='store_true')
parser.add_argument('--outputfilename', '-o')

args = parser.parse_args()

layersheader, layersdata = readcsv.readcsv(args.layersfilename, delimiter=args.csvcolumnseparator, headerlines=args.layersskiplines, onlystr=True)
layercodes = layersdata[args.layerscodecolumn-1]
tops = layersdata[args.layerstopcolumn-1]
bottoms = layersdata[args.layersbottomcolumn-1]

if tops[0] == args.csvemptycell:
    tops[0] = np.nan
if bottoms[-1] == args.csvemptycell:
    bottoms[-1] = np.nan

tops = np.array(map(float, tops))
bottoms = np.array(map(float, bottoms))

tops += args.topshift
bottoms += args.bottomshift

if args.csvfilename:
    csvheader, csvdata = readcsv.readcsv(args.csvfilename, delimiter=args.csvcolumnseparator, headerlines=args.csvskiplines, onlystr=True)
    codes1 = csvdata[args.csvcode1column-1]
    codes2 = csvdata[args.csvcode2column-1]
    
    codes1tocodes2dict = {}
    for key, value in zip(codes1, codes2):
        if key not in codes1tocodes2dict:
            codes1tocodes2dict[key] = value

    for i in range(len(layercodes)):
        layercodes[i] = codes1tocodes2dict[layercodes[i]]

layercodes = np.array(map(int, layercodes), dtype=int)

inputlas = LAS.open(args.wellfilename, 'r')
inputlas.read()

if not args.depthmnem:
    depth = inputlas.data[0]
else:
    depthindex = inputlas.curvesnames.index(args.depthmnem)
    depth = inputlas.data[depthindex],

if tops[0] is np.nan:
    tops[0] = np.nanmin(depth)
if bottoms[-1] is np.nan:
    tops[-1] = np.nanmax(depth)

log = Utils.interpolate(depth, layercodes, tops, bottoms, nullvalue=args.nullcode, fillgaps=args.interpolate, extrapolate=False)

if not args.mnem:
    if args.csvfilename:
        mnem = csvheader[args.csvcode2column-1][0]
    else:
        mnem = layersheader[args.layerscodecolumn-1][0]
else:
    mnem = args.mnem

outputlas = LAS.open(args.outputfilename, 'w')
outputlas.header = LAS.LASWriter.correctcurvesection(inputlas.header, inputlas.curvesnames + [mnem], inputlas.curvesunits + [args.unit])
outputlas.header['C'][mnem]["DESC"] = "Created from an image using ImageToLithology"
outputlas.headerlayout = LAS.LASWriter.getprettyheaderlayout(outputlas.header)
outputlas.headersectionnames = inputlas.headersectionnames

outputlas.data = np.append(inputlas.data, log.reshape((1, -1)), axis=0)

outputlas.write()
