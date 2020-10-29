import unittest, json

import main.declare as declare

class VariablesDeclarationTest(unittest.TestCase):

    def test_input_declaration(self):
        
        # Json input
        input_str= """
        {
            "inputs": {
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
        }
        """

        # Expected MuSMV output
        expected= """
        I1: boolean;
        I2: {"1", "2", "3"};
        STATUS: {"stopped", "running"};
        """

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str)

        # Test
        self.assertMultiLineEqual(expected, declare.input(input_dict))

