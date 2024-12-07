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

# we want to go back 1 folder and import from utils, so below libs requried
import os
import sys
import pathlib
    
# our curr folder path
folder_path = pathlib.Path(__file__).parent.resolve()
sys.path.append(os.path.join(folder_path,'../'))
from utils import load_subtitles_dataset

nltk.download('punkt')
nltk.download('punkt_tab')
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
    
    
    # RUN get_them_inference() for whole subtitles dataset/ for all episodes
    def get_themes(self, dataset_path, save_path=None):
        
        
        # read saved output if exists
        ######################## THIS BELOW CODE GIVES BUG  ##################
        # if save_path is not None and os.path.exists(save_path):
        #     df = pd.read_csv(save_path)
        #     return df
        #*********************************************************************
        """
        Note :- the video did above three lines of code but there is bug
        BUG : It reads df from saved_path .csv, for in  gradio input themes for first time are : love, hate, self
        then if i run within these three it runs correctly as these three " love, hate, self" are saved in csv
        but if i give  love, hate, self, horror, fear IT GIVES ERROR on any new themes. commenting this solves the problem
        """
        #######################################################################
        
        
        
        # Save the processing into some file / path, so need to rerun and use it from this checkpoint
        
        # load dataset / FULL DATASET / ALL EPISODES
        df = load_subtitles_dataset(dataset_path)
        df  = df.head(2)
        
        # run inference / model
        output_themes = df['script'].apply(self.get_theme_inference)
        theme_df = pd.DataFrame(output_themes.tolist())
        df[theme_df.columns] = theme_df
        
        
        # Save output
        if save_path is not None:
            df.to_csv(save_path, index=False)
            
        return df