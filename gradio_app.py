# THIS IS GUI TO RUN THEME CLASSIFIER

import gradio as gr
from theme_classifier import ThemeClassifier

def get_themes(theme_list_str,subtitles_path,save_path):
    theme_list = theme_list_str.split(',')
    theme_classifier = ThemeClassifier(theme_list)



def main():
    # Creating rows and cols in UI
    with gr.Blocks() as iface: # initiates gradio blocks
        
        # creates row
        with gr.Row():
            # creates col inside row
            with gr.Column():
                gr.HTML("<h1> Theme Classification (Model : zero-shot-classifier)</h1>")

                # OUTPUT 
                with gr.Row():
                    with gr.Column():
                        plot = gr.BarPlot()
                        
                    # INPUT - THEME + SCRIPT + SAVE_PATH
                    with gr.Column():
                        theme_list = gr.Textbox(label="Themes")
                        subtitles_path = gr.Textbox(label="Subtitles or script path")
                        save_path = gr.Textbox(label="Save Path")
                        get_themes_button = gr.Button("Get Themes")
                        get_themes_button.click(get_themes, inputs=[theme_list,subtitles_path,save_path], outputs=[plot])
                        
    # launch the interface
    iface.launch(share=True)               
                    
if __name__ == '__main__':
    main()