import json
import io
import re
from datetime import datetime
import gzip
from collections import namedtuple
from django.conf import settings
from django.views import generic
from django.http import HttpResponse, JsonResponse, HttpRequest, FileResponse, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from extraction_numbers.class_data_base import DataBase
from extraction_numbers.re_named_entities import regex_numbers_str
from osa_settings.models import OSASettings
from osa_settings.forms import BaseConnectForm
from . import forms, models

ParagraphView = namedtuple('ParagraphView', ['p_after', 'target', 'p_before'])


def check_bd_connection(osa_settings):
    base_connection_map = {
        'server_ip': f'{osa_settings.server_name}/{osa_settings.port}',
        'database_name': osa_settings.path2base
    }
    base_form = BaseConnectForm(base_connection_map)
    if base_form.is_valid():
        return True
    else:
        return False


def initial_bd(osa_settings):
    if not check_bd_connection(osa_settings):
        raise ConnectionBDError('ConnectionBDError', 'Connection Failed')
    init_map = {
        'path2db': osa_settings.path2base,
        'server_ip': osa_settings.server_name,
        'port': osa_settings.port,
    }
    db = DataBase(**init_map)
    return db


class ConnectionBDError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    pass


class PageNav:
    template_name = 'index/pagination.html'

    def __init__(self, page_id: int, records_count: int, url: str, segment, numbers_of_page: int = 5):
        self.page_id: int = page_id
        self.records_count: int = records_count
        self.url: str = url
        self.segment: int = segment
        self.numbers_of_page: int = numbers_of_page
        self.__generate_array()

    def __generate_array(self):
        remain = self.records_count % self.segment
        if remain == 0:
            self.last_page: int = int(self.records_count / self.segment)
        else:
            self.last_page: int = int(self.records_count / self.segment) + 1
        page_sum = self.page_id + self.numbers_of_page
        if page_sum >= self.last_page:
            self.array = list(range(self.page_id, self.last_page, 1))
        else:
            self.array = list(range(self.page_id, self.page_id + self.numbers_of_page))
        if self.page_id != 1 and len(self.array):
            self.array.insert(0, 1)
        if self.page_id == self.last_page and self.page_id != 1:
            self.array.insert(0, 1)
        self.array.append(self.last_page)

    def __str__(self):
        return render_to_string(self.template_name, {'navigation': self})


