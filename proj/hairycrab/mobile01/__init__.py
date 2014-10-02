# -*- coding: utf-8 -*-
import proj.lib.jData as jData
page=jData.getWebPage('http://www.mobile01.com/')
print(page[:1000])
page.decode('big5')


text.decode('big5').decode('big5')
text = '測試'
print(text.decode('big5').decode('big5'))
page
text.decode('big5')

f = open('text.txt', 'r')
b_str = f.read()
f.close()
print b_str.decode('utf-8')  # 自行判斷標準輸出編碼
print b_str.decode('utf-8').encode('big5') # 標準輸出編碼為 big5