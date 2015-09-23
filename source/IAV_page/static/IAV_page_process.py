import sys
sys.path.remove('/Users/agatorano/Code/metascape/metascape.org/static')
sys.path.append("/Users/agatorano/Code/IAV/IAV.org/static")
print(sys.path)
import os
import time
import pandas as pd
import numpy as np
import go
from pandas import options

options.io.excel.xlsx.writer= 'xlsxwriter'

def read_file(file_):
  name = '/Users/agatorano/Code/IAV/IAV.org/static/Table_S4.xlsx'
  xls1 = pd.read_excel(name,index_col=None, na_values=['NA'])

  if len(file_)>0:
    name = '/Users/agatorano/Code/IAV/IAV.org/media/'+file_
    xls2 = pd.read_excel(name,index_col=None, na_values=['NA'])
    return xls1,xls2 
  else:
    return xls1

def get_genes(xls):
  return [x for x in xls[xls.columns.values[0]]]

def check_proteins(xls,flu_protein):

  flu_protein=flu_protein.replace('\'','')
  flu_protein=flu_protein.replace('[','')
  flu_protein=flu_protein.replace(']','')
  flu_protein=flu_protein.replace(' ','')
  flu_protein=flu_protein.split(',')
  all_genes = ['ALL','NONE','ANY','HA','NA','NP','M1','M2','NS1','NEP','PA','PB1','PB2','PB1F2']
  list_ = [str(el).split(" ") for el in list(xls.FluProteins)] 
  set_ = [set(el) for el in list_]


  if('NONE' in flu_protein):
    xls = xls.iloc[[i for i in range(len(xls)) if(list_[i][0]=='nan')]]
  elif('ALL' in flu_protein):
    flu_protein.remove('ALL')
    ind = [i for i in range(len(xls)) if set(flu_protein).issubset(set_[i])]
    xls=xls.iloc[ind]
  elif('ANY' in flu_protein):
    xls = xls.iloc[[i for i in range(len(xls)) if(list_[i][0]!='nan')]]
  else:
    xls = xls.iloc[[i for i in range(len(xls)) if([1 for el in flu_protein if(el in set_[i])])]]

  return xls

def get_list(z_score,screens,flu_protein,word_search,file_):

  name = '/Users/agatorano/Code/IAV/IAV.org/static/proteinatlas.xlsx'
  protein_annotate = xls1 = pd.read_excel(name,index_col=None, na_values=['NA']) 

  temp=[]

  for row in protein_annotate.iterrows():
      index, data = row
      temp.append(data.tolist())

  if len(file_)>0:
    xls_in,xls_u = read_file(file_)
  else:
    xls_in = read_file(file_)
    xls_u = ''

  if(z_score !=0):
    print('hey')
    print(z_score)
    if(z_score>0):
      xls_in = xls_in[xls_in['Z_RSA'].astype(float)>=z_score]
    elif(z_score<0):
      xls_in = xls_in[xls_in['Z_RSA'].astype(float)<=z_score]
    #xls_out= xls_out[xls_out['Gene'].isin(xls_in['Gene'].tolist())]

  if(len(flu_protein)!=0):
    xls_in = check_proteins(xls_in,flu_protein)
    #xls_out= xls_out[xls_out['Gene'].isin(xls_in['Gene'].tolist())]

  if(screens!=0):
    xls_in = xls_in[xls_in['BrassHit']+xls_in['WatanabeHit']+xls_in['KonigHit']+xls_in['KarlasHit']+xls_in['ShapiraHit']+xls_in['WardHit']+xls_in['SuHit']+xls_in['TranHit']>=screens]
    #xls_out= xls_out[xls_out['Gene'].isin(xls_in['Gene'].tolist())]

  if(len(word_search)!=0):
    genes=[]
    for list_ in temp:
      for el in list_:
        if(word_search.lower() in str(el).lower()):
          genes.append(list_[0])
    xls_in = xls_in[xls_in['Symbol'].isin(genes)]
    #xls_out= xls_out[xls_out['Gene'].isin(xls_in['Gene'].tolist())]
  
  if len(xls_u)>0:
    c_0 = xls_in.columns.values
    c_1 = xls_u.columns.values
    xls_in.columns=c_0
    c_0[0]=c_1[0]
    xls_in = xls_u.merge(xls_in,how='left')

  genes = get_genes(xls_in)

  genes = list(map(str,genes))
  go_ = go.GO(DIR='/Users/agatorano/Code/IAV/IAV.org/static/')
  go_ = go_.analysis(S_hit=genes)

  top10=''

  if 'None' not in str(type(go_)):

    x=[]
    for ge in xls_in[xls_in.columns.values[0]]:
      x.append(go_[go_['GeneID'].str.contains(str(ge))]['GO'].tolist())

    x = list(map(str,x))
    for el,i in zip(x,range(len(x))):
      x[i] = el.replace(']','')
      x[i] = x[i].replace('[','')

    xls_in['GO'] = pd.Series(x).values

    x=[]

    for ge in xls_in[xls_in.columns.values[0]]:
      x.append(go_[go_['GeneID'].str.contains(str(ge))]['Description'].tolist())

    x = list(map(str,x))
    for el,i in zip(x,range(len(x))):
      x[i] = el.replace(']','')
      x[i] = x[i].replace('[','')

    xls_in['GO_Description'] = pd.Series(x).values

    go_.sort('LogP', ascending=False, inplace=True)
    top10 = go_.tail(10)

  path=save_file(xls_in)
  
  return [path,xls_in,genes,top10]

def save_file(xls_out):
  date_ = time.strftime("%Y/%m/%d")
  time_ = time.strftime("%I:%M:%S")

  filename= 'genelist_%s.xlsx'%(time_)
  path='/Users/agatorano/Code/IAV/IAV.org/media/IAV_page/%s/'%(date_)
  media_path='IAV_page/%s/'%date_+filename

  output_directory = os.path.dirname(path)
  if not os.path.exists(output_directory):
    os.makedirs(output_directory)

  xls_out.to_excel(path+filename,index=False)
  
  return media_path

def main():
  xls = read_file()
  print(get_list(-1.5,0,"",''))

if __name__ =='__main__':
  main()
