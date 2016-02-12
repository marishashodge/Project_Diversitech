"""Utility file to seed diversity database."""

from sqlalchemy import func
from model import Company
from model import Category

from model import connect_to_db, db

from server import app
import pandas as pd
import os

os.getcwd()

os.chdir("/Users/Mandela/Documents/Project")


def load_companies():
    """Load companies into database."""
    data = pd.read_csv("Diversitech-Table.csv")
    print "Companies"

    # Company.query.delete()

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


def load_categories():
    """Load categories into database."""
    data = pd.read_csv("Diversitech-Table.csv")
    print "Categories"

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



if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    connect_to_db(app)
    db.create_all()
    print "Connected to DB."

    # Import different types of data
    load_companies()
    load_categories()  