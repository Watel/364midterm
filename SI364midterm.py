###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, TextAreaField, ValidationError
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
import requests
import indicoio


## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

# All app.config values
app.config['SECRET_KEY'] = 'hard to guess string'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/midterm364"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Other setup
manager = Manager(app) # In order to use manager
db = SQLAlchemy(app) # For database use



# INDICOIO REST API KEY
# https://indico.io/docs
indicoio.config.api_key = '23329f73b399978ebf52ba145b3f286c'




##################
##### MODELS #####
##################



#Model structures emulated from HW3
class Courses(db.Model):
    __tablename__ = "courses"
    studentid = db.Column(db.Integer, primary_key=True)
    major = db.Column(db.String(64))
    name = db.Column(db.String(64))
    course1 = db.Column(db.String(64))
    course2 = db.Column(db.String(64))
    child = db.relationship('Ratings', backref='course')

class Ratings(db.Model):
    __tablename__ = "ratings"
    id = db.Column(db.Integer, primary_key=True)
    studentid = db.Column(db.Integer, db.ForeignKey("courses.studentid"))
    rating1 = db.Column(db.String(64))
    comment1 = db.Column(db.String())
    rating2 = db.Column(db.String(64))
    comment2 = db.Column(db.String())
    comment1_score = db.Column(db.String(64))
    comment2_score = db.Column(db.String(64))




###################
###### FORMS ######
###################

class CourseForm(FlaskForm):
    studentid = StringField("Please enter your Student ID #:", validators=[Required()])
    major = StringField("Please enter your major:", validators=[Required(), Length(min=1)])
    name = StringField("Please enter your full name:", validators=[Required(), Length(min=1)])
    course1 = StringField("Please enter the first course you are taking (i.e. SI364):", validators=[Required(), Length(min=5)])
    course2 = StringField("Please enter the second course you are taking (i.e. SI364):", validators=[Required(), Length(min=5)])
    submit = SubmitField()

    def validate_studentid(self,field):
        if len(str(field.data)) < 8 and field.data is not int:
            raise ValidationError("Please enter 8 integers.")
        if Courses.query.filter_by(studentid=field.data).first():
            raise ValidationError("Student ID already exists!")


class RatingComments(FlaskForm):
    RATING_CHOICES = [("1","1"), ("2","2"), ("3","3"), ("4","4"), ("5","5"), ("6","6"), ("7","7"), ("8", "8"), ("9","9"), ("10","10")]
    rating1 = SelectField("please rate your overall experience in your first class (0-lowest, 10-highest)",
                          choices=RATING_CHOICES, validators=[Required()])
    comment1 = TextAreaField("please comment on your overall experience in your first class", validators=[Required()])
    rating2 = SelectField("please rate your overall experience in your second class (0-lowest, 10-highest)",
                          choices=RATING_CHOICES, validators=[Required()])
    comment2 = TextAreaField("please comment on your overall experience in your second class.", validators=[Required()])
    submit = SubmitField()

class SearchForm(FlaskForm):
    search = StringField("Please Enter a Student ID to search:", validators=[Required()])
    submit = SubmitField()


#######################
###### VIEW FXNS ######
#######################

@app.route('/')
def home():
    return redirect(url_for("course_form"))

@app.route('/about')
def about():
    return render_template("index.html")

@app.route('/course_form', methods=['GET', 'POST'])
def course_form():
    form = CourseForm()
    return render_template('course_form.html', form=form)

@app.route('/rating_form', methods=['GET', 'POST'])
def rating_form():
    form = CourseForm()
    form2 = RatingComments()

    if form.validate_on_submit():

        studentid = form.studentid.data
        major = form.major.data
        name = form.name.data
        course1 = form.course1.data
        course2 = form.course2.data
        entry = Courses(studentid=studentid, major=major, name=name, course1=course1, course2=course2)
        db.session.add(entry)
        db.session.commit()

        #https://stackoverflow.com/questions/27611216/how-to-pass-a-variable-between-flask-pages
        session['course1'] = course1
        session['course2'] = course2
        session['name'] = name
        return render_template('rating_form.html', form=form2, course1=course1, course2=course2, name=name, major=major)

    # Pulled from HW3 about flashing errors
    errors = [v for v in form.errors.values()]
    if len(errors) > 0:
        flash("!!!! ERRORS IN FORM SUBMISSION - " + str(errors))
    return redirect(url_for('course_form'))


