from collections import OrderedDict

def transition_definition(in_dict):
    """Define transition firing conditions in NuSMV

    Parameters:
    ----------
    in_dict: dict

    Returns:
    -------
    out_str: string
    """
    out_str= ""

    for key in iter(in_dict):

        # Get value of current transition
        value= in_dict[key]

        # Pre-places
        pre= value[0]
        # Pre-places condition
        pre_str= "("
        for idx,item in enumerate(pre):
            # Not last element
            if idx < len(pre)-1:
                pre_str= pre_str + item + " & "
            else:
                pre_str= pre_str + item

        pre_str= pre_str + ")"

        # Inputs
        req_inputs= value[1]
        # Required inputs condition
        req_str= "( "
        for idx_out,item in enumerate(req_inputs):

            # Temp string opening brace
            temp_str= "("

            # Check if condition is specified as a raw string
            if isinstance(item[0], str):
                temp_str= temp_str + item[0]
            
            else:
                high_ins= item[0]
                low_ins= item[1]
                # temp inputs
                for idx_high,high_in in enumerate(high_ins):
                    # Not last item
                    if idx_high < len(high_ins)-1:
                        temp_str= temp_str + high_in + " & "
                    # If last item
                    else:
                        # If there are no low outputs required
                        if len(low_ins) < 1:
                            temp_str= temp_str + high_in
                        else:
                            temp_str= temp_str + high_in + " & "
                
                # Low inputs
                for idx_low,low_in in enumerate(low_ins):
                    # Not last item
                    if idx_low < len(low_ins)-1:
                        temp_str= temp_str + "!" + low_in + " & "
                    # If last item
                    else:
                        temp_str= temp_str + "!" + low_in

            # Temp string closing brace
            temp_str= temp_str + ")"   

            # If not last item, add an OR operator
            if idx_out < (len(req_inputs)-1):
                temp_str= temp_str + " | "

            # Append Temp string to req_str
            req_str= req_str + temp_str

        # req_str closin brace
        req_str= req_str + " )"

        # Post-places
        post= value[2]
        # Post-places condition
        post_str= "("
        for idx_post,item_post in enumerate(post):
            # Not last element
            if idx_post < len(post)-1:
                post_str= post_str + "!" + item_post + " & "
            else:
                post_str= post_str + "!" + item_post

        post_str= post_str + ")"

        # Append transition name to output
        out_str= out_str + key + ":= "
        # Append pre-place condition
        out_str= out_str + pre_str + " & "
        # Append inputs condition
        out_str= out_str + req_str + " & "
        # Append post-place condition
        out_str= out_str + post_str + ";\n"

    return out_str


def stab_definition(in_dict):
    """Define stability checking condition in NuSMV

    Parameters:
    ----------
    in_dict: dict

    Returns:
    -------
    out_str: string
    """
    out_str="stab:= !("

    keys= list(in_dict)
    for idx,key in enumerate(keys):
        # If not last item
        if idx < len(keys)-1:
            # Append transition name and add OR
            out_str= out_str + key + " | "
        else:
            # Append transition name
            out_str= out_str + key

    # Add closing brace and semicolon
    out_str= out_str + ");\n"

    return out_str


def output_definition(in_dict):
    """Define output set/reset and equivalent condition in NuSMV

    Parameters:
    ----------
    in_dict: dict

    Returns:
    -------
    out_str: string
    """

    # Get set of boolean outputs
    output_set= set()

    for key in list(in_dict):
        if not key == "initial":
            for output in in_dict[key][0][0]:
                output_set.add(output)
            for output in in_dict[key][0][1]:
                output_set.add(output)
    
    # Sort alphabetically
    output_set= sorted(output_set)
    
    # Collate list of places for which each output is set/reset
    output_dict= OrderedDict()

    for output in output_set:
        # Initialize list of places for which output is set/reset
        output_dict[output]= [[],[]]

    for output in output_set:
        # Initialize list of places for which output is set/reset
        output_dict[output]= [[],[]]

        for key in list(in_dict):
            # Add places for which output is set
            if output in in_dict[key][0][0]:
                output_dict[output][0].append(key)

            # Add places for which output is reset
            if output in in_dict[key][0][1]:
                output_dict[output][1].append(key)

    # Generate output string
    set_output_str= "-- SET\n"
    reset_output_str= "-- RESET\n"
    output_str= "-- OUTPUT\n"

    # Loop through output keys
    for key in list(output_dict):
        output= output_dict[key]

        # Get set places
        set_output_str= set_output_str +  key + "_set:= "
        # If the output is set at at least one place
        if len(output[0]) > 0:
            for idx_set,place_set in enumerate(output[0]):
                # Not last item
                if idx_set < len(output[0])-1:
                    set_output_str= set_output_str + output[0][idx_set] + " | "
                # Last Item
                else:
                    set_output_str= set_output_str + output[0][idx_set] + ";\n"
        # If output is not set at any place
        else:
            set_output_str= set_output_str + "FALSE;\n"

        # Get reset places
        reset_output_str= reset_output_str +  key + "_reset:= "
        # If output is reset at at least 1 place
        if len(output[1]) > 0:
            for idx_reset,place_reset in enumerate(output[1]):
                # Not last item
                if idx_reset < len(output[1])-1:
                    reset_output_str= reset_output_str + output[1][idx_reset] + " | "
                # Last Item
                else:
                    reset_output_str= reset_output_str + output[1][idx_reset] + ";\n"

        # If output is not reset at any place
        else:
            reset_output_str= reset_output_str + "FALSE;\n"


        # Compose output string
        output_str= output_str + key + ":= " + key + "_set & !" + key + "_reset;\n" 


    # Non-boolean outputs
    # Get dictionary of outputs, the places that set them, and their assigned values
    output_dict= dict()

    for key in list(in_dict):
        if not key == "initial":
            # Check if exists
            try:
                if in_dict[key][1] and isinstance(in_dict[key][1], list):
                    # Get string
                    val= in_dict[key][1][0]
                    # Split string on :=
                    output_name, aa, output_val= val.partition(":=") 
                    output_dict[output_name]= [key, output_val]
            except: 
                pass

    nb_output_str= "-- Non-Boolean Outputs\n"

    # Compose string to set outputs
    for key in list(output_dict):
        nb_output_str= nb_output_str + key + ":= case\n" + \
            "   " + output_dict[key][0] + ": " + output_dict[key][1] + ";\n" + \
            "   TRUE: 0;\n" + \
            "esac;\n"

    # Return
    out_str= set_output_str + reset_output_str + output_str+ nb_output_str

    return out_str

