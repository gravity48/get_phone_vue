from celery import shared_task
from get_phone_view.celery import app
from extraction_numbers.DocHeandler import DocHandler, ProjectsInit
from .models import ProjectSettings, ENTITY_PROJ, RETRAINING_PROJ


@app.task
def launch_entity_proj(kwargs: dict):
    ProjectSettings.objects.filter(proj_type=ENTITY_PROJ).update(is_run=True)
    check_processed_file = kwargs.pop('check_processed_file')
    sync_proj = kwargs.pop('sync_proj')
    proj_init = ProjectsInit(**kwargs)
    proj_init.run_entity_with_celery(check_processed_file, sync_proj)
    ProjectSettings.objects.filter(proj_type=ENTITY_PROJ).update(is_run=False)


@app.task
def launch_retrain_proj(kwargs: dict):
    ProjectSettings.objects.filter(proj_type=RETRAINING_PROJ).update(is_run=True)
    doc_id = kwargs.pop('doc_id')
    delete_non_existent = kwargs.pop('delete_non_existent')
    proj_init = ProjectsInit(**kwargs)
    proj_init.run_retrain_proj(doc_id, delete_non_existent)
    ProjectSettings.objects.filter(proj_type=RETRAINING_PROJ).update(is_run=False)

