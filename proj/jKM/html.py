# -*- coding: utf-8 -*-

from proj.jHtml import *
import proj.jHtml as jHtml
import datetime
import shutil

def generateHtmls(env, book):
    generateCover(env, book)
    for chapterName, chapter in book['chapters'].items():
        generateSummary(env, chapterName, chapter)
        for pageName, page in chapter['pages'].items():
            generatePage(env, chapterName, pageName, page)
    
def generateCover(env, book):
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
    
    for chapterName, chapter in sorted(book['chapters'].items()):
        tr=Tag('tr')
        table.addTag(tr)
        td1=Tag('td')
        tr.addTag(td1)
        td2=Tag('td', style={'text-align':'left'})
        tr.addTag(td2)
        td1.addTag(Tag('a', properties={'href':chapterName+'.html'}, innerHtml=chapterName))

        for pageName in sorted(chapter['pages'].keys()):
            td2.addTag(Tag('a', properties={'href':chapterName + '__' + pageName+'.html'}, innerHtml=pageName))
            td2.addText('<br />')

    html.save(env['KM_TEMP']+r'\_cover.html')
    
def generateSummary(env, chapterName, chapter):
    print(chapterName)
    html = Html()
    html.addText('<br/>')
    html.addTag(Tag('b', innerHtml=chapterName))
    html.addText('<br/>'*2)
    table=Tag('table', properties={'style':'border-style:none;left:30;position:absolute'})
    html.addTag(table)
    for pageName, page in sorted(chapter['pages'].items()):
        tr=Tag('tr')
        table.addTag(tr)
        desc=chapter['Description'] if 'Description' in chapter else ''
        href=env['KM_TEMP']+'\\'+chapterName+'__'+pageName+'.html'
        a=Tag('a', innerHtml=pageName, properties={'href':href})
        td=Tag('td', style={'text-align':'left','border-style':'none'})
        td.addTag(a)
        tr.addTag(td)
        tr.addTag(Tag('td', innerHtml=desc, style={'text-align':'left','border-style':'none'}))
    html.save(env['KM_TEMP']+'\\'+chapterName+'.html')
    

def generatePage(env, chapterName, pageName, page):
    html=page2Html(env, pageName, page)
    filePath=env['KM_TEMP']+'\\'+chapterName+'__'+pageName+'.html'
    html.save(filePath)
    print('  --> %s' %filePath)

def getSection(env, html, section, level=0):
    key=unicode(section['key'])
    value=unicode(section['value'])
    
    properties=section['properties']
    remark=unicode(properties['remark']) if 'remark' in properties else ''
    url=unicode(properties['url']) if 'url' in properties else ''
    innerLink=unicode(properties['innerLink']) if 'innerLink' in properties else ''
    image=unicode(properties['image']) if 'image' in properties else ''
    style=unicode(properties['style']) if 'style' in properties else ''

    # --- key ---
    if key=='*':
        key='<font color="red">*</font>'
    elif key in ['v', 'o']:
        key=key
    elif value=='' and len(section['sections'])>0:
        key='<b>'+key+'</b>'
    elif value=='':
        key=key
    else:
        key+=':'

    # --- value ---
    if value!='':
        value=value.replace('<', '&lt;').replace('\n', '\n<br />')            

    # --- properties ---
    if remark != '':
        remark=unicode(section['properties']['remark'])
        remark='<div class="remark" style="background-color:#FFDDDD">'+remark.replace('\n', '<br />')+'</div>'
        
    if image!='':
        imageFileName=image.split('\\')[-1]
        shutil.copyfile(env['KM_DATA']+'\\'+image, env['KM_TEMP']+'\\'+imageFileName)
        value+='<br /><img name="image" src="'+imageFileName+'" />'
    
    if style=='pre':
        value='<pre>%s</pre>' %value

    if innerLink!='':
        value='<a href="'+innerLink+'">'+value+'</a>'

    if url!='':
        value='<a target="_blank" href="'+url+'">'+value+'</a>'
    

    table=Tag('table', style={'border-style':'none'})
    tr=Tag('tr')
    table.addTag(tr)

    td0=Tag('td'
        , properties={'class':'indent'}
        , innerHtml='&nbsp;'*8*level
    )    
    tr.addTag(td0)
    td1=Tag('td'
        , properties={'class':'k'}
        , innerHtml=key
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
    
    for subSection in section['sections']:
        getSection(env, html, subSection, level+1)
        
    return True

def page2Html(env, pageName, page):
    KM_DATA=env['KM_DATA']
    KM_TEMP=env['KM_TEMP']
    html=jHtml.Html()
    html.body.addText(getJQuery())
    html.body.addText(getPanel(env, pageName, page))
    
    for section in page['sections']:
        getSection(env, html, section)

    return html

def getProperty(page, key):
    return page[key] if key in page else ''

def getJQuery():
    return '''
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
    '''

def getPanel(env, pageName, page):
    status=getProperty(page, 'status')
    status='' if status.lower()=='complete' else status

    desc=getProperty(page, 'description')

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
    '''%(pageName, status, desc)
    
    panel += '''
	<style type="text/css">
        img {border-style:dotted;border-width:1px;box-shadow:4px 4px 3px rgba(20%%,20%%,40%%,0.5)}
        .infoTable_1 {border-style:none;text-align:right;vertical-align:top;background-color:#FFEEFF}
        .infoTable_2 {border-style:none;text-align:left;vertical-align:top;background-color:#FFEEFF}
        .indent {border-style:none}
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
        getProperty(page, 'description')
        , getProperty(page, 'status')
        , getProperty(page, 'tags')
        , getProperty(page, 'author')
        , getProperty(page, 'createDate')
        , getProperty(page, 'updateDate')
    )
    return panel
