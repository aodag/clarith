from formalchemy import FieldSet
from clarith.sqla import DBSession

__author__ = 'aodag'


class FormView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def fieldset(self):
        fs = FieldSet(self.model, data=self.request.POST, session=DBSession)
        self.configure(fs)
        return fs

    def __call__(self):
        fs = self.fieldset()
        if self.request.POST and fs.validate():
            values = fs.to_dict(with_prefix=False)
            result = self.validated(values)
            if result is not None:
                return result
        values = dict(fs=fs)
        self.template_values(values)
        return values

    def configure(self, fs):
        pass

    def validated(self, values):
        pass

    def template_values(self, values):
        pass