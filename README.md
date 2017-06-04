# ImageToLithology

Converts an image file to a lithology log.

The repository has 3 mains programs:

1. `imagetolayers.py`: converts an image file (*.png, for example), to a CSV file with the layers found in the image.

2. `layerstoimage.py`: do the inverse of the previous program. It's used for quality control purposes.

3. `layerstolas.py`: add the layers from a CSV file as a new curve in a LAS file.

The folder `sample` contains a sample synthetic dataset to test the program, as well the expected outputs of the 3 programs.

All programs provide a command line interface that is described below.

# Usage

## `imagetolayers.py` command line arguments

- `--imagefilename` (or `-i`): file name of the image to be converted.
- `--csvfilename` (or `-c`): file name of a CSV file containing the colors and codes of lithologies.
- `--csvcodecolumn` (optional): column number of the lithologies codes in the CSV file described above. Column counting starts from 1. If this argument is omitted, the first column will be used.
- `--csvcolorcolumn` (optional): column number of the lithologies colors in the CSV file described above. Column counting starts from 1. If this argument is omitted, the second column will be used.
- `--csvskiplines` (optional): number of lines that will be skipped when reading the CSV file (i.e. the header, or columnt titles). If this argument is omitted, a single line will be skipped.
- `--csvcolumnseparator` (optional): column separator used in the CSV file. If this argument is omitted, comma (`,`) will be used as column separator.
- `--csvcolorformat` (optional): color format used in the CSV file. For now, can be `html`, `rgb` or `int`. You can find more on this further in this document. If this argument is omitted, html formatting will be assumed.
- `--distancemetric` (optional): distance metric to be used by the program. It can be one of the following: `human`, `l1`, `l2` or `max`. You can find more on this further in this document. If this argument is omitted, `human` distance will be used.
- `--maximumdistance` (optional): maximum distance tolerated by the program to consider two colors as the same. You can find more on this further in this document. If this argument is omitted, `0.02` will be used.
- `--dontfillgaps` (optional): this argument don't have an associated value. If it is present, the gaps between layers of the same column will not be filled.
- `--topdepth` (or `-t`, optional): depth associated with the top of the image. If this argument and `--bottomdepth` are both omitted, the pixel positions in the image will be used as the depth.
- `--bottomdepth` (or `-b`, optional): depth associated with the bottom of the image. If this argument and `--topdepth` are both omitted, the pixel positions in the image will be used as the depth.
- `--topshift` (optional): a value to be added to the tops of the layers found by the program. If this argument is omitted, no shift will be performed.
- `--bottomshift` (optional): a value to be added to the bottoms of the layers found by the program. If this argument is omitted, no shift will be performed.
- `--columntitles` (optional): titles of the three columns in the output file, namely: lithology codes, tops and bottoms of the layers. If this argument is omitted, `CODE TOP BOTTOM` will be used.
- `--outputfilename`, `-o`: name of the output CSV file.

## `layerstoimage.py` command line arguments

- `--layersfilename` (or `-i`): file name of the CSV file containing the layers data.
- `--layerscodecolumn` (optional): column number of the lithologies codes in the CSV file passed in `--layersfilename`. Column counting starts from 1. If this argument is omitted, the first column will be used.
- `--layerstopcolumn` (optional): column number of the tops of the layers in the CSV file passed in `--layersfilename`. Column counting starts from 1. If this argument is omitted, the second column will be used.
- `--layersbottomcolumn` (optional): column number of the bottoms of the layers in the CSV file passed in `--layersfilename`. Column counting starts from 1. If this argument is omitted, the third column will be used.
- `--layerskiplines` (optional): number of lines that will be skipped when reading the CSV file passed in `--layersfilename` (i.e. the header, or columnt titles). If this argument is omitted, a single line will be skipped.
- `--csvfilename` (or `-c`): file name of a CSV file containing the colors and codes of lithologies.
- `--csvcodecolumn` (optional): column number of the lithologies codes in the CSV file passed in `--csvfilename`. Column counting starts from 1. If this argument is omitted, the first column will be used.
- `--csvcolorcolumn` (optional): column number of the lithologies colors in the CSV file passed in `--csvfilename`. Column counting starts from 1. If this argument is omitted, the second column will be used.
- `--csvskiplines` (optional): number of lines that will be skipped when reading the CSV file passed in `--csvfilename` (i.e. the header, or columnt titles). If this argument is omitted, a single line will be skipped.
- `--csvcolumnseparator` (optional): column separator used in the CSV file. If this argument is omitted, comma (`,`) will be used as column separator.
- `--csvcolorformat` (optional): color format used in the CSV file. For now, can be `html`, `rgb` or `int`. You can find more on this further in this document. If this argument is omitted, html formatting will be assumed.
- `--nullcolor` (optional): color to be used when there is a gap between layers. Should use the format specified in the argument above. If this argument is omitted, black will be used.
- `--topdepth` (or `-t`, optional): depth associated with the top of the image. If this argument and `--bottomdepth` are both omitted, the pixel positions in the image will be used as the depth.
- `--bottomdepth` (or `-b`, optional): depth associated with the bottom of the image. If this argument and `--topdepth` are both omitted, the pixel positions in the image will be used as the depth.
- `--topshift` (optional): a value to be added to the tops of the layers found by the program. If this argument is omitted, no shift will be performed.
- `--bottomshift` (optional): a value to be added to the bottoms of the layers found by the program. If this argument is omitted, no shift will be performed.
- `--width`: width of the output image in pixels.
- `--height`: height of the output image in pixels.
- `--outputfilename` (or `-o`): name of the output image file.

