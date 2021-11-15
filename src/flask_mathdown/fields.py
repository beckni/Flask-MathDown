from wtforms.fields import TextAreaField
from .widgets import MathDown


class MathDownField(TextAreaField):
    widget = MathDown()
