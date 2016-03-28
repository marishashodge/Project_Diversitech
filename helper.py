from model import connect_to_db, db, Company, Category, Review

def get_us_ethnic_percentages():
    """Return a dictionary of percentages for each ethnic category in the u.s. population."""

    #for each company get the diversity numbers
    us_population = Company.query.filter(Company.name == 'u.s. population').one()
    categories_for_us_population = us_population.categories

    us_numbers = {}

    for category in categories_for_us_population:
        us_numbers[category.category] = category.percentage

    return us_numbers


def get_gender_top10():
    """Return a list of the top 5 companies in gender diversity."""
    gender_rating_dict = {}

    us_population = Company.query.filter(Company.name == 'u.s. population').one()

    f_us = us_population.female_overall
    m_us = us_population.male_overall

    companies = Company.query.all()

    for company in companies:

        if company.name == 'u.s. population' or company.name == 'average from our sample':
            continue

        else:
            categories = company.categories
            #find the absolute difference between company gender (female only) percentage and US gender percentage
            f_diff_from_us = abs(company.female_overall - f_us)
            gender_rating_dict[company.company_id] = f_diff_from_us

    # Calculate top 5 companies in gender diversity
    gender_top_10 = sorted(gender_rating_dict, key=gender_rating_dict.get)[:10]

    genderTop10 = []

    for x in gender_top_10:
        company = Company.query.filter(Company.company_id == x).first()
        genderTop10.append(company)

    return genderTop10


def get_ethnic_count():
    """Return a dictionary of companies and their ethnic diversity numbers."""

    us_numbers = get_us_ethnic_percentages()

    ethnic_rating_dict = {}

    companies = Company.query.all()

    for company in companies:

        if company.name == 'u.s. population' or company.name == 'average from our sample':
            continue

        else:
            categories = company.categories
            ethnic_count = 0

            #find the absolute difference between company ethicity percentages and US ethnicity percentage
            for category in categories:
                # Check to see if category is in this list: ['White', 'Asian', 'Latino', 'Black', 'Two+ races', 'Other']
                if category.category in ['White', 'Asian', 'Latino', 'Black', 'Two+ races', 'Other']:
                    diff_from_us = abs(us_numbers[category.category] - category.percentage)
                    ethnic_count += diff_from_us

                # Divide ethnic count by the number of categories to get an average
                ethnic_num = ethnic_count / 6
                # Add total ethnic count for each company to ethnic_rating_dictionary
                ethnic_rating_dict[company.company_id] = ethnic_num

    return ethnic_rating_dict


def get_ethnic_dict_sorted():
    """Return a list of the top 5 companies in ethnic diversity."""

    ethnic_rating_dict = get_ethnic_count()
    # Calculate top 5 companies in ethnic diversity
    ethnic_top_5 = sorted(ethnic_rating_dict, key=ethnic_rating_dict.get)[:10]

    return ethnic_top_5


def get_ethnic_top10():
    """Return a list of the top 5 companies."""

    ethnic_top_10 = get_ethnic_dict_sorted()

    ethnicTop10 = []

    for y in ethnic_top_10:
        company = Company.query.filter(Company.company_id == y).first()
        ethnicTop10.append(company)

    return ethnicTop10

def get_gender_company_percentages(company_id):

    categories_for_company = Category.query.filter(Category.company_id == company_id)

    company_list = []

    # Add overall company numbers
    company = Company.query.get(company_id)

    c_f =  company.female_overall
    company_list.append(c_f)

    c_m = company.male_overall
    company_list.append(c_m)

    # Add tech company numbers
    for category in categories_for_company:

        if category.category == 'Female Tech':
            company_female_tech = category.percentage
            company_list.append(company_female_tech)

        if category.category == 'Male Tech':
            company_male_tech = category.percentage
            company_list.append(company_male_tech)

        if category.category == 'Female Managers':
            female_manager_percentage = category.percentage
            company_list.append(female_manager_percentage)

        if category.category == 'Male Managers':
            male_manager_percentage = category.percentage
            company_list.append(male_manager_percentage)

    return company_list

def get_gender_avg_percentages():
    """Return a list of average gender diversity."""

    average_list = []

    # Add average overall numbers
    average = Company.query.filter(Company.name == 'average from our sample').one()
    categories_for_average = average.categories

    a_f =  average.female_overall
    average_list.append(a_f)

    a_m = average.male_overall
    average_list.append(a_m)

    # Add average tech numbers
    for category in categories_for_average:

        if category.category == 'Female Tech':
            female_tech_percentage = category.percentage
            average_list.append(category.percentage)

        if category.category == 'Male Tech':
            male_tech_percentage = category.percentage
            average_list.append(category.percentage)

        if category.category == 'Female Managers':
            female_manager_percentage = category.percentage
            average_list.append(female_manager_percentage)

        if category.category == 'Male Managers':
            male_manager_percentage = category.percentage
            average_list.append(male_manager_percentage)

    return average_list

