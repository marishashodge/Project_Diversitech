"""Diversitech"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Company, Category, Review
from helper import *
import os

import requests

app = Flask(__name__)

app.secret_key = "54312"

# StructUndefined allows for Jinja2 to raise an error when there is an undefined variable
app.jinja_env.undefined = StrictUndefined


@app.route('/d3Chart/<int:company_id>')
def chart(company_id):

    company_list = get_gender_company_percentages(company_id)
    average_list = get_gender_avg_percentages()

    # company females
    data1 = company_list[0]
    # company males
    data2 = company_list[1]

    # average females
    data5 = average_list[0]
    # average males
    data6 = average_list[1]

    if len(company_list) > 2:

        data3 = company_list[2]
        # company tech males
        data4 = company_list[3]

        # average tech females
        data7 = average_list[2]
        # average tech males
        data8 = average_list[3]

    else:

        data3 = 0
        # company tech males
        data4 = 0
        # average tech females
        data7 = 0
        # average tech males
        data8 = 0


    return render_template("d3-3.html", data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, data7=data7, data8=data8)



@app.route('/')
def index():
    """Homepage."""

    genderTop10 = get_gender_top10()


    g_1 = genderTop10[0].company_id
    g_n1 = genderTop10[0].name
    g_2 = genderTop10[1].company_id
    g_n2 = genderTop10[1].name
    g_3 = genderTop10[2].company_id
    g_n3 = genderTop10[2].name
    g_4 = genderTop10[3].company_id
    g_n4 = genderTop10[3].name
    g_5 = genderTop10[4].company_id
    g_n5 = genderTop10[4].name
    g_6 = genderTop10[5].company_id
    g_n6 = genderTop10[5].name
    g_7 = genderTop10[6].company_id
    g_n7 = genderTop10[6].name
    g_8 = genderTop10[7].company_id
    g_n8 = genderTop10[7].name
    g_9 = genderTop10[8].company_id
    g_n9 = genderTop10[8].name
    g_10 = genderTop10[9].company_id
    g_n10 = genderTop10[9].name

    ethnicTop10 = get_ethnic_top10()

    e_1 = ethnicTop10[0].company_id
    e_n1 = ethnicTop10[0].name
    e_2 = ethnicTop10[1].company_id
    e_n2 = ethnicTop10[1].name
    e_3 = ethnicTop10[2].company_id
    e_n3 = ethnicTop10[2].name
    e_4 = ethnicTop10[3].company_id
    e_n4 = ethnicTop10[3].name
    e_5 = ethnicTop10[4].company_id
    e_n5 = ethnicTop10[4].name
    e_6 = ethnicTop10[5].company_id
    e_n6 = ethnicTop10[5].name
    e_7 = ethnicTop10[6].company_id
    e_n7 = ethnicTop10[6].name
    e_8 = ethnicTop10[7].company_id
    e_n8 = ethnicTop10[7].name
    e_9 = ethnicTop10[8].company_id
    e_n9 = ethnicTop10[8].name
    e_10 = ethnicTop10[9].company_id
    e_n10 = ethnicTop10[9].name

    # print ethnicTop10
    # print genderTop10


    return render_template("home.html", g1=g_1, g2=g_2, g3=g_3, g4=g_4, g5=g_5,
                                        gn1=g_n1, gn2=g_n2, gn3=g_n3, gn4=g_n4, gn5=g_n5,
                                        g6=g_6, g7=g_7, g8=g_8, g9=g_9, g10=g_10,
                                        gn6=g_n6, gn7=g_n7, gn8=g_n8, gn9=g_n9, gn10=g_n10,
                                        e1=e_1, e2=e_2, e3=e_3, e4=e_4, e5=e_5,
                                        en1=e_n1, en2=e_n2, en3=e_n3, en4 = e_n4, en5=e_n5,
                                        e6=e_6, e7=e_7, e8=e_8, e9=e_9, e10=e_10,
                                        en6=e_n6, en7=e_n7, en8=e_n8, en9=e_n9, en10=e_n10
                                        )



@app.route('/search', methods=["POST"])
def search_companies():
    """Send user to company page or 'company-not-found.html' based on search query."""

    company_searched = request.form.get("search")

    company_verified = company_searched[0].capitalize() + company_searched[1:].lower()

    company = Company.query.filter(Company.name == company_verified).first()

    if company:
        id_of_company = company.company_id
        return redirect("/company/" + str(id_of_company))

    else:
        return render_template("company-not-found.html", company=company_verified)



@app.route('/company/<int:company_id>')
def company_info(company_id):
    """Company page with diversity details."""

    print "I'm in!"

    company = Company.query.get(company_id)
    print company

    categories_for_company = company.categories
    print categories_for_company

    reviews = get_company_reviews(company_id)
    print reviews

    overall_rating = get_company_overall_rating(company_id)
    print overall_rating

    report_date = generate_report_date(company_id)
    print report_date


    company_list = get_gender_company_percentages(company_id)
    average_list = get_gender_avg_percentages()

    # company females
    data1 = company_list[0]
    # company males
    data2 = company_list[1]
    # average females
    data5 = average_list[0]
    # average males
    data6 = average_list[1]

    if company.name == "Amazon":
        # company tech females
        data3 = 0
        # company tech males
        data4 = 0
        # average tech females
        data7 = 0
        # average tech males
        data8 = 0
        # company manager females
        data9 = company_list[2]
        # company manager males
        data10 = company_list[3]
        # average manager females
        data11 = average_list[2]
        # average manager males
        data12 = average_list[3]

    else:

        if len(company_list) > 2:
            # company tech females
            data3 = company_list[2]
            # company tech males
            data4 = company_list[3]
            # average tech females
            data7 = average_list[2]
            # average tech males
            data8 = average_list[3]
            # company manager females
            data9 = company_list[4]
            # company manager males
            data10 = company_list[5]
            # average manager females
            data11 = average_list[4]
            # average manager males
            data12 = average_list[5]


        else:
            # company tech females
            data3 = 0
            # company tech males
            data4 = 0
            # average tech females
            data7 = 0
            # average tech males
            data8 = 0
            # company manager females
            data9 = 0
            # company manager males
            data10 = 0
            # average manager females
            data11 = 0
            # average manager males
            data12 = 0

    # print report_date

    print report_date
    print reviews
    print "I made it!"

    return render_template("company-page.html", display_company=company, categories=categories_for_company,
                                                reviews=reviews, overallRating=overall_rating, reportDate=report_date, data1=data1,
                                                data2=data2, data3=data3, data4=data4, data5=data5,
                                                data6=data6, data7=data7, data8=data8, data9=data9, data10=data10, data11=data11, data12=data12)


################################### JSON ROUTES #######################################################



@app.route("/company-gender/<int:company_id>.json")
def get_gender_info(company_id):
    """Returns gender diversity info for company."""

    gender_list_of_dicts = generate_gender_info(company_id)

    return jsonify(gender_list_of_dicts)


@app.route("/company-ethnicity/<int:company_id>.json")
def get_ethnicity_info(company_id):
    """Returns ethnic diversity info for companies."""

    ethnic_list_of_dicts = generate_ethnicity_info(company_id)

    return jsonify(ethnic_list_of_dicts)


@app.route("/company-gender-tech/<int:company_id>.json")
def return_gender_tech_json(company_id):
    """Return gender diversity in technical roles."""

    tech_list_of_dicts = generate_gender_tech_dict(company_id)



    if tech_list_of_dicts["tech"]:

        return jsonify(tech_list_of_dicts)

    return "False"

@app.route("/company-gender-managers/<int:company_id>.json")
def return_gender_managers_json(company_id):
    """Return gender diversity in management roles."""

    managers_list_of_dicts = get_gender_manager_dict(company_id)

    if managers_list_of_dicts["tech"]:

        return jsonify(managers_list_of_dicts)

    return "False"


@app.route("/company-ethnicity-tech/<int:company_id>.json")
def return_ethnicity_tech_info(company_id):
    """Return ethnic diversity in technical roles."""

    tech_dicts = generate_ethnicity_tech_dict(company_id)

    if tech_dicts["datasets"][0]['data']:

        return jsonify(tech_dicts)

    return "False"


############################################# NEWS #####################################################

@app.route("/news/<int:company_id>.json")
def return_news_search(company_id):
    """Returns Google news search for company news in diversity."""

    company = Company.query.get(company_id)
    company_name = company.name

    company_news = { "results": []}

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


############################################# REVIEWS #####################################################

@app.route("/review/<int:company_id>")
def show_review_page(company_id):
    """Allow user to write a review."""

    company = Company.query.get(company_id)

    return render_template('review.html', company_id=company_id, company=company)


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

    square_logo = results["response"]["employers"][0]["squareLogo"]

    company_glassdoor["overallRating"] = overall_rating
    company_glassdoor["reviewsURL"] = reviews_url
    company_glassdoor["reviewHeadline"] = featured_review_headline
    company_glassdoor["reviewPros"] = featured_review_pros
    company_glassdoor["reviewCons"] = featured_review_cons
    company_glassdoor["reviewRating"] = featured_review_rating

    if company_name == "HP":
        company_glassdoor["squareLogo"] = "http://fixstream.com/wp-content/uploads/2015/08/hp-logo-square.jpg"
    else:
        company_glassdoor["squareLogo"] = square_logo

    return jsonify(company_glassdoor)

# @app.route("/logo/<int:company_id>.json")
#     """Returns a company logo from Glassdoor API."""
#
#     company = Company.query.get(company_id)
#     company_name = company.name
#
#     url = "http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=55828&t.k=fhcJ0ZT1E89&action=employers&q=" + str(company_name)
#
#     # Need to set the User-Agent in the header of http request to be able to access Glassdoor API
#     resp = requests.get(url, headers={'User-Agent': 'curl/7.30.0'})
#     results = resp.json()
#     company_glassdoor = {}
#
#     square_logo = results["response"]["employers"][0]["squareLogo"]
#
#     company_glassdoor["squareLogo"] = square_logo
#
#     return jsonify(company_glassdoor)


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

    flash("Your review has been received!")
    return redirect("/company/" + str(id_of_company))



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    PORT = int(os.environ.get("PORT", 5000))

    app.run(debug=True, host="0.0.0.0", port=PORT)
