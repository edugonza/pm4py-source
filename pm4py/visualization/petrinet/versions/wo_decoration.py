from pm4py.models.petri import visualize

def apply(net, initial_marking, final_marking, log=None, parameters=None):
    """
    Apply method for Petri net visualization (useful for recall from factory; it calls the graphviz_visualization method)

    Parameters
    -----------
    net
        Petri net
    initial_marking
        Initial marking
    final_marking
        Final marking
    log
        (Optional) trace log
    parameters
        Algorithm parameters

    Returns
    -----------
    viz
        Graph object
    """
    return visualize.apply(net, initial_marking, final_marking, parameters=parameters)