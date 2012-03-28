from fabric.api import env, run, sudo, put, local, get
from fabric.context_managers import prefix, cd
from fabric.contrib.files import upload_template
from fabric.contrib.project import rsync_project
from fabric.operations import reboot


RSYNC_EXCLUDE = ['*.pyc','/.hg','/.git','/.idea','/bin','/develop-eggs','eggs', 'parts','.installed.cfg', 'downloads', 'bootstrap.py','/*.egg-info']


def rsync():
    rsync_project(remote_dir='wsgiapp', local_dir=".", delete=True, extra_opts="-C", exclude=RSYNC_EXCLUDE)
    with cd('wsgiapp'):
        run('make')

def make():
    with cd('wsgiapp'):
        run('make')

def make_clean():
    with cd('wsgiapp'):
        run('make clean')


def runserver():
    with cd('wsgiapp'):
        run('./bin/gunicorn isi:main')
