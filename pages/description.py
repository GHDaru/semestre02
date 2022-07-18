from matplotlib.pyplot import annotate
import unidecode
import re
import streamlit as st
import pandas as pd
from annotated_text import annotated_text


class Numbers():
    def __init__(self):
        self.color = "#8ef"
        self.number_pattern_raw = '([-+]?[0-9]*[\.,]?[0-9]+)'
        self.number_pattern_change = f" (\g<0>,'NUMBER',{self.color}) "
        self.number_pattern_extract = f"\((.*?),'NUMBER',{self.color}\)"               
    
    def parse_numbers(self, desc):
        """
        Change all numbers integer or float to sugested pattern
        default: NBR number and \g<0> value founded
        Args:
            desc (str): string to parse numbers
            repl (str, optional): Standard string. Defaults to ' <NBR:\g<0>> '.
        """        
        desc = re.sub(self.number_pattern_raw, self.number_pattern_change, desc)      
        #Extract extra spaces
        desc = re.sub('\s{2,}',' ',desc)  
        return desc
    
    
    def extract_numbers(self, desc, processed = False):
        if not processed:
            desc = self.parse_numbers(desc)
        return re.findall(self.number_pattern_extract, desc)
    
class Description(Numbers):
    def __init__(self, description):
        Numbers.__init__(self)
        self.description = description
        self.description_normalized = self.normalize(self.description)
        self.description_processed = self.parse_numbers(self.description_normalized)
        self.annoted_description = self.desc2annotated(self.description_processed)
        self.objets = {'NUMBERS': self.extract_numbers(self.description_processed, True)}
    
    def normalize(self, text):
        """
        Transforma texto para minúsculo e sem acento
        Entrada:
        texto
        Retorno:
        Texto no formato minúsculo e sem acento.
        """
        return unidecode.unidecode(text.lower())   
    
    
    def __str__(self):
        return f'{self.description_processed},{self.description_normalized},{self.description_processed},{self.objets}'
    
    def to_annotated(self):
        pass
        


descricao = st.text_input('Produto', placeholder='Digite o GTIN')

#desc = Description(descricao)



annotated_text(
    "This ",
    '("is", "verb", "#8ef")',
    " some ",
    ("annotated", "adj", "#faa"),
    ("text", "noun", "#afa"),
    " for those of ",
    ("you", "pronoun", "#fea"),
    " who ",
    ("like", "verb", "#8ef"),
    " this sort of ",
    ("thing", "noun", "#afa"),
    "."
)





