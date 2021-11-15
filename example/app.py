from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_mathdown import MathDown
from flask_mathdown.fields import MathDownField
from wtforms.fields import SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
pagedown = MathDown(app)


class MathDownFormExample(FlaskForm):
    mathdown = MathDownField('Enter your markdown')
    mathdown2 = MathDownField('Enter your markdown')
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MathDownFormExample()
    text = None
    text2 = None
    if form.validate_on_submit():
        text = form.mathdown.data
        text2 = form.mathdown2.data
    else:
        form.mathdown.data = ('# This is demo #1 of Flask-MathDown\n'
                              '**Markdown** is rendered on the fly in the '
                              '<i>preview area below</i>!')
        form.mathdown2.data = ('# This is demo #2 of Flask-MathDown\nThe '
                               '*preview* is rendered separately from the '
                               '*input*, and in this case it is located above.')
    return render_template('index.html', form=form, text=text, text2=text2)


if __name__ == '__main__':
    app.run(debug=True)
