#!/usr/bin/python3

#==============================================================================
# IMPORTS
import argparse, os, json
from collections import OrderedDict

import main.generate_smv_st as generate_smv_st

#==============================================================================
# COMMAND-LINE HELP, OPTIONS, ARGUMENTS

cl_parser= argparse.ArgumentParser(
    description="Generate NuSMV ans ST for SIPN from JSON."
    )

# Arguments
# Input JSON
cl_parser.add_argument(
    'input_json', metavar='source', nargs=1,
    help='Path to source JSON file'
    )

# SMV Only
cl_parser.add_argument(
    '--smv', action='store_true',
    help='Generate NuSMV only'
    )

# ST Only
cl_parser.add_argument(
    '--st', action='store_true',
    help='Generate ST only'
    )

# Collect arguments
run_options= cl_parser.parse_args()


st_enabled= False
smv_enabled= False

if run_options.smv or run_options.st:
    if run_options.smv:
        smv_enabled= True
    
    if run_options.st:
        st_enabled= True

else:
    smv_enabled= True
    st_enabled= True

#====================================================================
# READ SOURCE FILE

with open(run_options.input_json[0]) as f:
    input_dict= json.load(f, object_pairs_hook=OrderedDict)

#====================================================================
# OUTPUT

# GENERATE OUTPUT
output_smv= generate_smv_st.smv(input_dict)

input_path= run_options.input_json[0]

# Prepare output file path
old_file_name= os.path.basename(input_path)

# Remove filename from path
dir_path= os.path.abspath(input_path).replace(old_file_name, "")

# Remove extension from filename if it exists
file_name= old_file_name.split(".")[0]

# New file path
new_file_path= dir_path + file_name + ".smv"

if smv_enabled:
    # Write to output file
    with open(new_file_path, "w") as f:
        f.write(output_smv)







#====================================================================
# OUTPUT

# GENERATE ST
output_st= generate_smv_st.st(input_dict)

# New file path
new_file_path= dir_path + file_name + ".st"

if st_enabled:
    # Write to output file
    with open(new_file_path, "w") as f:
        f.write(output_st)