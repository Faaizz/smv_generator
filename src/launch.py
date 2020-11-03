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

# Stop State
cl_parser.add_argument(
    '--stop', dest='stop', action="store_true",
    help='Generate transitions from every other marking to the idle state.'
    )

# Stop Place
cl_parser.add_argument(
    '--stop_place', dest='stop_place', action="store", default= "IDLE",
    help='Idle place name'
    )

# Stop Input
cl_parser.add_argument(
    '--stop_input', dest='stop_input', action="store", default= "STOP",
    help='Stop input name'
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

# Stop Transitions Definition
if (run_options.stop == True):
    definition= definition + """--- STOP PLACE\n""" + \
    define.stop_transitions_definition(run_options.stop_place, run_options.stop_input, input_dict["places"])
    # Stop stability
    stop_stable= " & " + define.stop_stab_definition(run_options.stop_place, input_dict["places"]) + ";\n"
else:
    stop_stable= ";\n"


# Stability Definition
definition= definition + """ 
-- STABLE
""" + define.stab_definition(input_dict["transitions"]) + stop_stable
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