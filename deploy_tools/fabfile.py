from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/rowanv/sparklines_dash.git'  # 1


def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)  # 23
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_virtualenv(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):  # 1
        run('cd %s && git fetch' % (source_folder,))  # 23
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))  # 4
    current_commit = local("git log -n 1 --format=%H", capture=True)  # 5
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))  # 6


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):  # 1
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (  # 2
        virtualenv_folder, source_folder
    ))
