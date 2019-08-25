import warnings

# Ignore scipy/ndimage/interpolation.py:611: UserWarning: From scipy 0.13.0, the output
# shape of zoom() is calculated with round() instead of int() - for thes e inputs the
# size of the returned array has changed.
warnings.filterwarnings("ignore", "From scipy.*", UserWarning)
