#!/usr/bin/env python
import re 
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

def bargraph_GO(dataframe, path,df, file_count):
    """
    Given a pandas DataFrame containing GO enrichment information, generate a
    bar graph for the top 10 enriched categories. Write the result to the given
    path. 
    """
    
    if file_count==1: 
      # make sure that the information is sorted by p-value
      dataframe.sort('LogP', ascending=False, inplace=True)
      top10 = dataframe.tail(10)
      
      go_categories = top10['Description'].tolist()
      for el,i in zip(go_categories,range(len(go_categories))):
        matches = re.findall("[\(\[].*?[\)\]]", el)    
        go_categories[i] = re.sub("[\(\[].*?[\)\]]", "", el)    
        go_categories[i] = go_categories[i]+' '+matches[0]
        go_categories[i] = go_categories[i].replace("Genes annotated by the ","")
        curr = str(go_categories[i])
        if len(curr)>300:
          spaces = [m.start() for m in re.finditer('\s', curr)]
          curr=curr[:spaces[int(len(spaces)/5)]]+ "\n"+curr[spaces[int(len(spaces)/5)]:]
          curr=curr[:spaces[int(len(spaces)*2/5)]]+ "\n"+curr[spaces[int(len(spaces)*2/5)]:]
          curr=curr[:spaces[int(len(spaces)*3/5)]]+ "\n"+curr[spaces[int(len(spaces)*3/5)]:]
          curr=curr[:spaces[int(len(spaces)*4/5)]]+ "\n"+curr[spaces[int(len(spaces)*4/5)]:]
          go_categories[i] = curr 
        elif len(curr)>200:
          spaces = [m.start() for m in re.finditer('\s', curr)]
          curr=curr[:spaces[int(len(spaces)/4)]]+ "\n"+curr[spaces[int(len(spaces)/4)]:]
          curr=curr[:spaces[int(len(spaces)*2/4)]]+ "\n"+curr[spaces[int(len(spaces)*2/4)]:]
          curr=curr[:spaces[int(len(spaces)*3/4)]]+ "\n"+curr[spaces[int(len(spaces)*3/4)]:]
          go_categories[i] = curr 
        elif len(curr)>120:
          spaces = [m.start() for m in re.finditer('\s', curr)]
          curr=curr[:spaces[int(len(spaces)/3)]]+ "\n"+curr[spaces[int(len(spaces)/3)]:]
          curr=curr[:spaces[int(len(spaces)*2/3)]]+ "\n"+curr[spaces[int(len(spaces)*2/3)]:]
          go_categories[i] = curr 
        elif len(curr)>60:
          spaces = [m.start() for m in re.finditer('\s', curr)]
          curr=curr[:spaces[int(len(spaces)/2)]]+ "\n"+curr[spaces[int(len(spaces)/2)]:]
          go_categories[i] = curr 
        #print(go_categories[i])
      y_values = range(len(go_categories))
      logP_values = (-1 * top10['LogP']).tolist()
      
      # plt.xkcd()
      plt.style.use('ggplot')
      plt.figure(figsize=(10,10))

      plt.barh(y_values, logP_values, align="center")
      plt.yticks(y_values, go_categories,linespacing=1)
      plt.xlabel("P-value (-log10)")
      plt.ylabel("GO category")
      plt.subplots_adjust(right=1)
      plt.subplots_adjust(left=0.65)
      plt.ylim(ymin=-1)
      #plt.tight_layout()
      
      # make directories if they don't exist
      output_directory = os.path.dirname(path)
      if not os.path.exists(output_directory):
          os.makedirs(output_directory)
      
      plt.savefig(path)
    else:
      #print("HEY IN GRAPH")
      #print(df)
      #mask = df.isnull()
      #print("HEY IN GRAPH PART TWO")
      plt.figure(figsize=(40,30))
      #plt.tight_layout()
      ax = sns.heatmap(df,annot=True,fmt = '.1f',linewidths=0.5,square=True)
      #print("HEY IN GRAPH PART THREE")
      output_directory = os.path.dirname(path)
      if not os.path.exists(output_directory):
          os.makedirs(output_directory)
      
      plt.savefig(path,bbox_inches='tight')
    
if __name__ == '__main__':
    import pandas
    df = pandas.read_csv('test.csv')
    bargraph_GO(df, '/tmp/bar.pdf')
