function generateGlassdoorDetails(evt) {

    $.get("/glassdoor-results/{{ display_company.company_id }}.json", function(data) {
        $('#rating').html(data.reviewRating);
    });

    $.get("/glassdoor-results/{{ display_company.company_id }}.json", function(data) {
        $('#headline').html(data.reviewHeadline);
     });

    $.get("/glassdoor-results/{{ display_company.company_id }}.json", function(data) {
        $('#pros').html(data.reviewPros);

     });

    $.get("/glassdoor-results/{{ display_company.company_id }}.json", function(data) {
        $('#cons').html(data.reviewCons);

     });

    $.get("/glassdoor-results/{{ display_company.company_id }}.json", function(data) {
        $('.glassdoor-button').attr("href", data.reviewsURL);

     });


    
}

$("#reviews").click(generateGlassdoorDetails);
