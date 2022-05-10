import os
import json
import app.config

#15
def test_logfile_misc_debug():
    """ check if misc_debug.log exists """
    test_path = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(test_path, '../app/logs')
    filepath = os.path.join(log_dir, "misc_debug.log")
    assert os.path.isfile(filepath) #== False

#16
def test_logfile_misc_debug():
    """ check if misc_debug.log exists """
    log_dir = app.config.Config.LOG_DIR
    filepath = os.path.join(log_dir, "misc_debug.log")
    assert os.path.isfile(filepath) == False

#17
def test_logfile_request():
    """ check if misc_debug.log exists """
    test_path = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(test_path, '../app/logs')
    filepath = os.path.join(log_dir, "request.log")
    assert os.path.isfile(filepath) == False