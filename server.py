"""Diversitech"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
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

    reviews = Review.query.all()

    return render_template("company-page.html", display_company=company, categories=categories_for_company, reviews=reviews)


@app.route("/review/<int:company_id>")
def show_review_page(company_id):
    """Allow user to write a review."""

    company = Company.query.get(company_id)

    return render_template('review.html', company_id=company_id, company=company)


@app.route("/submitted/<int:company_id>", methods=["POST"])
def add_user_comment(company_id):
    """Add new user comment to company page."""

    # form_company = request.form.get("company")
    form_rating = request.form.get("rating")
    form_emp_status = request.form.get("employee_status")
    form_title = request.form.get("title")
    form_pros = request.form.get("pros")
    form_cons = request.form.get("cons")

    # company = Company.query.filter(Company.name == form_company).one()
    # id_of_company = company.company_id

    review = Review(company_id=company_id, rating=form_rating, employee_status=form_emp_status,
                    review_title=form_title, pros=form_pros, cons=form_cons)

    db.session.add(review)
    db.session.commit()

    # reviews = Review.query.all()

    flash("Your comment has been received!")
    return redirect("/company/" + str(company_id))



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
