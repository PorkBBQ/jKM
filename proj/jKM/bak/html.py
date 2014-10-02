
import proj.jKM as jKM
import proj.jData as jData
import proj.jChm as jChm

def generateChm(collection, name='KM', KM_HOME=r'proj\KM\temp'):
    import proj.jChm
    chm=jChm.Chm(name)
    chm.paras['path']=KM_HOME
    chm.addPage(jChm.Page('cover', 'cover', '_cover.html'))
    
    for subject in collection:
        subjectName=subject['name']
        chm.addPage(jChm.Page(subjectName, subjectName, subjectName+'.html', 0, 'cover'))    
        for doc in subject['docs']:
            docName=subjectName+'__'+doc['name']
            chm.addPage(jChm.Page(docName, docName, docName+'.html', 0, subjectName))
    print(chm.generateAll())
    
#    html_hadoop=jHtml.Html()
#    html_hadoop.body.addText('section hadoop')
#    html_cover.save(r'proj\KM\temp\hadoop.html')
#    chm.addPage(jChm.Page('hadoop', 'hadoop', 'hadoop.html'))

    
#        for doc in subject['docs']:
            
#    for docName in docNames:
#        print docName
#        chm.addPage(jChm.Page(docName, docName, docName+'.html', 0, 'hadoop'))
    
#    print(chm.generateAll())



    
def generateHtml(collection, KM_HOME=r'proj\KM\temp'):
    import proj.jHtml as jHtml
    html_cover=jHtml.Html()
    html_cover.body.addText('notes')
    html_cover.save(KM_HOME+r'\_cover.html')
    
    for subject in collection:
        html_cover=jHtml.Html()
        html_cover.body.addText('notes')
        html_cover.save(KM_HOME+'\\'+subject['name']+'.html')
        
        for doc in subject['docs']:
            print(doc['name'])
            html=doc2Html(doc)
            filePath=KM_HOME+'\\'+subject['name']+'__'+doc['name']+'.html'
            html.save(filePath)
            print('save: '+filePath)


        
def doc2Html(doc):
    import proj.jHtml as jHtml
    html=jHtml.Html()
    for item in doc['items']:
        key=str(item['key'])+'&nbsp;:&nbsp;'
        value=item['value']
        if item['key']=='*':
            key='&nbsp;'*2+'<font color="red">*</font>'+'&nbsp;'*2
        if item['key'] in ['v', 'o']:
            key='&nbsp;'*2+item['key']+'&nbsp;'*2
    
        if item['value'] in ['', '$l']:
            key=item['key']
            value=''
        #line='<p style="line-height:12px">&nbsp;'*16*item['level']+name+value+'</p>'
        line='&nbsp;'*16*item['level']+str(key)+str(value)+'<br />'
        html.body.addText(line)
    return html



generateHtml(collection, KM_HOME)
generateChm(collection, 'KM', KM_HOME)