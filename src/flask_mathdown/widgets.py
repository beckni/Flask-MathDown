from wtforms.widgets import TextArea
from markupsafe import Markup

mathdown_pre_html = '<div class="flask-mathdown"><div id="wmd-button-bar-%(field)s"></div>'
mathdown_post_html = '</div>'
preview_html = '''
<div class="flask-mathdown-preview" id="wmd-preview-%(field)s"></div>
 <script type="text/javascript">
    window.addEventListener("load", function () {
        var converter = new Markdown.Converter()
        var editor = new Markdown.Editor(converter, "-%(field)s");
        var mathjaxEditing = createMathjaxEditing();
        mathjaxEditing.prepareWmdForMathJax(editor, "-%(field)s", [['$']])
        editor.run();
    });
</script>	
'''  # noqa: E501


class MathDown(TextArea):
    def __call__(self, field, **kwargs):
        show_input = True
        show_preview = True
        if 'only_input' in kwargs or 'only_preview' in kwargs:
            show_input = kwargs.pop('only_input', False)
            show_preview = kwargs.pop('only_preview', False)
        if not show_input and not show_preview:
            raise ValueError('One of show_input and show_preview must be true')
        html = Markup('')
        if show_input:
            class_ = kwargs.pop('class', '').split() + \
                kwargs.pop('class_', '').split()
            class_ += ['flask-mathdown-input']
            html += Markup(mathdown_pre_html % {'field': field.name}) + super(MathDown, self).__call__(
                field, id='wmd-input-' + field.name,
                class_=' '.join(class_), **kwargs) + Markup(mathdown_post_html)
        if show_preview:
            html += Markup(preview_html % {'field': field.name})
        return Markup(html)
