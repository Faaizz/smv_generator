#!/usr/bin/python3

#==============================================================================
# IMPORTS
import argparse, os, shutil, subprocess, json
from collections import OrderedDict

import main.declare as declare
import main.define as define
import main.assign as assign

#==============================================================================
# COMMAND-LINE HELP, OPTIONS, ARGUMENTS

cl_parser= argparse.ArgumentParser(
    description="Generate NuSMV for SIPN from JSON. Outputs result as output.smv"
    )

# Arguments
# Input JSON
cl_parser.add_argument(
    'input_json', metavar='source', nargs=1,
    help='Path to source JSON file'
    )

# Collect arguments
run_options= cl_parser.parse_args()


#====================================================================
# READ SOURCE FILE

with open(run_options.input_json[0]) as f:
    input_dict= json.load(f, object_pairs_hook=OrderedDict)


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
""" + declare.input_declaration(input_dict["inputs"])

# Place Declaration
declaration= declaration + """ 
-- PLACES
""" + declare.place_declaration(input_dict["places"])



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


#====================================================================
# OUTPUT

# Write to output file
with open("output.smv", "w") as f:
    f.write(declaration + definition + assignment)