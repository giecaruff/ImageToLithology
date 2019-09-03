# ImageToLithology

Converts an image file to a lithology log.

It is common (at least in Brazilian universities) to have the lithologic log for a well in an image file (as part of a report in a PDF format, for example) and the wireline logs in a LAS file. Transform this data into a useful format is often a laborious task. The goal of this repository is to provide an automatic solution for this issue. Only three files are necessary:

- the image file (preferably in high resolution and with no compression, for preserving the colors);

- a CSV file that "translates" the colors into lithologies codes;

- the LAS file (actually this is optional, as will be seen further).

The repository has 3 main programs:

1. `imagetolayers.py`: converts an image file (*.png, for example), to a CSV file with the layers found in the image.

2. `layerstoimage.py`: do the inverse of the previous program. It's used for quality control purposes.

3. `layerstolas.py`: add the layers from a CSV file as a new curve in a LAS file.

## Dependencies

This program only has three dependencies:

- `numpy`: arrays manipulation;
- `scipy`: data interpolation;
- `imageio`: image input/output.

It was developed and tested using:

- `Python 3.7.3 64 bit on win32`
- `numpy 1.17.1`
- `scipy 1.3.1`
- `PIL 2.5.0`

If you wish, you can use [`pipenv`](https://github.com/pypa/pipenv) to install all dependencies using the following command:

```
cd path\to\ImageToLighology
pipenv install
```

## Sample data

The folder `sample` contains a synthetic dataset to test the program, as well the expected outputs of the 3 programs. Below are the sample input image and CSV files:

- Sample image (usually it will be way taller):

    ![Sample input image](https://github.com/rcg-uff/ImageToLithology/blob/master/sample/figure.png)

- Sample CSV (in Portuguese):

    ```csv
    LITOLOGIA,ABREVIACAO,COR,CODIGO
    ANIDRITA,AND,#dd1dff,82
    ARDOSIA,ARS,#00dd00,77
    AREIA,ARE,#ffff3f,48
    ARENITO,ARN,#ffff3f,49
    ARENITO ARGILOSO,ARL,#7eff00,25
    ARENITO CARBONATICO,ARC,#3fbeff,26
    ARENITO CONGLOMERATICO,ARO,#ffbe1d,27
    ARENITO FOSFATICO,ARF,#ffff3f,28
    ARENITO TOBACEO,ART,#dddddd,29
    ARGILA,ARG,#7eff00,55
    ARGILITO,AGT,#7eff00,56
    ...
    ```

All programs provide a command line interface that are described below.

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
- `--wellfilename` (or `-w`): file name of the input LAS file.
- `--depthmnem` (optional): mnemoic of the depth "curve" in the input LAS file. If this argument is omitted, the first curve will be used as the depth (as specified in the LAS 2.0 standard).
- `--mnem` (optional): mnemoic of the curve that will be created. If this argument is omitted, the name found on the appropriate CSV file column header will be used.
- `--unit` (optional): unit of the curve that will be created. If this argument is omitted, the new curve will have no unit.
- `--nullcode` (optional): code number that will be used where there is no value for the new curve. If this argument is omitted, -1 will be used.
- `--interpolate` (optional): this argument don't have an associated value. If it is present, gaps between layers will be interpolated.
- `--outputfilename` (or `-o`): name of the output LAS file.

## Example

This example uses the data in the folder `sample`. To generate a CSV file containing the layers from the image `figure.png` the following command should be used:

```
python imagetolayers.py -i sample\figure.png -c sample\colors.csv --csvcodecolumn 4 --csvcolorcolumn 3 -t 585.125 -b 635.0 -o sample\output.csv
```

The arguments `--csvcodecolumn 4` and `--csvcolorcolumn 3` were used because the lithologies codes and colors are, respectively in the the fourth and third columns in the CSV file. The top and bottom depths (`-t 585.125 -b 635.0`) were obtained from the LAS file. Note that the used image may be relative only to a part of the well, and not necessarily the whole well. The default values for the other arguments were used. The output file is shown below:

```csv
CODE,TOP,BOTTOM
21,585.125,596.25
57,597.0,601.25
48,602.0,614.75
57,615.5,618.5
48,619.25,629.875
66,630.625,635.0
```

For quality control of the generated file, it is advised to run `layerstoimage.py` in order to produce a new image for comparison with the original one. For doing so, this command was used:

```
python layerstoimage.py -i sample\output.csv -c sample\colors.csv --csvcodecolumn 4 --csvcolorcolumn 3 -t 585.125 -b 635.0 --width 400 --height 400 -o sample\output.png
```

The output image shape (`--width 400 --height 400`) was choosen to match the original image. The image produced in this step is shown below:

![Sample output image](https://github.com/rcg-uff/ImageToLithology/blob/master/sample/output.png)

Note that it perfectly matches the original image (that was shown in the beggining of this document). It may not always be the case.

The final step is to add the layers obtained from the image as a curve in a LAS file. In this example it is done using this command:

```
python layerstolas.py -i sample\output.csv -w sample\welllog.las -o sample\output.las
```

An excerpt of the output LAS file is shwon below:

```
...
~C
 DEPT.M                         :                                             
 AAA .BBB                       :                                             
 CCC .DDD                       :                                             
 CODE.                          : Created from an image using ImageToLithology
~A
       635     0.0045     1.0144         66
   634.875     0.0074     1.0578         66
    634.75      0.063     1.0438         66
   634.625     0.0441     1.0293         66
     634.5     0.1379     0.9951         66
   634.375     0.0751      1.033         66
    634.25     0.0451     0.9921         66
...
```

Note that since the new curve mnemoic was not specified, it was used the column title of the layers' CSV file. In its turn, the column titles were also not specified when creating the layers' CSV file, and the default titles were used.

# Known issues/limitations

Images where the colors in the same lithology are not homogeneous can perform badly. It may occur in compressed images where the color values are not preserved. Can also happens when the image comes from a photography or scanner (though this kinds of images have not been tested).

The `imagetolayers.py` program cannot differentitate between lithologies with the same color but different hatch patterns. Actually the program can detect hatch patterns at all.

In cases where there is more than one lithology with the same color in the CSV value the first occurrance will be used.

# Other topics

## Color format

Right now the programs support only three color formats: `html`, `rgb` and `int`. The `html` is the default format used in html files and many other programs. It consists of a hash symbol (`#`) followed by 6 hexadecimal characters. The first two decimal caracters represent the red value, the next two, the green value, and the last two the blue value. The `rgb` format is composed of 3 integer numbers between 0 and 255 separated by spaces. The numbers are the red, green and blue values, respectively. Lastly, the `int` format is an integer number. The number value for a color is the equivalent to convert a `html` value of this color (minus the `#`) from hexadecimal to decimal. Below are some colors examples in the three formats:

| Color | `html`  | `rgb`       | `int`    |
| :---- | :------ | :---------- | :------- |
| White | #ffffff | 255 255 255 | 16777215 |
| Black | #000000 | 0 0 0       | 0        | 
| Red   | #ff0000 | 255 0 0     | 16711680 |
| Green | #00ff00 | 0 255 0     | 65280    |
| Blue  | #0000ff | 0 0 255     | 255      |

## Color distance and max distance

Due to many reasons, the colors in the image file might not perfectly match those specified in the CSV file. When there is no perfect match, the color in the CSV file that is closest to the color in the image is chosen.

There are four different metrics for calculating the distance between two colors: `human`, `l1`, `l2` and `max`. For all metrics the colors are considered as a 3 dimensional vector, with the dimensions being the red, green and blue values. The `human` distance metric is a mathematical approximation of how the human eye perceives colors. The `l1` metric (as the name implies) calculates the l1-norm distance between the colors (also known as Manhattan distance). Similarly, the `l2` metric calculates the l2-norm distance (also known as Euclidian distance). The `max` distance uses the maximum absolute value in the difference vector between the colors. All metrics are normalized in such a way that the distance between white (`#ffffff` in `html` format) and black (`#000000`) is equal to 1.0.

A maximum allowed distance can be specified using the `--maxdistance` argument (which defaults to 0.02). When the color in the image exceeds the maximum distance for all available colors in the CSV file, it is attributed a null color value for this color. For avoiding errors, the maximum allowed distance should be less than half of the minimum distance between colors in the CSV file (this does not hold for the `human` metric, since the triangle inequality does not hold true for this metric).
