import sys
sys.path.append("/Users/agatorano/Code/metascape/metascape.org/static")

import datetime
import logging
import os

from django.http import HttpResponse
from django.shortcuts import render,render_to_response,redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from IAV_page.models import Sess_IAV,IAV
from IAV_page.forms import IAVForm, ExistingIAVForm
from IAV_process import *

import go
from viz import *

def split_list(alist, wanted_parts=1):
  length = len(alist)
  data =  [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
           for i in range(wanted_parts) ]
  new_data=[]
  for el in data:
    del el[0]
    new_data.append(el)

  return new_data

def IAV_home(request):

  return render(request,
        'IAV_page/home.html',
        {'IAVform':IAVForm()},
        )

def view_IAV(request,sess_i):

  sess_= Sess_IAV.objects.get(id=sess_i)
  form = ExistingIAVForm(for_page=sess_)

  data = IAV.objects.filter(sess_id=sess_)[0]
  file_ = data.docfile_iav.name

  iav = get_list(float(data.z_score),int(data.screens),data.flu_proteins,data.word_search,file_)
  path = iav[0]
  xls_out = iav[1]
  gene_list = iav[2]
  top10_go = iav[3]

  if len(top10_go)>0:
    count=0
    for el in top10_go['Description']:
      top10_go['Description'][count]=el.replace(',','.')
      count+=1
    count=0

    data1 = top10_go.to_csv()
    count = data1.count('\n')
    data1 = data1.replace('\n',',')
    data1 = data1.split(',')
    data1 = split_list(data1,count)
    for i  in range(len(data1)-1):
      data1[i+1][-2] = data1[i+1][-2].replace('.',',')
    data=[]

    for i in range(2):
      data.append(data1[i])
      
    now = datetime.datetime.now()
    img_path = 'img/'+now.strftime("%Y/%m/%d/img%H_%M.png")
    img = '/Users/agatorano/Code/metascape/metascape.org/media/'+img_path

    data.append(data1[-1])
    bargraph_GO(top10_go,img,'',1)


  if(len(top10_go)==0):
    no_='There are not enough genes for Enrichment'
    return render(request,
        'IAV_page/IAV.html',
        {'sess':sess_, 'IAVform':form,'path':path,'no_':no_}
        )
  else:
    #bargraph_GO(data_,img)
    return render(request,
        'IAV/IAV.html',
        #{'sess':sess_, 'IAVform':form,'path':path,'img':img_path}
        {'sess':sess_, 'IAVform':form,'path':path,'img':img_path}
        )
    

def new_IAV(request):

  if(request.method == 'POST'):
    form = IAVForm(request.POST,request.FILES)
    if form.is_valid():
      sess_ = Sess_IAV.objects.create()
      if(len(form.cleaned_data.get("flu_proteins"))==0):
        flu=['ANY']
      else:
        flu=form.cleaned_data.get("flu_proteins")
      docfile_iav = form.cleaned_data.get("docfile_iav")
      form.save(for_page=sess_)
      #IAV.objects.create(
      #    sess=sess_,
      #    z_score = request.POST.get("z_score"),
      #    screens = request.POST.get("screens"),
      #    flu_proteins = flu,
      #    word_search = request.POST.get("word_search"),
      #    docfile_iav = form.cleaned_data.get("docfile_iav")
      #    )
      return redirect(sess_)
  else:
    form = IAVForm()
  return render(request,
        'IAV_page/home.html',
        {'IAVform':form},
        )
