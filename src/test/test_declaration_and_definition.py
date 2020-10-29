import unittest, json
from collections import OrderedDict

import main.declare as declare
import main.define as define

class VariablesDeclarationTest(unittest.TestCase):

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
        self.assertEqual(expected, declare.input_declaration(input_dict))

    
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
        self.assertEqual(expected, declare.place_declaration(input_dict))


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