class SearchNumbersView(generic.View):
    template_name = 'searchnumber/show_numbers.html'
    phone_view_template = 'searchnumber/phone_view.html'

    @staticmethod
    def _selection_numbers(regex_list_phone: list, paragraph, phone, indent):
        new_paragraph = []
        for regex in regex_list_phone:
            result = regex.finditer(paragraph)
            for match in result:
                number = match.group('phone')
                number_clear = re.sub(r'\D', '', number)
                if number_clear == phone:
                    if indent >= match.start():
                        p_before = paragraph[:match.start()]
                    else:
                        p_before = paragraph[match.start() - indent:match.start()]
                    target = paragraph[match.start():match.end()]
                    p_after = paragraph[match.end():match.end() + indent]
                    paragraph_view = ParagraphView(p_after, target, p_before)
                    if paragraph_view not in new_paragraph:
                        new_paragraph.append(ParagraphView(p_after, target, p_before))
        return new_paragraph

    def _download_file(self, request: HttpRequest):
        file_form = forms.FileForm(request.POST, request.FILES)
        if file_form.is_valid():
            numbers_list = file_form.cleaned_data['numbers_list']
            osa_settings = OSASettings.objects.all()[:1].get()
            try:
                db = initial_bd(osa_settings)
            except ConnectionBDError:
                error = json.dumps({'fatal_error': 'Connection Failed'})
                return error, settings.ERROR_STATUS
            records_number_on_page = osa_settings.records_number_on_page
            phone_render_context, page_nav = self.__render_numbers_view(numbers_list, 1, records_number_on_page, db)
            phone_render = render_to_string(self.phone_view_template, phone_render_context)
            response = {
                'phone_render': phone_render,
                'page_nav': str(page_nav),
            }
            response = json.dumps(response)
            models.QuestionHistory.objects.filter(user=request.user).update(numbers_json=numbers_list)
            return response, settings.SUCCESS_STATUS
        else:
            errors = json.loads(file_form.errors.as_json())
            return errors, settings.ERROR_STATUS

    def __render_numbers_view(self, phone_view_list, page_id, records_number_on_page, db):
        offset = records_number_on_page * (page_id - 1)
        osa_settings = OSASettings.objects.all()[:1].get()
        phone_view_list, record_count = db.retrieving_numbers_information_integer(
            phone_view_list,
            records_number_on_page, offset)
        regex_list_phone = []
        for regex_numbers in regex_numbers_str:
            regex_list_phone.append(re.compile(regex_numbers))
        for phone_view in phone_view_list:
            phone_view.paragraph = self._selection_numbers(regex_list_phone, phone_view.paragraph, phone_view.phone,
                                                           osa_settings.indent)
            phone_view.filepath = phone_view.filepath.replace(settings.TRAINING_PATH, settings.MEDIA_URL)
        page_nav = PageNav(page_id, record_count, 'search_numbers:index', records_number_on_page)
        phone_render_context = {
            'phone_view_list': phone_view_list,
            'page_nav': page_nav,
        }
        return phone_render_context, page_nav

    def _search_number(self, request: HttpRequest):
        search_numbers_form = forms.SearchNumbersForm(request.POST)
        if search_numbers_form.is_valid():
            osa_settings = OSASettings.objects.all()[:1].get()
            try:
                db = initial_bd(osa_settings)
            except ConnectionBDError:
                error = json.dumps({'fatal_error': 'Connection Failed'})
                return error, settings.ERROR_STATUS
            records_number_on_page = osa_settings.records_number_on_page
            phone_view_list = [int(search_numbers_form.cleaned_data['search_string']), ]
            phone_render_context, page_nav = self.__render_numbers_view(phone_view_list, 1, records_number_on_page, db)
            phone_render = render_to_string(self.phone_view_template, phone_render_context)
            response = {
                'phone_render': phone_render,
                'page_nav': str(page_nav),
            }
            response = json.dumps(response)
            models.QuestionHistory.objects.filter(user=request.user).update(
                numbers_json=[int(search_numbers_form.cleaned_data['search_string']), ])
            return response, settings.SUCCESS_STATUS
        else:
            errors = json.loads(search_numbers_form.errors.as_json())
            return errors, settings.ERROR_STATUS

    def get(self, request: HttpRequest):
        page_id = request.GET.get('page_id', default=0)
        if not page_id:
            return render(request, self.template_name)
        try:
            page_id = int(page_id)
            assert page_id > 0, 'Page_id must more than zero'
        except (ValueError, AssertionError):
            return render(request, self.template_name)
        osa_setting = OSASettings.objects.all()[:1].get()
        query_dict = models.QuestionHistory.objects.filter(user=request.user).values('numbers_json').get()
        try:
            db = initial_bd(osa_setting)
        except ConnectionBDError:
            return render(request, self.template_name)
        phone_view_context, page_nav = self.__render_numbers_view(query_dict['numbers_json'], page_id,
                                                                  osa_setting.records_number_on_page, db)
        return render(request, self.template_name, phone_view_context)

    def post(self, request):
        try:
            event = request.POST['event']
        except KeyError:
            return HttpResponse({'error': 'No event'}, status=settings.ERROR_STATUS)
        if event == 'search_number':
            response, status = self._search_number(request)
            if status == settings.ERROR_STATUS:
                return JsonResponse(response, status=status)
            else:
                return HttpResponse(response, status=status)
        if event == 'download_file':
            response, status = self._download_file(request)
            if status == settings.ERROR_STATUS:
                return JsonResponse(response, status=status)
            else:
                return HttpResponse(response, status=status)


class DownloadExcelView(generic.View):

    def get(self, request):
        osa_setting = OSASettings.objects.all()[:1].get()
        query_dict = models.QuestionHistory.objects.filter(user=request.user).values('numbers_json').order_by(
            'id').last()
        try:
            db = initial_bd(osa_setting)
        except ConnectionBDError:
            return HttpResponse('Connection not found', status=settings.ERROR_STATUS)
        phone_view_list, phone_count = db.retrieving_numbers_information_integer(query_dict['numbers_json'], None, 0)
        f = io.BytesIO()
        for phone, paragraph, filename, filepath in phone_view_list:
            row_string = f'{phone}, """{paragraph}""", {filename}, {filepath}\n'
            f.write(row_string.encode('cp1251'))
        f.seek(0)
        return FileResponse(f, filename=f'{datetime.now().strftime("%d-%m-%Y %H:%M")}.csv', as_attachment=True)
