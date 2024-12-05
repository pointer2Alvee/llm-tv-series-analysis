from glob import glob # for file paths
import pandas as pd # for tabular dataset
import numpy as np

# put all above from (2) Load Dataset in a single function : 
def load_subtitles_dataset(dataset_path):
    subtitles_paths = glob(dataset_path + '/*.ass')
    scripts = []
    episode_num = []
    for path in subtitles_paths: #path is the directory/file.ass
        # print(f"debug path: {path}")
        # from each path/ subtitle file read lines
        with open(path, 'r', encoding='utf-8') as file: # without  encoding='utf-8' gives error, not shown in video
            lines = file.readlines()
            
            # data/line cleaning
            lines = lines[27:] # data from line 27, because before it are meta data
            lines = [",".join(line.split(',')[9:]) for line in lines ]# remove everything before the 9th comma , we just want the text
        
        # data/line cleaning
        lines = [line.replace('\\N',' ') for line in lines ]# remove \\n from the text
        script = " ".join(lines) # all texts to one big paragraph

        episode = int(path.split('-')[-1].split('.')[0].strip())
        scripts.append(script)
        episode_num.append(episode)

    df = pd.DataFrame.from_dict({"episode" : episode_num, "script": scripts})
    return df

