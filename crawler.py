import requests
from scrapy.selector import Selector
import pandas as pd
from datetime import timedelta, date
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import matplotlib
from config import url, image_save_path
matplotlib.use('Agg')


def crawl_view_state():

    response = requests.get(url)
    content_str = response.content.decode("utf8")
    view_state = Selector(text=content_str).xpath('//input[@id="__VIEWSTATE"]/@value').extract_first()
    view_state_gen = Selector(text=content_str).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()

    return view_state, view_state_gen

def create_post_obj(stock_code):
    
    today = date.strftime(date.today()  , "%Y%m%d")
    view_state, view_state_gen = crawl_view_state()
    post_obj = {
                '__EVENTTARGET' : 'btnSearch',
                '__VIEWSTATE': view_state,
                '__VIEWSTATEGENERATOR': view_state_gen,
                'today' : today,
                'sortBy' : 'shareholding',
                'sortDirection': 'desc',
                'txtShareholdingDate' : None,
               'txtStockCode' : stock_code}
    
    return post_obj

def crawl_shareholding(date, post_obj):
    
    post_obj['txtShareholdingDate'] = date
    response = requests.post(url, data = post_obj)
    content_str = response.content.decode("utf8")
    name = Selector(text=content_str).xpath("//td[contains(@class, 'col-participant-name')]/div[contains(@class, 'mobile-list-body')]").css('::text').extract()
    participant_id = Selector(text=content_str).xpath("//td[contains(@class, 'col-participant-id')]/div[contains(@class, 'mobile-list-body')]").css('::text').extract()
    percent = Selector(text=content_str).xpath("//td[contains(@class, 'col-shareholding-percent')]/div[contains(@class, 'mobile-list-body')]").css('::text').extract()    
    participant_id += name[len(participant_id):]
    
    return participant_id, percent


def daterange(start_date, end_date):
    
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def transform_date(date_str):
    
    year = int(date_str[:4])
    month = int(date_str[5:7])
    day = int(date_str[8:10])
    date_datetime = date(year, month, day)
    
    today = date.today()
    last_day = today - timedelta(days=1)
    first_day = today - timedelta(days=365)
    if date_datetime>last_day:
        date_datetime = last_day
    elif date_datetime<first_day:
        date_datetime = first_day
            
    return date_datetime

def crawl_main(stock_code, start_date_str, end_date_str):        
    
    list_df = []
    start_date = transform_date(start_date_str)
    end_date = transform_date(end_date_str)
    post_obj = create_post_obj(stock_code)
    for single_date in daterange(start_date, end_date):
        date_str = single_date.strftime("%Y/%m/%d")
        participant_id, percent = crawl_shareholding(date_str, post_obj)
        df = pd.DataFrame()
        df['participant_id'] = participant_id
        df['percent'] = percent
        df['date'] = date_str
        list_df.append(df)
        
    df_all = pd.concat(list_df)
    df_all['percent'] = df_all['percent'].str[:-1].astype(float)

    return df_all.reset_index(drop = True)

def trend_plot(stock_code, start_date_str, end_date_str):
    
    df_all = crawl_main(stock_code, start_date_str, end_date_str)
    end_date_str = df_all['date'].max()
    participant_id_list = df_all[df_all['date'] == end_date_str]['participant_id'].head(10).tolist()
    df_select = df_all[df_all['participant_id'].isin(participant_id_list)]
    df_select = df_select.set_index('date')
    
    figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')
    df_select.groupby('participant_id')['percent'].plot(legend=True)
    plt.savefig(image_save_path)    
    
    return df_select.reset_index().to_dict('records')

def transaction_finder(stock_code, start_date_str, end_date_str, threshold):
    
    df_all = crawl_main(stock_code, start_date_str, end_date_str)
    df_all = df_all.sort_values(by=['participant_id', 'date'])
    df_all['pct_diff'] = df_all.groupby('participant_id')['percent'].diff()
    
    df_sell = df_all[df_all['pct_diff']<-threshold]
    df_sell['pct_diff'] = df_sell['pct_diff'].abs()
    df_buy = df_all[df_all['pct_diff']>threshold]

    df_sell = df_sell.rename(columns = {'participant_id' : 'participant_id_SELL'})
    df_buy = df_buy.rename(columns = {'participant_id' : 'participant_id_BUY'})

    df_exchange = pd.merge(df_buy[['participant_id_BUY', 'date', 'pct_diff']], df_sell[['participant_id_SELL', 'date', 'pct_diff']], on = ['date', 'pct_diff'])
    df_exchange = df_exchange.rename(columns = {'pct_diff' : 'exchange_shares'})
    df_exchange = df_exchange.sort_values(by = ['date', 'exchange_shares']).round(2)
    
    return df_exchange[['date', 'participant_id_BUY', 'participant_id_SELL', 'exchange_shares']].to_dict('records')