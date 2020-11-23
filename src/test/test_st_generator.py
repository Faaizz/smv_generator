import unittest, json
from collections import OrderedDict

import main.st.declare as declare
import main.st.define as define

class ST_Test(unittest.TestCase):

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
        expected= 'S_AL1_ST1 AT %IX100.0 : BOOL;\n' + \
            'S_AL1_ST2 AT %IX100.1 : BOOL;\n' + \
            'STATUS AT %IX100.2 : BOOL;\n' + \
            'AL1_ST_X_POS AT %IW100 : INT;\n' + \
            'AL1_ST_Y_POS AT %IW101 : INT;\n'

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str, object_pairs_hook=OrderedDict)
        
        # Test
        self.assertMultiLineEqual(expected, declare.input_declaration(input_dict))


    def test_internal_declaration(self):

        #Json input
        input_str= r"""
        {
            "timer_P1": [
                [
                    "MODULE",
                    {
                        "Q": "boolean",
                        "ET": [
                            "{\"zero\", \"half\", \"full\"}",
                            "zero",
                            "{\"zero\", \"half\", \"full\"}"
                        ]
                    }
                ],
                [
                    "TON",
                    "timer_P1(IN:= P1, PT:= T#100ms)"
                ]
            ],
            "count": [
                [
                    "0..10",
                    0,
                    "{0, 3, 7, 10}"
                ],
                [
                    "INT",
                    "count:=0"
                ]
            ]
        }
        """

        # Expected NuSMV
        expected= "timer_P1: TON;\n" +\
            "count: INT;\n" 

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str, object_pairs_hook=OrderedDict)

        # Test
        self.assertMultiLineEqual(expected, declare.internal_declaration(input_dict))


    def test_output_declaration(self):
        
        # Json input
        input_str= r"""
        {
            "AL1_ST_X_SET": ["%QW100", "INT"],
            "AL1_ST_Y_SET":  ["%QW101", "INT"],
            "RP_AL1_ST_CLAMP":  ["%QX100.0"],
            "RC_AL1_ST": ["%QX100.3"]
        }
        """

        # Expected MuSMV
        expected= 'AL1_ST_X_SET AT %QW100 : INT;\n' + \
            'AL1_ST_Y_SET AT %QW101 : INT;\n' + \
            'RP_AL1_ST_CLAMP AT %QX100.0 : BOOL;\n' + \
            'RC_AL1_ST AT %QX100.3 : BOOL;\n'

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str, object_pairs_hook=OrderedDict)
        
        # Test
        self.assertMultiLineEqual(expected, declare.output_declaration(input_dict))

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
        expected= "PS2 : BOOL := 1;\n" + "PS4 : BOOL := 0;\n" + "PSE0 : BOOL := 1;\n" + "STABLE : BOOL := 0;\n"

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str, object_pairs_hook=OrderedDict)

        # Test
        self.assertMultiLineEqual(expected, declare.place_declaration(input_dict))


    #================================================================
    ## DEFINITIONS


    def test_internal_definition(self):

        #Json input
        input_str= r"""
        {
            "timer_P1": [
                [
                    "MODULE",
                    {
                        "Q": "boolean",
                        "ET": [
                            "{\"zero\", \"half\", \"full\"}",
                            "zero",
                            "{\"zero\", \"half\", \"full\"}"
                        ]
                    }
                ],
                [
                    "TON",
                    "timer_P1(IN:= P1, PT:= T#100ms)"
                ]
            ],
            "count": [
                [
                    "0..10",
                    0,
                    "{0, 3, 7, 10}"
                ],
                [
                    "INT",
                    "count:=0"
                ]
            ]
        }
        """

        # Expected NuSMV
        expected= "timer_P1(IN:= P1, PT:= T#100ms);\n" +\
            "count:=0;\n" 

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str, object_pairs_hook=OrderedDict)

        # Test
        self.assertMultiLineEqual(expected, define.internal_definition(input_dict))


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
        expected= "STABLE:=0;\n" + \
        "WHILE STABLE=0 DO\n" + \
        "   STABLE:=1;\n" + \
        "   (*T1*)\n" + \
        "   IF (P1 AND P2) AND ( (I1 AND I2 AND NOT I4) OR (I3 AND NOT I4) ) AND (NOT P3) THEN\n" + \
        "       P1:=0;\n" + \
        "       P2:=0;\n" + \
        "       P3:=1;\n" + \
        "       STABLE:=0;\n" + \
        "   END_IF;\n" + \
        "   (*T2*)\n" + \
        "   IF (P3) AND ( (I4 AND NOT I1 AND NOT I2) OR (I4 AND NOT I3) ) AND (NOT P1 AND NOT P2) THEN\n" + \
        "       P3:=0;\n" + \
        "       P1:=1;\n" + \
        "       P2:=1;\n" + \
        "       STABLE:=0;\n" + \
        "   END_IF;\n" + \
        "END_WHILE;\n"
        

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str, object_pairs_hook=OrderedDict)

        # Test
        self.assertMultiLineEqual(expected, define.transition_definition(input_dict))


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
        expected= "(*AL1_ST_GRAB*)\n" + \
            "IF PSE0 THEN\n" + \
            "   AL1_ST_GRAB:=1;\n" + \
            "END_IF;\n" + \
            "(*RP_AL1_ST_CLAMP*)\n" + \
            "IF PS2 OR PS4 THEN\n" + \
            "   RP_AL1_ST_CLAMP:=1;\n" + \
            "END_IF;\n" + \
            "(*AL1_EMIT*)\n" + \
            "IF PSE0 THEN\n" + \
            "   AL1_EMIT:=0;\n" + \
            "END_IF;\n" + \
            "(*AL1_ST_GRAB*)\n" + \
            "IF PS2 OR PS4 THEN\n" + \
            "   AL1_ST_GRAB:=0;\n" + \
            "END_IF;\n" + \
            "(*RC_AL1_ST*)\n" + \
            "IF PSE0 THEN\n" + \
            "   RC_AL1_ST:=0;\n" + \
            "END_IF;\n" + \
            "(*AL1_ST_Z_SET*)\n" + \
            "IF PS4 THEN\n" + \
            "   AL1_ST_Z_SET:=750;\n" + \
            "END_IF;\n" 

        # Convert Json string to python dictionary
        input_dict= json.loads(input_str, object_pairs_hook=OrderedDict)
        
        # Test
        self.assertMultiLineEqual(expected, define.output_definition(input_dict))
