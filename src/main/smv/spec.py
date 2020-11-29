
def manual(in_dict):
    """Add manually entered specifications in NuSMV

    Parameters:
    ----------
    in_dict: dict
        Dictionary of "manual" attribute of the "specifications" object

    Returns:
    -------
    out_str: string
    """

    out_str= ""

    # Loop through items
    for spec in in_dict["manual"]:
        out_str= out_str + "SPEC\n" + spec + ";\n"

    return out_str


def auto(in_dict):
    """Automatically generate specifications for some general properties of SIPNs
    
    Parameters:
    ----------
    in_dict: dict
        Dictionary of root json object

    Returns:
    -------
    out_str: str
    """

    out_str= ""

    try:
        if in_dict["specifications"]["auto"]:
            gen_auto= True
        else:
            gen_auto= False
    except KeyError:
        gen_auto= False

    # If auto specs requested
    if gen_auto:

        #============================================================
        # Liveness, deadlocks, and dead transitions
        liveness= "--CHECK LIVENESS\n"
        deadlock_st= "--CHECK DEADLOCKS\n" + "SPEC\n" + "AG(EF("
        deadlock= ""
        deadlock_end= " ));\n"
        dead= "--CHECK DEAD TRANSITIONS\n"

        # Transitions
        transitions= list(in_dict["transitions"])

        for idx,transition in enumerate(transitions):
            liveness= liveness +\
                "SPEC\n" +\
                "AG(EF({0}));\n".format(transition)

            dead= dead +\
                "SPEC\n" +\
                "EF({0});\n".format(transition)

            # Check if last element
            if (idx+1) == len(transitions):
                deadlock= deadlock + " {0}".format(transition)
            # Otherwise
            else:
                deadlock= deadlock + " {0} |".format(transition)

        # Output
        out_str= out_str + liveness + deadlock_st + deadlock +\
             deadlock_end + dead

        #============================================================
        # Unstable cycles
        unstable_cycles= "--CHECK UNSTABLE CYCLES\n" + "SPEC\n" + "AG(EF(stab));\n"

        # Output
        out_str= out_str + unstable_cycles


        #============================================================
        # Contradictory and empty outputs

        # Boolean outputs
        bool_outputs= [
            key for key in list(in_dict["outputs"]) \
            if "%QX" in in_dict["outputs"][key][0] 
            ]

        contradictory= "--CHECK CONTRADICTORY OUTPUTS\n" 
        empty= "--CHECK EMPTY OUTPUTS\n"

        for output in bool_outputs:
            contradictory= contradictory +\
                "SPEC\n" +\
                "AG( stab -> ! ({0}_set & {0}_reset) );\n".format(output)

            empty= empty +\
                "SPEC\n" +\
                "AG( stab -> {0}_set | {0}_reset );\n".format(output)

        # Output
        out_str= out_str + contradictory + empty


    # Return
    return out_str