## `layerstolas.py` command line arguments

- `--layersfilename` (or `-i`): file name of the CSV file containing the layers data.
- `--layerscodecolumn` (optional): column number of the lithologies codes in the CSV file passed in `--layersfilename`. Column counting starts from 1. If this argument is omitted, the first column will be used.
- `--layerstopcolumn` (optional): column number of the tops of the layers in the CSV file passed in `--layersfilename`. Column counting starts from 1. If this argument is omitted, the second column will be used.
- `--layersbottomcolumn` (optional): column number of the bottoms of the layers in the CSV file passed in `--layersfilename`. Column counting starts from 1. If this argument is omitted, the third column will be used.
- `--layerskiplines` (optional): number of lines that will be skipped when reading the CSV file passed in `--layersfilename` (i.e. the header, or columnt titles). If this argument is omitted, a single line will be skipped.
- `--layersemptycell` (optional): value that should be interpreted as an empty cell when reading the CSV file passed in `--layersfilename`. Only the top of the first layer or the bottom of the last layer can be empty. If this argument is omitted, only textless cells will be considered empty.
- `--csvfilename` (or `-c`, optional): file name of a CSV file containing the colors and codes of lithologies. In this program this file should only be used to "translate" the code value in the layers CSV file. For example, if the text code was used in the layers CSV it should be translated to a numeric value.
- `--csvcode1column` (optional): column number of the lithologies codes present in the CSV file passed in `--layersfilename`. Column counting starts from 1. If this argument is omitted, the first column will be used.
- `--csvcode2column` (optional): column number of the lithologies colors to which those in the CSV file passed in `--layersfilename` will be translated. Column counting starts from 1. If this argument is omitted, the second column will be used.
- `--csvskiplines` (optional): number of lines that will be skipped when reading the CSV file passed in `--csvfilename` (i.e. the header, or columnt titles). If this argument is omitted, a single line will be skipped.
- `--csvcolumnseparator` (optional): column separator used in the CSV file. If this argument is omitted, comma (`,`) will be used as column separator.
- `--topshift` (optional): a value to be added to the tops of the layers found by the program. If this argument is omitted, no shift will be performed.
- `--bottomshift` (optional): a value to be added to the bottoms of the layers found by the program. If this argument is omitted, no shift will be performed.
- `--wellfilename`: file name of the input LAS file.
- `--depthmnem` (optional): mnemoic of the depth "curve" in the input LAS file. If this argument is omitted, the first curve will be used as the depth (as specified in the LAS 2.0 standard).
- `--mnem` (optional): mnemoic of the curve that will be created. If this argument is omitted, the name found on the appropriate CSV file column header will be used.
- `--unit` (optional): unit of the curve that will be created. If this argument is omitted, the new curve will have no unit.
- `--nullcode` (optional): code number that will be used where there is no value for the new curve. If this argument is omitted, -1 will be used.
- `--interpolate` (optional): this argument don't have an associated value. If it is present, gaps between layers will be interpolated.
- `--outputfilename` (or `-o`): name of the output LAS file.
