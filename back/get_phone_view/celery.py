import os
import pika

from celery import Celery as _Celery


class Celery(_Celery):

    def get_message_count(self, queue):
        '''
        Raises: amqp.exceptions.NotFound: if queue does not exist
        '''
        with self.connection_or_acquire() as conn:
            return conn.default_channel.queue_declare(
                queue=queue, passive=True).message_count


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'get_phone_view.settings')

#app = Celery('get_phone_view', broker='amqp://user:000092@172.17.0.1:5672')

app = Celery('get_phone_view')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
