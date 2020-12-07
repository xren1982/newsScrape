import os
import pandas as pd
import json

def crawl():
    cacheClean()
    os.system("scrapy crawl finsmes -o ./bin/finsmes.json")
    os.system("scrapy crawl privateequitywire -o ./bin/privateequitywire.json")
    os.system("scrapy crawl wjs -o ./bin/wjs.json")
    os.system("scrapy crawl altassets -o ./bin/altassets.json")
    os.system("scrapy crawl privateequityinternational -o ./bin/privateequityinternational.json")
    os.system("scrapy crawl privateequityiwire -o ./bin/privateequityiwire.json")
    os.system("scrapy crawl vccircle -o ./bin/vccircle.json")
    os.system("scrapy crawl pehub -o ./bin/pehub.json")
    os.system("scrapy crawl cityam -o ./bin/cityam.json")
    os.system("scrapy crawl penews -o ./bin/penews.json")
    os.system("scrapy crawl venturecapitaljournal -o ./bin/venturecapitaljournal.json")
    os.system("scrapy crawl buyoutsinsider -o ./bin/buyoutsinsider.json")
    os.system("scrapy crawl secondariesinvestor -o ./bin/secondariesinvestor.json")
    os.system("scrapy crawl unquote -o ./bin/unquote.json")
    os.system("scrapy crawl prnewswire -o ./bin/prnewswire.json")
    os.system("scrapy crawl businesswire -o ./bin/businesswire.json")
    os.system("scrapy crawl globenewswire -o ./bin/globenewswire.json")
    os.system("scrapy crawl prweb -o ./bin/prweb.json")
    os.system("scrapy crawl cision -o ./bin/cision.json")
    os.system("scrapy crawl globalsageknowledge -o ./bin/globalsageknowledge.json")
    os.system("scrapy crawl internationaladviser -o ./bin/internationaladviser.json")
    os.system("scrapy crawl asianinvestor -o ./bin/asianinvestor.json")
    os.system("scrapy crawl fundselectorasia -o ./bin/fundselectorasia.json")
    os.system("scrapy crawl toplegalit -o ./bin/toplegalit.json")
    os.system("scrapy crawl lawasia -o ./bin/lawasia.json")
    os.system("scrapy crawl pionline -o ./bin/pionline.json")
    os.system("scrapy crawl realdeals -o ./bin/realdeals.json")

    dataFiles = getJsonFile()
    print('Data Scrapped in below files:')
    for f in dataFiles:
        print(f)

def getJsonFile():
    dir = os.getcwd()
    bin = os.path.join(dir, "bin")
    fileList = os.listdir(bin)
    dataFiles = [file for file in fileList if file.endswith(".json") and file.__contains__('input') == False]
    dataFileList = []
    for file in dataFiles:
        dataFileList.append(os.path.join(bin, file))
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

    col = ['site', 'search key', 'no. of matches', 'headlines', 'dates', 'links', 'content', 'len']
    df = pd.DataFrame(columns=col)

    if inpData['crawl'] == 'Y':
        crawl()
    dataFiles = getJsonFile()
    for i in dataFiles:
        _, spy = os.path.split(i)
        spy = spy[:-5]
        print(spy)
        key = inpData[spy]
        print(spy)

        try:
            dfx = pd.DataFrame(json.load(open(i)))
            dfx['search key'] = dfx['headlines'].apply(lambda x: SearchList(list(key.split(',')), x))
            dfx['len'] = dfx['search key'].apply(lambda x: len(x))
            dfx['no. of matches'] = dfx['search key'].apply(lambda x: 0 if len(x) == 0 else len(list(x.split(','))))
            #dfx = dfx[dfx['len'] > 0]
            print(dfx.shape)
            df = df.append(dfx, ignore_index = True)
        except Exception as e:
            print("Error Opening the file: "+str(e))

    df.columns = [c.upper() for c in df]
    df[[c for c in df if c != 'LEN']].to_excel(writer, sheet_name='Master Sheet', index=False)
    print(df.shape)

    writer.save()
    print('Web Crawl Complete!')