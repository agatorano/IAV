#!/usr/bin/env python
import re 
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def bargraph_GO(dataframe, path):
    """
    Given a pandas DataFrame containing GO enrichment information, generate a
    bar graph for the top 10 enriched categories. Write the result to the given
    path. 
    """
    
    # make sure that the information is sorted by p-value
    dataframe.sort('LogP', ascending=False, inplace=True)
    top10 = dataframe.tail(10)
    
    go_categories = top10['Description'].tolist()
    for el,i in zip(go_categories,range(len(go_categories))):
      matches = re.findall("[\(\[].*?[\)\]]", el)    
      go_categories[i] = re.sub("[\(\[].*?[\)\]]", "", el)    
      go_categories[i] = go_categories[i]+' '+matches[0]
    y_values = range(len(go_categories))
    logP_values = (-1 * top10['LogP']).tolist()
    
    # plt.xkcd()
    fig = plt.figure()
    #plt.style.use('ggplot')
    ax = fig.add_subplot(111)

    ax.barh(y_values, logP_values, align="center")
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.set_yticks(y_values, go_categories)
    ax.set_xlabel("P-value (-log10)")
    ax.set_ylabel("GO category")
    plt.subplots_adjust(right=.9)
    plt.subplots_adjust(left=0.125)
    plt.ylim(ymin=-1)
    #plt.tight_layout(pad=1.08)
    
    # make directories if they don't exist
    output_directory = os.path.dirname(path)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    plt.savefig(path)
    
if __name__ == '__main__':
    import pandas
    df = pandas.read_csv('test.csv')
    bargraph_GO(df, '/tmp/bar.pdf')
