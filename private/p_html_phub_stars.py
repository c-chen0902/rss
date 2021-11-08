from _html_to_df import RSS_page
import re
import time
from datetime import datetime

# --------------------------------------------------------------------------------------------------
page_info_dict = {
    
    'page_url':'https://www.pornhub.com/pornstar/danika-mori/videos/upload',
    'page_title':'Danika Mori',
    
    'title':{
        'selector':'.row-5-thumbs.videos .thumbnail-info-wrapper.clearfix > span > a',
        'attribute':'title',
        'prefix':'' 
    },
    
    'url':{
        'selector':'.row-5-thumbs.videos .thumbnail-info-wrapper.clearfix > span > a',
        'attribute':'href',
        'prefix':'https://www.pornhub.com'        
    },
    
    'date':{
        'selector':'',
        'attribute':'text',
        'prefix':'' 
    },
    
    'description':{
        'selector':'',
        'attribute':'text',
        'prefix':'' 
    },
    
    'img':{
        'selector':'.row-5-thumbs.videos .phimage > a > img',
        'attribute':'data-src',
        'prefix':'' 
    }}


# --------------------------------------------------------------------------------------------------
def f_date(_date):
    _date = datetime.utcnow()
    _date = _date.strftime('%c')    
    return _date  

def f_title(x):
    return x    

# --------------------------------------------------------------------------------------------------
dic_webpages = {
    'Danika Mori':'https://www.pornhub.com/pornstar/danika-mori/videos/upload',
    'Made in Canarias':'https://www.pornhub.com/pornstar/madeincanarias/videos/upload'
}

for page_title, page_url in dic_webpages.items():    
    page_info_dict['page_title'] = page_title
    page_info_dict['page_url'] = page_url
    page = RSS_page(page_info_dict)    
    page.get()
    df = page.get_rss_df()
    df['date'] = df['date'].apply(f_date)
    page.df_to_csv(df)
    page.csv_to_xml()
    time.sleep(1)

# --------------------------------------------------------------------------------------------------
# page.preview()    
# page.test('.row-5-thumbs.videos .thumbnail-info-wrapper.clearfix > span > a')