/home/www:
  file.directory:
    - makedirs: True
    - user: www-data
    - group: www-data

www-data:
  group.present:
    - system: True
  user.present:
    - fullname: app user
    - shell: /usr/sbin/nologin
    - home: /home/www
    - makedirs: True
    - groups:
      - www-data

python:
  pkg:
    - installed

python-dev:
  pkg:
    - installed

python-pip:
  pkg:
    - installed

python-virtualenv:
  pkg:
    - installed

pip-install:
  cmd.run:
    - name: pip install pymongo tornado requests raven pytz -i http://pypi.douban.com/simple
    - user: root

supervisor:
  pkg:
    - installed

/etc/supervisor/conf.d/gandalf.conf:
  file.managed:
    - source: salt://prod/gandalf/gandalf.conf
    - user: root
    - group: root
    - mode: '0644'

