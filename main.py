from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    submit = SubmitField('Submit')
    cafe_url = StringField(label='Cafe Location in URL (Google Maps URL)', validators=[URL(message="This is not a proper URL")])
    cafe_opening_time = StringField(label='Opening Time', validators=[DataRequired()])
    cafe_closing_time = StringField(label='Closing Time', validators=[DataRequired()])
    coffee_rating = SelectField(label='Coffee Rating', choices=[('☕','☕'),('☕☕','☕☕'),('☕☕☕','☕☕☕'),('☕☕☕☕','☕☕☕☕'),('☕☕☕☕☕','☕☕☕☕☕')])
    wifi_rating = SelectField(label='Wifi Strength Rating',
                                choices=[('📶', '📶'), ('📶📶', '📶📶'), ('📶📶📶', '📶📶📶'), ('📶📶📶📶', '📶📶📶📶'), ('📶📶📶📶📶', '📶📶📶📶📶')])
    power_rating = SelectField(label='Power Outlet Rating',
                                choices=[('⚡', '⚡'), ('⚡⚡', '⚡⚡'), ('⚡⚡⚡', '⚡⚡⚡'), ('⚡⚡⚡⚡', '⚡⚡⚡⚡'), ('⚡⚡⚡⚡⚡', '⚡⚡⚡⚡⚡')])


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['POST','GET'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        if request.method == "POST":
            details = [form.cafe.data, form.cafe_url.data, form.cafe_opening_time.data, form.cafe_closing_time.data,
                       form.coffee_rating.data, form.wifi_rating.data, form.power_rating.data]
            with open('cafe-data.csv', 'a', encoding='utf-8', newline='') as cd:
                writer = csv.writer(cd)
                writer.writerow(details)
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows, rows=len(list_of_rows))


if __name__ == '__main__':
    app.run(debug=True)
