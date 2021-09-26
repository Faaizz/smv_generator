![unit_test_workflow](https://github.com/Faaizz/smv_generator/workflows/Unit%20Tests/badge.svg)

# SMV and ST Generator
Python program to generate SMV language for model checking and IEC 61131 Structured Text (ST) PLC code from JSON representation of Signal Interpreted Petri Nets (SIPN). 

## How It Works
The program takes a json specification of the SIPN as input, and produces a symbolic model checker in the [NuSMV](http://nusmv.fbk.eu/) language. 
For the program to function properly, the input json must follow some laid out syntax which is outlined below.  

The program translates the json input into NuSMV code by performing the following activities:
- Declare all places as variables of type "boolean"
- Declare all inputs as variables of the specified types
- Define transition firing conditions based on specified pre-places, inputs combinations (which may be specified as a raw string), and post-places for each transition
- Define variable *stab* to check stability of markings
- Define the *set* and *reset* conditions for each boolean output based on information obtained from the places
- Define the present value of each output at every stable marking
- Assign initial values to inputs and construct how they obtain next values accordingly (automatically for boolean inputs, but relies on provided inofrmation for inputs of other types)
- Assign initial values to places accordingly and construct how they obtain next values based on the firing of transitions


The program translates the json input into ST code by performing the following activities:
- Declare all places as variables of type "BOOL" and assign initial values based on the specified initial markings
- Declare all inputs and outputs as variables of the specified types and PLC addresses
- Define transition firing conditions based on specified pre-places, inputs combinations (which may be specified as a raw string), and post-places for each transition
- Fire transitions in a loop in order to set outputs only at stable markings
- Set the value of each output at every stable marking


## How to Run
You can generate NuSMV for model checking and ST PLC code by running:
```shell
python ./launch.py /path/to/json/file
```
Note that the output files are stored in the parent directory of the specified JSON file.

## JSON Syntax
It should be noted that terms like *inputs*, *places*, *transitions*, and *outputs* in this section are used to represent the names of such entities. 


### 1- Places
The root json object must have a *places* attribute, which holds an array. 
This *places* array in turn contains an attribute to represent each place in the SIPN. 
Subsequently, each SIPN place attribute is an array with the following elements:   
1. Element 0: An array with 2 elements. The first being an array of boolean outputs that should be set at the place, and the second an array of boolean outputs that should be reset at such place. *Required*   
1. Element 1: An array of manually specified output assignments for non-boolean outputs. *Optional*  
1. Element 2: A comment string. *Optional*  

In addition, there's an *initial* attribute in the *places* object which holds an array of places that should be marked initially. 
Each place array can contain an optional 3rd element which holds comments about the place, this element is not used in processing.   

Illustration:

```json

{
    "places": {
        "PLACE1": [
            [
                ["AL1_GRAB"],
                ["RP_AL1_CLAMP"],
            ],
            ["AL1_X_SET=80"],
            "Textual description of the significance of this place"
        ],
        "PLACE2":[
            [
                ["RP_AL1_CLAMP"],
                ["AL1_GRAB"]
            ],
            "Comment text."            
        ],
        "initial": [ "P1", "P3" ]
    }
}
```

In the above example, *PLACE1* when marked, sets *AL1_GRAB* as TRUE, *RP_AL1_CLAMP* as FALSE, and *AL1_X_SET* as 80. 
While when *PLACE2* is marked, *RP_AL1_CLAMP* is set TRUE and *AL1_GRAB* FALSE.  


### 2- Inputs
The inputs into the SIPN are registered in the *inputs* attribute of the root json object. 


Illustration:
```json

{
    "inputs": {

        "S_AL1_ST1": ["boolean", "%IX100.0"],
        "S_AL1_ST2": ["boolean", "%IX100.1"],
        "S_AL1_ST3": ["boolean", "%IX100.2"],
        "RP_AL1_ST_CLAMPED": ["boolean", "%IX100.3"],
        "AL1_ST_DETECTED": ["boolean", "%IX100.4"],
        "RESET": ["boolean", "%IX100.5"],
        "AL1_ST_X_POS": [
            [
                "{0, 400, 860}",
                0,
                "{0, 400, 860}"
            ],
            "%IW100"
        ],
        "AL1_ST_Y_POS": [
            [
                "{0, 300, 560}",
                0,
                "{0, 300, 560}"
            ],
            "%IW101"
        ],
        "AL1_ST_Z_POS": [
            [
                "{0, 200, 410, 750}",
                0,
                "{0, 200, 410, 750}"
            ],
            "%IW102"
        ]
        
    }

```

### 3- Transitions
A *transitions* attribute must be present in the root json object. 
This attribute holds an object which contains named attributes representing each transition. 

Each such attribute should be an array with at least 3 elements: 
- *Element 0*: An array of places that must be marked for the transition to fire;

- *Element 1*: An array of arrays indicating the required transition conditions. 
The transition conditions may be specified as raw text by specifying a string in the array. Otherwise, it can be specified with as a combination of inputs that should be HIGH and inputs that should be LOW. The first element is an array of inputs that should be set for the transition to fire, while the second is an array of inputs that should be reset for the transition to fire; and 

- *Element 2*: An array of places that must be left unmarked for the transition to fire.  

For example, if transition *T1* has pre-places *P1* and *P2*, requires inputs *I1* and *I2* to be set and *I4* not set or input *I3* to be set and *I4* not set, and has post-place *P3*, we have in NuSMV:


Then the entry for transitions in the *transitions* object should look like:
```json
{
    "transitions": {
        "TS3": [
            ["PS2"],
            [
                [
                    ["RP_AL1_ST_CLAMPED"], []
                ]
            ],
            ["PS3"]
        ],
        "TS4": [
            ["PS3"],
            [
                [
                    "(AL1_ST_Y_POS>540) & (AL1_ST_Y_POS<580)"
                ]
            ],
            ["PS4"]
        ]
    }
}
```
