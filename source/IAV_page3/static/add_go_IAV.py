import pandas as pd
import math
from go import GO

def get_column(name):
  xls=upload_pandas(name)
  col = xls[xls.columns.tolist()[len(xls.columns)-5]]
  col = col.tolist()
  int_col=[]
  for el in col:
    if math.isnan(el):
      int_col.append('NA')
    else:
      int_col.append(int(el))
  return int_col

def add_enrich_IAV(go_data,xls,name):
  xls = pd.read_excel('/Users/agatorano/Code/metascape/metascape.org/media/'+name,index_col=None, na_values=['NA'])
  writer = pd.ExcelWriter('/Users/agatorano/Code/metascape/metascape.org/media/'+name)
  xls.to_excel(writer,'process',index=False)
  data.to_excel(writer,'enrichment',index=False)

def main():
  pass

if __name__=='__main__':
  main()
