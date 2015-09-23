from django import forms
from IAV_page.models import Sess_IAV,IAV
import os

class IAVForm(forms.ModelForm):

  OPTIONS = (
    ("ALL","CONTAINS ALL YOU SELECTED"),
    ("ANY","ANY PROTEINS"),
    ("HA","HA"),
    ("NA","NA"),
    ("NP","NP"),
    ("M1","M1"),
    ("M2","M2"),
    ("NS1","NS1"),
    ("NEP","NEP"),
    ("PA","PA"),
    ("PB1","PB1"),
    ("PB2","PB2"),
    ("PB1F2","PB1F2"),
    )
  z_options= (
      (-1.645,"0.1"),
      (-1.96,"0.05"),
      (-2.575,"0.01"),
      (-3.3,"0.001"),
      )
  ['ALL','NONE','ANY','HA','NA','NP','M1','M2','NS1','NEP','PA','PB1','PB2','PB1F2']

  z_score = forms.ChoiceField(required=False,widget=forms.Select(attrs={
    "title":"Choose A Desired Significance Score Threshold",
    'type':'checkbox',
    'class':'btn btn-default dropdown-toggle',
    'value':'0.05'}),
    choices=z_options)

  screens = forms.IntegerField(widget=forms.NumberInput(attrs={
    "title":"Choose The Minimum Number Of RNAi Screens The Gene Was Found In",
    'class':'form-control',
    'value':'2',
    'min':'0',}))

  flu_proteins = forms.MultipleChoiceField(required=False,widget=forms.CheckboxSelectMultiple(attrs={
    "title":"Select Any Number Of Flu Proteins",
    'type':'checkbox'}),
    choices=OPTIONS)

  word_search = forms.CharField(required=False, widget=forms.Textarea(attrs={
    "title":"Type Any Terms Associated To Your Desired Gene",
    'class':'form-control',
    'rows':1,
    'cols':6,
    'placeholder':'Example: kinase, secreted protein, transcription factor'}))

  docfile_iav = forms.FileField(required=False, widget=forms.FileInput(attrs={
      "title":"Optional - Entering a file will join data found in our database to the right of your input data. Be warry of sparcity",
      'class':'filestyle','data-classButton':"btn btn-primary",
      'data-input':"false",'data-classIcon':"icon-plus",
      'data-buttonText':"Upload Data",}))

  def __init__(self, *args, **kwargs):
    super(IAVForm, self).__init__(*args, **kwargs)
    self.fields["word_search"].required = False


  class Meta:
    model=IAV
    fields=('z_score','screens','flu_proteins','word_search','docfile_iav')

  def clean_docfile_iav(self):
    docfile = self.cleaned_data.get('docfile_iav',False)
    print(docfile)
    name = docfile.name
    extension = os.path.splitext(name)[1]

    if extension != '.xls' and extension != '.xlsx':
      raise forms.ValidationError("only excel files allowed ")

    if docfile._size<int("27000"):
      raise forms.ValidationError("File Not Large Enough For Upload")

    return docfile

#  def save(self,for_page,z_score,screens,flu_proteins,word_search,docfile_iav):
#    self.instance.sess = for_page
#    self.instance.z_score = z_score
#    self.instance.screens = screens
#    self.instance.flu_proteins = flu_proteins
#    self.instance.word_search = word_search
#    self.instance.docfile_iav = docfile_iav
#    return super().save()

  def save(self,for_page):
    self.instance.sess = for_page
    return super().save()

class ExistingIAVForm(IAVForm):

  def __init__(self,for_page,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.instance.sess=for_page

  def save(self):
    return forms.models.ModelForm.save(self)
