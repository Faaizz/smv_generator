#!/usr/bin/python3

#==============================================================================
# IMPORTS
import argparse, os, shutil, subprocess, json
from collections import OrderedDict

import main.declare as declare
import main.define as define
import main.assign as assign
import main.spec as spec

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
""" + \
"-- " + str(list(input_dict["inputs"])) + "\n" + \
declare.input_declaration(input_dict["inputs"])

# Place Declaration
declaration= declaration + """ 
-- PLACES
""" + \
"-- " + str(list(input_dict["places"])) + "\n" + \
declare.place_declaration(input_dict["places"])



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
# SPECIFICATIONS

specification= """

--=====================================================================
--SPECIFICATIONS
--=====================================================================

"""
# Manual Specifications

try:
    specification= specification + spec.manual(input_dict["specifications"])
except KeyError as e:
    pass

#====================================================================
# OUTPUT

# Write to output file
with open("output.smv", "w") as f:
    f.write(declaration + definition + assignment + specification)