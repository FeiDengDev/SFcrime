from flask import Flask, render_template, request
from crime_analysis import display_result
from wtforms import Form, FloatField, validators

class InputForm(Form):
    lon = FloatField(
        label='Input Longitude', default=-122.44,
        validators=[validators.InputRequired()])
    lat = FloatField(
        label='Input Latitude', default=37.76,
        validators=[validators.InputRequired()])

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        result = display_result(form.lon.data, form.lat.data)
    else:
        result = None

    return render_template('view.html', form=form, result=result)

if __name__ == '__main__':
    app.run(debug=True)