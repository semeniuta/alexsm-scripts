# alexsm-scripts

Python and Bash scripts for source code analysis, image format manipulations, enhancement of the output of standard Unix tools, backing up Unix configuration files, and other use cases. 

All examples below presume that the directory containing the scripts is added to the `PATH` environment variable.

## apthist

Parses the `apt` history log on Ubuntu/Debian (`/var/log/apt/history.log`) with different output options. 

Since `history.log` gets eventually archived, the script allows supplying the `--file` argument to speicify e.g. a combined history from all archives and the current log. 

The `list` action outputs for each entry (index, date and time key, invoked command):

```bash
python apthist.py list
python apthist.py list --file /path/to/custom/history.log
```

The `describe` actions provides a detailed description 
of a particular entry indentified by its index from `list`:

```bash
python apthist.py describe --index 10
python apthist.py describe --index 10 --file /path/to/custom/history.log
```

The `packages` action prints a list of packages installed (one per line) for an entry identified by the index from `list`:

```bash
python apthist.py packages --index 10
```

## depfind

Find dependencies (imported Python modules) recursively in a directory

Usage example:

```python
python depfind.py EPypes/epypes/
```

## findtree

Visualize the file system structure of the result of find command in a tree form. 

In the following example, the current directory is searched for all Jupyter notebooks excluding the checkpoints, with the result being piped to `findtree`:

```bash
find . -name "*.ipynb" ! -name "*-checkpoint.ipynb" | python findtree.py
```

## grepimports

Find all imports of the specified Python package in both Python files and Jupyter notebooks

In the following example, all Python and Jupyter files in the `my_project` directory are scanned to find imports of `numpy`:

```bash
grepimports.sh numpy my_project
```

## libraryuse 

Process the output of `grepimports.sh` and display lists  of the importing Python scripts or Jupyter notebooks, grouped by each individual imported module.

Example:

```bash
grepimports.sh numpy my_project | python libraryuse.py
```

## pdf2im

The scripts uses ImageMagick to convert PDF figures in the current directory into the another format (e.g. JPEG, TIFF). The script can be supplied with the output directory or save the output files in the current directory.

In the following example, all PDFs in the `figures` directory to JPEG and saves them in `~/Desktop/out_images`:

```bash
cd figures
mkdir ~/Desktop/out_images
pdf2im.sh ~/Desktop/out_images jpg
```

## rmlatexaux

Remove auxillary LaTeX-produced files (`aux`, `log`, `synctex.gz`, `bbl`, `blg`) from the current directory.

```bash
cd my_latex_paper
rmlatexaux
```

## cplatex

Copy important files of a LaTeX project to another directory. Files that get copied:
`tex`, `bib`, `cls` and figures in the `Images` directory (so far the solution is too custom/rigid and shall be made more flexible).

Example:

```bash
mkdir ~/Desktop/my_latex_paper_backup

cd /path/to/my_latex_paper
cplatex.sh ~/Desktop/my_latex_paper_backup
```

## confbackup

Backup Unix configuration files on macOS, Ubuntu, and Raspbian, and saves the backup in a directory tagged with a timestamp, e.g. `~/confbackup_2018-10-31_080945`.

The default parent directory (`~`) can be overriden with the `--out` parameter

Usage examples:

```bash
python confbackup.py --plaform pi
python confbackup.py --plaform ubuntu --out /dir/to/save
```

