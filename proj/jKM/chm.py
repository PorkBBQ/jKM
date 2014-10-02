# -*- coding: utf-8 -*-

def generateChm(env, book):
    KM_TEMP=env['KM_TEMP']
    outputPaths=env['OUTPUTS'].split(',')
    name=env['NAME']
    
    import proj.jChm as jChm
    import shutil
    
    chm=jChm.Chm(name)
    chm.paras['path']=KM_TEMP
    chm.paras['title']=name
    chm.addPage(jChm.Page('cover', env['NAME'], '_cover.html'))
    
    
    for chapterName, chapter in sorted(book['chapters'].items()):
        chm.addPage(jChm.Page(chapterName, chapterName, chapterName+'.html', 0, 'cover'))    
        for pageName, page in sorted(chapter['pages'].items()):
            pageKey=chapterName + '__'+ pageName
            chm.addPage(jChm.Page(pageKey, pageName, pageKey+'.html', 0, chapterName))
    
    print(chm.generateAll())
    print('--> ' + KM_TEMP + '\\' + name + '.chm')

    for outputPath in outputPaths:
        shutil.copyfile(KM_TEMP + '\\' + name + '.chm', outputPath +'\\'+name+'.chm')
        print('copy to --> '+ outputPath + '\\' + name + '.chm')

