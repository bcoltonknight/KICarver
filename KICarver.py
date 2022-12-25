import struct
import os
import zlib
import argparse


def initargs():
    parser = argparse.ArgumentParser(
        prog='KingsIsle Entertainment WAD Asset Extractor',
        description='A tool which extracts locally saved assets from KIWAD files. Creates folders and subdirectories in CWD',
        epilog='Be gay, do crime :)'
    )
    parser.add_argument('filename')
    parser.add_argument('-v', '--verbose',
                        action='store_true')
    parser.add_argument('-o', '--output',
                        default='',
                        help='The output directory for carved files')
    return parser.parse_args()


def extract(data, compressed, fileName):
    # Ensure file has local save
    if list(filter(lambda x: x != 0, data)) == []:
        return False

    # Create directories if need be
    if not os.path.exists(os.path.dirname(fileName)) and os.path.dirname(fileName) != '':
        os.makedirs(os.path.dirname(fileName), exist_ok=True)

    # Extract uncompressed data
    if not compressed:
        with open(fileName, 'wb') as f:
            f.write(data)

    # Extract compressed data
    else:
        with open(fileName, 'wb') as f:
            f.write(zlib.decompress(data))

    # If nothing failed return True
    return True


if __name__ == '__main__':
    MAGIC_BYTE_OFFSET = 5
    args = initargs()

    # Validate input file exists
    if not os.path.isfile(args.filename):
        print('[!] Filename must be a file!')
        exit(1)

    # Normalize outout folder format
    if args.output != '' and args.output[-1] != '/':
        args.output = args.output + '/'

    # Set the index of the first file
    fileIndex = 13

    # Open and read file data
    wadBytes = open(args.filename, 'rb').read()

    # Validate file is actually a valid KIWAD file by reading first five magic bytes
    if wadBytes[0:5] != b'KIWAD':
        print('[!] File must be a KIWAD file')
        quit(1)

    # Initialize struct objects
    headerStruct = struct.Struct('I I')
    fileStruct = struct.Struct('=I I I ? I I')

    # Unpack header data and adjust script accordingly
    version, numFiles = headerStruct.unpack(wadBytes[MAGIC_BYTE_OFFSET:13])
    print(f'[*] Archive version: {version}')
    print(f'[*] Compressed Files: {numFiles}')
    print('*' * 35)

    # If version is two, a padding byte is added to the end of the headers, so increment the index by one
    if version == 2:
        fileIndex += 1

    # Iterate through all files
    for i in range(numFiles):
        # Unpack file data information
        offset, size, comp_size, compressed, checksum, path_len = fileStruct.unpack(wadBytes[fileIndex:fileIndex+21])
        fileName = struct.unpack(f'{path_len - 1}s', wadBytes[fileIndex + 21:fileIndex + 20 + path_len])[0].decode()

        # Print information for debugging/it being kinda neat
        if args.verbose:
            print(f'File Offset: {offset}')
            print(f'File Size: {size}')
            print(f'Compressed Size: {comp_size}')
            print(f'Compressed?: {compressed}')
            print(f'Checksum: {checksum}')
            print(f'Path Length: {path_len}')
            print(f'File Path: {fileName}')
        try:
            # Attempt to extract file from the data at the location of the extracted offset
            extracted = extract(wadBytes[offset:offset+size], compressed, args.output + fileName)

            # Check if there was data extracted
            if extracted:
                print(f'[*] Extracted {fileName} successfully')
            else:
                print(f'[!] {fileName} was an empty file')
        except Exception as e:
            # Catch errors and print them for debugging
            print(f'[!] Failed to extract {fileName} due to {e}')
        if args.verbose:
            print('*' * 35)
        # Increment by the known length of the file info + the length of the path string
        fileIndex = fileIndex + 21 + path_len
