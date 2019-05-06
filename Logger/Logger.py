import pandas as pd
import time
import sys

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
    def __init__(self):            
        self.log_df = pd.DataFrame()
        self.n = 0
        self.reset()
    
    def reset(self):
        """Reset the metrics average meters."""
        # Save last epoch average value of metrics (unless it's the first epoch)
        if self.n > 0:
            self.log_df = self.log_df.append(self._average(), ignore_index=True)
        self.n += 1
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
    
    def save_log(self, path):
        """Save log dataframe to path."""
        self.log_df.to_csv(path, index=False)
    
    def _average(self):
        return {key: self.avgmeters[key].average() for key in self.avgmeters}
            
    def __str__(self):
        avg = self._average()
        str_list = [key + ": %.4f" % round(avg[key], 4) for key in avg]
        return (" - ").join(str_list)
    
    def _show(self, t_thresh=0.1):
        t_now = time.time()
        if t_now - self.last_update >= t_thresh:
            sys.stdout.write("\r" + str(self))
            sys.stdout.flush()
            self.last_update = t_now
