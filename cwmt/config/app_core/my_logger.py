# from cwmt.config.app_core import AppCore
from cwmt.config.app_core.status_codes import StatusCode, StatusCodes
from flask import flash
import inspect


class MyLogger:
    @staticmethod
    def log(status_code:StatusCode, e:Exception=None, should_print:bool=False, should_flash:bool=False, should_log:bool=False, logger=[]):


        if e is not None:
            msg = f"[{status_code.code}] {status_code.pub_msg}. Exception: {e}"
        else:
            msg = f"[{status_code.code}] {status_code.pub_msg}"

        if should_print:
            MyLogger._print_to_console(msg)
        
        if should_flash:
            flash(msg, status_code.flash_color)
        
        if should_log:
            MyLogger._log_to_logger(msg, logger)
        return None
    
    @staticmethod
    def _print_to_console(msg:str, e:Exception=None):
        loc = MyLogger._get_call_location()

        print("*"*50)
        if e is None:
            print(f"msg:{msg} || loc:{loc}")
        else:
            print(f"msg:{msg} || loc:{loc} || Exception: {e}")
        print("*"*50)
    
    @staticmethod
    def _log_to_logger(message:str, all_loggers):
        for l in all_loggers:
            l.error(f"{message}")

    @staticmethod
    def _get_call_location():
        frame = inspect.currentframe()
        caller_frame = frame.f_back.f_back.f_back  # Go back two frames to get the caller
        file_name = caller_frame.f_code.co_filename
        line_number = caller_frame.f_lineno
        return (file_name, line_number)