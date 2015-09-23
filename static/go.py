#!/usr/bin/env python
import numpy as np
import pandas as pd
import re
import os
from scipy.stats import hypergeom

TO_LOG10 = 2.302585092994046 # Divide by this value to change base e to base 10

class GO(object):

    SPECIES = {
        'human': 9606,
    }
    GO_ROOT={"BP":"GO:0008150","MF":"GO:0003674","CC":"GO:0005575"}
    GO_DESCRIPTION={"BP":"Biological Process","MF":"Molecular Function","CC":"Cellular Component"}
    HOMEDIR="/depts/ChemInfo/GO/HS2012/"
    N_TRIVIAL=1000;

    def __init__(self, DIR='', entrez=None, taxID=None, user_go = None):
        DIR=DIR or GO.HOMEDIR
                
        if user_go is not None:
            if os.path.isfile(user_go):
              t=pd.read_csv(user_go, sep='\t')
        elif os.path.isfile(DIR+"AllAnnotations.tsv"):
            t=pd.read_csv(DIR+"AllAnnotations.tsv", sep='\t')
        else:
            print ('No GO Annotations available.')
        
        self.GO_GENE={}
        self.GO_DESCRIPTION={}
        self.GO_TYPE={}
        # self.eg=entrez or ez.EntrezGene()
        # taxID=taxID or self.eg.C_TAX_ID['human']
        # self.eg.load_db()
        n=len(t)
        self.ALL_GENE=set()
        for i in range(n):
            s_go=t.GO[i]
            s_type=t.TYPE[i]
            s_des=t.DESCRIPTION[i]
            S_genes=t.GENES[i].split(",")          
            # S_genes=[s for s in S_genes if self.eg.C_SPECIES[s]==taxID ]
            if len(S_genes)>GO.N_TRIVIAL or len(S_genes)==0: continue
            self.GO_DESCRIPTION[s_go]=s_des or s_go
            if pd.isnull(s_des): #yzhong 03242014 
                self.GO_DESCRIPTION[s_go]=s_go #yzhong 03242014
            self.GO_TYPE[s_go]=s_type
            self.GO_GENE[s_go]=set(S_genes)
            self.ALL_GENE.update(self.GO_GENE[s_go])

    def go_description(self, s_go):
        if s_go in self.GO_DESCRIPTION:
            return self.GO_DESCRIPTION[s_go]
        return s_go

    def filter_genes_by_go(self, s_go, S_genes):
        if s_go in self.GO_GENE:
            return list(set(S_genes).intersection(self.GO_GENE[s_go]))
        else:
            return []

    def go_size(self, s_go):
        S_gene=self.GO_GENE[s_go]
        return len(S_gene)

    def analysis_go(self, s_go, S_hit, N_total=0, SRC_GENE=None, min_overlap=3):
        c={'GO':s_go, '#TotalGeneInLibrary':N_total, '#GeneInGO':0, '#GeneInHitList':0, '#GeneInGOAndHitList':0, 'LogP':0.0, 'Enrichment':0}
        #if SRC_GENE is not None:
        #    print "SRC_GENE: "+str(len(SRC_GENE))
        S_gene=self.GO_GENE[s_go]
        if not N_total:
            N_total=len(self.ALL_GENE)
        if SRC_GENE is not None:
            S_gene=S_gene.intersection(SRC_GENE)
            S_hit=set(S_hit).intersection(SRC_GENE)
        else:
            S_hit=set(S_hit)
        c['#GeneInGO']=len(S_gene)
        c['#GeneInHitList']=len(S_hit)
        if c['#GeneInGO']<min_overlap or c['#GeneInHitList']<min_overlap:
            return None
        S_both=S_gene.intersection(S_hit)
        c['#GeneInGOAndHitList']=len(S_both)
        if c['#GeneInGOAndHitList']<min_overlap:
            return None
        c['%InGO']=c['#GeneInGOAndHitList']*100.0/c['#GeneInHitList']
        q=min(max(c['%InGO']/100, 1.0/c['#GeneInHitList']), 1-1.0/c['#GeneInHitList'])
        c['STDV %InGO']=np.sqrt(q*(1-q)/c['#GeneInHitList'])*100
        c['Enrichment']=c['%InGO']/100.0*N_total/c['#GeneInGO']
        S=[int(x) for x in S_both]
        S.sort()
        c['GeneID']='|'.join([str(x) for x in S])
        if c['#GeneInGOAndHitList']<min_overlap: return c
        c['LogP'] = hypergeom.logsf(c['#GeneInGOAndHitList']-1, N_total, c['#GeneInGO'], c['#GeneInHitList'])
        c['LogP'] = c['LogP'] / TO_LOG10
        return c

    def analysis(self, S_hit, S_go=None, SRC_GENE=None, min_overlap=3, min_enrichment=0, p_cutoff=0.01):
        rslt=[]
        if S_go is None:
            S_go=self.GO_GENE.keys()
        if SRC_GENE is not None:
            if type(SRC_GENE) is list:
                SRC_GENE=set(SRC_GENE)
            N_total=len(self.ALL_GENE.intersection(SRC_GENE))
        else:
            N_total=len(self.ALL_GENE)
        # self.eg.load_db()
        for s_go in S_go:
            if s_go not in self.GO_GENE: continue
            c=self.analysis_go(s_go, S_hit, N_total, SRC_GENE=SRC_GENE, min_overlap=min_overlap)
            if c is None:
                continue
            if min_enrichment>0 and c['Enrichment']<min_enrichment: continue
            if p_cutoff<1 and 10**c['LogP']>p_cutoff: continue
            c['Description']="("+self.GO_TYPE[s_go]+") "+self.go_description(s_go)
            S_gene=c['GeneID'].split('|')
            # S_symbol=[self.eg.C_GENENEW[x] if x in self.eg.C_GENENEW else x for x in S_gene]
            S_symbol=['X']
            c['Hits']='|'.join(S_symbol)
            rslt.append(c)
        if len(rslt):
            t=pd.DataFrame(rslt)
            t=t.sort_index(by=['LogP','Enrichment','#GeneInGOAndHitList'], ascending=[True,False,False])
            t=t.reindex(columns=['GO','Description','LogP','Enrichment','#TotalGeneInLibrary',
                '#GeneInGO','#GeneInHitList','#GeneInGOAndHitList','%InGO','STDV %InGO','GeneID','Hits'])
            return t
        else:
            return None

def main():
  go=GO(DIR='/Users/agatorano/Code/metascape/metascape.org/static/')
  print(go)
  S_hit=['26526', '7105', '7102', '23555']
  t_go=go.analysis(S_hit=S_hit)
  print (t_go)

if __name__=="__main__":
  main()
