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

    genderTop5 = []

    ethnicTop5 = []

    #for each company get the diversity numbers
    companies = Company.query.all()

    us_population = Company.query.filter(Company.name == 'U.S. Population').one()

    f_us = us_population.female_overall
    m_us = us_population.male_overall

    categories_for_us_population = us_population.categories

    ['White', 'Asian', 'Latino', 'Black', 'Two+ races', 'Other']

    for category in categories_for_us_population:

        if category.category == 'White':
            white_us_percentage = category.percentage

        if category.category == 'Asian':
            asian_us_percentage = category.percentage

        if category.category == 'Latino':
            latino_us_percentage = category.percentage

        if category.category == 'Black':
            black_us_percentage = category.percentage

        if category.category == 'Two+ races':
            two_us_percentage = category.percentage

        if category.category == 'Other':
            other_us_percentage = category.percentage

    gender_rating_dict = {}
    ethnic_rating_dict = {}

    for company in companies:
        if company.name == 'U.S. Population' or company.name == 'average from our sample':
            continue

        else:

            categories = company.categories
            ethnic_count = 0

            #find the absolute difference between company gender (female only) percentage and US gender percentage
            f_diff_from_us = abs(company.female_overall - f_us)
            gender_rating_dict[company.company_id] = f_diff_from_us

            #set the variables for company ethnicity categories
            #find the absolute difference between company ethicity percentages and US ethnicity percentage
            for category in categories:

                if category.category == 'White':
                    white_percentage = category.percentage
                    white_diff_from_us = abs(white_percentage - white_us_percentage)
                    ethnic_count += white_diff_from_us

                if category.category == 'Asian':
                    asian_percentage = category.percentage
                    asian_diff_from_us = abs(asian_percentage - asian_us_percentage)
                    ethnic_count += asian_diff_from_us

                if category.category == 'Latino':
                    latino_percentage = category.percentage
                    latino_diff_from_us = abs(latino_percentage - latino_us_percentage)
                    ethnic_count += latino_diff_from_us

                if category.category == 'Black':
                    black_percentage = category.percentage
                    black_diff_from_us = abs(black_percentage - black_us_percentage)
                    ethnic_count += black_diff_from_us

                if category.category == 'Two+ races':
                    two_percentage = category.percentage
                    two_diff_from_us = abs(two_percentage - two_us_percentage)
                    ethnic_count += two_diff_from_us

                if category.category == 'Other':
                    other_percentage = category.percentage
                    other_diff_from_us = abs(other_percentage - other_us_percentage)
                    ethnic_count += other_diff_from_us


            # Take the average of the ethnic_count
            ethnic_num = ethnic_count / 6
            # Add total ethnic count for each company to ethnic_rating_dictionary
            ethnic_rating_dict[company.company_id] = ethnic_num

    # Calculate top 5 companies in gender diversity
    gender_top_5 = sorted(gender_rating_dict, key=gender_rating_dict.get)[:5]

    # Calculate top 5 companies in ethnic diversity
    ethnic_top_5 = sorted(ethnic_rating_dict, key=ethnic_rating_dict.get)[:5]

    print gender_top_5
    print ethnic_top_5

    for x in gender_top_5:
        company = Company.query.filter(Company.company_id == x).first()
        genderTop5.append(company)

    for y in ethnic_top_5:
        company = Company.query.filter(Company.company_id == y).first()
        ethnicTop5.append(company)


    return render_template("home.html", genderTop5=genderTop5, ethnicTop5=ethnicTop5)


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
            label_for_us_female = 'Female - Tech: ' + str(female_tech_percentage) + '%'

        if category.category == 'Male Tech':
            male_tech_percentage = category.percentage
            label_for_us_male = 'Male - Tech: ' + str(male_tech_percentage) + '%'


    tech_list_of_dicts = {'tech': [],
                        'average': [
                                        {
                                            "value": female_tech_percentage,
                                            "color": "#0066ff",
                                            "highlight": "#FF5A5E",
                                            "label": label_for_us_female
                                        },

                                        {
                                            "value": male_tech_percentage,
                                            "color": "#cc00cc",
                                            "highlight": "#FF5A5E",
                                            "label": label_for_us_male
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
    label_for_us_female = 'Female: ' + str(average.female_overall) + '%'
    label_for_us_male = 'Male: ' + str(average.male_overall) + '%'


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
                                            "label": label_for_us_female
                                        },

                                        {
                                            "value": average.male_overall,
                                            "color": "#cc00cc",
                                            "highlight": "#FF5A5E",
                                            "label": label_for_us_male
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
def return_glassdoor_results(company_id):
    """Returns Glassdoor api results for company."""

    company = Company.query.get(company_id)
    company_name = company.name

    url = "http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=55828&t.k=fhcJ0ZT1E89&action=employers&q=" + str(company_name)

    # Need to set the User-Agent in the header of http request to be able to access Glassdoor API
    resp = requests.get(url, headers={'User-Agent': 'curl/7.30.0'})

    results = resp.json()

    company_glassdoor = {}

    reviews_url = results["response"]["attributionURL"]
    overall_rating = results["response"]["employers"][0]["overallRating"]
    featured_review_headline = results["response"]["employers"][0]["featuredReview"]["headline"]
    featured_review_pros = results["response"]["employers"][0]["featuredReview"]["pros"]
    featured_review_cons = results["response"]["employers"][0]["featuredReview"]["cons"]
    featured_review_rating = results["response"]["employers"][0]["featuredReview"]["overall"]

    company_glassdoor["overallRating"] = overall_rating
    company_glassdoor["reviewsURL"] = reviews_url
    company_glassdoor["reviewHeadline"] = featured_review_headline
    company_glassdoor["reviewPros"] = featured_review_pros
    company_glassdoor["reviewCons"] = featured_review_cons
    company_glassdoor["reviewRating"] = featured_review_rating

    return jsonify(company_glassdoor)

@app.route("/news/<int:company_id>.json")
def return_news_search(company_id):
    """Returns Google news search for company news in diversity."""

    company = Company.query.get(company_id)
    company_name = company.name

    company_news = { "results": []}

    # url = "https://ajax.googleapis.com/ajax/services/search/news?v=1.0&q=" + str(company_name) + "%20diversity"

    url = ('https://ajax.googleapis.com/ajax/services/search/news?v=1.0&q=' + str(company_name) + '%20diversity&userip=50.148.158.131')

    resp = requests.get(url)

    results = resp.json()

    all_results = results["responseData"]

    ind_results = all_results["results"]

    for i in range(len(ind_results)):


        news_url = ind_results[i]["unescapedUrl"]
        news_title = ind_results[i]["title"]
        news_publisher = ind_results[i]["publisher"]
        news_publ_date = ind_results[i]["publishedDate"][:-15]
        news_content = ind_results[i]["content"]

        one_result = {}

        one_result["unescapedUrl"] = news_url
        one_result["title"] = news_title
        one_result["publisher"] = news_publisher
        one_result["publishedDate"] = news_publ_date
        one_result["content"] = news_content

        company_news["results"].append(one_result)

    return jsonify(company_news)



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
