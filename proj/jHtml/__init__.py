# -*- coding: utf-8 -*-

jCSS_1='''
    body {    font-family: arial;   line-height:24px    }
    pre {    font-family: arial    }
    table {    border: 1px solid #666666;    border-collapse: collapse;    }
    td,th {    border: 1px solid #666666;    padding: 5;     font-size: 10pt;    text-align:center;    }
    th {    background-color: FFDDBB;  }
    a:link    {        color: #0000FF;        text-decoration: none;    }
    a:visited    {        color: #0000FF;        text-decoration: none;    }
    a:hover    {        color: #FF0000;        text-decoration: underline;    }
    a:active    {        color: #FF0000;        text-decoration: underline;    }
'''

class Tag:
    def __init__(self, tagType, id='', name='', innerHtml='', properties={}, style={}):
        self.tagType=tagType        
        self.properties=properties
        self.style=style
        self.properties['id']=id if id else ''
        self.properties['name']=name if name else ''
        self.innerHtml=innerHtml if innerHtml else ''
        self.tags=[]

    def setProperty(self, key, value):
        self.properties[key]=value
    
    def getProperty(self, key):
        return self.properties[key]
        
    def addTag(self, tag):
        self.tags.append(tag)
    
    def addText(self, text):
        self.tags.append(Tag('_text', innerHtml=text))
    
    def getTag(self, value, property='id', child=True):
        tags=[tag for tag in self.tags if property in tag.properties.keys() and tag.properties[property]==value]
        if child==True:
            for tag in self.tags:
                tags+=tag.getTag(property=property, value=value)
        return tags
        
    def getTagByType(self, tagType='', child=True):
        tags=[tag for tag in self.tags if tag.tagType==tagType]
        if child==True:        
                for tag in self.tags:
                    tags+=tag.getTagByType(tagType=tagType)
        return tags
        
    def getHtml(self, indent=True, indentCnt=0):
        bf=[]
        if self.tagType=='_text':
            if indent==True:
                bf.append('\t'*indentCnt)
            bf.append(self.innerHtml+'\n')
            #bf.append('\n')
        else:
            if indent==True:
                bf.append('\t'*indentCnt)
            bf.append('<')
            bf.append(self.tagType)
            
            for k, v in self.properties.items():
                if v:
                    bf.append(' %s="%s"' %(k, v))
            
            if self.style:
                style=''
                for k, v in self.style.items():
                    style+='%s:%s;' %(k,v)
                bf.append(' style="%s"' %style)

            bf.append('>')
            if self.innerHtml:
                bf.append('\n')
                if indent==True:
                    bf.append('\t'*(indentCnt+1))
                bf.append(self.innerHtml)
            if indent==True:
                bf.append('\n')
            
            for t in self.tags:
                bf.append(t.getHtml(indent=indent, indentCnt=indentCnt+1))
            
            if indent==True:
                bf.append('\t'*indentCnt)
            bf.append('</')
            bf+=self.tagType
            bf.append('>')
            if indent==True:
                bf.append('\n')
        return ''.join(bf)


class Html(Tag):

    def __init__(self, css='jCss_1', jQuery=True):
        
        Tag.__init__(self, 'html')
        head=Tag('head')
        body=Tag('body')
        self.addTag(head)
        self.addTag(body)
        self.head=head
        self.body=body
        
        if css=='jCss_1':
            head.addTag(Tag('style', properties={'type':'text/css'}, innerHtml=jCSS_1))

        head.addTag(Tag('META', properties={'http-equiv':'Content-Type', 'content':'text/html'}))
        if jQuery==True:
            jq=Tag('script', properties={'src':'http://code.jquery.com/jquery-1.10.1.min.js'})
            body.addTag(jq)
        
    def save(self, fileName, encode='big5'):
        f=open(fileName, 'w')
        #f.write(self.getHtml().encode('utf-8', 'ignore'))
        f.write(self.getHtml().encode(encode))
        #f.write(self.getHtml())
        f.close

class Table(Tag):
    def __init__(self, df=''):
        Tag.__init__(self, 'table')
        if str(type(df))=="<class 'pandas.core.frame.DataFrame'>":
            self.loadDf(df)

    def loadDf(self, df):
        tr=Tag('tr')
        for col in df.columns:
            tr.addTag(Tag('th', innerHtml=col))
        self.addTag(tr)
        for row in df.iterrows():
            tr=Tag('tr')
            #print(row[1][1])
            for cell in row[1]:
                try:
                    tr.addTag(Tag('td', innerHtml=str(cell)))
                except:
                    tr.addTag(Tag('td'))
            self.addTag(tr)

