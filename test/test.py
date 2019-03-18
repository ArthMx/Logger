from Logger import MetricsLogger
from tqdm import tqdm
import time

logger = MetricsLogger()

for i in tqdm(range(10)):
    logger.reset()
    
    for j in tqdm(range(10)):
        time.sleep(0.1)
        logger.update({"j": j + i})
        
    for k in range(10):
        time.sleep(0.05)
        logger.update({"k": k + i / 2})
        
    logger.save_log()
    

test_log_df = logger.get_log_df()
test_log_df

test_log_df.plot()