# BASICALLY SHIFTING ALL CODES 
# from theme_classification_development.ipynb to this file and utils/data_loader.py

# IMPORTING 
from transformers import pipeline # importing hugging face
from nltk import sent_tokenize # sentence tokenizer, separate text to multiple sentences
import nltk
import torch
from glob import glob # for file paths
import pandas as pd # for tabular dataset
import numpy as np

    
    
# all codes from notebook but inside a class
class ThemeClassifier():
    
    # INIT MODEL FROM HUGGING FACE AND THEME LIST, LOAD MODEL etc
    def __init__(self, theme_list) -> None:
        self.model_name = "facebook/bart-large-mnli"
        self.device  = 0 if torch.cuda.is_available() else 'cpu'
        self.theme_list = theme_list
        self.theme_classifier =  self.load_model(self.device)

    # LOAD MODEL AND USE IT ON GPU (device)
    def load_model(self, device):
        theme_classifier = pipeline(
            "zero-shot-classification",
            model=self.model_name,
            device=device
        )
        return theme_classifier
    
    
    # TOKENIZE LINES FROM SUBITILES, RUN MODEL ON SUBTITLES DATASET
    def get_theme_inference(self, script):
        script_sentences = sent_tokenize(script)
        
        # Batch sentences
        # batch sentences
        sentence_batch_size = 20
        script_batches = []
        for index in range(0, len(script_sentences), sentence_batch_size):
            sent = " ".join(script_sentences[index:index + sentence_batch_size])
            script_batches.append(sent)

        # Run model
        theme_output = self.theme_classifier(
            script_batches[:2],
            self.theme_list,
            multi_label=True
        )
        
        # structured/wrangle Output
        themes = {}
        for output in theme_output:
            for label,score in zip(output['labels'],output['scores']):
                if label not in themes:
                    themes[label] = []
                themes[label].append(score)

        # Find mean of each theme, (batch_1_score + batch_2_score + batch_n_score) / n
        themes = {key : np.mean(value) for key,value in themes.items()}
        
        # each score below for each theme is a mean of all scores of that theme    
        return themes