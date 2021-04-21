from django.shortcuts import render
from testapp.models import Framework
import urllib.request
import urllib
from urllib.parse import unquote
from urllib.parse import urlparse, urljoin
import re
from bs4 import BeautifulSoup
import requests

total_urls_visited = 0
def homeview(request):
    flag=False
    title=None
    iurls_count = None
    eurls_count = None
    turls_count = None
    iurls = None
    eurls = None
    if request.method=="POST":
        flag=True
        inputurl=request.POST.get("url")
        f=Framework(Url=inputurl)
        f.save()
        reqs = requests.get(inputurl)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        title=set()
        for t in soup.find_all('title'):
            x = t.get_text()
            title.add(x)

        internal_urls = set()
        external_urls = set()

        def is_valid(url):
            """
            Checks whether `url` is a valid URL.
            """
            parsed = urlparse(url)
            return bool(parsed.netloc) and bool(parsed.scheme)

        def get_all_website_links(url):
            """
            Returns all URLs that is found on `url` in which it belongs to the same website
            """
            # all URLs of `url`
            urls = set()
            # domain name of the URL without the protocol
            domain_name = urlparse(url).netloc
            soup = BeautifulSoup(requests.get(url).content, "html.parser")
            for a_tag in soup.findAll("a"):
                href = a_tag.attrs.get("href")
                if href == "" or href is None:
                    # href empty tag
                    continue
                 # join the URL if it's relative (not absolute link)
                href = urljoin(url, href)
                # parsed_href = urlparse(href)
                # # remove URL GET parameters, URL fragments, etc.
                # href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
                if not is_valid(href):
                    # not a valid URL
                    continue
                if href in internal_urls:
                    # already in the set
                    continue
                if domain_name not in href:
                    # external link
                    if href not in external_urls:
                        print( "External link:",href)
                        external_urls.add(href)
                    continue
                print( "Internal link:", href)
                urls.add(href)
                internal_urls.add(href)
            for a_tag in soup.findAll("img"):
                href = a_tag.attrs.get("src")
                if href == "" or href is None:
                    # href empty tag
                    continue
                 # join the URL if it's relative (not absolute link)
                href = urljoin(url, href)
                # parsed_href = urlparse(href)
                # # remove URL GET parameters, URL fragments, etc.
                # href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
                if not is_valid(href):
                    # not a valid URL
                    continue
                if href in internal_urls:
                    # already in the set
                    continue
                if domain_name not in href:
                    # external link
                    if href not in external_urls:
                        print( "External link:",href)
                        external_urls.add(href)
                    continue
                print( "Internal link:", href)
                urls.add(href)
                internal_urls.add(href)

            return urls


        def crawl(url, max_urls=100):
            """
            Crawls a web page and extracts all links.
            You'll find all links in `external_urls` and `internal_urls` global set variables.
            params:
                max_urls (int): number of max urls to crawl, default is 30.
            """
            global total_urls_visited
            total_urls_visited += 1
            print("Crawling:", url)
            links = get_all_website_links(url)
            print(links)
            for link in links:
                if total_urls_visited > max_urls:
                    break
                crawl(link, max_urls=max_urls)




        crawl(inputurl)
        iurls_count = len(internal_urls)
        eurls_count = len(external_urls)
        turls_count = iurls_count + eurls_count
        iurls = internal_urls
        eurls = external_urls
        print("[+] Total Internal links:", len(internal_urls))
        print("[+] Total External links:", len(external_urls))
        print("[+] Total URLs:", len(external_urls) + len(internal_urls))
        print("[+] Total crawled URLs:", total_urls_visited)



        # reqs=requests.get(url)
        # soup = BeautifulSoup(reqs.text, 'html.parser')
        # title=set()
        # for t in soup.find_all('title'):
        #     x=t.get_text()
        #     title.add(x)
        # # urlcontent = urllib.request.urlopen(url).read().decode('utf-8')
        # # title = re.findall('<title>.*</title>', urlcontent)
        # #print(soup)
        # # urls = re.findall("(\w+):/([\w\-\.]+)(\w+).(\w+)", urlcontent)
        # print(title)
        # urls=set()
        # for link in soup.find_all('a'):
        #     print(link.get('href'))
        #     x=link.get('href')
        #     urls.add(x)
        # print(urls)
        # surls=set()
        # z=set()
        # def scrapurls(s):
        #     for url in s:
        #         if url not in surls and url[0:4]=="http":
        #             reqs = requests.get(url)
        #             soup = BeautifulSoup(reqs.text, 'html.parser')
        #             l = list(soup.find_all('a'))
        #             print(len(l))
        #             # z = set()
        #             for link in soup.find_all('a'):
        #                 x = link.get('href')
        #                 surls.add(x)
        #                 print(len(surls))
        #                 z.add(x)
        #             scrapurls(z)
        #             print(z)
        #
        #
        #
        # scrapurls(urls)
        # print(len(surls))
        # count=len(surls)
        # for x in surls:
        #     print(x)






        # print(urls)
        # print(len(urls))
        # for x in urls:
        #     urlcontent1 = urllib.request.urlopen(x[0]).read().decode('utf-8')
        #     surls=re.findall("((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)", urlcontent1)
        #     print(surls)
    return render(request,"testapp/home.html",{'title':title,"iurls_count":iurls_count,"eurls_count":eurls_count,"turls_count":turls_count,"iurls":iurls,"eurls":eurls,'flag':flag})

# Create your views here.
