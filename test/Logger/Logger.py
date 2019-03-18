import time
import datetime
import os
import pandas as pd


class AverageMeter(object):
    """Sum values to compute the mean."""
    def __init__(self):
        self.reset()

    def reset(self):
        self.count = 0
        self.sum = 0
        
    def update(self, val):
        self.count += 1
        self.sum += val
        
    def average(self):
        return self.sum / self.count

class MetricsLogger(object):
    """Track the values of different metrics, display their average values and save them
    in a log file."""
    def __init__(self, log_name=None):        
        # Make name of log file
        if log_name is None:
            log_name = ''
        else:
            log_name = log_name + '_'
        
        dt_str = '_'.join(str(datetime.datetime.now()).split('.')[0].split(' '))
        dt_str = dt_str.replace('-', '').replace(':', '')
        self.log_filename = log_name + dt_str + ".log"
        
        # Make logs directory if necessary
        if '/' not in self.log_filename:
            log_dir = "logs"
            if not os.path.isdir(log_dir):
                os.mkdir(log_dir)
            self.log_filename = os.path.join(log_dir, self.log_filename)
        
        # Initialize average meters
        self.reset()
    
    def reset(self):
        """Reset the metrics average meters."""
        self.avgmeters = {}
        self.last_update = time.time()
    
    def update(self, values, show=True):
        """Update metrics values and display their current average if show is True."""
        for key in values:
            if key not in self.avgmeters:
                self.avgmeters[key] = AverageMeter()
            self.avgmeters[key].update(values[key])
            
        if show:
            self._show()
            
    def save_log(self):
        """Write current average value of each metrics in a text file."""
        with open(self.log_filename, 'a') as f:
            f.write(str(self) + '\n')
            
    def get_log_df(self):
        return Get_log_df(self.log_filename)
    
    def _average(self):
        return {key: self.avgmeters[key].average() for key in self.avgmeters}
            
    def __str__(self):
        avg = self._average()
        str_list = [key + ": %.4f" % round(avg[key], 4) for key in avg]
        return (" - ").join(str_list)
    
    def _show(self, t_thresh=0.1):
        t_now = time.time()
        if t_now - self.last_update >= t_thresh:
            print(str(self), end='\r', flush=True)
            self.last_update = t_now
            
def Get_log_df(log_filename):
    """Return the content of a log file as a Dataframe."""
    # Open and read log file
    with open(log_filename, 'r') as f:
        logs = f.read()

    # Get keys appearing in log file and convert each line into dict
    keys = []
    log_list_of_dict = []
    for l in logs.split('\n'):
        kvs = l.split(' - ')
        line_dict = {}

        for kv in kvs:
            if ':' in kv:
                k, v = kv.split(': ')
                line_dict[k] = float(v)

                if k not in keys:
                    keys.append(k)

        if len(line_dict) > 0:
            log_list_of_dict.append(line_dict)

    # Make dictionnary of list of values
    log_dict_of_list = {}
    for k in keys:
        log_dict_of_list[k] = []

    # Append values to lists
    for line_dict in log_list_of_dict:
        for k in keys:
            if k in line_dict:
                log_dict_of_list[k].append(line_dict[k])
            else:
                log_dict_of_list[k].append(None)

    # Make dataframe
    log_df = pd.DataFrame(log_dict_of_list)
    return log_df