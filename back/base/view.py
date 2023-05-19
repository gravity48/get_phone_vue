class PartialUpdateMixin:
    http_method_names = ['get', 'put', 'delete']

    def put(self, request, *args, **kwargs):
        return self.update(request, partial=True, *args, **kwargs)
