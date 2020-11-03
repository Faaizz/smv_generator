

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
        if not isinstance(value[0], list):
            input_type= value[0]
        # if type is a list
        else:
            input_type= "{"
            for idx, item in enumerate(value[0]):
                # If not last item
                if idx < len(value[0])-1:
                    input_type= input_type + '"' + item + '"' + ", "
                # If last item
                else:
                    input_type= input_type + '"' + item + '"'
            
            input_type= input_type + "}"


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


def stop_transitions_declaration(stop_place, in_dict):
    """Declare stop transitions in NuSMV

    Parameters:
    ----------
    stop_place: str
        name of stop place
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
            temp= "T{0}{1}: ".format(key, stop_place) + "boolean;\n"
            out_str= out_str + temp

    return out_str


