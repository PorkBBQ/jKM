# -*- coding: utf-8 -*-
import os
import proj.jHtml

class Page:
    def __init__(self, name='', title='', fileName='', parent=0, parentName=''):
        self.name=name
        self.title=title
        self.fileName=fileName
        self.parent=parent
        self.parentName=parentName

class Chm:
    def __init__(self, name='chmTest', CHM_HOME=r'proj\chm\temp'):
        self.pages=[]
        self.paras={
            'name':name
            , 'chmUtilityPath':r'proj\jChm\hhc.exe'
            , 'path':CHM_HOME
            , 'defaultPage':'_cover.html'
            , 'title':'chmTest'
        }
        self.paras['chmFileName']=self.paras['name']+'.chm'
        self.paras['hhpFileName']=self.paras['name']+'.hhp'
        self.paras['hhcFileName']=self.paras['name']+'.hhc'

    def setParameter(self, key, val):
        self.paras[key]=val

    def getParameter(self, key):
        return self.paras[key]
        
    def addPage(self, page):
        self.pages.append(page)
        
    def addPages(self, pages):
        self.pages=self.pages+pages
        
    def setPages(self, pages):
        self.pages=pages
        
    def getHhc(self):
        self.hhc=proj.jHtml.Html(css='')
        #self.addHhcTag(self.hhc.body, 0, '')
        hhc='''
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<HTML>
<HEAD>
<meta name="GENERATOR" content="Microsoft&reg; HTML Help Workshop 4.1">
<!-- Sitemap 1.0 -->
</HEAD><BODY>
    <OBJECT TYPE="text/site properties">
        <PARAM NAME="Window Styles" value="0x800025">
        </PARAM>
        <PARAM NAME="Font" VALUE="Arial Unicode MS,8,0">
        </PARAM>
    </OBJECT>
        '''
        hhc+=self.addHhcPage(0, '')
        hhc+='''
</BODY></HTML>
        '''
        return hhc

    def addHhcPage(self, ix, name):
        children=[page for page in self.pages if 
            (page.parentName not in ['', 'none', None] and page.parentName==name)
            or (page.parentName in ['', 'none', None] and page.parent==ix)
        ]
        sorted(children)
        rtn=''
        for child in children:
            rtn+='''
<UL>
<LI><OBJECT type="text/sitemap">
<param name="Name" value="%s">
<param name="Local" value="%s">
</OBJECT>
%s
</UL>
            ''' % (child.title, child.fileName, self.addHhcPage(-1, child.name))
        return rtn

    def getHhp(self):
        rtn='''[OPTIONS]
Compatibility=1.1 or later
Compiled file=%s
Contents file=%s
Default Window=a
Default topic=%s
Display compile progress=No
Full-text search=Yes
Language=0x404 中文 (繁體，台灣)
Title=Notes

[WINDOWS]
a=,"%s",,"_cover.html",,,,,,0x23521,,0x3006,,,,,1,,,0
        ''' %(self.paras['chmFileName'], self.paras['hhcFileName'], self.paras['defaultPage'], self.paras['hhcFileName'])

        return rtn

    def generateHhp(self):
        file=open(self.paras['path']+'\\'+self.paras['hhpFileName'], 'w')
        file.write(self.getHhp())
        file.close()

    def generateHhc(self):
        file=open(self.paras['path']+'\\'+self.paras['hhcFileName'], 'w')
        file.write(self.getHhc())
        file.close()

    def generateChm(self):
        cmd=self.paras['chmUtilityPath']+' '+self.paras['path']+'\\'+self.paras['hhpFileName']
        print('\n==> "' + cmd + '"\n')
        str = os.popen(cmd).read()
        return str

    def generateAll(self):
        self.generateHhc()
        self.generateHhp()
        str=self.generateChm()
        return str
