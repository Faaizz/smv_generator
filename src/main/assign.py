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
        # Check if type is a string
        if isinstance(in_dict[key][0], str):
            # Initialization
            init_str= init_str + "init({0}):= ".format(key) + \
                in_dict[key][1] + ";\n"

            # Assignment
            assign_str= assign_str + \
                'next({0}):= case\n'.format(key) + \
                '   stab: {true, false};\n' +\
                '   true: {0};\n'.format(key) + \
                'esac;\n'
            
        # if type is not string
        else:
            # Initialization
            # Add quotes to initial value for non-booleans
            init_str= init_str + "init({0}):= ".format(key) + \
                '"{0}"'.format(in_dict[key][1]) + ";\n"

            assign_type= "{"
            for idx, item in enumerate(value[0]):
                # If not last item
                if idx < len(value[0])-1:
                    assign_type= assign_type + '"' + item + '"' + ", "
                # If last item
                else:
                    assign_type= assign_type + '"' + item + '"'
            
            assign_type= assign_type + "}"

            # Assignment
            assign_str= assign_str + \
                'next({0}):= case\n'.format(key) + \
                '   stab: {0};\n'.format(assign_type) +\
                '   true: {0};\n'.format(key) + \
                'esac;\n'

    # return
    out_str= init_str + assign_str
    
    return out_str