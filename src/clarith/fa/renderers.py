from formalchemy.fields import (
    TextAreaFieldRenderer,
)
from webhelpers2.html.tags import textarea
from .resources import richtextfield


class RichTextFieldRenderer(TextAreaFieldRenderer):
    def render(self, **kwargs):
        value = self.value and self.value or ''
        vars = dict(name=self.name, value=value)
        richtextfield.need()
        return textarea(name=self.name, content=value, id=self.name, class_='tinymceEditor', cols="80", rows="40")