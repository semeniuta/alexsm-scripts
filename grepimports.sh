#/bin/sh

#
# Find all imports of the specified Python package
# in both Python files and Jupyter notebooks
#
# Usage:
# grepimports mypackage /directory/to/search
#

if [ "$#" -ne 2 ]; then
    echo "Illegal number of arguments (should be 2, you've got $#)"
    exit 1
fi

py_module=$1
search_dir=$2

egrep -r "(import $py_module|from $py_module)" \
  --include "*.ipynb" \
  --include "*.py" \
  --exclude "*.ipynb_checkpoints*" \
  $search_dir 