import sys
from src.ml_project.logger import logging


def customizing_exception(exception:Exception, sys:sys):
    _,_,exc_tb =  sys.exc_info()                        # gets execution info
    file_name=exc_tb.tb_frame.f_code.co_filename        # get file name of occured exception
    error_message=f"Error occured in [{file_name}], line [{exc_tb.tb_lineno}], message [{str(exception)}]. "

    return error_message

class CustomException(Exception):
    def __init__(self, exception:Exception, sys:sys):
        super().__init__(exception)
        self.exception = customizing_exception(exception, sys)

    def __str__(self):
        return self.exception