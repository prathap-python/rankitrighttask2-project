from django.shortcuts import render
from testapp.models import Framework
import urllib.request
import urllib
from urllib.parse import unquote
import re
from bs4 import BeautifulSoup
import requests
def homeview(request):
    flag=False
    title=None
    surls=None
    count=None
    if request.method=="POST":
        flag=True
        url=request.POST.get("url")
        f=Framework(Url=url)
        f.save()
        reqs=requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        title=set()
        for t in soup.find_all('title'):
            x=t.get_text()
            title.add(x)
        # urlcontent = urllib.request.urlopen(url).read().decode('utf-8')
        # title = re.findall('<title>.*</title>', urlcontent)
        #print(soup)
        # urls = re.findall("(\w+):/([\w\-\.]+)(\w+).(\w+)", urlcontent)
        print(title)
        urls=set()
        for link in soup.find_all('a'):
            print(link.get('href'))
            x=link.get('href')
            urls.add(x)
        print(urls)
        surls=set()
        z=set()
        def scrapurls(s):
            for url in s:
                if url not in surls and url[0:4]=="http":
                    reqs = requests.get(url)
                    soup = BeautifulSoup(reqs.text, 'html.parser')
                    l = list(soup.find_all('a'))
                    print(len(l))
                    # z = set()
                    for link in soup.find_all('a'):
                        x = link.get('href')
                        surls.add(x)
                        print(len(surls))
                        z.add(x)
                    scrapurls(z)
                    print(z)



        scrapurls(urls)
        print(len(surls))
        count=len(surls)
        for x in surls:
            print(x)






        # print(urls)
        # print(len(urls))
        # for x in urls:
        #     urlcontent1 = urllib.request.urlopen(x[0]).read().decode('utf-8')
        #     surls=re.findall("((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)", urlcontent1)
        #     print(surls)
    return render(request,"testapp/home.html",{'title':title,'surls':surls,'count':count,'flag':flag})

# Create your views here.
