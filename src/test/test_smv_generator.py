import unittest, json
from collections import OrderedDict

import main.smv.declare as declare
import main.smv.define as define
import main.smv.assign as assign
import main.smv.spec as spec

class VariablesDeclarationTest(unittest.TestCase):

    #================================================================
    ## DECLARATIONS

    def test_input_declaration(self):
        
        # Json input
        input_str= r"""
        {
            "S_AL1_ST1": ["boolean", "%IX100.0"],
            "S_AL1_ST2": ["boolean", "%IX100.1"],
            "STATUS": [
                [
                    "{\"stopped\", \"running\"}",
                    "stopped",
                    "{\"stopped\", \"running\"}"
                ],
                "%IX100.2"
            ],
            "AL1_ST_X_POS": [
                [
                    "{0, 400, 860}",
                    0,
                    "{0, 400, 860}"
                ],
                "%IW100",
                "INT"
            ],
            "AL1_ST_Y_POS": [
                [
                    "{0, 300, 560}",
                    0,
                    "{0, 300, 560}"
                ],
                "%IW101",
                "INT"
            ]
        }
        """

        # Expected MuSMV
        expected= 'S_AL1_ST1: boolean;\n' + \
            'S_AL1_ST2: boolean;\n' + \
            'STATUS: {"stopped", "running"};\n' + \
            'AL1_ST_X_POS: {0, 400, 860};\n' + \
            'AL1_ST_Y_POS: {0, 300, 560};\n'

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str, object_pairs_hook=OrderedDict)

        # Test
        self.assertMultiLineEqual(expected, declare.input_declaration(input_dict))

    
    def test_place_declaration(self):

        # Json input
        input_str= """
        {
            "PS2": [
                [
                    ["RP_AL1_ST_CLAMP"], ["AL1_ST_GRAB"]
                ],
                "Product gets withing graber range"
            ],
           "PS4": [
                [
                    ["RP_AL1_ST_CLAMP"], ["AL1_ST_GRAB"]
                ],
                ["AL1_ST_Z_SET:=750"],
                "Move grabber down to pick up product"
            ],
            "PSE0": [
                [
                    [], ["AL1_EMIT", "RC_AL1_ST"]
                ],
                "New box arrived, stop conveyor"
            ],
            "initial": ["PS2", "PSE0"]
            
        }
        """

        # Expected NuSMV
        expected= "PS2: boolean;\n" + "PS4: boolean;\n" + "PSE0: boolean;\n"

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str, object_pairs_hook=OrderedDict)

        # Test
        self.assertMultiLineEqual(expected, declare.place_declaration(input_dict))

    
    #================================================================
    ## DEFINITIONS

    def test_transition_definition(self):

        # Json input
        input_str= """
        {
            "T1":[
                ["P1", "P2"],
                [
                    [ "I1 & I2 & !I4" ],
                    [ ["I3"], ["I4"] ]
                ],
                ["P3"],
                "T1 comment"
            ],
            "T2":[
                ["P3"],
                [
                    [ [], ["I1", "I2"] ],
                    [ "I4 & !I3" ]
                ],
                ["P1", "P2"],
                "T2 comment"
            ]
        }
        """

        # Expected NuSMV
        expected= "T1:= (P1 & P2) & ( (I1 & I2 & !I4) | (I3 & !I4) ) & (!P3);\n" + \
        "T2:= (P3) & ( (!I1 & !I2) | (I4 & !I3) ) & (!P1 & !P2);\n"    

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str, object_pairs_hook=OrderedDict)

        # Test
        self.assertMultiLineEqual(expected, define.transition_definition(input_dict))

    
    def test_stab_definition(self):

       # Json input
        input_str= """
        {
            "T1":[
                ["P1", "P2"],
                [
                    [ ["I1", "I2"], ["I4"] ],
                    [ "I3 & !I4" ]
                ],
                ["P3"],
                "T1 comment"
            ],
            "T2":[
                ["P3"],
                [
                    [ "I4 & ! (I1 | I2)" ],
                    [ ["I4"], ["I3"] ]
                ],
                ["P1", "P2"],
                "T2 comment"
            ]
        }
        """ 

        # Expected NuSMV
        expected= "stab:= !(T1 | T2);\n"

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str, object_pairs_hook=OrderedDict)

        # Test
        self.assertMultiLineEqual(expected, define.stab_definition(input_dict))

    def test_output_definition(self):

        # Json input
        input_str= """
        {
            "PS2": [
                [
                    ["RP_AL1_ST_CLAMP"], ["AL1_ST_GRAB"]
                ],
                "Product gets withing graber range"
            ],
           "PS4": [
                [
                    ["RP_AL1_ST_CLAMP"], ["AL1_ST_GRAB"]
                ],
                ["AL1_ST_Z_SET:=750"],
                "Move grabber down to pick up product"
            ],
            "PSE0": [
                [
                    ["AL1_ST_GRAB"], ["AL1_EMIT", "RC_AL1_ST"]
                ],
                "New box arrived, stop conveyor"
            ],
            "initial": ["PS2", "PSE0"]
            
        }
        """

        # Expected output
        expected= "-- SET\n" + \
            "AL1_EMIT_set:= FALSE;\n" + \
            "AL1_ST_GRAB_set:= PSE0;\n" + \
            "RC_AL1_ST_set:= FALSE;\n" + \
            "RP_AL1_ST_CLAMP_set:= PS2 | PS4;\n" + \
            "-- RESET\n" + \
            "AL1_EMIT_reset:= PSE0;\n" + \
            "AL1_ST_GRAB_reset:= PS2 | PS4;\n" + \
            "RC_AL1_ST_reset:= PSE0;\n" + \
            "RP_AL1_ST_CLAMP_reset:= FALSE;\n" + \
            "-- OUTPUT\n" + \
            "AL1_EMIT:= AL1_EMIT_set & !AL1_EMIT_reset;\n" + \
            "AL1_ST_GRAB:= AL1_ST_GRAB_set & !AL1_ST_GRAB_reset;\n" + \
            "RC_AL1_ST:= RC_AL1_ST_set & !RC_AL1_ST_reset;\n" + \
            "RP_AL1_ST_CLAMP:= RP_AL1_ST_CLAMP_set & !RP_AL1_ST_CLAMP_reset;\n" + \
            "-- Non-Boolean Outputs\n" + \
            "AL1_ST_Z_SET:= case\n" + \
            "   PS4: 750;\n" + \
            "   TRUE: 0;\n" + \
            "esac;\n"

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str, object_pairs_hook=OrderedDict)
        
        # Test
        self.assertMultiLineEqual(expected, define.output_definition(input_dict))

    #================================================================
    ## ASSIGNMETS

    def test_input_assignment(self):

        # Json input
        input_str= r"""
        {
            "I1": ["boolean", "%IX100.0"],
            "I2": [
                    [ 
                        "{\"1\", \"2\", \"3\"}",
                        "{\"1\", \"2\"}",
                        "{\"1\", \"2\", \"3\"}"
                    ],
                    "%IW101"
                ],
            "I3": [
                    [
                        "0..10",
                        5,
                        "{0, 5, 7}"
                    ],
                    "%IW100"
                ],
            "STATUS": [
                    [
                        "{\"stopped\", \"running\"}",
                        "stopped",
                        "{\"stopped\", \"running\"}"
                    ],
                    "%IX100.1"
                ]
        }
        """

        # Expected NuSMV
        expected= 'init(I1):= {TRUE, FALSE};\n' + \
            'init(I2):= {"1", "2"};\n' + \
            'init(I3):= 5;\n' + \
            'init(STATUS):= "stopped";\n' + \
            'next(I1):= case\n' + \
            '   stab: {TRUE, FALSE};\n' +\
            '   TRUE: I1;\n' + \
            'esac;\n' + \
            'next(I2):= case\n' + \
            '   stab: {"1", "2", "3"};\n' +\
            '   TRUE: I2;\n' + \
            'esac;\n'+ \
            'next(I3):= case\n' + \
            '   stab: {0, 5, 7};\n' +\
            '   TRUE: I3;\n' + \
            'esac;\n'+ \
            'next(STATUS):= case\n' + \
            '   stab: {"stopped", "running"};\n' +\
            '   TRUE: STATUS;\n' + \
            'esac;\n'

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str, object_pairs_hook=OrderedDict)

        # Test
        self.assertMultiLineEqual(expected, assign.input_assignment(input_dict))


    def test_place_assignment(self):
        # Json input
        places_str= """
        {
            "IDLE": [
                [
                    [],
                    []
                ],
                "Initial place"
            ],
            "P1": [
                    [
                    ["O1", "O2"],
                    ["O3"]
                ],
                ["O4:= 900"],
                "Place 1 comment"
            ],
            "P2":[
                    [
                    ["O2", "O3"],
                    ["O1", "O2"]
                ],
                "Place 2 comment"
            ],
            "P3": [
                    [
                    ["O1"],
                    ["O2", "O3"]
                ],
                "Place 3 comment"
            ],
            "initial": [ "IDLE" ]
            
        }
        """

        transitions_str= """
        {
            "T0": [
                ["IDLE"],
                [
                    [["START"], []]
                ],
                ["P1"]
            ],
            "T1":[
                ["P1", "P2"],
                [
                    [ ["I1", "I2"], ["I4"] ],
                    [ ["I3"], ["I4"] ]
                ],
                ["P3"],
                ["T1 comment"]
            ],
            "T2":[
                ["P3"],
                [
                    [ 
                        ["I4"], ["I1", "I2"] 
                    ],
                    [ 
                        ["I4"], ["I3"] 
                    ]
                ],
                ["P1", "P2"],
                ["T2 comment"]
            ]
        }
        """ 

        # Expected NuSMV
        expected= 'init(IDLE):= TRUE;\n' + \
            'init(P1):= FALSE;\n' + \
            'init(P2):= FALSE;\n' + \
            'init(P3):= FALSE;\n' + \
            'next(IDLE):= case\n' + \
            '   T0: FALSE;\n' +\
            '   TRUE: IDLE;\n' + \
            'esac;\n' + \
            'next(P1):= case\n' + \
            '   T0: TRUE;\n' +\
            '   T1: FALSE;\n' +\
            '   T2: TRUE;\n' +\
            '   TRUE: P1;\n' + \
            'esac;\n' + \
            'next(P2):= case\n' + \
            '   T1: FALSE;\n' +\
            '   T2: TRUE;\n' +\
            '   TRUE: P2;\n' + \
            'esac;\n' + \
            'next(P3):= case\n' + \
            '   T1: TRUE;\n' +\
            '   T2: FALSE;\n' +\
            '   TRUE: P3;\n' + \
            'esac;\n'

        # Convert Json string to python dictionary
        places_dict= json.loads(places_str, object_pairs_hook=OrderedDict)
        transitions_dict= json.loads(transitions_str, object_pairs_hook=OrderedDict)

        # Test
        self.assertMultiLineEqual(
            expected, assign.place_assignment(places_dict, transitions_dict)
            )

    
    #================================================================
    ## SPECIFICATIONS

    def test_manual_specs(self):

        # Json input
        input_str= """
        {
            "manual": [
                "AG(stab -> EF(P5))",
                "AG( ((CS_AL1_W < 4) | (CS_AL1_W > 8)) -> AF(!(P5 | P6)) )"
            ]            
        }
        """

        # Expected NuSMV
        expected= "SPEC\n" + \
            "AG(stab -> EF(P5));\n" + \
            "SPEC\n" + \
            "AG( ((CS_AL1_W < 4) | (CS_AL1_W > 8)) -> AF(!(P5 | P6)) );\n"

        
        # Convert Json string to python dictionary
        input_dict= json.loads(input_str, object_pairs_hook=OrderedDict)

        # Test
        self.assertMultiLineEqual(expected, spec.manual(input_dict))


        





























