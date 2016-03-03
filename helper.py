from model import connect_to_db, db, Company, Category, Review

def get_us_ethnic_percentages():
    """Return a dictionary of percentages for each ethnic category in the U.S. Population."""

    #for each company get the diversity numbers
    us_population = Company.query.filter(Company.name == 'U.S. Population').one()
    categories_for_us_population = us_population.categories

    us_numbers = {}

    for category in categories_for_us_population:
        us_numbers[category.category] = category.percentage

    return us_numbers


def get_gender_top5():
    """Return a list of the top 5 companies in gender diversity."""
    gender_rating_dict = {}

    us_population = Company.query.filter(Company.name == 'U.S. Population').one()

    f_us = us_population.female_overall
    m_us = us_population.male_overall

    companies = Company.query.all()

    for company in companies:

        if company.name == 'U.S. Population' or company.name == 'average from our sample':
            continue

        else:
            categories = company.categories
            #find the absolute difference between company gender (female only) percentage and US gender percentage
            f_diff_from_us = abs(company.female_overall - f_us)
            gender_rating_dict[company.company_id] = f_diff_from_us

    # Calculate top 5 companies in gender diversity
    gender_top_5 = sorted(gender_rating_dict, key=gender_rating_dict.get)[:5]

    genderTop5 = []

    for x in gender_top_5:
        company = Company.query.filter(Company.company_id == x).first()
        genderTop5.append(company)

    return genderTop5


def get_ethnic_count():
    """Return a dictionary of companies and their ethnic diversity numbers."""

    us_numbers = get_us_ethnic_percentages()

    ethnic_rating_dict = {}

    companies = Company.query.all()

    for company in companies:

        if company.name == 'U.S. Population' or company.name == 'average from our sample':
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
    ethnic_top_5 = sorted(ethnic_rating_dict, key=ethnic_rating_dict.get)[:5]

    return ethnic_top_5


def get_ethnic_top5():
    """Return a list of the top 5 companies."""

    ethnic_top_5 = get_ethnic_dict_sorted()

    ethnicTop5 = []

    for y in ethnic_top_5:
        company = Company.query.filter(Company.company_id == y).first()
        ethnicTop5.append(company)

    return ethnicTop5


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
    us_population = Company.query.filter(Company.name == 'U.S. Population').one()
    categories_for_us_population = us_population.categories

    #Initialize dictionary for basic ethnicity data
    ethnic_list_of_dicts = {
                        "labels": [],
                        "datasets": [
                                {
                                    "label": "Company",
                                    "fillColor": "rgba(221, 72, 20, 0.8)",
                                    "strokeColor": "rgba(221, 72, 20, 0.8)",
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

    return ethnic_list_of_dicts



if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
