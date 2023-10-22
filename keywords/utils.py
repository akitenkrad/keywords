import json
import os
import re
import sys
from datetime import date, datetime
from io import BytesIO

import numpy as np
import requests
from IPython import get_ipython
from pypdf import PdfReader


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


def extract_pdf_text(pdf_url: str) -> str:
    response = requests.get(pdf_url)
    memory_file = BytesIO(response.content)
    pdf_file = PdfReader(memory_file)

    total_texts = []
    for page in pdf_file.pages:
        _text = page.extract_text().strip().split(os.linesep)
        _text_lines = []
        for line in _text:
            if line.endswith("-"):
                line = line[0:-1]
            _text_lines.append(line)
        total_texts.append(" ".join(_text_lines))
    text = os.linesep.join(total_texts)
    return text


def _plus_s(word: str):
    out = r"\s*".join([c for c in word.lower() if len(c.strip()) > 0])
    return out


def extract_section_text(text, section_1, section_2) -> str:
    start_ptn = _plus_s(section_1.lower())
    end_ptn = _plus_s(section_2.lower())

    start_pos = [f for f in re.finditer(rf"{start_ptn}", text.lower(), flags=re.M | re.S | re.I)][0]
    end_pos = [f for f in re.finditer(rf"{end_ptn}", text.lower(), flags=re.M | re.S | re.I)][-1]
    start = start_pos.end()
    end = end_pos.start()
    extracted_text = text[start:end].strip()
    input_text = ""
    for line in extracted_text.split(os.linesep):
        if line.endswith("-"):
            input_text += line[:-1].strip() + " "
        else:
            input_text += line.strip() + " "
    return input_text


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
