from collections import defaultdict
import pandas as pd

import go
from pandas_sql import *
from excel_man import *

def format_gene_list(gene_list):
  if len(gene_list) != 2:
    gene_list = list(map(str,gene_list))
    return gene_list
  else:
    gene_list[0] = list(map(str,gene_list[0]))
    for i in range(len(gene_list[1])):
      gene_list[1][i] = list(map(str,gene_list[1][i]))
    return gene_list

def go_analysis(overlap,min_enrichment,pvalue,name,count,gene_list,f_names):

  names = []
  for i in range(count):
    names.append('File %s'%i)
  S_hit = format_gene_list(gene_list)
  if count==1:
    go = GO(DIR='/Users/agatorano/Code/metascape/metascape.org/static/')
    data = go.analysis(S_hit=S_hit,min_overlap=overlap,min_enrichment=min_enrichment,p_cutoff=pvalue)
    add_enrichment(name,data,count)
    return data
  
  else:
    go = GO(DIR='/Users/agatorano/Code/metascape/metascape.org/static/')
    data = go.analysis(S_hit=S_hit[0],min_overlap=overlap,min_enrichment=min_enrichment,p_cutoff=pvalue)
    add_enrichment(name,data,2)

    p_cat = defaultdict(list)

    indices = {}
    enrichments = []
    go = GO(DIR='/Users/agatorano/Code/metascape/metascape.org/static/')
    data_ = go.analysis(S_hit=S_hit[1][0],min_overlap=overlap,min_enrichment=min_enrichment,p_cutoff=pvalue)
    data_.drop(data_.columns[[1,3,4,5,6,7,8,9,10,11]],inplace=True,axis=1)
    #data_.sort('LogP', ascending=False, inplace=True)
    top15 = data_.tail(10)
    top15.rename(columns={'LogP': 'File0 p_v'}, inplace=True)
    pairs = top15.ix[:,[0,1]].values 
    for i in pairs:
      p_cat[i[0]]=[i[1]]
    #print("FIRST**\n")
    #print(str(top15.ix[:,[0,1]].values))
    #print(top15.ix[:,1].values)
    #print("END FIRST**\n")
    out = top15

    counter = 1
    for i in range(count-1):
      go = GO(DIR='/Users/agatorano/Code/metascape/metascape.org/static/')
      data_ = go.analysis(S_hit=S_hit[1][i+1],min_overlap=overlap,min_enrichment=min_enrichment,p_cutoff=pvalue)
      data_.drop(data_.columns[[1,3,4,5,6,7,8,9,10,11]],inplace=True,axis=1)
      #data_.sort('LogP', ascending=False, inplace=True)
      top15 = data_.tail(10)
      pairs = top15.ix[:,[0,1]].values 

      for el in pairs:
        if el[0] not in p_cat:
          p_cat[el[0]] = [el[1]]
          for j in range(counter):
            p_cat[el[0]].insert(0,float('NaN'))
        else:
          p_cat[el[0]].append(el[1])

      keys = p_cat.keys()
      for el in keys:
        if len(p_cat[el])==counter:
          p_cat[el].append(float('NaN'))

      counter+=1
      out['File%s p_v'%str(i+1)]=top15.ix[:,1]

    print("AFTER CHANGES\n")
    print(p_cat)
    print("END CHANGES\n")
    df = pd.DataFrame(columns=names)
    indexes = list(p_cat.keys())
    for el,i in zip(indexes,range(len(indexes))):
      df.loc[i] = p_cat[el]
    df.index = indexes
    print("AFTER CHANGES\n")
    print(df)
    print("END CHANGES\n")

    df.to_csv(path_or_buf='heat_test.csv')
    #for i in range(len(f_names)):
    #  out[i]['file#'] = f_names[i]


    #enrichments = pd.concat(enrichments)
    add_enrichment(name,df,3)

    return [data,enrichments,df]
    
  

def main():
  go_analysis()

if __name__ == "__main__":
  main()
