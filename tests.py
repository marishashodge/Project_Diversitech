"""Test suite for Diversitech app."""

import json
from unittest import TestCase
from server import app
import server
from model import connect_to_db, db, Company, Category, Review, example_data_companies, example_data_categories
from helper import *



class FlaskTests(TestCase):
    def setUp(self):
        """What you need to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, db_uri="postgresql:///testdb")

        # create tables and add sample data
        db.create_all()
        example_data_companies()
        example_data_categories()

    #################################################################################
    # Test any functions that only render a template.


    def test_load_homepage(self):
        """Tests to see if the index page shows up."""

        result = self.client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('<h1 style="color: white;">Tech Company Diversity Data and Reviews</h1>', result.data)


    def test_load_company(self):
        """Tests to see if the company 13 page loads."""

        result = self.client.get('/company/13')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Google', result.data)

    def test_load_review(self):
        """Tests to see if the company 2 page loads."""

        result = self.client.get('/review/2')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Submit a Review', result.data)

    ##############################################################################
    # Test any functions that will query data.

    def test_process_review(self):
        """Test to see if the review form will process correctly."""

        result = self.client.post("/submitted/<int:company_id>",
                                  data={'form_company': "Google",
                                        'form_rating': "5",
                                        'form_emp_status': "Current Employee",
                                        'form_title': "Great Company!",
                                        'form-pros': "Yay!",
                                        'form_cons': "No!",
                                        'form_gender': "Female",
                                        'form-ethnicity': "Black",
                                        'form_recommend': "yes",
                                        },
                                  follow_redirects=True)
        self.assertIn('No', result.data)
        self.assertNotIn('Yelp', result.data)

    #############################################################################
    # Test any functions that will query data.

    def test_find_company(self):
        """Find a company in the sample data."""

        company1 = Company.query.filter(Company.name == "Yelp").first()
        self.assertEqual(company1.name, "Yelp")

    def test_find_category(self):
        """Find a category in the sample data for a given company"""

        cat1 = Category.query.filter(Category.company_id == 4, Category.category == 'White').first()
        self.assertEqual(cat1.percentage, 60)

    # def test_find_review(self):
    #     """Find a review in the sample data."""
    #
    #     r1 = Review.query.filter(Review.review_id == 1).first()
    #     self.assertEqual(r1.rating, 1)

    # def test_categories_for_company(self):
    #     """Find categories for a given company."""
    #
    #     r = self.client.get("/company-gender/2.json")
    #
    #     # Turn json -> Python dictionary
    #     info = json.loads(r.data)
    #
    #     self.assertEqual(len(info['company']), 2)
    #
    def tearDown(self):
        """What you need to do at the end of every test."""

        db.session.close()
        db.drop_all()



if __name__ == "__main__":
    import unittest

    unittest.main()
