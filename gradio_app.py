# THIS IS GUI TO RUN THEME CLASSIFIER

import gradio as gr
import pandas as pd
from theme_classifier import ThemeClassifier


# FOR CHAR NET
from character_network import NamedEntityRecognizer, CharacterNetworkGenerator

def get_themes(theme_list_str,subtitles_path,save_path):
    theme_list = theme_list_str.split(',')
    
    # self modified
    theme_list = [theme.strip() for theme in theme_list] #trimming trailing-leading spaces like ," love" to "love"
    # print(f"DEBUG, theme_list : {theme_list}")    
    
    theme_classifier = ThemeClassifier(theme_list)
    output_df = theme_classifier.get_themes(subtitles_path,save_path)
    
    # remove dialogue,episode,script columns
    # loop over all themes and take all except dialogue
    theme_list = [theme for theme in theme_list if theme != "dialogue"] #space before d
    #print(f"DEBUG, theme_list {theme_list}")
    output_df = output_df[theme_list]
    
    output_df = output_df[theme_list].sum().reset_index()

    # rename cols : 
    output_df.columns = ['Theme', 'Score']
    
    # THI BELOW IS ACCORDING TO VIDEO : NOT WORKING ! maybe gradio version upgraded
    ######################################################
    # output_chart = gr.BarPlot(
    #     value = output_df, 
    #     x="Theme",
    #     y="Score",
    #     title="Series Theme",
    #     tooltip=["Theme", "Score"],
    #     interactive=True,
    #     vertical=False,
    #     width = 500,
    #     height=260,
    # )
    
    # DEBUG :
    #print(output_df)
    #print(type(output_df))
    
    #return output_chart
    ######################################################

    return output_df # must return a pandas dataframe



# NOT RECOMMENDED AS GLOBAL PANDAS EMPTY DF, BUT WORKING AS OF NOW
###################BUG REMAINS ######################
output_df = pd.DataFrame({
    "Theme": [],
    "Score": []
    }) 
#####################################################


## get_character_network
def get_character_network(subtitles_path, ner_path):
    ner = NamedEntityRecognizer()
    ner_df = ner.get_ners(subtitles_path, ner_path)
    
    character_network_generator = CharacterNetworkGenerator()
    relationship_df = character_network_generator.generate_character_network(ner_df)
    html = character_network_generator.draw_network_graph(relationship_df)
    
    return html
    

def main():
    # Creating rows and cols in UI
    with gr.Blocks() as iface: # initiates gradio blocks
        
        
        ### THEME CLASSIFICATION GUI SECTION     
        with gr.Row():   # creates row
            # creates col inside row
            with gr.Column():
                gr.HTML("<h1> Theme Classification (Model : zero-shot-classifier)</h1>")

                # OUTPUT 
                with gr.Row():
                    with gr.Column():
                        #plot = gr.BarPlot() # THI BELOW IS ACCORDING TO VIDEO : NOT WORKING !
                        
                        # plot = gr.DataFrame(headers=["Theme", "Score"], label="Theme Scores")

                        plot = gr.BarPlot(
                            value=output_df,
                            y="Theme",
                            x="Score",
                            title="Series Theme",
                            tooltip=["Theme", "Score"],
                            interactive=True,
                            vertical=False,
                            width = 500,
                            height=260,
                            
                        )
                        
                    # INPUT - THEME + SCRIPT + SAVE_PATH
                    with gr.Column():
                        theme_list = gr.Textbox(label="Themes")
                        subtitles_path = gr.Textbox(label="Subtitles or script path")
                        save_path = gr.Textbox(label="Save Path")
                        get_themes_button = gr.Button("Get Themes")  
                        
                        # we use gradio to vizualize instead of seaborn or matplotlib
                        
                        get_themes_button.click(
                            fn=get_themes, 
                            inputs=[theme_list,subtitles_path,save_path], 
                            outputs=[plot]
                        )
             
             
        ### CHARACTER NETWORK GUI SECTION
        with gr.Row(): # creates row
            # creates col inside row
            with gr.Column():
                gr.HTML("<h1> Character-Network (Model : en_core_web_trf)</h1>")

                # OUTPUT 
                with gr.Row():
                    with gr.Column():
                        
                        # output will not be a bar plot like prev one, but some html
                        network_html = gr.HTML()
                        
                    # INPUT - THEME + SCRIPT + SAVE_PATH
                    with gr.Column():
                        subtitles_path = gr.Textbox(label="Subtitles or script path")
                        ner_path = gr.Textbox(label="NERs Save path")
                        get_network_graph_button = gr.Button("Get Character Network")  

                        # we use gradio to vizualize instead of seaborn or matplotlib
                        
                        get_network_graph_button.click(
                            fn=get_character_network, 
                            inputs=[subtitles_path,ner_path], 
                            outputs=[network_html]
                        )
            
              
    # launch the interface
    iface.launch(share=True)               
                    
if __name__ == '__main__':
    main()