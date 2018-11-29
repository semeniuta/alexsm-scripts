#/bin/sh

#
# Copy LaTeX project to another directory 
# (only .tex, .bib, .cls files and figures in the Images directory)
#
# Example:
# cd /path/to/my/latex_project
# /path/to/cplatex.sh /path/to/parent/dst
#

declare -a masks=("*.tex" "*.cls" "*.bib")

if [ -z "$1" ]; then # checks for empty string
    echo "Parent directory is empty. Using $HOME/Desktop"
    parent_dir="$HOME/Desktop"
else
    parent_dir=$1
fi

current_dir_name=${PWD##*/} # top-level name of the current directory
out_dir="$parent_dir/$current_dir_name"

if [ -d "$out_dir" ]; then # if the directory exists
    echo "Directory $out_dir already exists. Exiting"
    exit 1
fi

mkdir $out_dir

for mask in "${masks[@]}"
do

    if ls $mask 1> /dev/null 2>&1; then
        cp -r $mask $out_dir
    fi

done

mkdir "$out_dir/Images"

for fig_file in Images/*
do
    
    # Copy files, not directories
    if [ -f "$fig_file" ]; then
        cp "$fig_file" "$out_dir/Images"
    fi

done

echo "Done: copied the project to $out_dir"