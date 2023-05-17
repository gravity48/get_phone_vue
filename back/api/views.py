import copy
import os
import re
import typing

from django.conf import settings
from django.contrib.auth.models import User

from api.models import SettingsModel
from api.serializers import (
    MyTokenObtainPairSerializer,
    UserSerializer,
    DataBaseSettingsSerializer,
    DataBaseSettingsUpdateSerializer,
    DocExtensionsSerializer,
    DocStatusSerializer,
    ProjectSettingsSerializer,
    ProjectSettingsUpdateSerializer,
    PhoneViewSerializer,
    FolderSerializer,
)
from index.models import UserRequestsList
from collections import OrderedDict
from django.db.models import Count
from rest_framework import viewsets, permissions, status, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from api import models


# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            self.queryset.get(pk=pk).delete()
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DataBaseViewSet(generics.RetrieveUpdateAPIView):
    serializer_class = DataBaseSettingsSerializer

    def get_object(self):
        return SettingsModel.objects.get(pk=1)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DataBaseSettingsUpdateSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExtensionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.DocExtensionModel.objects.all()
    serializer_class = DocExtensionsSerializer


class DocStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.DocStatusModel.objects.filter(id__lte=500).all()
    serializer_class = DocStatusSerializer


class ProjectSettingsView(generics.RetrieveUpdateAPIView):
    serializer_class = ProjectSettingsSerializer

    def get_object(self):
        return models.ProjectsSettings.objects.get(proj_type=self.request.GET['proj'])

    def partial_update(self, request, *args, **kwargs):
        serializer = ProjectSettingsUpdateSerializer(
            self.get_object(), data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        serializer = ProjectSettingsUpdateSerializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectSettingListView(viewsets.ModelViewSet):
    serializer_class = ProjectSettingsSerializer
    queryset = models.ProjectsSettings.objects.all().order_by('id')

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None, *args, **kwargs):
        serializer = ProjectSettingsUpdateSerializer(self.get_object(), request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectStartView(APIView):
    def post(self, request):
        """
        try:
            action_ = request.data.pop('action')
            db_ = DataBaseSettingsSerializer(SettingsModel.objects.get(pk=1))
        except Exception as e:
            e = repr(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        if action_ == 'start_proj':
            data = WebSocketClient().start_project(request.data, db_.data)
            ProjectsSettings.objects.filter(pk=request.data['id']).update(is_start=True)
            return Response(data, status=status.HTTP_200_OK)
        if action_ == 'stop_proj':
            data = WebSocketClient().stop_proj(request.data)
            ProjectsSettings.objects.filter(pk=request.data['id']).update(is_start=False)
            return Response(data, status=status.HTTP_200_OK)
        if action_ == 'status_proj':
            data = WebSocketClient().status_proj(request.data)
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        """


class PhonesView(APIView):
    serializer_class = PhoneViewSerializer

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
                        p_before = paragraph[: match.start()]
                    else:
                        p_before = paragraph[match.start() - indent : match.start()]
                    target = paragraph[match.start() : match.end()]
                    p_after = paragraph[match.end() : match.end() + indent]
                    paragraph_view = OrderedDict(
                        {'p_after': p_after, 'target': target, 'p_before': p_before}
                    )
                    if paragraph_view not in new_paragraph:
                        new_paragraph.append(paragraph_view)
        return new_paragraph

    def _render_numbers(self, serializer_data):
        """
        result = []
        regex_list = []
        for regex_numbers in regex_numbers_str:
            regex_list.append(re.compile(regex_numbers))
        for _ in serializer_data:
            dict_ = OrderedDict(
                {
                    'number': _['number'],
                    'paragraph': self._selection_numbers(
                        regex_list, _['paragraph'], _['number'], 30
                    ),
                    'filename': _['filename'],
                    'filepath': _['filepath'].replace(settings.TRAINING_PATH, settings.MEDIA_URL),
                    'doc_date': _['doc_date'],
                }
            )
            result.append(dict_)
        return result
        """

    @staticmethod
    def get_numbers(filter_):
        return (
            models.TelephonesModel.objects.values('number')
            .filter(number_integer__in=filter_)
            .annotate(dcount=Count('number'))
            .order_by()
        )

    @staticmethod
    def get_queryset_number(number, page_id):
        queryset = (
            models.TelephonesModel.objects.all()
            .values(
                'number',
                'paragraph__text',
                'paragraph__doc__filepath',
                'paragraph__doc__filename',
                'paragraph__doc__date',
            )
            .filter(number_integer=int(number))
            .order_by('-paragraph__doc__date')
        )
        count_ = queryset.count()
        limit_ = page_id * 5 - 5
        offset = limit_ + 5
        if count_ % 5:
            count_ = count_ // 5 + 1
        else:
            count_ = count_ / 5
        return queryset[limit_:offset], count_

    def _filter2phones(self, filter_, query_params=None):
        phones = OrderedDict()
        numbers = self.get_numbers(filter_)
        for number in numbers:
            current_page = 1
            if query_params is not None:
                current_page = query_params.get(number['number'], 1)
            queryset, count_ = self.get_queryset_number(number['number'], current_page)
            serializer = self.serializer_class(queryset, many=True)
            data = self._render_numbers(serializer.data)
            phones[number['number']] = OrderedDict(
                {'data': data, 'current_page': current_page, 'max_page': count_}
            )
        return phones

    def _new_question(self, request) -> OrderedDict:
        context = OrderedDict()
        search_str = request.data['search_string']
        filter_ = request.data['validate_data']
        phones = self._filter2phones(filter_)
        user_request = UserRequestsList(
            request=search_str, validate_data=filter_, user=request.user
        )
        user_request.save()
        context['phones'] = phones
        context['response_id'] = user_request.id
        return context

    def _pagination(self, request) -> OrderedDict:
        context = OrderedDict()
        number = request.data['phone']
        page_id = request.data['page_id']
        queryset, count_ = self.get_queryset_number(number, page_id)
        serializer = self.serializer_class(queryset, many=True)
        data = self._render_numbers(serializer.data)
        context[number] = OrderedDict({'data': data, 'current_page': page_id, 'max_page': count_})
        return context

    def _previous_request(self, request) -> OrderedDict:
        context = OrderedDict()
        query_params: dict = copy.deepcopy(request.data)
        request_id = query_params.pop('request_id')
        user_request = UserRequestsList.objects.get(pk=request_id)
        filter_ = user_request.validate_data
        phones = self._filter2phones(filter_, query_params)
        context['search_string'] = user_request.request
        context['phones'] = phones
        context['response_id'] = user_request.id
        return context

    def post(self, request):
        action_ = request.GET['action']
        if action_ == 'new_question':
            context = self._new_question(request)
            return Response(context, status=status.HTTP_200_OK)
        if action_ == 'pagination':
            context = self._pagination(request)
            return Response(context, status=status.HTTP_200_OK)
        if action_ == 'previous_request':
            context = self._previous_request(request)
            return Response(context, status=status.HTTP_200_OK)


class DirectoriesView(APIView):
    @staticmethod
    def _get_sub_directory(directory) -> typing.List[FolderSerializer]:
        return [
            FolderSerializer(f.name, f.path + '/', None)
            for f in os.scandir(directory)
            if f.is_dir()
        ]

    @staticmethod
    def get_root_directory():
        serializer = FolderSerializer('mnt', settings.TRAINING_PATH, None)
        return [
            serializer._asdict(),
        ]

    def _get_sub_dir_action(self, request):
        folder = request.data['folder']
        directory_list = self._get_sub_directory(folder)
        serializer_data = list(map(lambda x: x._asdict(), directory_list))
        return serializer_data

    def post(self, request):
        action_ = request.GET['action']
        if action_ == 'get_sub_dir':
            data = self._get_sub_dir_action(request)
            return Response(data, status=status.HTTP_200_OK)
        if action_ == 'get_root_dir':
            data = self.get_root_directory()
            return Response(data, status=status.HTTP_200_OK)
