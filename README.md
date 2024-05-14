# foldercat

Traverses through a directory tree and concatenates the results of each file into a single file.

A fork of [folder\_to\_text\_file](https://github.com/danielljones79/folder_to_text_file)

## Usage
```
python foldercat.py [-h] [-e EXCLUDES [EXCLUDES ...]]
                         [-i INCLUDES [INCLUDES ...]] [-o OUTPUT] [-v] [-n]
                         dir [dir ...]
```

### positional arguments:
```dir``` The paths of the directories to traverse.

### optional arguments:
```-h, --help``` show a help message and exit.

```-e EXCLUDES [EXCLUDES ...], --exclude EXCLUDES [EXCLUDES ...]```
    A list of regular expressions to exclude specific file
    paths from the output.

```-i INCLUDES [INCLUDES ...], --include INCLUDES [INCLUDES ...]```
    A list of regular expressions to include specific file
    paths in the output.

```-o OUTPUT, --output OUTPUT```
    The file path where the concatenated output will be
    written.

```-v, --verbose``` Display verbose logging output.

```-n, --no-header```
    Omit the header containing the file name before each
    file content in the output.


## To Run
```shell
python foldercat.py /path/to/your/folder -o output.txt
```
