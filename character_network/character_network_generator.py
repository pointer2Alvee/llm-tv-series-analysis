import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network

class CharacterNetworkGenerator():

    def __init__(self):
        pass
    
    
    def generate_character_network(self, df):
        window=10 # if two chars appearin within 10 sentences
        entity_relationship = []
        
        # for each row/episodes
        for row in df['ners']:
            
            previous_entities_in_window = []
            
            # for each sentence of each episode
            for sentence in row:
                #print(f"debug, sentence : {sentence}")
                
                # convertes sentence set to list, empty set to empty list
                previous_entities_in_window.append(list(sentence)) # list of lists : 2D list
                #print(f"debug, previous_entities_in_window : {previous_entities_in_window}")
                previous_entities_in_window = previous_entities_in_window[-window:] # last 10 sentences as -window = -10
                
                # flatten 2d list to 1d list
                previous_entities_flattened = sum(previous_entities_in_window, [])
                #print (f"debug, pre-ent-flatnd = {previous_entities_flattened}")
                
                for entity in sentence:
                    for entity_in_window in previous_entities_flattened:
                        if entity != entity_in_window:
                            entity_relationship.append(sorted([entity,entity_in_window]))
        
        relationship_df = pd.DataFrame({'value' : entity_relationship})
        relationship_df['source'] = relationship_df['value'].apply(lambda x: x[0])
        relationship_df['target'] = relationship_df['value'].apply(lambda x: x[1])
        
        #count
        relationship_df = relationship_df.groupby(['source', 'target']).count().reset_index()
        relationship_df = relationship_df.sort_values('value', ascending=False) # most signiicant chars are in top and less sign9ificant chars in bottom so descending order 
        
        return relationship_df
                      
                      
    def draw_network_graph(self, relationship_df):
        relationship_df = relationship_df.head(200) # limiting to 200 chars
        # transforms the chars to a network by network x lib
        G = nx.from_pandas_edgelist(
            relationship_df,
            source='source',
            target='target',
            edge_attr='value',
            create_using=nx.Graph() # give a visualization engine
            
        )

        net = Network(notebook=True, width="1000px", height="700px", bgcolor="#222222", font_color="white", cdn_resources="remote")
        node_degree = dict(G.degree) # size of each char node

        nx.set_node_attributes(G, node_degree, 'size')
        net.from_nx(G)
        
        html = net.generate_html()
        html = html.replace("'", "\"")
        
        
        # just copy pasted from vid's git
        output_html = f"""<iframe style="width: 100%; height: 600px;margin:0 auto" name="result" allow="midi; geolocation; microphone; camera;
                            display-capture; encrypted-media;" sandbox="allow-modals allow-forms
                            allow-scripts allow-same-origin allow-popups
                            allow-top-navigation-by-user-activation allow-downloads" allowfullscreen=""
                            allowpaymentrequest="" frameborder="0" srcdoc='{html}'></iframe>"""
    
        return output_html