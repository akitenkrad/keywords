import sys

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


if is_notebook():
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm
