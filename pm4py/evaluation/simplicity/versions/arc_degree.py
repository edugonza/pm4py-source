def apply(petri_net, parameters=None):
    """
    Gets simplicity from a Petri net

    The approach is suggested in the paper
    Blum, Fabian Rojas. Metrics in process discovery. Technical Report TR/DCC-2015-6,
    Computer Science Department, University of Chile, 2015.

    Parameters
    -----------
    petri_net
        Petri net

    Returns
    -----------
    simplicity
        Simplicity measure associated to the Petri net
    """
    arcDegree = 0.0
    if len(petri_net.transitions) > 0:
        arcDegree = float(len(petri_net.places)) / float(len(petri_net.transitions))
    simplicity = 1.0 / (1.0 + arcDegree)
    return simplicity