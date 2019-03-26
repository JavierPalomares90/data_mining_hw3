#python utility to scrape all pdfs from http://proceedings.mlr.press/v80/

import re
from urllib.request import urlopen
from urllib.parse import urlparse
import os

URL = 'http://proceedings.mlr.press/v80/'
DOWNLOAD_PATH = "./pdfs/"


def get_all_links():
    # connect to the url
    website = urlopen(URL)
    # get the html code
    html = website.read().decode('utf8')

    # use re.findall to get all the links
    links = re.findall('"((http|ftp)s?://.*?)"', html)
    return links

def get_pdf_links(links):
    pdfs = []
    pattern = re.compile(".*\.pdf")
    for tuple in links:
        link = tuple[0]
        matches = re.match(pattern,link)
        if matches:
            pdfs.append(link)
    return pdfs

def download_pdfs(pdfs):
    for pdf_link in pdfs:
        pdf = urlopen(pdf_link)
        o = urlparse(pdf_link)
        print("Downloading {}".format(pdf_link))
        file_name = os.path.basename(o[2])
        path = DOWNLOAD_PATH + file_name
        f = open(path,'wb+')
        f.write(pdf.read())
        f.close()




def main():
    links = get_all_links()
    pdf_links = get_pdf_links(links)
    download_pdfs(pdf_links)

if __name__=='__main__':
    main()

