rsync-file:
  cmd.run:
    - name: rsync --delete -avz salt-master.curio.im:/srv/salt/prod/gandalf/dist/gandalf /tmp

kill-app:
  cmd.run:
    - name: supervisorctl stop gandalf

update-app:
  cmd.run:
    - name: rsync --delete -avz /tmp/gandalf/ /home/www/gandalf && chmod +x /home/www/gandalf && chown -R www-data:www-data /home/www/gandalf
    - user: root
    - group: root

run-app:
  cmd.run:
    - name: supervisorctl start gandalf
