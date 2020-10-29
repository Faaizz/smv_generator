import unittest, json

import main.declare as declare

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
        expected= """
        I1: boolean;
        I2: {"1", "2", "3"};
        STATUS: {"stopped", "running"};
        """

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str)

        # Test
        self.assertMultiLineEqual(expected, declare.input(input_dict))

    
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
        expected= """
        P1: boolean;
        P2: boolean;
        """

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str)

        # Test
        self.assertMultiLineEqual(expected, declare.input(input_dict))


    def test_transition_condition(self):

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
        expected= """
        T1:= (P1 & P2) & ( (I1 & I2 & !I4) | (I3 & !I4) ) & (!P3);  
        T2:= (P3) & ( (I4 & !I1 & !I2) | (I4 & !I3) ) & (!P1 & !P2);  
        """

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str)

        # Test
        self.assertMultiLineEqual(expected, declare.input(input_dict))

    
    def test_stab_delaration(self):

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
        expected= """
        stab:= !(T1 | T2);
        """

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str)

        # Test
        self.assertMultiLineEqual(expected, declare.input(input_dict))

