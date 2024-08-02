import json
import os
import re
import sys
from datetime import date, datetime

import numpy as np
from IPython import get_ipython


def is_notebook() -> bool:
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMInteractiveShell":
            return True  # Jupyter notebook qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal ipython
        elif "google.colab" in sys.modules:
            return True  # Google Colab
        else:
            return False
    except NameError:
        return False


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif hasattr(obj, "__iter__"):
            return list(obj)
        elif isinstance(obj, datetime):
            return obj.strftime("%Y%m%d %H:%M:%S.%f")
        elif isinstance(obj, date):
            return datetime(obj.year, obj.month, obj.day, 0, 0, 0).strftime("%Y%m%d %H:%M:%S.%f")
        else:
            return super().default(obj)
