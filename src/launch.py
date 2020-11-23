#!/usr/bin/python3

#==============================================================================
# IMPORTS
import argparse, os, json
from collections import OrderedDict

import main.smv.declare as declare
import main.smv.define as define
import main.smv.assign as assign
import main.smv.spec as spec

import main.st.declare as st_declare
import main.st.define as st_define

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
# NuSMV
#====================================================================

#====================================================================
# DECLARATION

declaration= """
MODULE main

--=====================================================================
--DECLARATION
--=====================================================================

VAR

"""

# Input Declaration
declaration= declaration + """
-- INPUTS
""" + \
"-- " + str(list(input_dict["inputs"])) + "\n" + \
declare.input_declaration(input_dict["inputs"])

# Place Declaration
declaration= declaration + """ 
-- PLACES
""" + \
"-- " + str(list(input_dict["places"])) + "\n" + \
declare.place_declaration(input_dict["places"])

# Internal variable Declaration
try:
    internal_dict= input_dict["internals"]
    internal_mod, internal_main= declare.internal_declaration(internal_dict)

    declaration= internal_mod + declaration + internal_main
except:
    pass



#====================================================================
# DEFINITION

definition= """

--=====================================================================
--DEFINITION
--=====================================================================

DEFINE

"""

# Transition Definition
definition= definition + """
-- TRANSITIONS
""" + define.transition_definition(input_dict["transitions"])

# Stability Definition
definition= definition + """ 
-- STABLE
""" + define.stab_definition(input_dict["transitions"])
# Output Definition
definition= definition + """ 
-- OUTPUTS
""" + define.output_definition(input_dict["places"])


#====================================================================
# ASSIGNMENT

assignment= """

--=====================================================================
--ASSIGNMENT
--=====================================================================

ASSIGN

"""

# Input Assignment
assignment= assignment + """
-- INPUTS
""" + assign.input_assignment(input_dict["inputs"])

# Place Assignment
assignment= assignment + """ 
-- PLACES
""" + assign.place_assignment(input_dict["places"], input_dict["transitions"])

# Internal variable Declaration
try:
    internal_dict= input_dict["internals"]
    int_assign= assign.internal_assignment(internal_dict)

    assignment= assignment + int_assign
except:
    pass


#====================================================================
# SPECIFICATIONS

specification= """

--=====================================================================
--SPECIFICATIONS
--=====================================================================

"""
# Manual Specifications

try:
    specification= specification + spec.auto(input_dict)
    specification= specification + spec.manual(input_dict["specifications"])
except KeyError as e:
    pass

#====================================================================
# OUTPUT

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
        f.write(declaration + definition + assignment + specification)





#====================================================================
# STRUCTURED TEXT
#====================================================================

#====================================================================
# PROGRAM AND CONFIGURATION

# PROGRAM START
program_start= """
PROGRAM program0

"""
# PROGRAM END
program_end= """

END_PROGRAM

"""

# CONFIGURATION
configuration= """

CONFIGURATION config0

    RESOURCE res0 ON PLC
        TASK task0(INTERVAL := T#20ms, PRIORITY := 0);
        PROGRAM instance0 WITH task0 : program0;
    END_RESOURCE

END_CONFIGURATION

"""

#====================================================================
# DECLARATION

declaration= """

(*=====================================================================*)
(*DECLARATION*)
(*=====================================================================*)

VAR

"""

# Input/Output Declaration
declaration= declaration + """
(*INPUTS*)
""" + \
st_declare.input_declaration(input_dict["inputs"]) + \
st_declare.output_declaration(input_dict["outputs"]) + \
"""
END_VAR
"""


# Place Declaration
declaration= declaration + """

VAR

(*PLACES*)

""" + \
st_declare.place_declaration(input_dict["places"]) + \
"""
END_VAR

"""


#====================================================================
# TRANSITIONS

definition= """

(*=====================================================================*)
(*TRANSITIONS*)
(*=====================================================================*)

"""

# Transition 
definition= definition + st_define.transition_definition(input_dict["transitions"])


definition= definition + """

(*=====================================================================*)
(*OUTPUTS*)
(*=====================================================================*)

"""

# Outputs 
definition= definition + st_define.output_definition(input_dict["places"])



#====================================================================
# OUTPUT


# New file path
new_file_path= dir_path + file_name + ".st"

if st_enabled:
    # Write to output file
    with open(new_file_path, "w") as f:
        f.write(program_start + declaration + definition + program_end + configuration)