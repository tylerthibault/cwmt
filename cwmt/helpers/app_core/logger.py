from flask import flash
import datetime
import os

class Logger:
    level = {
        'debug': 0,
        'info': 1,
        'warning': 2,
        'error': 3,
        'critical': 4,
    }

    def __init__(self, log_file=None):
        # Accept an optional log_file parameter
        self.log_file = self.init_log_file(log_file)
        self.level = Logger.level['info']

    def init_log_file(self, log_file=None):
        if log_file is None:
            # Set default directory and file name if no log_file is provided
            log_dir = os.path.join(os.getcwd(), "logs")
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            log_file = os.path.join(log_dir, f'log_{today}.txt')
        else:
            log_dir = os.path.dirname(log_file)
            today = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # Create folder if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Create dated log file if it doesn't exist
        if not os.path.exists(log_file):
            with open(log_file, 'w') as f:
                f.write(f'Log file created on {today}\n')
        
        return log_file

    def log(self, message, with_flash=False, flash_category='error', status='info'):
        if Logger.level[status] >= self.level:
            with open(self.log_file, 'a') as f:
                msg = f'{status.upper()} | {datetime.datetime.utcnow()}: {message}'
                f.write(msg + '\n')

        if with_flash:
            flash(message, flash_category)