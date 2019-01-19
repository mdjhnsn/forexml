import matplotlib.pyplot as plt
import oandapyV20
import pandas as pd
from oandapyV20.contrib.factories import InstrumentsCandlesFactory
from myauth import myauth

accountID, access_token = myauth.myAuth()
client = oandapyV20.API(access_token=access_token)
instrument = "EUR_USD"
params = {
    'from': '2019-01-13T22:00:00Z',
    # 'to': '2019-01-17T22:00:00Z',
    'granularity': 'M1',
    'includeFirst': True,
}


def cnv(r, h):
    # get all candles from the response and write them as a record to handle h
    for candle in r.get('candles'):
        ctime = candle.get('time')[0:19]
        try:
            rec = "{time},{open},{high},{low},{close},{volume},{complete}".format(
                time=ctime,
                open=candle['mid']['o'],
                high=candle['mid']['h'],
                low=candle['mid']['l'],
                close=candle['mid']['c'],
                volume=candle['volume'],
                complete=candle['complete']
            )
        except Exception as e:
            print(e, r)
        else:
            h.write(rec + "\n")


datafile = '/Users/mj/Repos/forexml/data/{}.{}.out'.format(instrument, params['granularity'])
with open(datafile, "w") as o:
    n = 0
    for r in InstrumentsCandlesFactory(instrument=instrument, params=params):
        rv = client.request(r)
        cnt: int = len(r.response.get('candles'))
        print('REQUEST: {} {} {}, received: {}'.format(r, r.__class__.__name__, r.params, cnt))
        n += cnt
        cnv(r.response, o)
        print("Check the datafile: {} under /tmp!, it contains {} records".format(datafile, n))

file_path = '/Users/mj/Repos/forexml/data/EUR_USD.M1.out'
col_names = ['time','open', 'high', 'low', 'close', 'volume', 'complete']
df = pd.read_csv(filepath_or_buffer=file_path, names=col_names)

df.set_index(['time'], inplace=True)
plt.plot(df['close'])
plt.show()
plt.close()

# close = df['close']
#
# span0 = 100
# df0 = close.index.searchsorted(close.index)
# df0 = df0[df0 > 0]
# df0 = pd.Series(close.index[df0 - 1], index=close.index[close.shape[0] - df0.shape[0]:])
# df0 = close.loc[df0.index] / close.loc[df0.values].values - 1
# df0 = df0.ewm(span=span0).std()
# plt.plot(df0)
# plt.show()
# plt.plot(df['close'])
