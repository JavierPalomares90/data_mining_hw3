# python utility to scrape all pdfs from http://proceedings.mlr.press/v80/
# Author: Javier Palomares
import heapq
import re
from urllib.request import urlopen
from urllib.parse import urlparse
import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from os import listdir
from os.path import isfile, join
# From PDFInterpreter import both PDFResourceManager and PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
# Import this to raise exception whenever text extraction from PDF is not allowed
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string


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


def read_pdfs():
    pdf_files = [f for f in listdir(DOWNLOAD_PATH) if isfile(join(DOWNLOAD_PATH, f))]
    word_freq = {}

    stopWords = set(stopwords.words('english'))
    stopWords.add('et')
    stopWords.add('al')
    for pdf_file in pdf_files:

        path = DOWNLOAD_PATH + pdf_file
        fp = open(path,'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser)
        extracted_text = ""

        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed

        rsrcmgr = PDFResourceManager()

        # set parameters for analysis
        laparams = LAParams()

        # Create a PDFDevice object which translates interpreted information into desired format
        # Device needs to be connected to resource manager to store shared resources
        # device = PDFDevice(rsrcmgr)
        # Extract the decive to page aggregator to get LT object elements
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # Create interpreter object to process page content from PDFDocument
        # Interpreter needs to be connected to resource manager for shared resources and device
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # Ok now that we have everything to process a pdf document, lets process it page by page
        for page in PDFPage.create_pages(document):
            # As the interpreter processes the page stored in PDFDocument object
            interpreter.process_page(page)
            # The device renders the layout from interpreter
            layout = device.get_result()
            # Out of the many LT objects within layout, we are interested in LTTextBox and LTTextLine
            for lt_obj in layout:
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    text = lt_obj.get_text()
                    # remove any characters that pdfminer was not able to
                    # convert to unicode and converts to (cid:%%)
                    text = re.sub('(cid:[0-9]+)','',text)
                    # make all text lowercase
                    text = text.lower()
                    # remove line breaks
                    text = text.replace('-\n','')
                    # remove all punctuation from the text
                    text = text.translate(str.maketrans('', '', string.punctuation))
                    # remove new line
                    text = text.replace('\n',' ')
                    text = text.replace('−',' ')

                    extracted_text += text
        words = word_tokenize(extracted_text)
        for word in words:
            # don't include stop words or numeric words or single chars representing mathematical variables
            if (word not in stopWords) and (word.isnumeric()==False) and (len(word) > 1):
                # take all word to lowercase
                word = word.lower()
                count = word_freq.get(word,0)
                word_freq[word] = count+1
        fp.close()

    return word_freq

def write_freqs(word_freq):
    with open("word_freqs.txt", 'w') as f:
        for word, count in word_freq.items():
            f.write('{} {}\n'.format(word,count))

def get_top_ten(word_freq):
    heap = [(-value, key) for key, value in word_freq.items()]
    largest = heapq.nsmallest(10, heap)
    largest = [(key, -value) for value, key in largest]
    return largest

def main():
    links = get_all_links()
    pdf_links = get_pdf_links(links)
    download_pdfs(pdf_links)
    word_freq = read_pdfs()
    write_freqs(word_freq)
    largest = get_top_ten(word_freq)
    print(largest)


if __name__=='__main__':
    main()