@app.route('/display_data', methods=['GET', 'POST'])
def display_data():
    form2 = RatingComments()
    if request.method == "POST":

        #https://stackoverflow.com/questions/27611216/how-to-pass-a-variable-between-flask-pages
        course1 = session.get('course1', None)
        course2 = session.get('course2', None)
        name = session.get('name', None)

        rating1 = form2.rating1.data
        comment1 = form2.comment1.data
        rating2 = form2.rating2.data
        comment2 = form2.comment2.data

        #Query for existing student id from Courses table, to populate into Ratings table
        #Modeled from HW3
        studentid = Courses.query.filter_by(course1=course1, course2=course2, name=name).first().studentid

        #API requires quotes for submission
        c1 = '"' + comment1 + '"'
        c2 = '"' + comment2 + '"'

        #API method to get sentiment list
        #https://indico.io/docs
        probs_lst = indicoio.sentiment([c1, c2])
        c1_prob = probs_lst[0]
        c2_prob = probs_lst[1]

        #Convert 0-1 score to positive or negative
        if c1_prob > 0.5:
            c1_tag = "positively"
        else:
            c1_tag = "negatively"

        if c2_prob > 0.5:
            c2_tag = "positively"
        else:
            c2_tag = "negatively"

        #Ratings table add, commit data,
        entry = Ratings(studentid=studentid, rating1=rating1, rating2=rating2, comment1=comment1,
                        comment2=comment2, comment1_score=c1_prob, comment2_score=c2_prob)
        db.session.add(entry)
        db.session.commit()

        return render_template("display_data.html", course1=course1, course2=course2, c1_tag=c1_tag, c2_tag=c2_tag, c1_prob=c1_prob, c2_prob=c2_prob)


@app.route('/unique_majors')
def unique_majors():
    major_set = set()

    #Query for all majors, add into set
    #Pulled from HW3
    for major in Courses.query.all():
        major_set.add(major.major)

    #Set should return unique majors, convert to list
    major_lst = list(major_set)

    #Make a dictionary of counts for each major using .count()
    #https://stackoverflow.com/questions/25605410/count-the-number-of-rows-with-a-condition-with-sqlalchemy
    #Pulled from HW3
    major_counts = dict()
    for major in major_lst:
        major_student_lst = Courses.query.filter_by(major=major).all()
        maj_sum = 0
        for student in major_student_lst:
            r1 = Ratings.query.filter_by(studentid = student.studentid).first().rating1
            r2 = Ratings.query.filter_by(studentid = student.studentid).first().rating2
            max_rating = max(int(r1), int(r2))
            maj_sum += max_rating
        maj_avg = maj_sum / (len(major_student_lst))

        major_counts[major] = (Courses.query.filter_by(major=major).count(), maj_avg)


    #Sort dictionary using lambda function, by descending order
    #https://stackoverflow.com/questions/3121979/how-to-sort-list-tuple-of-lists-tuples
    d = sorted(major_counts.items(), key=lambda x: x[1][1], reverse=True)

    return render_template('unique_majors.html', majors=d)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form3 = SearchForm()

    return render_template("search.html", form=form3)


@app.route('/search_results', methods=['GET', 'POST'])
def search_results():
    form3 = SearchForm()
    if request.method == "GET":

        studentid = request.args.get('search')
        try:
            name = Courses.query.filter_by(studentid=studentid).first().name
            major = Courses.query.filter_by(studentid=studentid).first().major
            course1 = Courses.query.filter_by(studentid=studentid).first().course1
            course2 = Courses.query.filter_by(studentid=studentid).first().course2
            r1 = Ratings.query.filter_by(studentid=studentid).first().rating1
            r2 = Ratings.query.filter_by(studentid=studentid).first().rating2
        except:
            return render_template("search_results_none.html")


        return render_template("search_results.html", name=name, major=major, course1=course1, course2=course2, r1=r1, r2=r2)


##Error handling route - 404
#Pulled from HW3
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

##Error handling route - 500
#Pulled from HW3
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    db.create_all()
    app.run(use_reloader=True,debug=True)

