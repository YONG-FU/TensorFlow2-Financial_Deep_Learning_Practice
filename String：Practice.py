import pandas as pd
import csv

tb = pd.read_html('http://www.chinadrugtrials.org.cn/clinicaltrials.searchlistdetail.dhtml')
tb.to_csv(r'1.csv', mode='a', encoding='utf_8_sig', header=1, index=0)