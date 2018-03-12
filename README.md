# Introduction
Hi there, this is my SI364 Midterm Assignment.  In a nutshell, it allows students to enter in their basic profile information, then asks them for two courses for them to rate and comment on.  This app then makes a REST API call to determine the sentiment (pos/neg) of each comment!  I also add in the ability to list all the unique majors and their average rating score, as well as the ability to return results for one specific student id.

# Code Checklist:

**1. Ensure that the SI364midterm.py file has all the setup (app.config values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on http://localhost:5000 (and the other routes you set up)**

**2. Add navigation in base.html with links (using a href tags) that lead to every other viewable page in the application. (e.g. in the lecture examples from the Feb 9 lecture, like this )**

**3. Ensure that all templates in the application inherit (using template inheritance, with extends) from base.html and include at least one additional block.**

**4. Include at least 2 additional template .html files we did not provide.**

**5. At least one additional template with a Jinja template for loop and at least one additional template with a Jinja template conditional. These could be in the same template, and could be 1 of the 2 additional template files.**

**6. At least one errorhandler for a 404 error and a corresponding template.**

**7. At least one request to a REST API that is based on data submitted in a WTForm.**

**8. At least one additional (not provided) WTForm that sends data with a GET request to a new page.**

9. At least one additional (not provided) WTForm that sends data with a POST request to the same page.

*I was unable to create a WTForm that sent data through a POST request to the same page.  I struggled to find from lecture/discussion examples on how to implement this, as POSTing to the same page wasn't all too common.  If possible, could we get a refresher on how this works? Much appreciated!*

**10. At least one custom validator for a field in a WTForm.**

**11. At least 2 additional model classes.**

**12. Have a one:many relationship that works properly built between 2 of your models.**

**13. Successfully save data to each table.**

**14. Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for).**

**15. Query data using an .all() method in at least one view function and send the results of that query to a template.**

**16. Include at least one use of redirect. (HINT: This should probably happen in the view function where data is posted...)**

**17. Include at least one use of url_for. (HINT: This could happen where you render a form...)**

**18. Have at least 3 view functions that are not included with the code we have provided. (But you may have more! Make sure you include ALL view functions in the app in the documentation and ALL pages in the app in the navigation links of base.html.)**

# Routes -> Templates
1. `/` leads to `course_form.html`
2. `about` leads to `index.html`
3. `course_form` leads to `course_form.html`
4. `rating_form` leads to `rating_form.html` or back to `course_form.html` if validation fails
5. `display_data` leads to `display_data.html`
6. `unique_majors` leads to `unique_majors.html`
7. `search` leads to `search.html`
8. `search_results` leads to `search_results.html`

