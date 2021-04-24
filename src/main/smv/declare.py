

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
        value= in_dict[key][0]
        # Check if SMV type is not a list
        if not isinstance(value, list):
            # Type is boolean
            input_type= value
        
        else: 
            # Type is specified as raw string
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
        if not key == "initial":
            temp= key + ": " + "boolean;\n"
            out_str= out_str + temp

    return out_str



def internal_declaration(in_dict):
    """Declare internal variables (and modules if necessary) in NuSMV

    Parameters:
    ----------
    in_dict: dict
        "internal" attribute of root json object

    Returns:
    -------
    out_modules: str
        Modules declaration

    out_main: str
        Variables declaration in main module
    """

    out_modules= ""
    out_main= "\n\n-- INTERNAL\n"

    modules= []

    # Declaration in Main module
    # Loop through elements to check for MODULES
    for key in list(in_dict):
        if isinstance(in_dict[key][0][0], str):
            if in_dict[key][0][0] == "MODULE":
                modules.append(key)
                out_main= out_main + "{0}: {0}_mod;\n".format(key)

            # Non modules
            else:
                out_main= out_main + "{0}: {1};\n".format(key, in_dict[key][0][0])

    
    # Declaration of additional modules
    for module in modules:
        out_modules= out_modules + "MODULE {0}_mod\n".format(module)
        out_modules= out_modules + "VAR\n"
        modules_assign= "ASSIGN\n"

        mod_vars= in_dict[module][0][1]
        for mod_var in list(mod_vars):
            # Simple string declaration of varianle
            if isinstance(mod_vars[mod_var], str) \
                and mod_vars[mod_var] == "boolean":
                out_modules= out_modules + "{0}: boolean;\n".format(mod_var)
                # Assignment
                modules_assign= modules_assign + "init({0})".format(mod_var) + ":= {TRUE, FALSE};\n"
                modules_assign= modules_assign + "next({0})".format(mod_var) + ":= {TRUE, FALSE};\n"

            # Complex declaration
            else:
                out_modules= out_modules + '{0}: {1};\n'.format(mod_var, mod_vars[mod_var][0])
                # Assignment
                modules_assign= modules_assign + 'init({0})'.format(mod_var) + ':= "{}";\n'.format(mod_vars[mod_var][1])
                modules_assign= modules_assign + 'next({0})'.format(mod_var) + ':= {};\n'.format(mod_vars[mod_var][2])

        out_modules= out_modules + modules_assign


    # Return
    return (out_modules, out_main)
