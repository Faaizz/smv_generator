![unit_test_workflow](https://github.com/Faaizz/smv_generator/workflows/Unit%20Testing/badge.svg)

# SMV Generator
Python program to generate SMV language for Signal Interpreted Petri Net (SIPN) model checking from JSON representation of such model. 

## How It Works
The program takes a json specification of the SIPN as input, and produces a symbolic model checker in the [NuSMV](http://nusmv.fbk.eu/) language. 
For the program to function properly, the input json must follow some laid out syntax which is outlined below.  

The program translates the json input into NuSMV code that performs the following activities:
- Declare all places as variables of type "boolean"
- Declare all inputs as variables of the specified types
- Define transition firing conditions based on specified pre-places, inputs, and post-places for each transition
- Define variable *stab* to check stability of markings
- Define the *set* and *reset* conditions for each output based on information obtained from the places
- Define the present value of each output at every statble marking
- Assign initial values to inputs and construct how they obtain next values
- Assign initial values to places and construct how they obtain next values based on the firing of transitions

## JSON Syntax
It should be noted that terms like *inputs*, *places*, *transitions*, and *outputs* in this section are used to represent the names of such entities. 


### 1- Places
The root json object must have a *places* attribute, which is an an itself. 
This *places* object in turn contains an attribute to represent each place in the SIPN. 
Subsequently, each SIPN place attribute is an array with 2 elements. 
The first and second elements are arrays of outputs that should be set and reset at such place respectively. 
In addition, there's an *initial* attribute in the *places* object. 
This attribute is an array that holds the places that are initially marked.  

Illustration:

```json

{
    "places": {
        "PLACE1": [
            ["OUTPUT1", "OUTPUT2"],
            ["OUTPUT3"]
        ],
        "PLACE2":[
            ["OUTPUT3"],
            ["OUTPUT1", "OUTPUT2"]
        ],
        "initial": [ "P1", "P3" ]
    }
}
```

In the above example, *PLACE1* when marked, sets *OUTPUT1* and *OUTPUT2* and resets *OUTPUT3*. 
While when *PLACE2* is marked, *OUTPUT3* is set and the other 2 outputs reset.  


### 2- Inputs
The inputs into the SIPN are registered in the *inputs* attribute of the root json object. 
Each input is a 2-element array specified as a named attribute of the *inputs* object. 
The first element is the string *"boolean"* if the input is of type *boolean*, 
or an array of possible values the input can assume (specified as strings). 
The second element is the initial value of the input (also specified as a string).  

Illustration:
```json

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

```

### 3- Transitions
A *transitions* attribute must be present in the root json object. This attribute holds an object which contains named attributes representing each transition. 
Each such attribute should be an array with 3 elements: 

- *Element 0*: An array of places that must be marked for the transition to fire;
- 
- *Element 1*: An array of arrays indicating the required transition condition. The systax for elements is a little convoluted. 
The element itself is an array which contains other arrays. Each of the child arrays is a 2-element array of inputs conbinations that can trigger the transition- the first element is an array of inputs that should be set for the transition to fire, while the second is an array of inputs that should be reset for the transition to fire; and 

- *Element 2*: An array of places that must be left unmarked for the transition to fire.  

For example, if transition *T1* has pre-places *P1* and *P2*, requires inputs *I1* and *I2* to be set and *I4* not set or input *I3* to be set and *I4* not set, and has post-place *P3*, we have in NuSMV:
```smv
VAR
-- Inputs
I1: boolean;
I2: boolean;
I3: boolean;

-- Places
P1: boolean;
P2: boolean;
P3: boolean;

DEFINE
-- T1 input requirements
T1_inputs:= (I1 & I2 & !I4) | (I3 & !I4);

-- T1 pre-places marked
T1_pre:= P1 & P2;

-- T1 post-place free
T1_post:= !P3;

-- T1 fires
T1_fires:= T1_pre & T1_inputs & T1_post;

```  

Then the entry for transition *T1* in the *transitions* object should look like:
```json
{
    "transitions": {
        "T1":[
            ["P1", "P2"],
            [
                [ ["I1", "I2"], ["I4"] ],
                [ ["I3"], ["I4"] ]
            ],
            ["P3"]
        ]
    }
}
```
