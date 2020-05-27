import sys
from cx_Freeze import setup, Executable
from multiprocessing import pool
from queue import Queue
import threading
import os

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
build_exe_options = {"packages": ["os",""
                                       "queue","threading","scipy"], "excludes": ["tkinter","scipy.spatial.cKDTree"],'includes': ['atexit','multiprocessing','scipy.sparse.csgraph._validation'],
                     "include_files": [(os.path.join(os.getcwd(),'pyinstaller_files','xgboost.dll'),"lib\\xgboost\\xgboost.dll"),]
                     }

includes = ['numpy','scipy.sparse.csgraph._validation']
options = {
    'build_exe': build_exe_options,
}

executables = [
    Executable('main.py', base=base)
]

setup(name='simple_PyQt5',
      version='0.1',
      description='Sample cx_Freeze PyQt5 script',
      options=options,
      executables=executables
      )