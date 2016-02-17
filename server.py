"""Diversitech"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Company, Category, Review

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


@app.route('/company/<int:company_id>')
def show_company(company_id):
    """Company page with diversity details."""

    company = Company.query.get(company_id)

    categories_for_company = company.categories

    reviews = Review.query.filter(Review.company_id == company_id).all()

    return render_template("company-page.html", display_company=company, categories=categories_for_company, reviews=reviews)


#########################################################################################################

@app.route("/company-gender/<int:company_id>.json")
def get_gender_info(company_id):

    company = Company.query.get(company_id)
    label_for_female = 'Female - ' + str(company.female_overall) + '%'
    label_for_male = 'Male - ' + str(company.male_overall) + '%'

    average = Company.query.get(28)
    label_for_avg_female = 'Female - ' + str(average.female_overall) + '%'
    label_for_avg_male = 'Male - ' + str(average.male_overall) + '%'


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
                            'us':[

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
                                        ]
                            }



    return jsonify(gender_list_of_dicts)



@app.route("/company-diversity-extra/<int:company_id>.json")
def get_extra_ethnicity_info(company_id):

    company = Company.query.get(company_id)

    categories_for_company = Category.query.filter(Category.company_id == company_id)

    #Initialize dictionary for extra ethnicity data 
    extra_ethnic_list_of_dicts = {}
    extra_ethnic_list_of_dicts[company.name.encode('UTF-8')] = []

    for category in categories_for_company:

        #Extra ethnicity data  
        if category.category == 'White Tech':
            extra_ethnic_list_of_dicts[company.name.encode('UTF-8')].append(
                                        {
                                            "value": category.percentage,
                                            "color": "#F7464A",
                                            "highlight": "#FF5A5E",
                                            "label": 'White Tech'
                                        })


        elif category.category == 'Asian Tech':
            extra_ethnic_list_of_dicts[company.name.encode('UTF-8')].append(
                                        {
                                            "value": category.percentage,
                                            "color": "#9999ff",
                                            "highlight": "#FF5A5E",
                                            "label": 'Asian Tech'
                                        })


        elif category.category == 'Latino Tech':
            extra_ethnic_list_of_dicts[company.name.encode('UTF-8')].append(
                                        {
                                            "value": category.percentage,
                                            "color": "#66ff99",
                                            "highlight": "#FF5A5E",
                                            "label": 'Latino Tech'
                                        })


        elif category.category == 'Black Tech':
            extra_ethnic_list_of_dicts[company.name.encode('UTF-8')].append(
                                        {
                                            "value": category.percentage,
                                            "color": "#ffff66",
                                            "highlight": "#FF5A5E",
                                            "label": 'Black Tech'
                                        })


        elif category.category == 'Two+ races Tech':
            extra_ethnic_list_of_dicts[company.name.encode('UTF-8')].append(
                                        {
                                            "value": category.percentage,
                                            "color": "#333399",
                                            "highlight": "#FF5A5E",
                                            "label": 'Two+ races Tech'
                                        })


        elif category.category == 'Other Tech':
            extra_ethnic_list_of_dicts[company.name.encode('UTF-8')].append(
                                        {
                                            "value": category.percentage,
                                            "color": "#66ff33",
                                            "highlight": "#FF5A5E",
                                            "label": 'Other Tech'
                                        })

    return jsonify(extra_ethnic_list_of_dicts) 



@app.route("/company-diversity/<int:company_id>.json")
def get_ethnicity_info(company_id):
    """Get diversity info for companies from database and return json."""

    #How do I get the info for just one company???

    company = Company.query.get(company_id)


    categories_for_company = Category.query.filter(Category.company_id == company_id)
    categories_for_average = Category.query.filter(Category.company_id == 28)
    categories_for_us_population = Category.query.filter(Category.company_id == 1)

    #Initialize dictionary for basic ethnicity data 
    ethnic_list_of_dicts = {
                        "labels": [],
                        "datasets": [
                                {
                                    "label": "Company Ethnicity (%)",
                                    "fillColor": "rgba(218,165,117,0.5)",
                                    "strokeColor": "rgba(218,165,117,0.8)",
                                    "highlightFill": "rgba(218,165,117,0.75)",
                                    "highlightStroke": "rgba(218,165,117,1)",
                                    "data": []
                                },
                                {
                                    "label": "Average Ethnicity for Companies (%) ",
                                    "fillColor": "rgba(151,187,205,0.5)",
                                    "strokeColor": "rgba(151,187,205,0.8)",
                                    "highlightFill": "rgba(151,187,205,0.75)",
                                    "highlightStroke": "rgba(151,187,205,1)",
                                    "data": []
                                },
                                {
                                    "label": "US Ethnicity (%)",
                                    "fillColor": "rgba(220,220,220,0.5)",
                                    "strokeColor": "rgba(220,220,220,0.8)",
                                    "highlightFill": "rgba(220,220,220,0.75)",
                                    "highlightStroke": "rgba(220,220,220,1)",
                                    "data": []
                                },
                            ]}


    #Initialize dictionary for gender data
    # gender_dict = {}
    # gender_dict[company.name.encode('UTF-8')] = []

    # #Initialize dictionary for extra gender data
    # extra_gender_dict = {}
    # extra_gender_dict[company.name.encode('UTF-8')] = []

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




        #     ethnic_list_of_dicts[company.name.encode('UTF-8')].append(
        #                                 {
        #                                     "value": category.percentage,
        #                                     "color": "#F7464A",
        #                                     "highlight": "#FF5A5E",
        #                                     "label": 'White'
        #                                 })

        # elif category.category == 'Asian':
        #     ethnic_list_of_dicts[company.name.encode('UTF-8')].append(
        #                                 {
        #                                     "value": category.percentage,
        #                                     "color": "#9999ff",
        #                                     "highlight": "#FF5A5E",
        #                                     "label": 'Asian'
        #                                 })

        # elif category.category == 'Latino':
        #     ethnic_list_of_dicts[company.name.encode('UTF-8')].append(
        #                                 {
        #                                     "value": category.percentage,
        #                                     "color": "#66ff99",
        #                                     "highlight": "#FF5A5E",
        #                                     "label": 'Latino'
        #                                 })

        # elif category.category == 'Black':
        #     ethnic_list_of_dicts[company.name.encode('UTF-8')].append(
        #                                 {
        #                                     "value": category.percentage,
        #                                     "color": "#ffff66",
        #                                     "highlight": "#FF5A5E",
        #                                     "label": 'Black'
        #                                 })

        # elif category.category == 'Two+ races':
        #     ethnic_list_of_dicts[company.name.encode('UTF-8')].append(
        #                                 {
        #                                     "value": category.percentage,
        #                                     "color": "#333399",
        #                                     "highlight": "#FF5A5E",
        #                                     "label": 'Two+Races'
        #                                 })

        # elif category.category == 'Other':
        #     ethnic_list_of_dicts[company.name.encode('UTF-8')].append(
        #                                 {
        #                                     "value": category.percentage,
        #                                     "color": "#66ff33",
        #                                     "highlight": "#FF5A5E",
        #                                     "label": 'Other'
        #                                 })
   
    # return jsonify(ethnic_list_of_dicts)

   

    # print ethnic_list_of_dicts
    return jsonify(ethnic_list_of_dicts)



###########################################################################################################
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

    company = Company.query.filter(Company.name == form_company).one()
    id_of_company = company.company_id

    review = Review(company_id=id_of_company, rating=form_rating, employee_status=form_emp_status,
                    review_title=form_title, pros=form_pros, cons=form_cons)

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
