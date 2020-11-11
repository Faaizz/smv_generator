

def input_declaration(in_dict):
    """Declare input variables in NuSMV

    Parameters:
    ----------
    in_dict: dict

    Returns:
    -------
    out_str: string
    """

    out_str= ""

    # loop through elements
    for key in iter(in_dict):
        value= in_dict[key]
        # Check if type is not a list
        if not isinstance(value, list):
            # Type is boolean
            input_type= value
        
        else: 
            # Type is specified as array of raw string values
            input_type= value[0]

        temp= key + ": " + input_type + ";\n"
        out_str= out_str + temp

    return out_str


def place_declaration(in_dict):
    """Declare place variables in NuSMV

    Parameters:
    ----------
    in_dict: dict

    Returns:
    -------
    out_str: string
    """

    out_str= ""

    # Loop through items
    for key,value in in_dict.items(): 
        # Skip the "initial" attribute of places
        if not (key == "initial"):
            temp= key + ": " + "boolean;\n"
            out_str= out_str + temp

    return out_str