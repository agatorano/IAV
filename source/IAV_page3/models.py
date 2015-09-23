from django.db import models
from django.core.urlresolvers import reverse

class Sess_IAV(models.Model):

  def get_absolute_url(self):
    return reverse('view_IAV',args=[self.id])

class IAV(models.Model):

  z_score = models.TextField(blank=True,null=True)
  docfile_iav = models.FileField(upload_to='IAV_page/documents/%Y/%m/%d')
  screens = models.IntegerField(default=0)
  flu_proteins = models.TextField(blank=True,null=True)
  word_search = models.TextField(blank=True,null=True)
  sess = models.ForeignKey(Sess_IAV,default=None)
