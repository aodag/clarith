from pyramid.decorator import reify
from formalchemy import FieldSet
from rebecca.view import BasicView

__author__ = 'aodag'


class FormView(BasicView):

    @reify
    def fieldset(self):
        fs = FieldSet(self.model, data=self.request.POST, 
                      session=self.db_session)
        return fs

    def __call__(self):
        fs = self.fieldset
        self.configure(fs)
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


class EditFormView(FormView):
    def load_model(self):
        pass

    @reify
    def fieldset(self):
        model = self.load_model()
        fs = FieldSet(model, data=self.request.POST)
        return fs
