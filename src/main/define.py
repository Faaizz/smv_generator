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
            high_ins= item[0]
            low_ins= item[1]
            # Temp string opening brace
            temp_str= "("
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
