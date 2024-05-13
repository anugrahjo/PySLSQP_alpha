import warnings
import numpy as np
try:
    import h5py
except ImportError:
    warnings.warn("h5py not found, saving and loading data disabled")
    h5py = None

def import_h5py_file(filepath):
    if h5py is None:
        raise ImportError("h5py not found, saving and loading data disabled")
    try:
        return h5py.File(filepath, 'r')
    except:
        raise FileNotFoundError(f"File {filepath} not found or not a valid h5py file.")
    
def save_iteration(file, iter, vars, out_dict):
    '''
    Save the data from one iteration to an active file.

    Parameters
    ----------
    file : str
        Loaded file.
    iter : int
        Iteration number.
    vars : list
        List of variable names to save.
    out_dict : dict
        Dictionary with variable names as keys and variable values as values.
    '''
    file.create_group('iter_' + str(iter))
    for var in vars:
        file[f'iter_{iter}'][var] = out_dict[var]
    
def print_dict_as_table(data):
    """
    Print a dictionary as a table.

    Parameters
    ----------
    data : dict
        Dictionary to print as a table.
    """
    print("--------------------------------------------------")
    for key, value in data.items():
        print(f"        {key:20} : {value}")
    print("--------------------------------------------------")
    
def print_file_contents(file_path):
    '''
    Print the contents of the saved file.
    
    Parameters
    ----------
    file_path : str
        Path to the saved file.        
    '''
    file = import_h5py_file(file_path)
    print("Available data in the file:")
    print("---------------------------")
    try:
        print("     Attributes of optimization  :", list(file.attrs.keys()))
    except:
        warnings.warn("No attributes found in the file.")
    try:
        print("     Saved variable iterates     :", list(file['iter_0'].keys()))
    except:
        warnings.warn("No variable iterates found in the file.")
    try:
        print("     Results of Optimization     :", list(file['results'].keys()))
    except:
        warnings.warn("No results found in the file.")
    file.close()

def load_variables(filepath, vars, itr_start=0, itr_end=-1, major_iter=False):
    '''
    Load specified variable iterates between itr_start and itr_end from the saved file.
    Returns a dictionary with the variable names as keys and list of variable iterates as values.
    Note the variables at itr_start and itr_end are included in the output.

    Parameters
    ----------
    filepath : str
        Path to the saved file.
    vars : str or list
        Variable names to load from the saved file.
    itr_start : int, default=0
        Starting iteration to load the variables from.
        Negative indices are allowed with -1 representing the last iteration
        and -2 representing the second last iteration and so on.
    itr_end : int, default=-1
        Ending iteration to load the variables from. 
        Negative indices are allowed with -1 representing the last iteration
        and -2 representing the second last iteration and so on.
    major_iter : bool, default=False
        If True, only major iterations are loaded.
        If False, all iterations are loaded irrespective of major or line search iterations.

    Returns
    -------
    out_data : dict
        Dictionary with variable names as keys and list of variable iterates as values.
    '''
    if not isinstance(filepath, str):
        raise ValueError("filepath must be a string.")
    
    if not isinstance(vars, (str, list)):
        raise ValueError("vars must be a string or a list of strings")
    if isinstance(vars, str):
        vars = [vars]
    if not all(isinstance(var, str) for var in vars):
        raise ValueError("vars must be a string or a list of strings")
    
    if not isinstance(itr_start, int):
        raise ValueError("itr_start must be an integer.")
    if not isinstance(itr_end, int):
        raise ValueError("itr_end must be an integer.")
    
    file  = import_h5py_file(filepath)
    print(file.keys())
    niter = len(file.keys()) - 2 # Number of iterations saved in the file [excludes 0th iteration and results]
    num_saves = len(file.keys()) - 1 # Number of iterations saved [includes 0th iteration but excludes results]
    if major_iter:
        niter = file['results']['num_majiter'][()]
    if (-(niter+1) <= itr_start <= niter) and (-(niter+1) <= itr_end <= niter):
        start = itr_start * 1
        if itr_start < 0:
            start = niter + itr_start + 1
        end = itr_end * 1
        if itr_end < 0:
            end = niter + itr_end + 1
        if start > end:
            raise ValueError(f"itr_start index ({start}) must be less than itr_end index ({end}).")
    else:
        raise ValueError(f"itr_start {itr_start} and itr_end {itr_end} must be within bounds (>={-(niter+1)} and <={niter}).")
    

    out_data = {}
    for var in vars:
        if var not in file['iter_0'].keys():
            raise ValueError(f"Variable {var} not found in the file.")
        out_data[var] = []

    if major_iter:
        for i in range(num_saves):
            if file[f'iter_{i}']['ismajor'][()] and file[f'iter_{i}']['majiter'][()] >= start:
                for var in vars:
                    out_data[var].append(file[f'iter_{i}'][var][()])
                if file[f'iter_{i}']['majiter'][()] == end:
                    break
    else:
        for i in range(start, end+1):
            for var in vars:
                out_data[var].append(file[f'iter_{i}'][var][()])
    
    file.close()

    return out_data

def load_results(filepath):
    '''
    Load the results of optimization from the saved file as a dictionary.

    Parameters
    ----------
    filepath : str
        Path to the saved file.

    Returns
    -------
    out_data : dict
        Dictionary with optimization results.
    '''
    file = import_h5py_file(filepath)
    result_dict = {}
    for key in file['results'].keys():
        result_dict[key] = file['results'][key][()]
        if key == 'message':
            result_dict[key] = result_dict[key].decode('utf-8')
    file.close()
    return result_dict

def load_attributes(filepath):
    '''
    Load the attributes of optimization from the saved file as a dictionary.

    Parameters
    ----------
    filepath : str
        Path to the saved file.

    Returns
    -------
    out_data : dict
        Dictionary with optimization attributes.
    '''
    file = import_h5py_file(filepath)
    attr_dict = {}
    for key in file.attrs.keys():
        attr_dict[key] = file.attrs[key]
    file.close()
    return attr_dict

if __name__ == "__main__":
    # print_file_contents('eq_slsqp.hdf5')
    # print_file_contents('ineq_slsqp.hdf5')
    # print_dict_as_table(load_variables('eq_slsqp.hdf5', 'iter', itr_start=0, itr_end=-1, major_iter=False))
    # print_dict_as_table(load_variables('eq_slsqp.hdf5', ['iter', 'majiter', 'mode'], itr_start=0, itr_end=-1, major_iter=True))
    # print_dict_as_table(load_attributes('eq_slsqp.hdf5'))
    # print_dict_as_table(load_results('eq_slsqp.hdf5'))
    print_dict_as_table(load_variables('options_slsqp.hdf5', 'x'))
    print_dict_as_table(load_results('options_slsqp.hdf5'))
    print_dict_as_table(load_variables('options_slsqp_hot.hdf5', 'x'))
    print_dict_as_table(load_results('options_slsqp_hot.hdf5'))
