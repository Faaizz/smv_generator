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
        input_str= """
        {
            "I1": [
                "boolean",
                "false"
            ],
            "I2": [
                ["1", "2", "3"],
                "1"
            ],
            "STATUS": [
                ["stopped", "running"],
                "stopped"
            ]
            
        }
        """

        # Expected MuSMV
        expected= 'I1: boolean;\n' + 'I2: {"1", "2", "3"};\n' + 'STATUS: {"stopped", "running"};\n'

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
                ["O3"]
            ],
            "P2":[
                ["O3"],
                ["O1", "O2"]
            ]
            
        }
        """

        # Expected NuSMV
        expected= "P1: boolean;\n" + "P2: boolean;\n"

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
                    [ ["I1", "I2"], ["I4"] ],
                    [ ["I3"], ["I4"] ]
                ],
                ["P3"]
            ],
            "T2":[
                ["P3"],
                [
                    [ ["I4"], ["I1", "I2"] ],
                    [ ["I4"], ["I3"] ]
                ],
                ["P1", "P2"]
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
                    [ ["I3"], ["I4"] ]
                ],
                ["P3"]
            ],
            "T2":[
                ["P3"],
                [
                    [ ["I4"], ["I1", "I2"] ],
                    [ ["I4"], ["I3"] ]
                ],
                ["P1", "P2"]
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
                ["O3"]
            ],
            "P2":[
                ["O2", "O3"],
                ["O1", "O2"]
            ],
            "P3": [
                ["O1"],
                ["O2", "O3"]
            ]
            
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
        input_str= """
        {
            "I1": [
                "boolean",
                "false"
            ],
            "I2": [
                ["1", "2", "3"],
                "1"
            ],
            "STATUS": [
                ["stopped", "running"],
                "stopped"
            ]
            
        }
        """

        # Expected NuSMV
        expected= 'init(I1):= false;\n' + \
            'init(I2):= "1";\n' + \
            'init(STATUS):= "stopped";\n' + \
            'next(I1):= case\n' + \
            '   stab: {true, false};\n' +\
            '   true: I1;\n' + \
            'esac;\n' + \
            'next(I2):= case\n' + \
            '   stab: {"1", "2", "3"};\n' +\
            '   true: I2;\n' + \
            'esac;\n'+ \
            'next(STATUS):= case\n' + \
            '   stab: {"stopped", "running"};\n' +\
            '   true: STATUS;\n' + \
            'esac;\n'

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str, object_pairs_hook=OrderedDict)

        # Test
        self.assertMultiLineEqual(expected, assign.input_assignment(input_dict))


    def test_place_assignment(self):
        # Json input
        places_str= """
        {
            "P1": [
                ["O1", "O2"],
                ["O3"]
            ],
            "P2":[
                ["O2", "O3"],
                ["O1", "O2"]
            ],
            "P3": [
                ["O1"],
                ["O2", "O3"]
            ],
            "initial": [ "P1", "P3" ]
            
        }
        """

        transitions_str= """
        {
            "T1":[
                ["P1", "P2"],
                [
                    [ ["I1", "I2"], ["I4"] ],
                    [ ["I3"], ["I4"] ]
                ],
                ["P3"]
            ],
            "T2":[
                ["P3"],
                [
                    [ ["I4"], ["I1", "I2"] ],
                    [ ["I4"], ["I3"] ]
                ],
                ["P1", "P2"]
            ]
        }
        """ 

        # Expected NuSMV
        expected= 'init(P1):= true;\n' + \
            'init(P2):= false;\n' + \
            'init(P3):= true;\n' + \
            'next(P1):= case\n' + \
            '   T1: false;\n' +\
            '   T2: true;\n' +\
            '   true: P1;\n' + \
            'esac;\n' + \
            'next(P2):= case\n' + \
            '   T1: false;\n' +\
            '   T2: true;\n' +\
            '   true: P2;\n' + \
            'esac;\n' + \
            'next(P3):= case\n' + \
            '   T1: true;\n' +\
            '   T2: false;\n' +\
            '   true: P3;\n' + \
            'esac;\n'

        # Convert Json string to python dictionary
        places_dict= json.loads(places_str, object_pairs_hook=OrderedDict)
        transitions_dict= json.loads(transitions_str, object_pairs_hook=OrderedDict)

        # Test
        self.assertMultiLineEqual(
            expected, assign.place_assignment(places_dict, transitions_dict)
            )




























