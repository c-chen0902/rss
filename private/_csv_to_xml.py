import os
import pandas as pd
from genrss import GenRSS

def f_csv_to_xml(csv_file, xml_file, page_title, page_url):
    
    feed = GenRSS(title=page_title, site_url=page_url, feed_url=page_url)
    
    df = pd.read_csv(csv_file)        
    df = df.iloc[0:200, :]
    
    for irow in range(df.shape[0]):              
        feed.item(
            title=str(df.loc[irow, 'title']),
            url=str(df.loc[irow, 'url']),
            description = (str(df.loc[irow, 'description']) 
                        + '<br><br><img src=' + str(df.loc[irow, 'img']) + '>'),                
            pub_date=str(df.loc[irow, 'date'])
            )
            
    xml = feed.xml()
    
    f = open (xml_file, 'w+', encoding='utf-8')
    f.write(xml)
    
    print('The XML file has been created.')