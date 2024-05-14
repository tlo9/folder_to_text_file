#!/usr/bin/env python3

import os
from pathlib import Path
from typing import Union, Sequence
import sys
import re

DEFAULT_OUTFILE = 'output.txt'

def traverse_folder(folder_path: Union[Path, str, Sequence[Union[Path, str]]],
    no_header: bool = False,
    includes: Sequence[str] = [],
    excludes: Sequence[str] = [],
    verbose: bool = False,
    output_path: Union[Path, str] = DEFAULT_OUTFILE) -> None:
    """
    Traverse through the specified folder(s) and its subfolders, outputting file contents to a single file.
    
    Args:
        folder_path (Union[Path, str, Sequence[Union[Path, str]]]): 
            The path(s) of the folder(s) to traverse. Can be a single path as a string or 
            a Path object, or a sequence of paths.
        no_header (bool, optional): 
            If True, omits the header containing the file name before each file content in the output. 
            Defaults to False.
        includes (Sequence[str], optional): 
            A list of regular expressions to include specific file paths in the output. 
            Defaults to an empty list.
        excludes (Sequence[str], optional): 
            A list of regular expressions to exclude specific file paths from the output. 
            Defaults to an empty list.
        verbose (bool, optional): 
            If True, displays verbose logging output. Defaults to False.
        output_path (Union[Path, str], optional): 
            The file path where the concatenated output will be written. 
            Defaults to DEFAULT_OUTFILE, which is 'output.txt'.

    Returns:
        None
    """
    
    if not isinstance(folder_path, Sequence):
        folder_path = [folder_path]

    output_path = Path(output_path)

    with open(output_path, "w") as f:
        for fol_path in folder_path:
            for root, dirs, files in os.walk(fol_path):
                for file in files:

                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, fol_path)

                    if verbose:
                        print(relative_path, end='')
                    
                    # Skip any paths that don't match any of the include patterns
                    
                    if len(includes) > 0 and all(re.search(incl, relative_path) is None for incl in includes):
                        if verbose:
                            print(": not included.")
                        continue

                    # Skip any paths that match any of the exclude patterns
                        
                    if any(re.search(excl, relative_path) is not None for excl in excludes):
                        if verbose:
                            print(": excluded.")
                        continue

                    if not no_header:
                        f.write(f"---- File Name: \"{relative_path}\" ----\n")
    
                    try:
                        with open(file_path, 'rb') as file_content:
                            content = file_content.read()
                        try:
                            # Try decoding as UTF-8
                            content_decoded = content.decode('utf-8')
                        except UnicodeDecodeError:
                            # If decoding fails, replace non-decodable parts
                            content_decoded = content.decode('utf-8', errors='replace')
                        f.write(content_decoded + "\n")

                        if verbose:
                            print()
                    except (IOError, UnicodeError) as e:  # catch any reading errors
                        print(f"Error reading file {file_path}: {e}", file=sys.stderr)

def main() -> None:
    from argparse import ArgumentParser

    parser = ArgumentParser(
        prog=sys.argv[0],
        description="Traverses through a directory tree and concatenates the results of each file into a single file.")
    parser.add_argument('dirs', metavar='dir', nargs='+', help="The paths of the directories to traverse.")
    parser.add_argument('-e', '--exclude', dest='excludes', nargs='+',
                        default=[],
                        help="A list of regular expressions to exclude specific file paths from the output.")
    parser.add_argument('-i', '--include', dest='includes', nargs='+',
                        default=[],
                        help="A list of regular expressions to include specific file paths in the output.")
    parser.add_argument('-o', '--output', default=DEFAULT_OUTFILE,
                        dest='output', type=str,
                        help="The file path where the concatenated output will be written.")
    parser.add_argument('-v', '--verbose',
                        help="Display verbose logging output.",
                        dest='verbose',
                        action='store_true')
    parser.add_argument('-n', '--no-header',
                        dest='no_header',
                        help="Omit the header containing the file name before each file content in the output.",
                        action='store_true')

    args = parser.parse_args()
    traverse_folder(args.dirs,
                    no_header=args.no_header,
                    includes=args.includes,
                    excludes=args.excludes,
                    verbose=args.verbose,
                    output_path=args.output)

if __name__ == "__main__":
    main()

