# -*- coding: utf-8 -*-

def getCover(title='_Untitiled', fileName='_cover', TEMP_HOME='temp'):
    import proj.jHtml as jHtml
    import proj.jChm as jChm
    import datetime as dt
    # html - cover   
    paras={'title':title
            , 'dt':dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            , 'fileName':fileName
            , 'TEMP_HOME':TEMP_HOME
        }         
    html=jHtml.Html()
    html.body.addText('<br/><br/><br/><br/><br/><br/><br/><br/><center style="font-size:30pt">%(title)s</center>' % paras)
    html.body.addText('<br/><br/><br/><br/><center style="font-size:12pt">Update:&nbsp;&nbsp;%(dt)s</center>' % paras)
    html.save(r'%(TEMP_HOME)s\%(fileName)s.html' % paras)
    return jChm.Page('cover', title, fileName+'.html', 0, '')
    

def getChapterHead(name='_chapterHead', title='_Untitiled', fileName='_chapterHead', parentName='cover', TEMP_HOME='temp', contents=[]):
    import proj.jHtml as jHtml
    import proj.jChm as jChm
    # html - cover  
    paras={'name':name
            , 'title':title
            , 'fileName':fileName
            , 'TEMP_HOME':TEMP_HOME
        }  
    html=jHtml.Html()
    html.body.addText('<br/><p style="font-size:20pt">%(title)s</p>' %paras)
    for _ in contents:
        html.body.addText('<br />'+'&nbsp;'*8+'<a href="%s.html">%s</a>&nbsp;&nbsp;-&nbsp;&nbsp;%s<br />'%(_[2], _[0], _[1]))
    html.save(r'%(TEMP_HOME)s\%(fileName)s.html' % paras)
    return jChm.Page(name, title, fileName+'.html', 0, parentName)

def getTemplate1(name='_template1', title='_Untitiled', desc='_desc', fileName='_template1', parentName='cover', TEMP_HOME='temp', content=''):
    import proj.jHtml as jHtml
    import proj.jChm as jChm
    # html - cover  
    paras={'name':name
            , 'title':title
            , 'desc':desc
            , 'fileName':fileName
            , 'TEMP_HOME':TEMP_HOME
        }  
    html=jHtml.Html()
    html.body.addText('<p style="font-size:18pt">%(title)s</p>'%paras)
    html.body.addText('<font style="font-size:10pt">%(desc)s</font><hr />'%paras)
    html.body.addText(content)
    html.save(r'%(TEMP_HOME)s\%(fileName)s.html' % paras)
    return jChm.Page(name, title, fileName+'.html', 0, parentName)
    
getTemplate1(content='I am content')