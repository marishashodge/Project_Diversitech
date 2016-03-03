"""Models and database functions for DiversiTech Poject."""

from flask_sqlalchemy import SQLAlchemy
import pandas as pd

db = SQLAlchemy()


##############################################################################
# Model definitions

class Company(db.Model):
    """Company list."""

    __tablename__ = "companies"

    company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64))
    # number_of_employees = db.Column(db.Integer, nullable=True)
    report_date = db.Column(db.String(64))
    female_overall = db.Column(db.Integer)
    male_overall = db.Column(db.Integer)

    def __repr__(self):
        """Show info about company."""

        return "<Company company_id=%s name=%s>" % (self.company_id, self.name)


class Category(db.Model):
    """Diversity categories."""

    __tablename__ = "categories"

    diversity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category = db.Column(db.String(64))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    percentage = db.Column(db.Integer)

    def __repr__(self):
        """Show info about categories."""

        return "<Category diversity_id=%s category=%s company_id=%s percentage=%s>" % (self.diversity_id, self.category, self.company_id, self.percentage)

    company = db.relationship('Company', backref=db.backref("categories", order_by=diversity_id))


class Review(db.Model):
    """Company reviews table."""

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    rating = db.Column(db.Integer)
    gender = db.Column(db.String(64))
    ethnicity = db.Column(db.String(64))
    employee_status = db.Column(db.String(64))
    review_title = db.Column(db.String(64))
    pros = db.Column(db.String(1000))
    cons = db.Column(db.String(1000))
    recommended = db.Column(db.String(64))

    def __repr__(self):
        """Show info about comment."""

        return "<Review review_id=%s company_id=%s rating=%s" % (self.review_id, self.company_id, self.rating)

    company = db.relationship('Company', backref=db.backref("review", order_by=review_id))

def example_data_companies():
    """Create some sample data."""

    # Empty out existing data in the case that it is run more than once
    Company.query.delete()
    Review.query.delete()

    data = pd.read_csv("Diversitech-Table.csv")

    for index, row in data.iterrows():
        name = row[0]
        # number_of_employees = row[28]
        report_date = row[2]
        female_overall = row[3]
        male_overall = row[4]

        company = Company(name=name,
                          # number_of_employees=number_of_employees,
                          report_date=report_date,
                          female_overall=female_overall,
                          male_overall=male_overall)

        db.session.add(company)

    db.session.commit()

def example_data_categories():

    Category.query.delete()

    data = pd.read_csv("Diversitech-Table.csv")

    categories = data.columns.values

    for index, row in data.iterrows():
        for i in range(len(row[5:21])):

            if row[i + 5] == "-":
                continue

            else:

                category = categories[i + 5]
                percentage = row[i + 5]
                company = Company.query.filter(Company.name == row[0]).first()
                id_of_company = company.company_id
                detail = Category(category=category,
                                  percentage=percentage,
                                  company_id=id_of_company)

                db.session.add(detail)

    db.session.commit()



##############################################################################
# Helper functions


def connect_to_db(app, db_uri="postgresql:///diversity"):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
