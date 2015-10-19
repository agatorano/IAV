from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/agatorano/IAV.git' 

def deploy():
  site_folder = '/home/%s/sites/IAV.org' % (env.user)
  source_folder = site_folder+'/source'
  _create_directory_structure_if_necessary(site_folder)
  _get_latest_source(site_folder)
  _update_settings(source_folder, env.host)
  _update_static_files(source_folder)
  _update_static_file_paths(source_folder)
  _update_media_file_paths(site_folder)
  _update_settings_url(source_folder)
  _update_database_login(site_folder)
  _update_database(source_folder)

def _create_directory_structure_if_necessary(site_folder):
  for subfolder in ('database', 'static','source','media'):
    run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_latest_source(source_folder):
  if exists(source_folder + '/.git'): 
    run('cd %s && git fetch' % (source_folder,)) 
  else:
    run('git clone %s %s' % (REPO_URL, source_folder))
  current_commit = local("git log -n 1 --format=%H", capture=True)
  run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _update_settings(source_folder, site_name):
  settings_path = source_folder + '/IAV/settings.py'
  sed(settings_path, "DEBUG = True", "DEBUG = False") 
  #sed(settings_path,
  #  'ALLOWED_HOSTS =.+$',
  #  'ALLOWED_HOSTS = ["%s"]' % (site_name,) 
  #)
  #  secret_key_file = source_folder + '/metascape/secret_key.py'
  #  if not exists(secret_key_file): 
  #    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
  #    key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
  #    append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
  #  append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_media_file_paths(site_folder):
  for file_ in ('excel_man.py','pandas_sql.py','IAV_process.py','add_go_IAV.py'):
    file_path = '%s/static/%s' % (site_folder,file_)
    sed(file_path,"/Users/agatorano/Code/IAV/IAV.org/media/","/home/elspeth/sites/IAV.org/media/")
  file_path = '%s/source/enrich/views.py' % (site_folder)
  sed(file_path,"/Users/agatorano/Code/IAV/IAV.org/media/","/home/elspeth/sites/IAV.org/media/")
  file_path = '%s/source/IAV/views.py' % (site_folder)
  sed(file_path,"/Users/agatorano/Code/IAV/IAV.org/media/","/home/elspeth/sites/IAV.org/media/")

def _update_database_login(site_folder):
  file_path = '%s/static/pandas_sql.py' % (site_folder)
  sed(file_path,"ag:529382Ag@localhost/","metascape:foul43-emote@localhost/")

def _update_static_file_paths(source_folder):
  file_path = '%s/uploads/views.py' % (source_folder)
  sed(file_path,"/Users/agatorano/Code/IAV/IAV.org/static","/home/elspeth/sites/IAV.org/static")
  file_path = '%s/enrich/views.py' % (source_folder)
  sed(file_path,"/Users/agatorano/Code/IAV/IAV.org/static","/home/elspeth/sites/IAV.org/static")
  file_path = '%s/IAV/views.py' % (source_folder)
  sed(file_path,"/Users/agatorano/Code/IAV/IAV.org/static","/home/elspeth/sites/IAV.org/static")
  file_path = '%s/../static/IAV_process.py' % (source_folder)
  sed(file_path,"/Users/agatorano/Code/IAV/IAV.org/static","/home/elspeth/sites/IAV.org/static")
  file_path = '%s/../static/analyze_go.py' % (source_folder)
  sed(file_path,"/Users/agatorano/Code/IAV/IAV.org/static","/home/elspeth/sites/IAV.org/static")

def _update_settings_url(source_folder):
  file_path= '%s/IAV/urls.py' % (source_folder)
  sed(file_path,"\+ static\(settings\.MEDIA_URL, document_root=settings\.MEDIA_ROOT\)","")
  
def _update_static_files(source_folder):
  run('cd %s /home/meta_user/anaconda3/envs/data_env/bin/python manage.py collectstatic --noinput' % (
    source_folder,
  ))

def _update_database(source_folder):
  run('cd %s /home/meta_user/anaconda3/envs/data_env/bin/python manage.py migrate --noinput' % (
    source_folder,
  ))
