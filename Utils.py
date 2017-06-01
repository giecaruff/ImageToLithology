import numpy as np
from scipy.interpolate import interp1d

def rgb2int(r, g, b):
	return r*256**2 + g*256 + b

def int2rgb(i):
	r = i // 256**2
	aux = i % 256**2
	g = aux // 256
	b = aux % 256
	return r, g, b

def html2rgb(h):
    r = int(h[1:3], 16)
    g = int(h[3:5], 16)
    b = int(h[5:7], 16)
    return r, g, b

def int2html(i):
    return '#{:0>6x}'.format(i)

def rgb2html(r, g, b):
    return '#{:0>2x}{:0>2x}{:0>2x}'.format(r, g, b)

def html2int(h):
    return rgb2int(*html2rgb(h))

def colordistance_humaneye(c1, c2):
    # source: https://www.compuphase.com/cmetric.htm
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    r_ = (r1 + r2)/510.0
    wr = 2.0 + r_
    wg = 4.0
    wb = 3.0 - r_
    dr = (r1 - r2)
    dg = (g1 - g2)
    db = (b1 - b2)
    dist = np.sqrt((wr*dr**2.0 + wg*dg**2.0 + wb*db**2.0))
    ndist = dist/(3.0*255.0)
    return ndist

def colordistance_l1(c1, c2):
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    dist = np.abs(r1 - r2) + np.abs(g1 - g2) + np.abs(b1 - b2)
    ndist = dist/(3.0*255.0)
    return ndist

def colordistance_l2(c1, c2):
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    dist = np.sqrt((r1 - r2)**2.0 + (g1 - g2)**2.0 + (b1 - b2)**2.0)
    ndist = dist/(3.0**0.5*255.0)
    return ndist

def colordistance_max(c1, c2):
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    dr = np.abs(r1 - r2)
    dg = np.abs(g1 - g2)
    db = np.abs(b1 - b2)
    dist = np.max((dr, dg, db))
    ndist = dist/(255.0)
    return ndist

dictcolordistance = dict(human=colordistance_humaneye, l1=colordistance_l1, l2=colordistance_l2, max=colordistance_max)

def imagergb2int(image_rgb):
    image_int = rgb2int(image_rgb[:, :, 0], image_rgb[:, :, 1], image_rgb[:, :, 2])
    return image_int

def imageint2rgb(image_int):
    image_rgb = np.transpose(np.array(int2rgb(image_int)), (1, 2, 0))
    return image_rgb

_MAXDISTANCE = 0.02
_NULL_COLOR = 0
_DISTMETRIC = 'human'

def flattenimage(image, colorlist, distmetric=_DISTMETRIC, maxdistance=_MAXDISTANCE, gapcolor=_NULL_COLOR):
    distfun = dictcolordistance[distmetric]
    
    nrows = image.shape[0]
    
    image_1d = np.empty(nrows, dtype=image.dtype)
    
    cache = {}
    
    for i in range(nrows):
        colors = np.unique(image[i, :])
        currentcolor = gapcolor
        distance = maxdistance
        
        for c1i in colors:
            for c2i in colorlist:
                
                key = frozenset((c1i, c2i))
                if key in cache:
                    dist = cache[key]
                else:
                    c1 = int2rgb(c1i)
                    c2 = int2rgb(c2i)
                    dist = distfun(c1, c2)
                    cache[key] = dist
                
                if dist <= distance:
                    currentcolor = c2i
                    distance = dist
        
        image_1d[i] = currentcolor
    
    return image_1d

def fattenimage(image_1d, ncols):
    image = np.reshape(image_1d, (image_1d.shape[0], 1))
    image = np.repeat(image, ncols, axis=1)
    return image

def fillgaps(image_1d, gapcolor=_NULL_COLOR):
    nrows = image_1d.shape[0]
    
    colorchange = np.empty(nrows, dtype=bool)
    colorchange[:-1] = (image_1d[1:] - image_1d[:-1]).astype(bool)
    colorchange[-1] = False
    
    colorchangeidxs = np.arange(nrows)[colorchange]
    
    changetogap = np.roll(np.roll(colorchange, 1)*(image_1d == gapcolor), -1)
    changefromgap = np.roll(colorchange*(image_1d == gapcolor), 1)
    
    ctbidxs = np.arange(nrows)[changetogap]
    cfbidxs = np.arange(nrows)[changefromgap]
    
    if image_1d[0] == gapcolor:
        cfbidxs = np.delete(cfbidxs, 0)
    
    if image_1d[-1] == gapcolor:
        ctbidxs = np.delete(ctbidxs, -1)
    
    newimage = np.copy(image_1d)
    
    for beg, end in zip(ctbidxs, cfbidxs):
        if image_1d[beg] == image_1d[end]:
            newimage[beg+1:end] = image_1d[beg]
    
    return newimage

def index2depth(index, n, top, bottom):
    depth = top + index/(n - 1.0)*(bottom - top)
    return depth

def depth2index(depth, n, top, bottom):
    index = (depth - top)/(bottom - top)*(n - 1.0)
    return index

def compress(image_1d, gapcolor=_NULL_COLOR):
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

def interpolate(new_x, y, tops, bottoms, nullvalue=_NULL_COLOR, fillgaps=False, extrapolate=False):
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
