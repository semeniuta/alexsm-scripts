#/bin/sh

#
# The scripts uses ImageMagick to convert figures in PDF 
# into the another format (e.g. JPEG, TIFF). 
#
# Converts all PDF files in the current directory 
#
# Can be supplied with the output directory 
# or save the output files in the current directory.
#
# Example:
# cd figures
# mkdir ~/Desktop/out_images
# /path/to/pdf2im.sh ~/Desktop/out_images jpg
#

if [ -z "$1" ]; then # checks for empty string
    echo "Output directory is empty. Using current directory"
    d="."
else
    d=$1
fi

echo "Output directory: $d"

if [ -z "$2" ]; then 
    echo "No output format specified. Using jpg"
    extension="jpg"
else
    extension=$2
fi

echo "Output format: $extension"

for f in *.pdf; do

    fn="${f%.*}" # file name without extension

    echo "Converting: $f -> $d/$fn.$extension"
    convert -density 300x300 $f $d/$fn.$extension
done;