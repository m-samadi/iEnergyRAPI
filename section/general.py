import pandas

# Convert a null value into a number
def null_to_num(val):
  if (pandas.isna(val) or val == ""):
    return -1
  else:
    return val
