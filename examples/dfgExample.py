import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from pm4py.algo.dfg import factory as dfg_factory, replacement as dfg_replacement
from pm4py.log.importer import xes as xes_importer
from pm4py.filtering.tracelog.auto_filter import auto_filter
from pm4py.filtering.tracelog.attributes import attributes_filter
from pm4py.visualization.dfg import factory as dfg_vis_factory

# measure could be frequency or performance
measure = "frequency"
log = xes_importer.import_from_file_xes('..\\tests\\inputData\\running-example.xes')
filtered_log = auto_filter.apply_auto_filter(log)
filtered_log_activities_count = attributes_filter.get_activities_from_log(filtered_log)
intermediate_log = attributes_filter.filter_log_by_specified_attributes(log, list(filtered_log_activities_count.keys()))
dfg_filtered_log = dfg_factory.apply(filtered_log, variant=measure)
dfg_intermediate_log = dfg_factory.apply(intermediate_log, variant=measure)
dfg_filtered_log = dfg_replacement.replace_values(dfg_filtered_log, dfg_intermediate_log)

gviz = dfg_vis_factory.apply(dfg_filtered_log, log=intermediate_log)
gviz.view()
#base64 = dfg_visualize.return_diagram_as_base64(activities_count, dfg_filtered_log, measure=measure)
#print(base64)