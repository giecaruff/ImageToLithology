import numpy as np
from PIL import Image
import argparse

import Utils
import readcsv

__NULL_COLOR = '#000000'
__RGB_INT_TYPE = np.uint8

parser = argparse.ArgumentParser()

parser.add_argument('--layersfilename', '-i')
parser.add_argument('--layerscodecolumn', type=int, default=1)
parser.add_argument('--layerstopcolumn', type=int, default=2)
parser.add_argument('--layersbottomcolumn', type=int, default=3)
parser.add_argument('--layersskiplines', type=int, default=1)
parser.add_argument('--csvfilename', '-c')
parser.add_argument('--csvcodecolumn', type=int, default=1)
parser.add_argument('--csvcolorcolumn', type=int, default=2)
parser.add_argument('--csvskiplines', type=int, default=1)
parser.add_argument('--csvcolumnseparator', default=',')
parser.add_argument('--csvemptycell', default='')
parser.add_argument('--csvcolorformat', default='html')
parser.add_argument('--nullcolor', default=__NULL_COLOR)
parser.add_argument('--topdepth', '-t', type=float, default=np.nan)
parser.add_argument('--bottomdepth', '-b', type=float, default=np.nan)
parser.add_argument('--topshift', type=float, default=0.0)
parser.add_argument('--bottomshift', type=float, default=0.0)
parser.add_argument('--width', type=int)
parser.add_argument('--height', type=int)
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

tops = np.array(list(map(float, tops)))
bottoms = np.array(list(map(float, bottoms)))

if args.topdepth is not np.nan and args.bottomdepth is not np.nan:
    n = args.height
    tops = Utils.depth2index(tops+args.topshift, n, args.topdepth, args.bottomdepth)
    bottoms = Utils.depth2index(bottoms+args.bottomshift, n, args.topdepth, args.bottomdepth)

csvheader, csvdata = readcsv.readcsv(args.csvfilename, delimiter=args.csvcolumnseparator, headerlines=args.csvskiplines, onlystr=True)
codes = csvdata[args.csvcodecolumn-1]

if args.csvcolorformat == 'html':
    colors = np.array(list(map(Utils.html2int, csvdata[args.csvcolorcolumn-1])), dtype=int)
    nullcolor = Utils.html2int(args.nullcolor)
elif args.csvcolorformat == 'rgb':
    # TODO: test and be aware of variations (int between 0 and 255 and float between 0 and 1, for instance)
    colors = np.array([Utils.rgb2int(*map(int, a.split())) for a in csvdata[[args.csvcolorcolumn-1]]], dtype=int)
    nullcolor = Utils.rgb2int(*map(int, args.nullcolor.split()))
elif args.csvcolorformat == 'int':
    colors = np.array(list(map(int, csvdata[[args.csvcolorcolumn-1]])), dtype=int)
    nullcolor = int(args.nullcolor)
else:
    print("Unable to handle color format: {}.".format(args.csvcolorformat))
    quit()

codestocolorsdict = {}
for key, value in zip(codes, colors):
    if key not in codestocolorsdict:
        codestocolorsdict[key] = value

layercolors = []
for code in layercodes:
    layercolors.append(codestocolorsdict[code])

layercolors = np.array(layercolors, dtype=int)

if tops[0] is np.nan:
    tops[0] = 0
if bottoms[-1] is np.nan:
    tops[-1] = args.height - 1

image_1d = Utils.interpolate(np.arange(args.height), layercolors, tops, bottoms, nullvalue=nullcolor)
image_int = Utils.fattenimage(image_1d, args.width)
image_rgb = Utils.imageint2rgb(image_int).astype(__RGB_INT_TYPE)
img = Image.fromarray(image_rgb, 'RGB')
img.save(args.outputfilename)
