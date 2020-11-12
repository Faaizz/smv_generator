
def manual(in_dict):
    """Add manually entered specifications in NuSMV

    Parameters:
    ----------
    in_dict: dict

    Returns:
    -------
    out_str: string
    """

    out_str= ""

    # Loop through items
    for spec in in_dict["manual"]:
        out_str= out_str + "SPEC\n" + spec + ";\n"

    return out_str

