import shutil
from argparse import ArgumentParser, Namespace, FileType
import csv
import re
import os.path



def main():
    try:
        # Parse the arguments passed to the application
        args = parse_args()
    except SystemExit:
        return -1

    # If the output directory is not specified, use the current working 
    # directory
    outdir = '.'
    if args.outdir != None:
        outdir = args.outdir

    # If the output directory is not specified, use the current working 
    # directory
    indir = '.'
    if args.indir != None:
        indir = args.indir


    with args.csvfile as csvfile:
        # Parse a comma-separated-value file
        filereader = csv.DictReader(csvfile, delimiter=',')

        # Choice to overwrite is false by default
        overwrite = 'no'

        # Files copied and skipped
        num_files_copied = 0
        num_files_skipped = 0
        num_files_not_exist = 0

        # For each row in the file...
        for row in filereader:

            # Strip off everything before the ':' from the front of the filenames
            # listed in the column titled 'Object ID'
            object_id_clean = row['Object ID'].split(
                ':')[-1]

            # Use the Object ID name along with the input directory as
            # the path to the original file 
            source_file_location = indir + '/' + object_id_clean + '.tif'

            # Use the GUID row value along with the output directory as
            # the path to the output file
            destination_file_location = outdir + '/' + row['GUID'] + '.tif' 

            # Indicate that we are copying a file
            print ('Copying', source_file_location, 'to', 
                destination_file_location, '...')

            # Check if the destination file exists.  Ask to proceed.
            if os.path.exists(destination_file_location) and \
                overwrite != 'all':

                overwrite = input('Destination file ' + 
                    destination_file_location + ' exists.  Overwrite? ' + 
                    '(yes/y, no/n, all/a)')

                # Normalize the string to 'all'
                if overwrite == 'a':
                    overwrite = 'all'

                # Normalize n to no
                if overwrite == 'n':
                    overwrite = 'no'

                if overwrite == 'no':
                    print (source_file_location, 'not copied.')
                    num_files_skipped += 1
                    continue

                # if the user hasn't selected overwriting all, reset to 'no'
                # for the next file
                if overwrite != 'all':
                    overwrite = 'no'

            # Check if the origin file exists.  Copy it to the name in the
            # column titled 'GUID,' print a warning if it does not
            if os.path.exists(source_file_location):
                try:
                    shutil.copyfile(
                        source_file_location, 
                        destination_file_location)
                    num_files_copied += 1
                except:
                    print('Cannot write to location ' + outdir + '. Exiting.')
                    return
            else:
                num_files_not_exist += 1
                print('File \'' + object_id_clean +
                    '.tif\' does not exist in directory')

        # Print final statistics
        print (
            'Files copied: {}. Files skipped: {}. Nonexistent files: {}'.format( 
            num_files_copied,
            num_files_skipped,
            num_files_not_exist))  

def parse_args() -> Namespace:
    """This method parses command-line arguments"""
    parser = ArgumentParser(
        description =\
            'Copy .tif files from their object ID name to a GUID name, based' +
            ' on values in a .csv spreadsheet')

    # Arguments that can be passed to this script
    parser.add_argument(
        '--csvfile', 
        metavar='CSVFILE',
        dest='csvfile', 
        type=FileType('r'),
        required=True,
        help='CSV file describing the \'to\' and \'from\' filenames. \n' +
            'This uses the column \'Object ID\' to determine the source,\n' +
            'and column \'GUID\' to determine the destination file name.')

    parser.add_argument(
        '--inputdir', 
        metavar='INDIR', 
        dest='indir', 
        type=str, 
        help='Directory where original files are located.  If not \n' +
             'specified, uses the current directory (where you are running\n' +
             ' from)')

    parser.add_argument(
        '--outputdir', 
        metavar='OUTDIR', 
        dest='outdir', 
        type=str, 
        help='Directory to put renamed files into.  If not specified, uses\n' +
             'the current directory (where you are running from)')

    return parser.parse_args()

if __name__ == "__main__":
    main()
