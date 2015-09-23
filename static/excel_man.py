import pandas as pd
import math
from go import GO

def upload_pandas(name,page):

  xls = pd.read_excel('/Users/agatorano/Code/metascape/metascape.org/media/'+name,sheetname=page,index_col=None, na_values=['NA'])
  return xls


def get_column(name,count):

  if count == 1:
    xls=upload_pandas(name,0)
    col = xls[xls.columns.tolist()[len(xls.columns)-5]]
    col = col.tolist()
    int_concat=[]
    for el in col:
      if math.isnan(el):
        int_concat.append('NA')
      else:
        int_concat.append(int(el))
    return int_concat

  else:

    xls=upload_pandas(name,count)
    col = xls[xls.columns.tolist()[0]]
    col = col.tolist()
    int_concat=[]
    for el in col:
      if math.isnan(el):
        int_concat.append('NA')
      else:
        int_concat.append(int(el))

    all_genes=[]
    for i in range(count):
      int_list=[]
      xls=upload_pandas(name,i)
      col = xls[xls.columns.tolist()[len(xls.columns)-5]]
      col = col.tolist()
      for el in col:
        if math.isnan(el):
          int_list.append('NA')
        else:
          int_list.append(int(el))
      all_genes.append(int_list)


    lists_ = [int_concat,all_genes]

    return lists_


def add_enrichment(name,data,count):
  if count == 1:
    xls = pd.read_excel('/Users/agatorano/Code/metascape/metascape.org/media/'+name,index_col=None, na_values=['NA'])
    writer = pd.ExcelWriter('/Users/agatorano/Code/metascape/metascape.org/media/'+name)
    xls.to_excel(writer,'multiple_gene_summary',index=False)
    data.to_excel(writer,'enrichment',index=False)
  elif count == 2:
    xls = pd.read_excel('/Users/agatorano/Code/metascape/metascape.org/media/'+name,sheetname='multiple_summary',index_col=None, na_values=['NA'])
    writer = pd.ExcelWriter('/Users/agatorano/Code/metascape/metascape.org/media/'+name)
    xls.to_excel(writer,'multiple_gene_summary',index=False)
    data.to_excel(writer,'concatenated_enrichment',index=False)
  elif count == 3:
    xls = pd.read_excel('/Users/agatorano/Code/metascape/metascape.org/media/'+name,sheetname='multiple_gene_summary',index_col=None, na_values=['NA'])
    xls_ = pd.read_excel('/Users/agatorano/Code/metascape/metascape.org/media/'+name,sheetname='concatenated_enrichment',index_col=None, na_values=['NA'])
    writer = pd.ExcelWriter('/Users/agatorano/Code/metascape/metascape.org/media/'+name)
    xls.to_excel(writer,'multiple_gene_summary',index=False)
    xls_.to_excel(writer,'concatenated_enrichment',index=False)
    data.to_excel(writer,'top_10_list_enrichment',index=False)

if __name__=='__main__':
  print(get_column('documents/2015/02/04/Workbook1_iIGqQAB.xlsx'))
