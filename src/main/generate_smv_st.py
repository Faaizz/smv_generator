#==============================================================================
# IMPORTS
import json
from collections import OrderedDict

from .smv import declare as declare
from .smv import define as define
from .smv import assign as assign
from .smv import spec as spec

from .st import declare as st_declare
from .st import define as st_define


def smv(input_dict):

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


    #OUTPUT
    output_smv= declaration + definition + assignment + specification

    return output_smv




def st(input_dict):
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

    # Internal variables Declaration
    try:
        int_dec= st_declare.internal_declaration(input_dict["internals"])

        declaration= declaration + """
VAR

(*INTERNAL VARIABLES*)

""" + int_dec + \
"""
END_VAR

"""
    except:
        print("No internal variables to declare in ST")

    #====================================================================
    # DEFINITIONS
    definition= ""

    # Internal variables Initialization
    try:
        int_init= st_define.internal_definition(input_dict["internals"])

        definition= definition + int_init
    except:
        print("No internal variables to initialize in ST")

    # TRANSITIONS
    definition= definition + """

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

    output_st= program_start + declaration + definition + program_end + configuration

    return output_st

