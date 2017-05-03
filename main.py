import numpy as np
from scipy import ndimage
from PIL import Image
import Utils

import readcsv

# def __compresstotopbottom_fail(image_1d, gapcolor=Utils._GAPCOLOR):
    # """Does not work in layers with no gap before their tops"""
    # nrows = image_1d.shape[0]
    
    # colorchange = np.empty(nrows, dtype=bool)
    # colorchange[:-1] = (image_1d[1:] - image_1d[:-1]).astype(bool)
    # colorchange[-1] = False
    
    # colorchangeidxs = np.arange(nrows)[colorchange]
    
    # bottoms = np.roll(np.roll(colorchange, 1)*(image_1d == gapcolor), -1)
    # tops = np.roll(colorchange*(image_1d == gapcolor), 1)
    
    # bottomidxs = np.arange(nrows)[bottoms]
    # topidxs = np.arange(nrows)[tops]
    
    # if image_1d[0] != gapcolor:
        # topidxs = np.append(0, topidxs)
    
    # if image_1d[-1] != gapcolor:
        # bottomidxs = np.append(bottomidxs, nrows-1)
    
    # colors = image_1d[topidxs]
    
    # return colors, topidxs, bottomidxs

def index2depth(i, n, top, bottom):
    return top + i/(n - 1.0)*(bottom - top)

def compresstotopbottom(image_1d, gapcolor=Utils._GAPCOLOR):
    nrows = image_1d.shape[0]
    
    colorchange = np.empty(nrows, dtype=bool)
    colorchange[:-1] = (image_1d[1:] - image_1d[:-1]).astype(bool)
    colorchange[-1] = False
    
    colorchangeidxs = np.arange(nrows)[colorchange]
    
    bottoms = np.append(colorchangeidxs, nrows-1)
    tops = np.append(0, colorchangeidxs+1)
    colors = image_1d[bottoms]
    
    isgap = colors == gapcolor
    
    bottoms = bottoms[~isgap]
    tops = tops[~isgap]
    colors = colors[~isgap]
    
    return colors, tops, bottoms

from scipy.interpolate import interp1d
def interpolate(new_x, y, tops, bottoms, nullvalue=Utils._GAPCOLOR, fillgaps=False, extrapolate=False):
    print new_x
    print tops
    print bottoms
    if fillgaps:
        y_ = np.repeat(y, 2)
        x_ = np.vstack((tops, bottoms)).T.flatten()
    else:
        epsilon = 1.0E-6
        y_ = np.vstack((np.zeros(len(y))+nullvalue, y, y, np.zeros(len(y))+nullvalue)).T.flatten()
        x_ = np.vstack((tops-epsilon, tops, bottoms, bottoms+epsilon)).T.flatten()
    
    if extrapolate:
        fill_value = 'extrapolate'
    else:
        fill_value = nullvalue
    
    f = interp1d(x_, y_, kind='nearest', bounds_error=False, fill_value=fill_value)
    return f(new_x)   

