# -*- coding: utf-8 -*-

from proj.jHtml import *
import proj.jHtml as jHtml
import datetime
import shutil

def generateHtmls(env, collection):
    generateCover(env, collection)
    for subjectName, subject in collection.items():
        generateSummary(env, subjectName, subject)
        for docName, doc in subject.items():
            generateDoc(env, subjectName, docName, doc)
            
def generateCover(env, collection):
    html=Html()
    html.body.addText('<br />'*4)
    html.body.addTag(Tag('center', properties={'style':'font-size:30pt'}, innerHtml=env['NAME']))
    html.body.addText('<br />'*2)
    html.body.addTag(Tag('center', properties={'style':'font-size:12pt'}, innerHtml=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    html.body.addText('<br />'*2)
    
    content=Tag('center')
    html.body.addTag(content)
    
    table=Tag('table', style={'width':'800'})
    content.addTag(table)
    
    for subjectName, subject in sorted(collection.items()):
        tr=Tag('tr')
        table.addTag(tr)
        td1=Tag('td')
        tr.addTag(td1)
        td2=Tag('td', style={'text-align':'left'})
        tr.addTag(td2)
        td1.addTag(Tag('a', properties={'href':subjectName+'.html'}, innerHtml=subjectName))
        for docName in sorted(subject.keys()):
            td2.addTag(Tag('a', properties={'href':subjectName + '__' + docName+'.html'}, innerHtml=docName))
            td2.addText('<br />')
    html.save(env['KM_TEMP']+r'\_cover.html')
    
def generateSummary(env, subjectName, subject):
    print(subjectName)
    html = Html()
    html.addText('<br/>')
    html.addTag(Tag('b', innerHtml=subjectName))
    html.addText('<br/>'*2)
    table=Tag('table', properties={'style':'border-style:none;left:30;position:absolute'})
    html.addTag(table)
    for docName, doc in sorted(subject.items()):
        tr=Tag('tr')
        table.addTag(tr)
        
        descs=[item for item in doc if item['key']=='Description']
        desc=descs[0]['value'] if len(descs)>0 else ''
        a=Tag('a', innerHtml=docName, properties={'href':env['KM_TEMP']+'\\'+subjectName+'__'+docName+'.html'})
        td=Tag('td', style={'text-align':'left','border-style':'none'})
        td.addTag(a)
        tr.addTag(td)
        tr.addTag(Tag('td', innerHtml=desc, style={'text-align':'left','border-style':'none'}))
    html.save(env['KM_TEMP']+'\\'+subjectName+'.html')
    

def generateDoc(env, subjectName, docName, doc):
    html=doc2Html(env, docName, doc)
    filePath=env['KM_TEMP']+'\\'+subjectName+'__'+docName+'.html'
    html.save(filePath)
    print('  --> %s' %filePath)
    
def doc2Html(env, docName, doc):
    KM_DATA=env['KM_DATA']
    KM_TEMP=env['KM_TEMP']
    html=jHtml.Html()
    html.body.addText('''
    <script>
        $(document).ready(function(){
        		$("[class='v']").mouseover(function(){    
        			$(this).css("background-color","#EEEEFF");
        		})
                	$("[class='v']").mouseout(function(){    
        			$(this).css("background-color","#FFFFFF");
        		})
        
        	var infoStatus=0
        	$("[name='infoButton']").css("color", "#0000FF");
        	$("[name='info']").css("display", "none");
        
        	$("[name='infoButton']").click(function(){
        		if(infoStatus==1){
        			$("[name='info']").fadeOut();
        			$(this).css("color", "#0000FF");
        		}
        		else{
        			$("[name='info']").fadeIn();
        			$(this).css("color", "#FF0000");
        		}
        		infoStatus=1-infoStatus;
        	});
         
        	var remarkStatus=1
        	$("[name='remarkButton']").css("color", "#FF0000");
        	$("[name='remarkButton']").click(function(){
        		if(remarkStatus==1){
        			$("[class='remark']").fadeOut();
        			$(this).css("color", "#0000FF");
        		}
        		else{
        			$("[class='remark']").fadeIn();
        			$(this).css("color", "#FF0000");
        		}
        		remarkStatus=1-remarkStatus;
        	});
    
        	var imageStatus=1
        	$("[name='imageButton']").css("color", "#FF0000");
        	$("[name='imageButton']").click(function(){
        		if(imageStatus==1){
        			$("[name='image']").fadeOut();
        			$(this).css("color", "#0000FF");
        		}
        		else{
        			$("[name='image']").fadeIn();
        			$(this).css("color", "#FF0000");
        		}
        		imageStatus=1-imageStatus;
        	});
         
        });
    </script>
    ''')

    status=getProperty(doc, 'status')
    status='' if status.lower()=='complete' else status
    desc=getProperty(doc, 'Description')
    
    panel='''
    <p style="font-size:18pt">%s
        <font style="font-size:10pt;color:red">&nbsp;&nbsp;&nbsp;&nbsp;%s</font>
    </p>
    <table width="100%%" style="border-style:none">
        <tr>
            <td style="border-style:none;text-align:left;vertical-align:top">
                <font style="font-size:10pt">%s</font>
            </td>
            <td style="border-style:none;text-align:right;vertical-align:top">
                <a href="#" name="infoButton">
                    info
                </a>
                &nbsp;|&nbsp;
                <a href="#" name="remarkButton">
                    remark
                </a>
                &nbsp;|&nbsp;
                <a href="#" name="imageButton">
                    image
                </a>
            </td>
        </tr>
    </table>
    <hr />
    '''%(docName, status, desc)
    
    html.body.addText(panel)
    
    infoTable='''
	<style type="text/css">
        img {border-style:dotted;border-width:1px;box-shadow:4px 4px 3px rgba(20%%,20%%,40%%,0.5)}
        .infoTable_1 {border-style:none;text-align:right;vertical-align:top;background-color:#FFEEFF}
        .infoTable_2 {border-style:none;text-align:left;vertical-align:top;background-color:#FFEEFF}
        .k {border-style:none;text-align:left;vertical-align:top}
        .v {border-style:none;text-align:left;vertical-align:top}
        .r {border-style:none;text-align:left;vertical-align:top}
	</style>
    <div name="info">
        <table width="100%%" style="border-style:none">
            <tr>
                <td class="infoTable_1">Description:</td>
                <td class="infoTable_2" width="100%%">%s</td>
            </tr>
            <tr>
                <td class="infoTable_1">Status:</td>
                <td class="infoTable_2">%s</td>
            </tr>
            <tr>
                <td class="infoTable_1">Tags:</td>
                <td class="infoTable_2">%s</td>
            </tr>
            <tr>
                <td class="infoTable_1">Author:</td>
                <td class="infoTable_2">%s</td>
            </tr>
            <tr>
                <td class="infoTable_1">CreateDate:</td>
                <td class="infoTable_2">%s</td>
            </tr>
            <tr>
                <td class="infoTable_1">UpdateDate:</td>
                <td class="infoTable_2">%s</td>
            </tr>
        </table>
    </div>
    ''' %(
        getProperty(doc, 'Description')
        , getProperty(doc, 'Status')
        , getProperty(doc, 'Tags')
        , getProperty(doc, 'Author')
        , getProperty(doc, 'CreateDate')
        , getProperty(doc, 'UpdateDate')
    )
    html.body.addText(infoTable)
    
    infos=['Description', 'Template', 'Status', 'Tags', 'Author', 'CreateDate', 'UpdateDate', 'Version']
    for item in [_ for _ in doc if _['key'] not in infos]:
        key=unicode(item['key'])
        value=unicode(item['value'])
        remark=unicode(item['remark']) if 'remark' in item.keys() else ''        
        url=item['url'] if 'url' in item.keys() else ''
        innerLink=item['innerLink'] if 'innerLink' in item.keys() else ''
        image=item['image'] if 'image' in item.keys() else ''
        hasChild=True if len([itm for itm in doc if itm['parentRow']==item['row']])>0 else False
        style=item['style'] if 'style' in item.keys() else ''
        
        # --- key ---
        if key=='*':
            key='<font color="red">*</font>'
        elif key in ['v', 'o']:
            key=item['key']
        elif value=='' and hasChild==True:
            key='<b>'+key+'</b>'
        elif value=='':
            key=key
        else:
            key+=':'
        
        # --- value ---
        if value!='':
            value=value.replace('<', '&lt;').replace('\n', '\n<br />')
            
        if image!='':
            imageFileName=image.split('\\')[-1]
            shutil.copyfile(KM_DATA+'\\'+image, KM_TEMP+'\\'+imageFileName)
            value+='<br /><img name="image" src="'+imageFileName+'" />'
        
        if style=='pre':
            value='<pre>%s</pre>' %value

        if innerLink!='':
            value='<a href="'+innerLink+'">'+value+'</a>'

        if url!='':
            value='<a target="_blank" href="'+url+'">'+value+'</a>'
            
        # --- remark ---
        remark='<div class="remark" style="background-color:#FFDDDD">'+remark.replace('\n', '<br />')+'</div>'
        
        table=Tag('table', style={'border-style':'none'})
        tr=Tag('tr')
        table.addTag(tr)
        
        td1=Tag('td'
            , properties={'class':'k'}
            , innerHtml='&nbsp;'*8*item['level']+key
        )
        tr.addTag(td1)
        
        td2=Tag('td'
            , properties={'class':'v'}
            , innerHtml=value
        )
        tr.addTag(td2)

        td3=Tag('td'
            , properties={'class':'r'}
            , innerHtml=remark
        )
        tr.addTag(td3)
        
        html.body.addTag(table)
    return html

def getProperty(doc, key):
    p=[item for item in doc if unicode(item['key']).lower()==key.lower()]
    p=p[0]['value'] if len(p)>0 else ''
    return p
    