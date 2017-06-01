# ImageToLithology

Converts an image file to a lithology log.

The repository has 3 mains programs:

1. `imagetolayers.py`: converts an image file (*.png, for example), to a CSV file with the layers found in the image.

2. `layerstoimage.py`: do the inverse of the previous program. It`s used for quality control purposes.

3. `layerstolas.py`: add the layers from a CSV file as a new curve in a LAS file.

The folder `sample` contains a sample synthetic dataset to test the program, as well the expected outputs of the 3 programs.

All programs provide a command line interface that is described below.

# Usage

## `imagetolayers.py` command line arguments

- `--imagefilename` (or `-i`): the file name of the image to be converted.
- `--csvfilename` (or `-c`): the file name of a CSV file containing the colors and codes of lithologies.
- `--csvcodecolumn` (optional): the column of the lithologies codes in the CSV file described above. Column counting starts from 1. If this argument is omitted, the first column will be used.
- `--csvcolorcolumn` (optional): the column of the lithologies colors in the CSV file described above. Column counting starts from 1. If this argument is omitted, the second column will be used.
- `--csvskiplines` (optional): number of lines that will be skipped when reading the CSV file (i.e. the header, or columnt titles). If this argument is omitted, a single line will be skipped.
- `--csvcolumnseparator` (optional): the column separator used in the CSV file. If this argument is omitted, comma (`,`) will be used as column separator.
- `--csvcolorformat` (optional): the color format used in the CSV file. For now, can be `html`, `rgb` or `int`. You can find more on this further in this document. If this argument is omitted, html formatting will be assumed.
- `--distancemetric` (optional): the distance metric to be used by the program. It can be one of the following: `human`, `l1`, `l2` or `max`. You can find more on this further in this document. If this argument is omitted, `human` distance will be used.
- `--maximumdistance` (optional): the maximum distance tolerated by the program to consider two colors as the same. You can find more on this further in this document. If this argument is omitted, `0.02` will be used.
- `--dontfillgaps` (optional): this argument don't have an associated value. If it is present, the gaps between layers of the same column will not be filled.
- `--topdepth` (or `-t`, optional): the depth associated with the top of the image. If this argument and `--bottomdepth` are both omitted, the pixel positions in the image will be used as the depth.
- `--bottomdepth` (or `-b`, optional): the depth associated with the bottom of the image. If this argument and `--topdepth` are both omitted, the pixel positions in the image will be used as the depth.
- `--topshift` (optional): a value to be added to the tops of the layers found by the program. If this argument is omitted, no shift will be performed.
- `--bottomshift` (optional): a value to be added to the bottoms of the layers found by the program. If this argument is omitted, no shift will be performed.
- `--columntitles` (optional): the titles of the three columns in the output file, namely: the lithology codes, tops and bottoms of the layers. If this argument is omitted, `CODE TOP BOTTOM` will be used.
- `--outputfilename`, `-o`: the name of the output CSV file.

## `layerstoimage.py` command line arguments
