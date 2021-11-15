Flask-MathDown
==============

[![Build status](https://github.com/beckni/Flask-MathDown/workflows/build/badge.svg)](https://github.com/beckni/Flask-MathDown/actions)

Implementation of StackOverflow's "PageDown" markdown editor with MathJax support for Flask and Flask-WTF.

What are PageDown and MathJax?
-----------------

[PageDown](https://code.google.com/p/PageDown/wiki/PageDown) is the JavaScript [Markdown](http://daringfireball.net/projects/markdown/) editor used on [Stack Overflow](http://stackoverflow.com/) and all the other question and answer sites in the [Stack Exchange network](http://stackexchange.com/).

[MathJax](https://www.mathjax.org) is a JavaScript display engine for mathematics that is used on [math.stackexchange](https://math.stackexchange.com).

Flask-MathDown provides a `MathDownField` class that extends [Flask-WTF](https://flask-wtf.readthedocs.org/en/latest/) with a specialized text area field that renders an HTML preview of the Markdown and math text on the fly as you type.

Installation
------------

    $ pip install flask-MathDown

Example
-------

The extension needs to be initialized in the usual way before it can be used:

    from flask_MathDown import MathDown
    
    app = Flask(__name__)
    MathDown = MathDown(app)
	
Static markdown text including math formulas can be rendered on the client side by calling `MathDown.include_mathdown()` in the template and 
adding the class `markdown` to the div containing the text.

	<html>
	<head>
	{{ mathdown.include_mathdown() }}
	</head>
	<body>
		<div class = "markdown">
			# Markdown example
			
			This text will be rendered on the client side including *math* like $f(x) = x^2$.
		</div>
	</body>
	</html>

To display an editor with a button bar and a preview window, create a form deriving from Flask-WTF's FlaskForm:

	from flask_wtf import FlaskForm
	from flask_mathdown import MathDown
	from flask_mathdown.fields import MathDownField
	from wtforms.fields import SubmitField
	
	class MathDownFormExample(FlaskForm):
		mathdown = MathDownField('Enter your markdown')
		submit = SubmitField('Submit')
		
The `MathDownField` works exactly like a `TextAreaField` (in fact it is a subclass of it). The handling in view functions is identical. For example:

    @app.route('/', methods = ['GET', 'POST'])
    def index():
        form = MathDownFormExample()
        if form.validate_on_submit():
            text = form.mathdown.data
            # do something interesting with the Markdown text
        return render_template('index.html', form = form)		
		
Finally, the template needs the support Javascript code added, by calling `mathdown.include_mathdown_editor()` somewhere in the page:

    <html>
    <head>
    {{ mathdown.include_mathdown_editor() }}
    </head>
    <body>
        <form method="POST">
            {{ form.hidden_tag() }}
            {{ form.mathdown(rows=10) }}
            {{ form.submit }}
        </form>
    </body>
    </html>		

To help adding specific CSS styling the `<textarea>` element has class `flask-mathdown-input` and the preview `<div>` has class `flask-mathdown-preview`.

With the template above, the preview area is created by the extension right below the input text area. For greater control, it is also possible to render the input and preview areas on different parts of the page. The following example shows how to render the preview area above the input area:

    <html>
    <head>
    {{ mathdown.include_mathdown_editor() }}
    </head>
    <body>
        <form method="POST">
            {{ form.mathdown(only_preview=True) }}
            {{ form.mathdown(only_input=True, rows=10) }}
            {{ form.submit }}
        </form>
    </body>
    </html>

Note that in all cases the submitted text will be the raw Markdown text. The rendered HTML is only used for the preview, if you need to render to HTML in the server then use a server side Markdown renderer like [Flask-Markdown](http://pythonhosted.org/Flask-Markdown/).



