from collections import OrderedDict
import logging

def input_assignment(in_dict):
    """Initialize and give assignment directives to input variables in NuSMV

    Parameters:
    ----------
    in_dict: dict

    Returns:
    -------
    out_str: string
    """

    # define initialization & assignment strings
    init_str= ""
    assign_str= ""

    # loop through elements
    for key,value in in_dict.items():
        # Check if type is a boolean
        if isinstance(in_dict[key], str):
            # Initialization
            init_str= init_str + "init({0})".format(key) + ":= {TRUE, FALSE};\n"

            # Assignment
            assign_str= assign_str + \
                'next({0}):= case\n'.format(key) + \
                '   stab: {TRUE, FALSE};\n' +\
                '   TRUE: {0};\n'.format(key) + \
                'esac;\n'
            
        # if type is not a boolean
        else:

            # Initialization
            init_val= in_dict[key][1]
            # Check if initial value is a string and is not n enum type
            if (isinstance(init_val, str) and not ("{" in init_val)):
                init_val= '"' + init_val + '"'

            init_str= init_str + "init({0})".format(key) + ":= {0};\n".format(init_val)

            # Assignment
            assign_str= assign_str + \
                'next({0}):= case\n'.format(key) + \
                '   stab: {0};\n'.format(in_dict[key][2]) +\
                '   TRUE: {0};\n'.format(key) + \
                'esac;\n'
            
    # return
    out_str= init_str + assign_str
    
    return out_str


def place_assignment(places_dict, transitions_dict):
    """Initialize and give assignment directives to places in NuSMV

    Parameters:
    ----------
    places_dict: dict
    transitions_dict: dict

    Returns:
    -------
    out_str: string
    """

    # define initialization & assignment strings
    init_str= ""
    assign_str= ""

    # Loop through places and initialize
    for place_key,value in places_dict.items():
        if not (place_key == "initial"):
            # Initialization
            initial= "FALSE"
            # Check if marked by default
            if place_key in places_dict["initial"]:
                initial= "TRUE"

            init_str= init_str + "init({0}):= ".format(place_key) + \
                initial + ";\n"

            # Assignment
            assign_str= assign_str + \
                    'next({0}):= case\n'.format(place_key) 
            # Loop through transitions
            for trans_key,value in transitions_dict.items():
                # Check if current place is a post-place of the current transition
                if place_key in transitions_dict[trans_key][2]:
                    assign_str= assign_str + \
                    '   {0}: TRUE;\n'.format(trans_key)

                # Check if current place is a pre-place of the current transition
                if place_key in transitions_dict[trans_key][0]:
                    assign_str= assign_str + \
                    '   {0}: FALSE;\n'.format(trans_key)

            assign_str= assign_str + \
                    '   TRUE: {0};\n'.format(place_key) + \
                    'esac;\n'


    # return
    out_str= init_str + assign_str

    return out_str
