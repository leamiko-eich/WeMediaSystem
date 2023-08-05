#encoding=utf-8
from bs4 import BeautifulSoup
from lxml import etree

class BaseApiUnit(object):
    def __init__(self):
        pass

    
    def convert_soup_to_lxml(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")

        # Convert BeautifulSoup element to lxml.etree.Element
        lxml_element = etree.fromstring(str(soup))

        
    def convert_lxml_to_soup(self, lxml_element):
        element_string = etree.tostring(lxml_element, encoding="unicode")

        # Parse the string using BeautifulSoup
        soup_element = BeautifulSoup(element_string, "html.parser")
        return soup_element

    
    def save_ele_as_html(self, target_element, file_name="ele.html"):
        target_element = self.convert_lxml_to_soup(target_element)
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(target_element.prettify())