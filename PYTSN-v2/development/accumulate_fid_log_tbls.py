import sys
import numpy as np
import pandas as pd

df1 = pd.DataFrame()
df2 = pd.DataFrame()
df3 = pd.DataFrame()

df1["flow_id"] = [1]
df1["rcv_time"] = [1.1]

df2["flow_id"] = [2]
df2["rcv_time"] = [1.1]

df3["flow_id"] = [1]
df3["rcv_time"] = [3]

df = pd.concat([df1,df2,df3])
df.reset_index(drop=True)

print df.drop_duplicates(subset=['flow_id'],  keep='last')