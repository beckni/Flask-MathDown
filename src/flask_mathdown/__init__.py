from markupsafe import Markup
from flask import Blueprint, current_app, url_for


class _mathdown(object):
    def include_mathdown(self):
        html = Markup(''' <script type="text/x-mathjax-config">
	MathJax.Hub.Config({"HTML-CSS": { preferredFont: "TeX", availableFonts: ["STIX","TeX"], linebreaks: { automatic:true }, EqnChunk: (MathJax.Hub.Browser.isMobile ? 10 : 50) },
		tex2jax: { inlineMath: [ ["$", "$"], ["\\\\(","\\\\)"] ], displayMath: [ ["$$","$$"], ["\\[", "\\]"] ], processEscapes: true, ignoreClass: "tex2jax_ignore|dno" },
 });
 </script>
 <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-AMS_HTML-full"></script>
 <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/pagedown/1.0/Markdown.Converter.min.js"></script>
 <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/pagedown/1.0/Markdown.Sanitizer.min.js"></script>
 <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/pagedown/1.0/Markdown.Editor.min.js"></script>
''')  # noqa: E501
        html += Markup(' <link rel="stylesheet" type="text/css" href="' + url_for('mathdown.static', filename='wmd.css') + '"></style>\n')
        html += Markup(' <script src="' + url_for('mathdown.static', filename='mathjax-editing.js') + '"></script>\n')
        return html
    
    def html_head(self):
        return self.include_pagedown()
        

class MathDown(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['mathdown'] = _mathdown()
        app.context_processor(self.context_processor)
        blueprint = Blueprint(
            'mathdown',
            __name__,
            template_folder = 'templates',
            static_folder = 'static',
            static_url_path = app.static_url_path + '/mathdown')
            
        app.register_blueprint(blueprint)

    @staticmethod
    def context_processor():
        return {'mathdown': current_app.extensions['mathdown']}
