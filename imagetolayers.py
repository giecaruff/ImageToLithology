import numpy as np
import imageio
import argparse

import Utils
import readcsv

__NULL_COLOR = 0

parser = argparse.ArgumentParser()

parser.add_argument('--imagefilename', '-i')
parser.add_argument('--csvfilename', '-c')
parser.add_argument('--csvcodecolumn', type=int, default=1)
parser.add_argument('--csvcolorcolumn', type=int, default=2)
parser.add_argument('--csvskiplines', type=int, default=1)
parser.add_argument('--csvcolumnseparator', default=',')
parser.add_argument('--csvcolorformat', default='html')
parser.add_argument('--distancemetric', default='human')
parser.add_argument('--maximumdistance', type=float, default=0.02)
parser.add_argument('--dontfillgaps', action='store_true')
parser.add_argument('--topdepth', '-t', type=float, default=np.nan)
parser.add_argument('--bottomdepth', '-b', type=float, default=np.nan)
parser.add_argument('--topshift', type=float, default=0.0)
parser.add_argument('--bottomshift', type=float, default=0.0)
parser.add_argument('--columntitles', nargs=3, default=['CODE', 'TOP', 'BOTTOM'])
parser.add_argument('--outputfilename', '-o')

args = parser.parse_args()

image_rgb = imageio.imread(args.imagefilename, pilmode='RGB')

csvheader, csvdata = readcsv.readcsv(args.csvfilename, delimiter=args.csvcolumnseparator, headerlines=args.csvskiplines, onlystr=True)
codes = csvdata[args.csvcodecolumn-1]

if args.csvcolorformat == 'html':
    colors = np.array(list(map(Utils.html2int, csvdata[args.csvcolorcolumn-1])), dtype=int)
elif args.csvcolorformat == 'rgb':
    # TODO: test and be aware of variations (int between 0 and 255 and float between 0 and 1, for instance)
    colors = np.array([Utils.rgb2int(*map(int, a.split())) for a in csvdata[[args.csvcolorcolumn-1]]], dtype=int)
elif args.csvcolorformat == 'int':
    colors = np.array(csvdata[[args.csvcolorcolumn-1]], dtype=int)
else:
    print("Unable to handle color format: {}.".format(args.csvcolorformat))
    quit()

colorstocodesdict = {}
for key, value in zip(colors, codes):
    if key not in colorstocodesdict:
        colorstocodesdict[key] = value

image_int = Utils.imagergb2int(image_rgb)
image_1d = Utils.flattenimage(image_int, np.unique(colors), distmetric=args.distancemetric, maxdistance=args.maximumdistance, gapcolor=__NULL_COLOR)
if not args.dontfillgaps:
    image_1d = Utils.fillgaps(image_1d, gapcolor=__NULL_COLOR)

layercolors, tops, bottoms = Utils.compress(image_1d, gapcolor=__NULL_COLOR)

if args.topdepth is not np.nan and args.bottomdepth is not np.nan:
    n = image_rgb.shape[0]
    tops = Utils.index2depth(tops, n, args.topdepth, args.bottomdepth) + args.topshift
    bottoms = Utils.index2depth(bottoms, n, args.topdepth, args.bottomdepth) + args.bottomshift

csvlineformat = '{{}}{0}{{}}{0}{{}}'.format(args.csvcolumnseparator)

csvlines = []
csvlines.append(csvlineformat.format(*args.columntitles))
for lc, t, b in zip(layercolors, tops, bottoms):
    csvlines.append(csvlineformat.format(colorstocodesdict[lc], t, b))

with open(args.outputfilename, 'w') as f:
    f.write('\n'.join(csvlines))
