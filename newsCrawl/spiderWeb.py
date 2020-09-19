import os
import pandas as pd
import json

def crawl():
    cacheClean()
    os.system("scrapy crawl finsmes -o finsmes.json")
    os.system("scrapy crawl privateequitywire -o privateequitywire.json")
    os.system("scrapy crawl wjs -o wjs.json")
    os.system("scrapy crawl altassets -o altassets.json")
    os.system("scrapy crawl privateequityinternational -o privateequityinternational.json")
    os.system("scrapy crawl privateequityiwire -o privateequityiwire.json")
    os.system("scrapy crawl vccircle -o vccircle.json")
    os.system("scrapy crawl pehub -o pehub.json")
    os.system("scrapy crawl cityam -o cityam.json")
    os.system("scrapy crawl penews -o penews.json")
    os.system("scrapy crawl venturecapitaljournal -o venturecapitaljournal.json")
    os.system("scrapy crawl buyoutsinsider -o buyoutsinsider.json")
    os.system("scrapy crawl secondariesinvestor -o secondariesinvestor.json")
    os.system("scrapy crawl unquote -o unquote.json")
    dataFiles = getJsonFile()
    print('Data Scrapped in below files:')
    for f in dataFiles:
        print(f)

def getJsonFile():
    dir = os.getcwd()
    fileList = os.listdir(dir)
    dataFiles = [file for file in fileList if file.endswith(".json") and file.__contains__('input') == False]
    dataFileList = []
    for file in dataFiles:
        dataFileList.append(os.path.join(dir, file))
    return dataFileList

def cacheClean():
    c = 0
    dataFileList = getJsonFile()
    for file in dataFileList:
        os.remove(file)
        c+=1
    print('Removed ' + str(c) + ' Files!')

def SearchList(kwList,string):
    s = ''
    for x in kwList:
        xLen = len(x.split())
        if xLen > 1:
            if (x.lower() in string.lower()):
                s = s+', '+str(x)
        elif xLen == 1:
            if (x.lower() in string.lower().split()):
                s = s+', '+str(x)
    return s[2:]

if __name__ == "__main__":


    writer = pd.ExcelWriter('output.xlsx', engine='openpyxl')
    f = open('input.json', )
    inpData = json.load(f)

    col = ['site', 'Master Search', 'Number of Matches', 'headlines', 'Dates', 'links', 'len']
    df = pd.DataFrame(columns=col)

    if inpData['crawl'] == 'Y':
        crawl()
    dataFiles = getJsonFile()

    for i in dataFiles:
        _, spy = os.path.split(i)
        spy = spy[:-5]

        key = inpData[spy]
        print(spy)

        try:
            dfx = pd.DataFrame(json.load(open(i)))
            dfx['Master Search'] = dfx['headlines'].apply(lambda x: SearchList(list(key.split(',')), x))
            dfx['len'] = dfx['Master Search'].apply(lambda x: len(x))
            dfx['Number of Matches'] = dfx['Master Search'].apply(lambda x: 0 if len(x) == 0 else len(list(x.split(','))))
            #dfx = dfx[dfx['len'] > 0]

            print(dfx.shape)
            df = df.append(dfx, ignore_index = True)
        except:
            print("Error Opening the file.")

    df.columns = [c.upper() for c in df]
    df[[c for c in df if c != 'LEN']].to_excel(writer, sheet_name='Master Sheet', index=False)
    print(df.shape)

    writer.save()
