# KICarver
A utility to extract game assets from KingsIsle WAD (KIWAD) files. 

### Usage
```python KICarver.py -o Extracted GameFile.wad```

```usage: KingsIsle Entertainment WAD Asset Extractor [-h] [-v] [-o OUTPUT] filename

A tool which extracts locally saved assets from KIWAD files. Creates folders and subdirectories in CWD

positional arguments:
  filename

options:
  -h, --help            show this help message and exit
  -v, --verbose
  -o OUTPUT, --output OUTPUT
                        The output directory for carved files
```

### Tool explanation 
Game data files can by default be found in ```C:\ProgramData\KingsIsle Entertainment\Wizard101\Data\GameData``` but this may change depending on your game installation location. File specification, which I based this tool on, was based on the research performed by Jon Palmisciano and can be found at https://github.com/jonpalmisc/libkiwad/blob/master/SPEC.org. The tool just extracts the WAD archive which contains all the game assets. Only files you have seen in game are actually compressed in the file so you will only see files you've seen them in game.
