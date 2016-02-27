def return_diversity_rating():
    """Return top 5 companies in gender diversity and ethnic diversity."""

    diversity_ratings = {
                        "genderTop5": [],
                        "ethnicTop5": [],
    }

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

            # Add total ethnic count for each company to ethnic_rating_dictionary
            ethnic_rating_dict[company.company_id] = ethnic_count

    # Calculate top 5 companies in gender diversity
    gender_top_5 = sorted(gender_rating_dict, key=gender_rating_dict.get)[:5]

    # Calculate top 5 companies in ethnic diversity
    ethnic_top_5 = sorted(ethnic_rating_dict, key=ethnic_rating_dict.get)[:5]

    print gender_top_5
    print ethnic_top_5

    for x in gender_top_5:
        company = Company.query.filter(Company.company_id == x).first()
        company_name = company.name.encode('UTF-8')
        diversity_ratings['genderTop5'].append(company_name)

    for y in ethnic_top_5:
        company = Company.query.filter(Company.company_id == y).first()
        company_name = company.name.encode('UTF-8')
        diversity_ratings['ethnicTop5'].append(company_name)

    return diversity_ratings
