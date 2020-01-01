import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

start_date = '2000-01-01'
end_date = '2015-12-31'

pro = ts.pro_api()

# Obtain  all stocks available
data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
data = data.dropna()
data.drop(data[data.symbol.astype('int') > 604000].index, inplace=True)

stock_list = [i for i in data.ts_code]

data.industry = data.industry.astype('category')


from multiprocessing.dummy import Pool as ThreadPool

def process(stock):
    df = ts.pro_bar(ts_code=stock, adj='qfq', start_date=start_date , end_date=end_date)
    df.sort_index(axis=0, ascending = False, inplace = True)
    df.reset_index(drop=True, inplace=True)
    df = df.drop(['pre_close', 'change', 'amount'], axis=1)
    df.to_csv('Data/'+stock.split('.')[0]+'.csv')



def main():
    pool = ThreadPool()
    pool.map(process, tqdm(stock_list))
    pool.close()
    pool.join()
    
#    all_stock = tqdm(stock_list)
#    for stock in all_stock:
#        symbol = stock.split('.')[0]
#        df = ts.pro_bar(ts_code=stock, adj='qfq', start_date=start_date , end_date=end_date)
#        df.sort_index(axis=0, ascending = False, inplace = True)
#        df.reset_index(drop=True, inplace=True)
#        df = df.drop(['pre_close', 'change', 'amount'], axis=1)
#        df.to_csv('Data/'+symbol+'.csv')



if __name__ == '__main__':
    main()
