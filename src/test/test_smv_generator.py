import unittest, json
from collections import OrderedDict

import main.declare as declare
import main.define as define
import main.assign as assign

class VariablesDeclarationTest(unittest.TestCase):

    #================================================================
    ## DECLARATIONS

    def test_input_declaration(self):
        
        # Json input
        input_str= r"""
        {
        "I1": "boolean",
        "I2": [ 
                "{\"1\", \"2\", \"3\"}",
                "1",
                "{\"1\", \"2\", \"3\"}"
            ],
        "I3": [
                "0..10",
                "{0, 4, 7}",
                "{0, 5, 7}"
            ],
        "STATUS": [
                "{\"stopped\", \"running\"}",
                "stopped",
                "{\"stopped\", \"running\"}"
            ]
        
        }
        """

        # Expected MuSMV
        expected= 'I1: boolean;\n' + \
            'I2: {"1", "2", "3"};\n' + \
            'I3: 0..10;\n' + \
            'STATUS: {"stopped", "running"};\n'

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str, object_pairs_hook=OrderedDict)

        # Test
        self.assertMultiLineEqual(expected, declare.input_declaration(input_dict))

    
    def test_place_declaration(self):

        # Json input
        input_str= """
        {
            "P1": [
                ["O1", "O2"],
                ["O3"],
                "Place 1 comment"
            ],
            "P2":[
                ["O2", "O3"],
                ["O1", "O2"],
                "Place 2 comment"
            ],
            "P3": [
                ["O1"],
                ["O2", "O3"]
            ],
            "initial": [ "P1", "P3" ]
            
        }
        """

        # Expected NuSMV
        expected= "P1: boolean;\n" + "P2: boolean;\n" + "P3: boolean;\n"

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
                    [ ["I4"], ["I1", "I2"] ],
                    [ "I4 & !I3" ]
                ],
                ["P1", "P2"],
                "T2 comment"
            ]
        }
        """

        # Expected NuSMV
        expected= "T1:= (P1 & P2) & ( (I1 & I2 & !I4) | (I3 & !I4) ) & (!P3);\n" + \
        "T2:= (P3) & ( (I4 & !I1 & !I2) | (I4 & !I3) ) & (!P1 & !P2);\n"    

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
            "P1": [
                ["O1", "O2"],
                ["O3"],
                "Place 1 comment"
            ],
            "P2":[
                ["O2", "O3"],
                ["O1", "O2"],
                "Place 2 comment"
            ],
            "P3": [
                ["O1"],
                ["O2", "O3"]
            ],
            "initial": [ "P1", "P3" ]
            
        }
        """

        # Expected output
        expected= "-- SET\n" + \
            "O1_set:= P1 | P3;\n" + \
            "O2_set:= P1 | P2;\n" + "O3_set:= P2;\n" + \
            "-- RESET\n" + \
            "O1_reset:= P2;\n" + \
            "O2_reset:= P2 | P3;\n" + "O3_reset:= P1 | P3;\n" + \
            "-- OUTPUT\n" + \
            "O1:= O1_set & !O1_reset;\n" + \
            "O2:= O2_set & !O2_reset;\n" + "O3:= O3_set & !O3_reset;\n"

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
            "I1": "boolean",
            "I2": [ 
                    "{\"1\", \"2\", \"3\"}",
                    "{\"1\", \"2\"}",
                    "{\"1\", \"2\", \"3\"}"
                ],
            "I3": [
                    "0..10",
                    5,
                    "{0, 5, 7}"
                ],
            "STATUS": [
                    "{\"stopped\", \"running\"}",
                    "stopped",
                    "{\"stopped\", \"running\"}"
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
                [],
                [],
                "Initial place"
            ],
            "P1": [
                ["O1", "O2"],
                ["O3"],
                "Place 1 comment"
            ],
            "P2":[
                ["O2", "O3"],
                ["O1", "O2"],
                "Place 2 comment"
            ],
            "P3": [
                ["O1"],
                ["O2", "O3"],
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



























