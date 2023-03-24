import json
from collections import namedtuple
import io
from datetime import datetime
import gzip
from django.conf import settings
from django.views import generic
from django.http import HttpResponse, JsonResponse, HttpRequest, FileResponse, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from extraction_numbers.class_data_base import DataBase
from functools import wraps
import re
from searchnumber.views import initial_bd, ConnectionBDError, PageNav, ParagraphView
from searchnumber.models import QuestionHistory
from osa_settings.models import OSASettings
from osa_settings.forms import BaseConnectForm
from . import forms, models

SctPrsDataTuple = namedtuple('SctPrsDataTuple', ['full_name', 'paragraph', 'filepath', 'filename'])

event_list = ['search_fio', ]


def parse_event(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        error_map = {'error': 'No event', }
        try:
            data = json.loads(args[0].body)
            event = data['event']
        except (ValueError, json.JSONDecodeError):
            return JsonResponse(error_map, status=settings.DEFAULT_ERROR_STATUS)
        if event in event_list:
            kwargs['event'] = event
            kwargs['data'] = data
            response = func(*args, **kwargs)
            return response
        else:
            return JsonResponse(error_map, status=settings.DEFAULT_ERROR_STATUS)

    return wrapper


decorators = [parse_event, ]


@method_decorator(parse_event, name='post')
class SearchfioView(generic.View):
    template_name = 'searchfio/searchfio.html'
    template_search = 'searchfio/fio_view.html'

    @staticmethod
    def _selection_pers_data(full_name, paragraph, indent: int):
        new_paragraph = []
        try:
            result = re.search(f'{full_name}', paragraph, re.IGNORECASE)
        except:
            print('hello')
        if result is None:
            new_paragraph.append(ParagraphView(paragraph, '', ''))
            return new_paragraph
        result = re.finditer(f'{full_name}', paragraph, re.IGNORECASE)
        for match in result:
            if indent >= match.start():
                p_before = paragraph[:match.start()]
            else:
                p_before = paragraph[match.start() - indent:match.start()]
            target = paragraph[match.start():match.end()]
            p_after = paragraph[match.end():match.end() + indent]
            new_paragraph.append(ParagraphView(p_after, target, p_before))
        return new_paragraph

    def _get_fio_data(self, prs_data, db, page_id, limit):
        osa_settings = OSASettings.objects.all()[:1].get()
        offset = limit * (page_id - 1)
        prs_data_list, record_count = db.get_personal_data(prs_data['last_name'], prs_data['first_name'],
                                                           prs_data['patronymic'], limit, offset)
        page_nav = PageNav(page_id, record_count, 'search_fio:index', limit)
        archive_path = OSASettings.objects.values('archive_path').all()[:1].get()['archive_path']
        for person_data in prs_data_list:
            person_data.paragraph = self._selection_pers_data(person_data.full_name, person_data.paragraph,
                                                              osa_settings.indent)
            person_data.filepath = person_data.filepath.replace(settings.TRAINING_PATH, settings.MEDIA_URL)
        return prs_data_list, page_nav

    def _search_fio(self, data, request):
        search_prs_data = forms.SearchPrsDataForm(data)
        if search_prs_data.is_valid():
            osa_settings = OSASettings.objects.all()[:1].get()
            try:
                db = initial_bd(osa_settings)
            except ConnectionBDError:
                error = json.dumps({'fatal_error': 'Connection Failed'})
                return error, settings.ERROR_STATUS
            prs_data_list, page_nav = self._get_fio_data(search_prs_data.cleaned_data, db, 1,
                                                         osa_settings.records_number_on_page)
            QuestionHistory.objects.filter(user=request.user).update(fio_json=search_prs_data.cleaned_data)
            prs_data_view = render_to_string(self.template_search, context={'prs_data_list': prs_data_list})
            response = {
                'prs_data_view': prs_data_view,
                'page_nav': str(page_nav),
            }
            return response, settings.SUCCESS_STATUS
        else:
            errors = json.loads(search_prs_data.errors.as_json())
            return errors, settings.DEFAULT_ERROR_STATUS

    def get(self, request):
        page_id = request.GET.get('page_id', default=0)
        if not page_id:
            return render(request, self.template_name)
        try:
            page_id = int(page_id)
            assert page_id > 0, 'Page_id must more than zero'
        except (ValueError, AssertionError):
            return render(request, self.template_name)
        osa_setting = OSASettings.objects.all()[:1].get()
        try:
            db = initial_bd(osa_setting)
        except ConnectionBDError:
            return render(request, self.template_name)
        prs_data = QuestionHistory.objects.filter(user=request.user).values('fio_json').get()
        prs_data_list, page_nav = self._get_fio_data(prs_data['fio_json'], db, page_id,
                                                     osa_setting.records_number_on_page)

        context = {
            'prs_data_list': prs_data_list,
            'page_nav': page_nav,
        }
        return render(request, self.template_name, context)

    def post(self, request, event, data):
        if event == 'search_fio':
            response, status = self._search_fio(data, request)
            return JsonResponse(response, status=status)
        return JsonResponse({'error': 'no event'}, status=settings.ERROR_STATUS)

    pass
