import os
import pandas as pd
import json

def crawl():
    cacheClean()
    os.system("scrapy crawl finsmes -o finsmes.json")
    os.system("scrapy crawl privateequitywire -o privateequitywire.json")
    os.system("scrapy crawl wjs -o wjs.json")
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

def SearchList(kwList, string):
    k = [x for x in kwList if (x.lower() in string.lower())]
    s = ''
    c = 1
    for i in k:
        if c == 1:
            s = str(i)
            c += 1
        else:
            s = s + ", " + str(i)
    return s

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

        dfx = pd.DataFrame(json.load(open(i)))
        dfx['Master Search'] = dfx['headlines'].apply(lambda x: SearchList(list(key.split()), x))
        dfx['len'] = dfx['Master Search'].apply(lambda x: len(x))
        dfx['Number of Matches'] = dfx['Master Search'].apply(lambda x: 0 if len(x) == 0 else len(list(x.split(','))))
        #dfx = dfx[dfx['len'] > 0]

        print(dfx.shape)
        df = df.append(dfx, ignore_index = True)

    df.columns = [c.upper() for c in df]
    df[[c for c in df if c != 'LEN']].to_excel(writer, sheet_name='Master Sheet', index=False)
    print(df.shape)

    writer.save()
