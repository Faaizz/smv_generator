from collections import OrderedDict


def transition_definition(in_dict):
    """Define transitions and stability in ST

    Parameters:
    ----------
    in_dict: dict

    Returns:
    -------
    out_str: string
    """

    out_str= "STABLE:=0;\n" + \
        "WHILE STABLE=0 DO\n" + \
        "   STABLE:=1;\n"

    # Iterate over items
    for key in iter(in_dict):
        # Get value of current transition
        value= in_dict[key]

        # Pre-places
        pre= value[0]
        # Pre-places condition
        pre_str= "("
        # Pre-places assignment
        pre_ass_str= ""
        for idx,item in enumerate(pre):
            # Not last element
            if idx < len(pre)-1:
                pre_str= pre_str + item + " AND "
            else:
                pre_str= pre_str + item
            # Assignment
            pre_ass_str= pre_ass_str + "       " + item + ":=0;\n"

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
                # Replace & with AND
                temp_temp= item[0].replace("&", "AND")
                # Replace | with OR
                temp_temp= temp_temp.replace("|", "OR")
                # Replace ! with NOT
                temp_temp= temp_temp.replace("!", "NOT ")

                temp_str= temp_str + temp_temp
            
            else:
                high_ins= item[0]
                low_ins= item[1]
                # temp inputs
                for idx_high,high_in in enumerate(high_ins):
                    # Not last item
                    if idx_high < len(high_ins)-1:
                        temp_str= temp_str + high_in + " AND "
                    # If last item
                    else:
                        # If there are no low outputs required
                        if len(low_ins) < 1:
                            temp_str= temp_str + high_in
                        else:
                            temp_str= temp_str + high_in + " AND "
                
                # Low inputs
                for idx_low,low_in in enumerate(low_ins):
                    # Not last item
                    if idx_low < len(low_ins)-1:
                        temp_str= temp_str + "NOT " + low_in + " AND "
                    # If last item
                    else:
                        temp_str= temp_str + "NOT " + low_in

            # Temp string closing brace
            temp_str= temp_str + ")"   

            # If not last item, add an OR operator
            if idx_out < (len(req_inputs)-1):
                temp_str= temp_str + " OR "

            # Append Temp string to req_str
            req_str= req_str + temp_str

        # req_str closin brace
        req_str= req_str + " )"

        # Post-places
        post= value[2]
        # Post-places condition
        post_str= "("
        # Post places assignment
        post_ass_str= ""
        for idx_post,item_post in enumerate(post):
            # Not last element
            if idx_post < len(post)-1:
                post_str= post_str + "NOT " + item_post + " AND "
            else:
                post_str= post_str + "NOT " + item_post
            # Assignment
            post_ass_str= post_ass_str + "       " + item_post + ":=1;\n"

        post_str= post_str + ")"

        # Append transition name to output
        out_str= out_str + "   (*" + key + "*)\n"
        # Append if statement
        out_str= out_str + "   IF "
        # Append pre-place condition
        out_str= out_str + pre_str + " AND "
        # Append inputs condition
        out_str= out_str + req_str + " AND "
        # Append post-place condition
        out_str= out_str + post_str
        # Add then keyword
        out_str= out_str + " THEN\n"
        # Assignments
        out_str= out_str + pre_ass_str
        out_str= out_str + post_ass_str
        # Stable
        out_str= out_str + "       STABLE:=0;\n"
        # End if
        out_str= out_str + "   END_IF;\n"


    # End while
    out_str= out_str + "END_WHILE;\n"

    return out_str



def output_definition(in_dict):
    """Define output set/reset and equivalent condition in ST

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

        for key in list(in_dict):
            # Add places for which output is set
            if output in in_dict[key][0][0]:
                output_dict[output][0].append(key)

            # Add places for which output is reset
            if output in in_dict[key][0][1]:
                output_dict[output][1].append(key)

    # Generate output string
    set_output_str= ""
    reset_output_str= ""

    # Loop through output keys
    for key in list(output_dict):
        output= output_dict[key]

        # If the output is set at at least one place
        if len(output[0]) > 0:
            # Get set places
            set_output_str= set_output_str + "(*" +   key + "*)\n"
            set_output_str= set_output_str + "IF "
            for idx_set,place_set in enumerate(output[0]):
                # Not last item
                if idx_set < len(output[0])-1:
                    set_output_str= set_output_str + output[0][idx_set] + " OR "
                # Last Item
                else:
                    set_output_str= set_output_str + output[0][idx_set] + " THEN\n"
                
            set_output_str= set_output_str + "   " + key + ":=1;\n" + "END_IF;\n"

        
        # If output is reset at at least 1 place
        if len(output[1]) > 0:
            # Get reset places
            reset_output_str= reset_output_str + "(*" +   key + "*)\n"
            reset_output_str= reset_output_str + "IF " 
            for idx_reset,place_reset in enumerate(output[1]):
                # Not last item
                if idx_reset < len(output[1])-1:
                    reset_output_str= reset_output_str + output[1][idx_reset] + " OR "
                # Last Item
                else:
                    reset_output_str= reset_output_str + output[1][idx_reset] + " THEN\n"
                
            reset_output_str= reset_output_str + "   " + key + ":=0;\n" + "END_IF;\n"



    # Non-boolean outputs
    # Get dictionary of outputs, the places that set them, and their assigned values
    output_list= list()

    for key in list(in_dict):
        if not key == "initial":
            # Check if exists
            try:
                if in_dict[key][1] and isinstance(in_dict[key][1], list):
                    # Get string
                    val= in_dict[key][1][0]
                    # Split string on :=
                    output_name, aa, output_val= val.partition(":=") 
                    output_list.append([output_name, key, output_val])
            except:
                pass

    nb_output_str= ""
    
    # Compose string to set outputs
    for output in output_list:
        nb_output_str= nb_output_str + "(*" + output[0] + "*)\n" + \
            "IF " + output[1] + " THEN\n" + \
            "   " + output[0] + ":=" + output[2] + ";\n" + \
            "END_IF;\n"

    # Return
    out_str= set_output_str + reset_output_str + nb_output_str

    return out_str

