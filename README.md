# rename_files
Script to read a CSV file that contains a list of object IDs and GUIDs that 
renames .tif files from the object ID name to the GUID name.

# Usage
python3 file_move_script.py --csvfile [filename] --inputdir [input dir] --outpudir [outdir]

This script requires that you pass in the name of the .csv file that contains
the mappings between object IDs and GUIDs.  It requires that the .csv file
has column headers for Object ID and GUID, such as:

Object ID,GUID
orig:asdf,12345678

This script assumes the origin information from the object ID (everything 
before the colon) is not part of a filename, so it will ignore it when
looking for files to rename.
