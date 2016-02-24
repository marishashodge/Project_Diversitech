"""Diversitech"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Company, Category, Review

import requests

app = Flask(__name__)

app.secret_key = "54312"

# StructUndefined allows for Jinja2 to raise an error when there is an undefined variable
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    companies = Company.query.filter(Company.name != 'U.S. Population',
                                     Company.name != 'average from our sample').order_by('name').all()

    us_population = Company.query.filter(Company.name == 'U.S. Population').one()

    average = Company.query.filter(Company.name == 'average from our sample').one()

    print us_population

    return render_template("home.html", companies=companies, us_population=us_population, average=average)


@app.route('/search', methods=["POST"])
def search_companies():
    """Send user to company page or 'company-not-found.html' based on search query."""

    company_searched = request.form.get("search")

    company = Company.query.filter(Company.name == company_searched).first()

    if company:
        id_of_company = company.company_id
        return redirect("/company/" + str(id_of_company))

    else:
        return render_template("company-not-found.html", company=company_searched)



@app.route('/company/<int:company_id>')
def show_company(company_id):
    """Company page with diversity details."""

    company = Company.query.get(company_id)

    categories_for_company = company.categories

    reviews = Review.query.filter(Review.company_id == company_id).all()

    return render_template("company-page.html", display_company=company, categories=categories_for_company, reviews=reviews)


################################### JSON ROUTES #######################################################


@app.route("/company-gender-tech/<int:company_id>.json")
def return_gender_tech_info(company_id):
    """Return gender diversity in technical roles."""

    categories_for_company = Category.query.filter(Category.company_id == company_id)

    average = Company.query.filter(Company.name == 'average from our sample').one()
    categories_for_average = average.categories

    for category in categories_for_average:

        if category.category == 'Female Tech':
            female_tech_percentage = category.percentage
            label_for_avg_female = 'Female - Tech: ' + str(female_tech_percentage) + '%'

        if category.category == 'Male Tech':
            male_tech_percentage = category.percentage
            label_for_avg_male = 'Male - Tech: ' + str(male_tech_percentage) + '%'


    tech_list_of_dicts = {'tech': [],
                        'average': [
                                        {
                                            "value": female_tech_percentage,
                                            "color": "#0066ff",
                                            "highlight": "#FF5A5E",
                                            "label": label_for_avg_female
                                        },

                                        {
                                            "value": male_tech_percentage,
                                            "color": "#cc00cc",
                                            "highlight": "#FF5A5E",
                                            "label": label_for_avg_male
                                        }
                                    ]}


    for category in categories_for_company:

        if category.category == 'Female Tech':
            company_female_tech = category.percentage
            label_for_tech_female = 'Female - Tech: ' + str(company_female_tech) + '%'
            tech_list_of_dicts['tech'].append({
                                            "value": company_female_tech,
                                            "color": "#ffff00",
                                            "highlight": "#FF5A5E",
                                            "label": label_for_tech_female
                                        })

        if category.category == 'Male Tech':
            company_male_tech = category.percentage
            label_for_tech_male = 'Male - Tech: ' + str(company_male_tech) + '%'
            tech_list_of_dicts['tech'].append({
                                            "value": company_male_tech,
                                            "color": "#009933",
                                            "highlight": "#FF5A5E",
                                            "label": label_for_tech_male
                                        })

    for category in categories_for_company:
        if category.category == 'Female Tech':

            return jsonify(tech_list_of_dicts)


    return "False"

@app.route("/company-ethnicity-tech/<int:company_id>.json")
def return_ethnicity_tech_info(company_id):
    """Return ethnic diversity in technical roles."""

    categories_for_company = Category.query.filter(Category.company_id == company_id)
    average = Company.query.filter(Company.name == 'average from our sample').one()
    categories_for_average = average.categories
    us_population = Company.query.filter(Company.name == 'U.S. Population').one()
    categories_for_us_population = us_population.categories

    tech_dicts = {
                        "labels": ['White', 'Asian', 'Latino', 'Black', 'Two+ races', 'Other'],
                        "datasets": [
                                {
                                    "label": "Company - Tech Roles",
                                    "fillColor": "rgba(218,165,117,1)",
                                    "strokeColor": "rgba(218,165,117,0.8)",
                                    "highlightFill": "rgba(218,165,117,0.75)",
                                    "highlightStroke": "rgba(218,165,117,1)",
                                    "data": []
                                },
                                {
                                    "label": "Average for Tech Companies - Tech Roles",
                                    "fillColor": "rgba(151,187,205,0.5)",
                                    "strokeColor": "rgba(151,187,205,0.8)",
                                    "highlightFill": "rgba(151,187,205,0.75)",
                                    "highlightStroke": "rgba(151,187,205,1)",
                                    "data": []
                                },
                                {
                                    "label": "US Population",
                                    "fillColor": "rgba(220,220,220,0.5)",
                                    "strokeColor": "rgba(220,220,220,0.8)",
                                    "highlightFill": "rgba(220,220,220,0.75)",
                                    "highlightStroke": "rgba(220,220,220,1)",
                                    "data": [],
                                },
                            ]}


    for category in categories_for_us_population:
        if category.category in ['White', 'Asian', 'Latino', 'Black', 'Two+ races', 'Other']:
            tech_dicts['datasets'][2]['data'].append(category.percentage)

    for category in categories_for_average:
        if category.category in ['White Tech', 'Asian Tech', 'Latino Tech', 'Black Tech', 'Two+ races Tech', 'Other Tech']:
            tech_dicts['datasets'][1]['data'].append(category.percentage)

    for category in categories_for_company:

        #Extra Ethnicity Data
        if category.category in ['White Tech', 'Asian Tech', 'Latino Tech', 'Black Tech', 'Two+ races Tech', 'Other Tech']:
            tech_dicts['datasets'][0]['data'].append(category.percentage)


    for category in categories_for_company:

        if category.category == 'White Tech':
            return jsonify(tech_dicts)

    return "False"






@app.route("/company-gender/<int:company_id>.json")
def get_gender_info(company_id):
    """Returns gender diversity info for company."""

    company = Company.query.get(company_id)
    label_for_female = 'Female: ' + str(company.female_overall) + '%'
    label_for_male = 'Male: ' + str(company.male_overall) + '%'



    average = Company.query.filter(Company.name == 'average from our sample').one()
    label_for_avg_female = 'Female: ' + str(average.female_overall) + '%'
    label_for_avg_male = 'Male: ' + str(average.male_overall) + '%'


    gender_list_of_dicts = {'company':[
                                        {
                                            "value": company.female_overall,
                                            "color": "#ffff00",
                                            "highlight": "#FF5A5E",
                                            "label": label_for_female
                                        },

                                        {
                                            "value": company.male_overall,
                                            "color": "#009933",
                                            "highlight": "#FF5A5E",
                                            "label": label_for_male
                                        }
                                        ],
                            'average':[

                                        {
                                            "value": average.female_overall,
                                            "color": "#0066ff",
                                            "highlight": "#FF5A5E",
                                            "label": label_for_avg_female
                                        },

                                        {
                                            "value": average.male_overall,
                                            "color": "#cc00cc",
                                            "highlight": "#FF5A5E",
                                            "label": label_for_avg_male
                                        }
                                        ]}

    


    # print gender_list_of_dicts
    return jsonify(gender_list_of_dicts)



@app.route("/company-ethnicity/<int:company_id>.json")
def get_ethnicity_info(company_id):
    """Returns ethnic diversity info for companies."""

    company = Company.query.get(company_id)


    categories_for_company = Category.query.filter(Category.company_id == company_id)
    average = Company.query.filter(Company.name == 'average from our sample').one()
    categories_for_average = average.categories
    us_population = Company.query.filter(Company.name == 'U.S. Population').one()
    categories_for_us_population = us_population.categories

    #Initialize dictionary for basic ethnicity data 
    ethnic_list_of_dicts = {
                        "labels": [],
                        "datasets": [
                                {
                                    "label": "Company",
                                    "fillColor": "rgba(218,165,117,1)",
                                    "strokeColor": "rgba(218,165,117,0.8)",
                                    "highlightFill": "rgba(218,165,117,0.75)",
                                    "highlightStroke": "rgba(218,165,117,1)",
                                    "data": []
                                },
                                {
                                    "label": "Average for Tech Companies",
                                    "fillColor": "rgba(151,187,205,0.5)",
                                    "strokeColor": "rgba(151,187,205,0.8)",
                                    "highlightFill": "rgba(151,187,205,0.75)",
                                    "highlightStroke": "rgba(151,187,205,1)",
                                    "data": []
                                },
                                {
                                    "label": "US Population",
                                    "fillColor": "rgba(220,220,220,0.5)",
                                    "strokeColor": "rgba(220,220,220,0.8)",
                                    "highlightFill": "rgba(220,220,220,0.75)",
                                    "highlightStroke": "rgba(220,220,220,1)",
                                    "data": [],
                                },
                            ]}

    for category in categories_for_us_population:
        if category.category in ['White', 'Asian', 'Latino', 'Black', 'Two+ races', 'Other']:
            ethnic_list_of_dicts['datasets'][2]['data'].append(category.percentage)

    for category in categories_for_average:
        if category.category in ['White', 'Asian', 'Latino', 'Black', 'Two+ races', 'Other']:
            ethnic_list_of_dicts['datasets'][1]['data'].append(category.percentage)

    for category in categories_for_company:

        #Basic Ethnicity Data
        if category.category in ['White', 'Asian', 'Latino', 'Black', 'Two+ races', 'Other']:
            ethnic_list_of_dicts['labels'].append(category.category.encode('UTF-8'))
            ethnic_list_of_dicts['datasets'][0]['data'].append(category.percentage)

    return jsonify(ethnic_list_of_dicts)


@app.route("/glassdoor-results/<int:company_id>.json")
def return_review_results(company_id):
    """Returns a Glassdoor overall review for company."""

    company = Company.query.get(company_id)
    company_name = company.name

    url = "http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=55828&t.k=fhcJ0ZT1E89&action=employers&q=" + str(company_name)

    # Need to set the User-Agent in the header of http request to be able to access Glassdoor API
    resp = requests.get(url, headers={'User-Agent': 'curl/7.30.0'})

    results = resp.json()

    company_glassdoor = {}

    overall_rating = results["response"]["employers"][0]["overallRating"]

    company_glassdoor["overallRating"] = overall_rating

    return jsonify(company_glassdoor)


############################################# REVIEW #####################################################

@app.route("/review/<int:company_id>")
def show_review_page(company_id):
    """Allow user to write a review."""

    company = Company.query.get(company_id)

    return render_template('review.html', company_id=company_id, company=company)


@app.route("/submitted/<int:company_id>", methods=["POST"])
def add_user_comment(company_id):
    """Add new user comment to company page."""

    form_company = request.form.get("company")
    form_rating = request.form.get("rating")
    form_emp_status = request.form.get("employee_status")
    form_title = request.form.get("title")
    form_pros = request.form.get("pros")
    form_cons = request.form.get("cons")
    form_gender = request.form.get("gender")
    form_ethnicity = request.form.get("ethnicity")
    form_recommend = request.form.get("recommend")

    company = Company.query.filter(Company.name == form_company).one()
    id_of_company = company.company_id

    review = Review(company_id=id_of_company, rating=form_rating, gender=form_gender,
                    ethnicity=form_ethnicity, employee_status=form_emp_status,
                    review_title=form_title, pros=form_pros, cons=form_cons, recommended=form_recommend)

    db.session.add(review)
    db.session.commit()

    # reviews = Review.query.all()

    flash("Your comment has been received!")
    return redirect("/company/" + str(id_of_company))




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
