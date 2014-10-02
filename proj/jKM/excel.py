
import os
import xlrd

def getBook(env):
    collection=getCollection(env)
    return collection2book(env, collection)


def getCollection(env):
    KM_DATA=env['KM_DATA']
    excelNames=env['BOOKS'] if 'BOOKS' in env else []
    if(excelNames==[]):
        excelNames = [f for f in os.listdir(KM_DATA) 
                if f.split('.')[-1] in ['xlsx', 'xls'] 
                    and f[0]!='~'
            ]
    collection=dict()
    for fileName in excelNames:
        print('<-- '+fileName)
        # excel=jData.getExcel(KM_DATA + '\\' + fileName)
        filePath=KM_DATA + '\\' + fileName
        excel = xlrd.open_workbook(filePath, encoding_override='big5')
        
        subject=getSubject(excel)
        subjectName=''.join(fileName.split('.')[:-1])
        collection[subjectName]=subject
    return collection

def getSubject(excel, sheetNames=[]):
    subject=dict()
    if sheetNames==[]:
        sheetNames=excel.sheet_names()
    for sheetName in sheetNames:
        sheet=excel.sheet_by_name(sheetName)        
        doc=getDoc(sheet)
        subject[sheetName]=doc
    return subject

'''
def getDoc(excel, sheetName):
    sheet=excel.sheet_by_name(sheetName)
    # DB =========================================
    content=getItems(sheet)
    doc=dict()
    doc['name']=sheetName
    doc['loadTime']=dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    doc['items']=content
    #print(json.dumps(doc, indent=4));
    return doc
'''

def getDoc(sheet):
    #sheet=book.sheet_by_name('jdk')
    #remarkColNo=self.getRemarkColNo(sheet)    
    items=[]

    for row in range(0,sheet.nrows):
        level=getCountLevel(sheet, row)
        if level==sheet.ncols-1:
            name=sheet.cell(row,level).value
            value=''
        else:
            name=sheet.cell(row,level).value
            value=sheet.cell(row,level+1).value
        line={'row':row
            , 'level':level
            , 'key':name
            , 'value':value
        }
        scs=getSpecialColumns(sheet)
        for sc in scs:
            if row!=0:
                line[sc[0]]=sheet.cell(row, sc[1]).value
        #, 'remark':'' if remarkColNo==-1 else sheet.cell(row,remarkColNo-1).value
        items.append(line)
        line['parentRow']=getParentRow(items, row)
        index=len([item for item in items if item['parentRow']==line['parentRow']])-1
        line['index']=index
    return items

def getParentRow(items, row):
    currentItem=items[row]
    parentItems=[item for item in items if item['level']==currentItem['level']-1 and item['row']<currentItem['row']]
    if len(parentItems)==0:
        parentRow=-1
    else:
        parentRow=parentItems[-1]['row']
    return parentRow

# return location of first non-empty cell given specified sheet and row#
def getCountLevel(sheet, row):  
    for col in range(0, sheet.ncols):
        if sheet.cell(row, col).value!='':
            return col
    return col

def getRemarkColNo(sheet):
    remarkColNo=sheet.ncols
    for row in range(0,sheet.nrows):
        #print(row, sheet.cell(row, sheet.ncols-2).value)
        if sheet.cell(row, sheet.ncols-2).value!='':
            remarkColNo=-1
    return remarkColNo

def getSpecialColumns(sheet):
    for col in range(sheet.ncols)[::-1]:
        emptyCol=True
        for row in range(sheet.nrows):
            if(sheet.cell(row,col).value!=''):
                emptyCol=False
        if emptyCol==True:
            specialColumns=list()
            for col2 in range(col+1, sheet.ncols):
                specialColumns.append([sheet.cell(0, col2).value,col2])
            return specialColumns
    return list()

def collection2book(env, collection):
    book={}
    book['name']=env['NAME']
    book['chapters']={}

    for chapterName in collection.keys():
        newChapter={}
        newChapter['name']=chapterName
        newChapter['desc']=''
        
        if '_meta' in collection[chapterName].keys():
            for row in collection[chapterName]['_meta']:
                if row['key']=='desc':
                    newChapter['desc']=row['value']
        newChapter['pages']={}
        for pageName in collection[chapterName].keys():
            if pageName[0]!='_': 
                rows=collection[chapterName][pageName]
                newChapter['pages'][pageName]=rows2page(rows)
        book['chapters'][chapterName]=newChapter
    if env['ENABLE_CATEGORY']==True:
        book=getSummary(book)
    return book
    
def getSummary(book):
    book['chapters']['_Categories']={}
    categories=book['chapters']['_Categories']
    categories['name']='_Categories'
    categories['pages']={}
    
    for chapterName, chapter in book['chapters'].items():
        for pageName, page in chapter['pages'].items():
            if 'category' in page:
                if page['category'] not in categories:
                    categories[page['category']]={}
                categories['pages'][pageName]=page
            
    return book    
    
def rows2page(rows):
    newPage={}
    newPage['sections']=[]
    metaNames=['description', 'status', 'author', 'createdate', 'updatedate', 'version', 'tags', 'category']
    for row in rows:
        if unicode(row['key']).lower() in metaNames:
            newPage[unicode(row['key']).lower()]=row['value']
        elif row['level']==0:
            newPage['sections'].append(addSection(rows, row))
    return newPage

    
def addSection(rows, row):
    newSection={}
    newSection['key']=row['key']
    newSection['value']=row['value']
    newSection['cell']='%d,%d' %(row['row']+1, row['level']+1)
    newSection['properties']={}
    for prt in row.keys():
        if prt not in ['key', 'value', 'index', 'level', 'parentRow', 'row']:
            if row[prt]:
                newSection['properties'][prt]=row[prt]
    newSection['sections']=[]
    for _ in rows:
        if _['parentRow']==row['row']:
            newSection['sections'].append(addSection(rows, _))

    return newSection