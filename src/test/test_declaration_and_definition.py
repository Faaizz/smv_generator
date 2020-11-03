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
            "I1": ["boolean"],
            "I2": [["1", "2", "3"]],
            "STATUS": [["stopped", "running"]]
            
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
                ["O3"],
                ["Place 1 comment"]
            ],
            "P2":[
                ["O2", "O3"],
                ["O1", "O2"],
                ["Place 2 comment"]
            ],
            "P3": [
                ["O1"],
                ["O2", "O3"],
                [""]
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
                    [ ["I1", "I2"], ["I4"] ],
                    [ ["I3"], ["I4"] ]
                ],
                ["P3"],
                ["T1 comment"]
            ],
            "T2":[
                ["P3"],
                [
                    [ ["I4"], ["I1", "I2"] ],
                    [ ["I4"], ["I3"] ]
                ],
                ["P1", "P2"],
                ["T2 comment"]
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
                ["P3"],
                ["T1 comment"]
            ],
            "T2":[
                ["P3"],
                [
                    [ ["I4"], ["I1", "I2"] ],
                    [ ["I4"], ["I3"] ]
                ],
                ["P1", "P2"],
                ["T2 comment"]
            ]
        }
        """ 

        # Expected NuSMV
        expected= "stab:= !(T1 | T2)"

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
                ["Place 1 comment"]
            ],
            "P2":[
                ["O2", "O3"],
                ["O1", "O2"],
                ["Place 2 comment"]
            ],
            "P3": [
                ["O1"],
                ["O2", "O3"],
                [""]
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
        input_str= """
        {
            "I1": ["boolean"],
            "I2": [["1", "2", "3"]],
            "STATUS": [["stopped", "running"]]
            
        }
        """

        # Expected NuSMV
        expected= 'init(I1):= {TRUE, FALSE};\n' + \
            'init(I2):= {"1", "2", "3"};\n' + \
            'init(STATUS):= {"stopped", "running"};\n' + \
            'next(I1):= case\n' + \
            '   stab: {TRUE, FALSE};\n' +\
            '   TRUE: I1;\n' + \
            'esac;\n' + \
            'next(I2):= case\n' + \
            '   stab: {"1", "2", "3"};\n' +\
            '   TRUE: I2;\n' + \
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
            "P1": [
                ["O1", "O2"],
                ["O3"],
                ["Place 1 comment"]
            ],
            "P2":[
                ["O2", "O3"],
                ["O1", "O2"],
                ["Place 2 comment"]
            ],
            "P3": [
                ["O1"],
                ["O2", "O3"],
                ["Place 3 comment"]
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
        expected= 'init(P1):= TRUE;\n' + \
            'init(P2):= FALSE;\n' + \
            'init(P3):= TRUE;\n' + \
            'next(P1):= case\n' + \
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


    def test_stop_transitions_definition(self):
        # Test transitions from all places to the specified stop place

        # Specified stop place
        stop_place= "IDLE"
        # Specfied stop input
        stop_input= "STOP"

        # Json input
        input_str= """
        {
            "IDLE": [
                [],
                []
            ],
            "P1": [
                ["O1", "O2"],
                ["O3"],
                ["Place 1 comment"]
            ],
            "P2":[
                ["O2", "O3"],
                ["O1", "O2"],
                ["Place 2 comment"]
            ],
            "P3": [
                ["O1"],
                ["O2", "O3"],
                ["Place 3 comment"]
            ],
            "initial": [ "P1", "P3" ]
            
        }
        """

        expected= 'TP1{0}:= (P1) & ( ({1}) ) & (!{0});\n'.format(stop_place, stop_input) + \
            'TP2{0}:= (P2) & ( ({1}) ) & (!{0});\n'.format(stop_place, stop_input) + \
            'TP3{0}:= (P3) & ( ({1}) ) & (!{0});\n'.format(stop_place, stop_input)

        # Convert Json string to Python dictionary
        input_dict= json.loads(input_str, object_pairs_hook=OrderedDict)

        # Test
        self.assertMultiLineEqual(expected, define.stop_transitions_definition(stop_place, stop_input, input_dict))

    def test_stop_stab_definition(self):
        # Test transitions from all places to the specified stop place

        # Specified stop place
        stop_place= "IDLE"
        # Specfied stop input
        stop_input= "STOP"

        # Json input
        input_str= """
        {
            "P1": [
                ["O1", "O2"],
                ["O3"],
                ["Place 1 comment"]
            ],
            "P2":[
                ["O2", "O3"],
                ["O1", "O2"],
                ["Place 2 comment"]
            ],
            "P3": [
                ["O1"],
                ["O2", "O3"],
                ["Place 3 comment"]
            ],
            "initial": [ "P1", "P3" ]
            
        }
        """

        expected= '!(TP1{0} | TP2{0} | TP3{0})'.format(stop_place)

        # Convert Json string to Python dictionary
        input_dict= json.loads(input_str, object_pairs_hook=OrderedDict)

        # Test
        self.assertMultiLineEqual(expected, define.stop_stab_definition(stop_place, input_dict))



























