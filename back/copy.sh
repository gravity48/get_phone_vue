#!/bin/bash
rsync -rlp --exclude '.git' --exclude 'venv' . /home/get_phone_view/
chown -R www-data:www-data /home/get_phone_view/
rm /var/run/celery/celery.pid
