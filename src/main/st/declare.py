
def input_declaration(in_dict):
    """Declare input variables in ST

    Parameters:
    ----------
    in_dict: dict
    
    Returns:
    -------
    out_str: string
    """

    out_str=""

    # loop through elements
    for key in iter(in_dict):
        value= in_dict[key][1]
        # Check variable type
        if ("X" in value) or ("W" in value):
            if ("X" in value):
                # Type is boolean
                input_type= "BOOL"

            if ("W" in value):
                # Type is word
                # Check if further information on type is specified
                try:
                    input_type= in_dict[key][2]
                except IndexError:
                    input_type= "WORD"
        
        else: 
            # Type not found
            err_str="Invalid variable type specified for ST at" +  value 
            raise ValueError(err_str)

        temp= key + " AT " + value  + " : " + input_type + ";\n"
        out_str= out_str + temp
        
    
    return out_str



def output_declaration(in_dict):
    """Declare output variables in ST

    Parameters:
    ----------
    in_dict: dict

    Returns:
    -------
    out_str: string
    """

    out_str=""

    # loop through elements
    for key in iter(in_dict):
        value= in_dict[key][0]
        # Check variable type
        if ("X" in value) or ("W" in value):
            if ("X" in value):
                # Type is boolean
                input_type= "BOOL"

            if ("W" in value):
                # Type is word
                # Check if further information on type is specified
                try:
                    input_type= in_dict[key][1]
                except KeyError:
                    input_type= value
        
        else: 
            # Type not found
            err_str="Invalid variable type specified for ST at" +  value 
            raise ValueError(err_str)

        temp= key + " AT " + value  + " : " + input_type + ";\n"
        out_str= out_str + temp

    return out_str



def place_declaration(in_dict):
    """Declare place variables in ST

    Parameters:
    ----------
    in_dict: dict

    Returns:
    -------
    out_str: string
    """

    out_str=""

    # Initially marked places
    initial= in_dict["initial"]

    # Loop through items
    for key,value in in_dict.items():
        if not key == "initial":
            temp= key + " : " + "BOOL := "
            # Inital value
            if key in initial:
                temp= temp + "1;\n"
            else:
                temp= temp + "0;\n"

            out_str= out_str + temp

    out_str= out_str  + "STABLE : BOOL := 0;\n"
    
    return out_str