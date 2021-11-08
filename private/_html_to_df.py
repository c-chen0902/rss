import re, os
import pandas as pd
import my_modules as mm
from datetime import datetime
from requests_html import HTMLSession
import pprint
from genrss import GenRSS
import time
import _merge_df_to_csv, _csv_to_xml

working_path = r'E:\OneDrive\Python\my_rsshub\data\private\\'

class RSS_page: 
        
    def __init__(self, _page_info_dict):                    
        self.page_url = _page_info_dict['page_url']
        self.page_title = _page_info_dict['page_title'].replace(' ','_')
        self.file_name = self.page_title.strip().lower().replace(' ','_')
        self.csv_file = working_path + 'data\\' + self.file_name + '.csv'
        self.xml_file = working_path + 'data\\' + self.file_name + '.xml'
        self.page_info_dict = _page_info_dict
        
                
    def get(self):
        session = HTMLSession()
        self.html_response = session.get(self.page_url)                
        print('\nGetting data for ', self.page_url, sep='')
        
        output_dict = {}
        for field in ['title', 'url', 'date', 'description', 'img']:
            output_dict[field] = []
            _selector = self.page_info_dict[field]['selector']
            _attribute = self.page_info_dict[field]['attribute']
            _prefix = self.page_info_dict[field]['prefix']
            
            if _selector != '':
                match_list = self.html_response.html.find(_selector)
                for item in match_list:
                    if _attribute == 'text':
                        item = item.text.strip()
                    else:
                        item = item.attrs[_attribute].strip()
                    if _prefix !='':
                        item = str(_prefix) + str(item)
                    output_dict[field].append(item)           
            else:
                for item in output_dict['title']:
                    item = str(_prefix)
                    output_dict[field].append(item)      
            
        df = pd.DataFrame.from_dict(output_dict, orient='index').transpose()
        df.fillna('', inplace=True)
        print(str(df.shape[0]), 'rows have been crawled.')        
        self.df = df
        
    def get_rss_df(self):
        return self.df
    
    
    def preview(self):
        self.df.to_html(working_path + 'preview.html')
        os.system('''start "" "''' + working_path + 'preview.html' + '"')
                            
                            
    def test(self, _selector):
        match_list = self.html_response.html.find(_selector)
        test_dict = {}
        test_dict[0] = {'match_count': len(match_list)}
        for index, item in enumerate(match_list):
            test_dict[index+1] = {}
            test_dict[index+1]['text'] = match_list[index].text
            for key, value in match_list[index].attrs.items():
                test_dict[index+1][key] = value
            
        index = 0
        while index <= 3:
            pprint.pprint(test_dict[index])
            index += 1
    
    def df_to_csv(self, df):
        _merge_df_to_csv.f_merge_df_to_csv(df, self.csv_file)
    
    def csv_to_xml(self):
        csv_file = self.csv_file   
        xml_file = self.xml_file       
        _csv_to_xml.f_csv_to_xml(csv_file, xml_file, self.page_title, self.page_url)

## main ============================================================================================
if __name__ == '__main__':
                  
    page_info_dict = {
        
        'page_url':'https://game.ithome.com/youxikuaibao',
        'page_title':'IT之家游戏快报',
        
        'title':{
            'selector':'div.fl h2>a.title',
            'attribute':'text',
            'prefix':'' 
        },
        
        'url':{
            'selector':'div.fl h2>a.title',
            'attribute':'href',
            'prefix':''        
        },
        
        'date':{
            'selector':'#list > div.fl > ul > li:nth-child(n) > div > div.o > div.d > span',
            'attribute':'text',
            'prefix':'' 
        },
        
        'description':{
            'selector':'#list > div.fl > ul > li:nth-child(n) > div > div.m',
            'attribute':'text',
            'prefix':'' 
        },
        
        'img':{
            'selector':'#list > div.fl > ul > li:nth-child(n) > a > img',
            'attribute':'src',
            'prefix':'https:' 
        }}


    def f_date(_date):
        _year = time.strftime("%Y", time.localtime()) 
        if re.search('今日', _date) != None:
            _date = datetime.utcnow()
        else:
            _month = re.sub(r'.*?(\d+)月.*','\g<1>', _date)
            _day = re.sub(r'.*?(\d+)日.*','\g<1>', _date)
            _date = ' '.join([_year, _month, _day])
            _date = time.mktime(time.strptime(_date,"%Y %m %d"))
            _date = datetime.fromtimestamp(_date)
        _date = _date.strftime('%c')
        return _date        


    page = RSS_page(page_info_dict)    
    page.get()
    df = page.get_rss_df()
    df['date'] = df['date'].apply(f_date)
    page.df_to_csv(df)
    page.csv_to_xml()
    
    # page.preview()    
    # page.test('div.fl h2>a.title')
#$