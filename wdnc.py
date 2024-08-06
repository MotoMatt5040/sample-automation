import os
import numpy as np

path = os.environ.get("WDNC_PATH")

wdnc = np.loadtxt(path, dtype=str)
