import requests
from requests.models import Response
from bs4 import BeautifulSoup
import json
import re
from base64 import b64decode

class Parser:
    BASE_URL = b64decode("aHR0cHM6Ly93d3cubmNiaS5ubG0ubmloLmdvdg==").decode("utf-8")
    KEYWORDS = [
        "LOCUS",
        "DEFINITION",
        "ACCESSION",
        "VERSION",
        "KEYWORDS",
        "SOURCE",
        "REFERENCE",
        "COMMENT",
        "REMARK",
        "PRIMARY",
        "FEATURES",
        "ORIGIN"
    ]
    SUBKEYWORDS_REF = [
        "AUTHORS",
        "CONSRTM",
        "TITLE",
        "JOURNAL",
        "PUBMED"
    ]
    SUBKEYWORDS_SOURCE = [
        "ORGANISM"
    ]
    def __init__(self):
        self.get_report_url = "{url}/sviewer/viewer.fcgi?id={id}&db={db}&report=genbank&conwithfeat=on&hide-cdd=on&retmode=html&withmarkup=on&tool=portal&log$=seqview&maxdownloadsize=1000000000000"
        self.get_search_url = "{url}/{db}/?term={term}"

    def filter_string(self, string:str):
        return re.sub("\s\s+", " ", string) + "\n"

    def jsonifyGenbank(self, content:str):
        jsonify_data = {}
        # split all lines
        content = content.split("\n")
        key = ""
        data = ""
        RFSKID = 0
        SCSKID = 0
        for i in content:
            line_content = i.split(" ")

            try:
                if line_content[2] in self.SUBKEYWORDS_REF:
                    key = f"{line_content[2]}_{RFSKID}"
                    data = self.filter_string(i[2+len(key):])

                if line_content[2] in self.SUBKEYWORDS_SOURCE:
                    key = f"{line_content[2]}_{SCSKID}"
                    data = self.filter_string(i[2+len(key):])

                if line_content[0] in self.KEYWORDS:
                    key = line_content[0]
                    if key == "SOURCE":
                        SCSKID += 1
                        key = f"SOURCE_{SCSKID}"
                    if key == "REFERENCE":
                        RFSKID += 1
                        key = f"REFERENCE_{RFSKID}"

                    data = self.filter_string(i[len(key):])


                else:
                    data += self.filter_string(i)

            except IndexError: pass            
            
            jsonify_data[key] = data

        return jsonify_data

    def parseGenbank(self, sm_id:int, db_type:str):
        url = self.get_report_url.format(url=self.BASE_URL, id=sm_id, db=db_type)
        data = requests.get(url, stream=True)
        soup = BeautifulSoup(data.content, 'html.parser')
        data = soup.find("pre", {"class": "genbank"})
        return self.jsonifyGenbank(data.text)

    def parseSearch(self, term:str, db_type:str):
        url = self.get_search_url.format(url=self.BASE_URL, db=db_type, term=term)
        data = requests.get(url, stream=True)
        soup = BeautifulSoup(data.content, 'html.parser')
        data = soup.find_all("div", {"class": "rprt"})
        container = []
        for i in data:
            title = i.find("p", {"class": "title"}).text
            description = i.find("p", {"class": "desc"}).text
            details = i.find("dl", {"class": "rprtid"}).text
            container.append((title, description, details))
        return container