if __name__ == '__main__':
    import argparse
    import json
    
    import LAS
    
    parser = argparse.ArgumentParser(description="Extract lithology codes from an image", add_help=True)
    
    parser.add_argument('--input', nargs='*')
    parser.add_argument('--output', nargs='*')
    
    args = parser.parse_args()
    
    inputfilenames = args.input
    outputfilenames = args.output
    
    inputfileextensions = [a.rsplit('.', 1)[1].lower() for a in inputfilenames]
    outputfileextensions = [a.rsplit('.', 1)[1].lower() for a in outputfilenames]
    
    image_rgb = None
    for i in range(len(inputfilenames)):
        try:
            image_rgb = ndimage.imread(inputfilenames[i], mode='RGB')
            inputfilenames.pop(i)
            imagefileextension = inputfileextensions.pop(i)
            break
        except:
            continue
    
    if image_rgb is None:
        print 'No image file found on the inputs.'
        quit()
    
    if 'csv' not in inputfileextensions:
        print 'No CSV file found on the inputs.'
        quit()
    else:
        csvidx = inputfileextensions.index('csv')
        csvfilename = inputfilenames.pop(csvidx)
        inputfileextensions.pop(csvidx)
    
    if 'json' not in inputfileextensions:
        print 'No JSON file found on the inputs.'
        quit()
    else:
        jsonidx = inputfileextensions.index('json')
        jsonfilename = inputfilenames.pop(jsonidx)
        inputfileextensions.pop(jsonidx)
    
    with open(jsonfilename, 'r') as f:
        pars = json.load(f)
    
    colorformat = pars['csv']['colorformat']
    
    csvheader, csvdata = readcsv.readcsv(csvfilename, delimiter=pars['csv']['delimiter'], decimal=pars['csv']['decimal'], headerlines=pars['csv']['headerlines'], nullstr=pars['csv']['nullstr'])
    codes = np.array(csvdata[pars['csv']['codecolumn']-1], dtype=float)
    
    if colorformat == 'html':
        colors = np.array(map(Utils.html2int, csvdata[pars['csv']['colorcolumn']-1]), dtype=int)
        nullcolor = Utils.html2int(pars['color']['nullcolor'])
    elif colorformat == 'rgb':
        # TODO: test and be aware of variations (int between 0 and 255 and float between 0 and 1, for instance)
        colors = np.array([Utils.rgb2int(*map(int, a.split())) for a in csvdata[pars['csv']['colorcolumn']-1]], dtype=int)
        nullcolor = Utils.rgb2int(*map(int, pars['color']['nullcolor'].split()))
    elif colorformat == 'int':
        colors = np.array(csvdata[pars['csv']['colorcolumn']-1], dtype=int)
        nullcolor = int(pars['color']['nullcolor'])
    else:
        print "Unable to handle color format: {}.".format(colorformat)
        quit()
    
    dictcolors2codes = {}
    for color, code in zip(colors, codes):
        if color not in dictcolors2codes:
            dictcolors2codes[color] = code
    
    colors = colors[np.isfinite(codes)]
    codes = codes[np.isfinite(codes)].astype(int)

    image_int = Utils.imagergb2int(image_rgb)

    image_1d = Utils.flattenimage(image_int, np.unique(colors), distmetric=pars['color']['distancemetric'], maxdistance=pars['color']['maxdistance'], gapcolor=nullcolor)

    image_1d = Utils.fillgaps(image_1d, gapcolor=nullcolor)
    
    layercolors, tops, bottoms = compresstotopbottom(image_1d, gapcolor=nullcolor)
    layercodes = np.empty(len(layercolors), dtype=int)
    for i in range(len(layercolors)):
        layercodes[i] = dictcolors2codes.get(layercolors[i], pars['log']['nullcode'])
    
    if imagefileextension in outputfileextensions:
        imageidx = outputfileextensions.index(imagefileextension)
        outputfileextensions.pop(imageidx)
        outputimagefilename = outputfilenames.pop(imageidx)
        
        image_1d2 = interpolate(np.arange(image_rgb.shape[0]), layercolors, tops, bottoms, nullvalue=nullcolor)
        image_int2 = Utils.fattenimage(image_1d2, image_rgb.shape[1])
        image_rgb2 = Utils.imageint2rgb(image_int2).astype(image_rgb.dtype)
        img = Image.fromarray(image_rgb2, 'RGB')
        img.save(outputimagefilename)
    
    top = pars['log']['topdepth']
    bottom = pars['log']['bottomdepth']
    mnem = pars['log']['lithologymnem']
    
    if top is None or bottom is None:
        top = 0
        bottom = image_rgb.shape[0] - 1
    else:
        tops = index2depth(tops, image_rgb.shape[0]-1, top, bottom)
        bottoms = index2depth(bottoms, image_rgb.shape[0]-1, top, bottom)
    
    if not mnem:
        mnem = 'CODE'
    
    textfileextension = 'txt'
    if textfileextension in outputfileextensions:
        textidx = outputfileextensions.index(textfileextension)
        outputfileextensions.pop(textidx)
        outputtextfilename = outputfilenames.pop(textidx)
        
        maxwidth = max(map(len, np.vstack((layercodes, tops, bottoms)).astype(str).flatten().tolist()))
        format = '{{:<{}}}'.format(maxwidth+1)*3
        text = []
        text.append(format.format(mnem, 'TOP', 'BOTTOM'))
        for c, t, b in zip(layercodes, tops, bottoms):
            text.append(format.format(c, t, b))
        
        with file(outputtextfilename, 'w') as f:
            f.write('\n'.join(text))
    
    lasfileextension = 'las'
    if lasfileextension in inputfileextensions and lasfileextension in outputfileextensions:
        inputlasidx = inputfileextensions.index(lasfileextension)
        outputlasidx = outputfileextensions.index(lasfileextension)
        
        inputlasfilename = inputfilenames[inputlasidx]
        outputlasfilename = outputfilenames[outputlasidx]
        
        las_input = LAS.open(inputlasfilename, 'r')
        las_input.read()
        
        las_output = LAS.open(outputlasfilename, 'w')
        las_output.header = LAS.LASWriter.correctcurvesection(las_input.header, las_input.curvesnames + [mnem], las_input.curvesunits + [''])
        las_output.header['C'][mnem]["DESC"] = "Created from an image using ImageToLithology"
        
        lithologylog = interpolate(las_input.data[0], layercodes, tops, bottoms, nullvalue=pars['log']['nullcode'], fillgaps=pars['log']['interpolate'], extrapolate=pars['log']['extrapolate'])
        
        las_output.data = np.append(las_input.data, lithologylog.reshape((1, -1)), axis=0)
        
        las_output.write()