def get_gender_manager_percentages(company_id):
    """Return list of gender diversity in management."""

    manager_list = []

    categories_for_company = Category.query.filter(Category.company_id == company_id)

    average = Company.query.filter(Company.name == 'average from our sample').one()
    categories_for_average = average.categories

    for category in categories_for_average:

        if category.category == 'Female Managers':
            female_m_percentage = category.percentage
            label_for_avg_female = 'Female - Managers ' + str(female_m_percentage) + '%'

        if category.category == 'Male Managers':
            male_m_percentage = category.percentage
            label_for_avg_male = 'Male - Managers: ' + str(male_m_percentage) + '%'






    managers_list_of_dicts = {'tech': [],
                        'average': [
                                        {
                                            "value": female_m_percentage,
                                            "color": "#0066ff",
                                            "highlight": "#FF5A5E",
                                            "label": label_for_avg_female
                                        },

                                        {
                                            "value": male_m_percentage,
                                            "color": "#cc00cc",
                                            "highlight": "#FF5A5E",
                                            "label": label_for_avg_male
                                        }
                                    ]}


    for category in categories_for_company:

        if category.category == 'Female Managers':
            company_female_m = category.percentage
            label_for_m_female = 'Female - Managers: ' + str(company_female_m) + '%'
            managers_list_of_dicts['tech'].append({
                                            "value": company_female_m,
                                            "color": "#ffff00",
                                            "highlight": "#FF5A5E",
                                            "label": label_for_m_female
                                        })

        if category.category == 'Male Managers':
            company_male_m = category.percentage
            label_for_m_male = 'Male - Managers: ' + str(company_male_m) + '%'
            managers_list_of_dicts['tech'].append({
                                            "value": company_male_m,
                                            "color": "#009933",
                                            "highlight": "#FF5A5E",
                                            "label": label_for_m_male
                                        })



    return managers_list_of_dicts



def generate_gender_tech_dict(company_id):
    """Return dictionary of gender diversity in technical roles."""

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



    return tech_list_of_dicts




def generate_ethnicity_tech_dict(company_id):
    """Return dictionary of ethnic diversity in technical roles."""

    categories_for_company = Category.query.filter(Category.company_id == company_id)
    average = Company.query.filter(Company.name == 'average from our sample').one()
    categories_for_average = average.categories
    us_population = Company.query.filter(Company.name == 'u.s. population').one()
    categories_for_us_population = us_population.categories
    company = Company.query.get(company_id)

    tech_dicts = {      "data1": [],
                        "data2": []

                        }

    tech_dicts = {
                        "labels": ['White', 'Asian', 'Latino', 'Black', 'Two+ races', 'Other'],
                        "datasets": [
                                {
                                    "label": company.name + "- Tech Roles",
                                    "fillColor": "rgba(173, 73, 182,0.9)",
                                    "strokeColor": "rgba(173, 73, 182,0.9)",
                                    "highlightFill": "rgba(173, 73, 182,0.75)",
                                    "highlightStroke": "rgba(173, 73, 182,1)",
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

    return tech_dicts


def generate_gender_info(company_id):
    """Returns a dictionary of gender diversity info for company."""

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

    return(gender_list_of_dicts)


def generate_ethnicity_info(company_id):
    """Returns a dictionary of ethnic diversity info for companies."""

    company = Company.query.get(company_id)
    categories_for_company = Category.query.filter(Category.company_id == company_id)
    average = Company.query.filter(Company.name == 'average from our sample').one()
    categories_for_average = average.categories
    us_population = Company.query.filter(Company.name == 'u.s. population').one()
    categories_for_us_population = us_population.categories

    #Initialize dictionary for basic ethnicity data
    ethnic_list_of_dicts = {
                        "labels": [],
                        "datasets": [
                                {
                                    "label": company.name,
                                    "fillColor": "rgba(173, 73, 182, 0.9)",
                                    "strokeColor": "rgba(173, 73, 182, 0.9)",
                                    "highlightFill": "rgba(173, 73, 182,0.75)",
                                    "highlightStroke": "rgba(173, 73, 182,1)",
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

    return ethnic_list_of_dicts


def get_company_overall_rating(company_id):

    reviews = Review.query.filter(Review.company_id == company_id).all()

    count = 0

    for review in reviews:
        count += review.rating

    overall_rating = average = count / len(reviews)

    return overall_rating


def get_company_reviews(company_id):

    reviews = Review.query.filter(Review.company_id == company_id).order_by(Review.review_id).all()

    # Only show the most recent two reviews and reverse them so the newest one is first
    two_recent_reviews = reviews[-3:]

    two_recent_reviews.reverse()

    return two_recent_reviews

def generate_report_date(company_id):

    company = Company.query.get(company_id)

    report_date = company.report_date

    if report_date == "-":

        report_date = 0

    return report_date


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from application import app
    connect_to_db(app, os.environ.get("DATABASE_URL"))
    print "Connected to DB."
