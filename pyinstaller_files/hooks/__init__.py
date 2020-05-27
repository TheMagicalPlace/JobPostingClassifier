
__all__ = ['FILE_PATHS']
import os

filenames = ['hook-pandas.py','hook-sklearn.metrics.cluster.py','hook-sklearn.tree.py','hook-scipy.py']
FILE_PATHS = [os.path.join(os.getcwd(),'hooks',file) for file in filenames]

