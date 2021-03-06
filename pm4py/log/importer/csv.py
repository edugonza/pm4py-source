from pm4py import log
import pandas as pd
import tempfile, os
from pm4py.log.importer.utils import df_filtering

def import_dataframe_from_csv_string(csv_string, sep=',', quotechar=None, nrows=None, sort=False, sort_field="time:timestamp"):
    """
    Import dataframe from CSV string

    Parameters
    -----------
    csv_string
        CSV string
    sep
        CSV columns delimiter
    quotechar
        (if specified) Character that starts/end big strings in CSV
    nrows
        (if specified) Maximum number of rows to read from the CSV
    sort
        Boolean value that tells if the CSV should be ordered
    sort_field
        If sort option is enabled, then the CSV is automatically sorted by the specified column

    Returns
    -----------
    df
        Pandas dataframe
    """
    fp = tempfile.NamedTemporaryFile(suffix='.csv')
    fp.close()
    with open(fp.name, 'w') as f:
        f.write(csv_string)
    df = import_dataframe_from_path(fp.name, sep=sep, quotechar=quotechar, nrows=nrows, sort=sort, sort_field=sort_field)
    os.remove(fp.name)
    return df

def import_from_csv_string(csv_string, sep=',', quotechar=None, nrows=None, sort=False, sort_field="time:timestamp", insert_event_indexes=False):
    """
    Import CSV log from CSV string

    Parameters
    -----------
    csv_string
        CSV string
    quotechar
        (if specified) Character that starts/end big strings in CSV
    nrows
        (if specified) Maximum number of rows to read from the CSV
    sort
        Boolean value that tells if the CSV should be ordered
    sort_field
        If sort option is enabled, then the CSV is automatically sorted by the specified column


    Returns
    -----------
    log
        Event log
    """
    fp = tempfile.NamedTemporaryFile(suffix='.csv')
    fp.close()
    with open(fp.name, 'w') as f:
        f.write(csv_string)
    log = import_from_path(fp.name, sep=sep, quotechar=quotechar, nrows=nrows, sort=sort, sort_field=sort_field, insert_event_indexes=insert_event_indexes)
    os.remove(fp.name)
    return log

def import_dataframe_from_path_wo_timeconversion(path, sep=',', quotechar=None, nrows=None):
    """
    Imports a dataframe from the given path (without doing the timestamp columns conversion)

    Parameters
    ----------
    path:
        Input CSV file path
    sep:
        column separator
    quotechar
        (if specified) Character that starts/end big strings in CSV
    nrows
        (if specified) Maximum number of rows to read from the CSV

     Returns
    -------
    pd
        Pandas dataframe
    """
    if quotechar:
        if nrows:
            df = pd.read_csv(path, sep=sep, quotechar=quotechar, nrows=nrows)
        else:
            df = pd.read_csv(path, sep=sep, quotechar=quotechar)
    else:
        if nrows:
            df = pd.read_csv(path, sep=sep, nrows=nrows)
        else:
            df = pd.read_csv(path, sep=sep)

    return df

def convert_timestamp_columns_in_df(df):
    """
    Convert all dataframe columns in a dataframe

    Parameters
    -----------
    df
        Dataframe

    Returns
    ------------
    df
        Dataframe with timestamp columns converted
    """
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_datetime(df[col])
            except ValueError:
                    pass
    return df

def import_dataframe_from_path(path, sep=',', quotechar=None, nrows=None, sort=False, sort_field="time:timestamp"):
    """
    Imports a dataframe from the given path

    Parameters
    ----------
    path:
        Input CSV file path
    sep:
        column separator
    quotechar
        (if specified) Character that starts/end big strings in CSV
    nrows
        (if specified) Maximum number of rows to read from the CSV
    sort
        Boolean value that tells if the CSV should be ordered
    sort_field
        If sort option is enabled, then the CSV is automatically sorted by the specified column

     Returns
    -------
    pd
        Pandas dataframe
    """
    df = import_dataframe_from_path_wo_timeconversion(path, sep=sep, quotechar=quotechar, nrows=nrows)
    df = convert_timestamp_columns_in_df(df)
    if sort and sort_field:
        df = df.sort_values(sort_field)
    return df

def convert_dataframe_to_event_log(df):
    """
    Converts a dataframe to an event log

    Parameters
    ----------
    df
        Pandas dataframe

     Returns
    -------
    log : :class:`pm4py.log.log.EventLog`
        An event log
    """
    return log.log.EventLog(df.to_dict('records'), attributes={'origin': 'csv'})

def import_from_path(path, sep=',', quotechar=None, nrows=None, sort=False, sort_field="time:timestamp", insert_event_indexes=False):
    """
    Imports a CSV file from the given path

    Parameters
    ----------
    path:
        Input CSV file path
    sep:
        column separator
    quotechar
        (if specified) Character that starts/end big strings in CSV
    nrows
        (if specified) Maximum number of rows to read from the CSV
    sort
        Boolean value that tells if the CSV should be ordered
    sort_field
        If sort option is enabled, then the CSV is automatically sorted by the specified column

     Returns
    -------
    log : :class:`pm4py.log.log.EventLog`
        An event log
    """
    df = import_dataframe_from_path(path, sep=sep, quotechar=quotechar, nrows=nrows, sort=sort, sort_field=sort_field)
    event_log = convert_dataframe_to_event_log(df)

    if insert_event_indexes:
        event_log.insert_event_index_as_event_attribute()

    return event_log