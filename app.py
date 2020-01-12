import requests as req
from bs4 import BeautifulSoup
import sys
from multiprocessing import Pool
from clint.arguments import Args
from clint.textui import puts, colored, indent
from azure.cognitiveservices.search.websearch import WebSearchAPI
from msrest.authentication import CognitiveServicesCredentials


GOOGLE_URL="https://www.google.com/search?q="
subscription_key = "49280ce76d2d44d5af706d0c92762c46" # It will expires in 7 Days

client = WebSearchAPI(CognitiveServicesCredentials(subscription_key))

args = Args()
if '-S' in args.flags:
    command=args.grouped['-S'][0]
else:
    command='inurl:php?=id'
    
def get_link_google(url):
    page=req.get(url).text
    with open('temp.html', 'w') as f:
        f.write(page)
    result=[]
    soup = BeautifulSoup(page, 'html.parser')
    res_div=soup.find_all(class_="BNeawe UPmit AP7Wnd")
    for div in res_div:
        link=div.text
        if 'id' in command:
            if 'id=' in link:
                result.append(link)
        else:
            result.append(link)

    return result

def get_link_bing(nb_page):
    result=[]
    offset=nb_page*10-10
    count=10
    web_data = client.web.search(query=command, offset=offset, count=count)
    web_results=web_data.web_pages.value
    for i in web_results:
        link=i.url
        if 'id' in command:
            if 'id=' in link:
                result.append(link)
        else:
            result.append(link)
    return result
        

if __name__ == '__main__':
    args = Args()
    if '-E' in args.flags and '-P' in args.flags and '-Pr' in args.flags:
        
        nb_page=1
        nb_pr=1
        try:
            nb_page=int(args.grouped['-P'][0])
        except:
            puts(colored.yellow("Warming: Incorrect argument Value -P : "+str(args.grouped['-P'][0])))

        try:
            nb_pr=int(args.grouped['-Pr'][0])
        except:
            puts(colored.yellow("Warming: Incorrect argument Value -Pr : "+str(args.grouped['-Pr'][0])))

        if '-S' in args.flags:
            command=args.grouped['-S'][0]
        else:
            command='inurl:php?=id'

        all_result=[]
        if 'google' in args.grouped['-E'][0]:
            urls=[]
            i=1
            while i<=nb_page:
                urls.append(GOOGLE_URL+str(command)+'&start='+str(i*10-10))
                i+=1
            print(urls)
            with Pool(nb_pr) as p:
                result=p.map(get_link_google, urls)
            for r in result:
                for e in r:
                    all_result.append(e)
        
        elif 'bing' in args.grouped['-E'][0]:
            pages=[]
            i=1
            while i<=nb_page:
                pages.append(i)
                i+=1
            with Pool(nb_pr) as p:
                result=p.map(get_link_bing, pages)
                for r in result:
                    for e in r:
                        all_result.append(e)

        nb_result=len(all_result)

        puts(colored.green("Searching for vunerable site using "+args.grouped['-E'][0]+" in "+args.grouped['-P'][0]+" page(s) With "+args.grouped['-Pr'][0]+" Process(es)."))
        puts(colored.yellow("************************************************************"))
        print()
        print()
        with indent(4, quote='==>'):
            for a in all_result:
                puts(colored.red(a))
        print()
        puts(colored.yellow("************************************************************"))
        puts(colored.green(str(nb_result)+" urls detected"))
        puts(colored.yellow("************************************************************"))
        print()
