import pandas as pd
import matplotlib.pyplot as plt

import oandapyV20
import oandapyV20.endpoints.instruments as instruments
client = oandapyV20.API(access_token=access_token)

from myauth import myauth
accountID, access_token = myauth.myAuth()

file_path = '/tmp/EUR_USD.M15.out'
col_names = ['time', 'complete', 'open', 'high', 'low', 'close', 'volume']
df = pd.read_csv(filepath_or_buffer=file_path, names=col_names)
close = df['close']
span0 = 100
df0 = close.index.searchsorted(close.index)
df0 = df0[df0 > 0]
df0 = pd.Series(close.index[df0-1], index=close.index[close.shape[0]-df0.shape[0]:])
df0 = close.loc[df0.index]/close.loc[df0.values].values-1
df0 = df0.ewm(span=span0).std()
plt.plot(df0)
plt.show()
plt.plot(df['close'])