import spacy
from nltk import sent_tokenize # import sentence tokenize

import os
import sys
import pathlib

from ast import literal_eval

import pandas as pd


# For loading dataset
folder_path = pathlib.Path().parent.resolve()
sys.path.append(os.path.join(folder_path, '../'))
from utils import load_subtitles_dataset

class NamedEntityRecognizer:
    def __init__(self):
        self.nlp_model = self.load_model()
        pass
    
    
    def load_model(self):
        nlp = spacy.load("en_core_web_trf")
        return nlp
    
    
    def get_ners_inference(self, script):
        script_sentences = sent_tokenize(script)
        ner_output = []
        
        for sentence in script_sentences:
            doc = self.nlp_model(sentence)
            
            ners = set() # for avoiding duplicates set is best
            
            for entity in doc.ents:
                # only get the named/person entities
                if entity.label_ == "PERSON":
                    full_name = entity.text
                    first_name = entity.text.split(" ")[0]
                    first_name.strip()
                    ners.add(first_name)
            ner_output.append(ners)

        
        return ner_output # see doc , this is the NAMED ENTITIES LIST
            
            
    
    def get_ners(self, dataset_path,save_path=None):
        
        ### WARNING ! PROBABLE BUG BELOW ####
        if save_path is not None and os.path.exists(save_path):
            df = pd.read_csv(save_path)
            # shift back from string to list
            df['ners'] = df['ners'].apply(lambda x: literal_eval(x) if isinstance(x,str) else x)
            return df
        ####################################
        
        # load dataset
        df = load_subtitles_dataset(dataset_path)
        
        # TODO : COMMENT THIS TO RUN ON WHOLE DATASET
        df = df.head(10)
        
        # Run Inference / Model , nlp_model
        df['ners'] = df['script'].apply(self.get_ners_inference)

   
        if save_path is not None:
            df.to_csv(save_path, index=False)
    
        return df