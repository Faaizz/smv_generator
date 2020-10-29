

def input_declaration(in_dict):
    """Declare input variables in NuSMV

    Parameters:
    ----------
    in_dict: dict

    Returns:
    -------
    out_str: string
    """

    # Assert input type
    assert type(in_dict) == "<type 'dict'>"

    out_str= "";

    # loop through elements
    for idx,val in enumerate(in_dict):
        temp= "";