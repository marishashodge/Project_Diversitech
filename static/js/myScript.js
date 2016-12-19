<script>


    var options = { responsive: true,
                    tooltipTemplate: "<%= value %>%",
                    multiTooltipTemplate: "<%= value %>%",
                    percentageInnerCutout : 65,
                };


    // Make donut chart of percent of men and women OVERALL
    var ctx_donut_gender = $("#donutChart3").get(0).getContext("2d");
    $("#gender-heading").html("Company Gender - Overall");
    $.get("/company-gender/{{ display_company.company_id }}.json", function (data) {
        var myDonutChart3 = new Chart(ctx_donut_gender).Doughnut(data.company, options);
        $('#donutLegend3').html(myDonutChart3.generateLegend());
    });


    // Make donut chart of average percent of men and women
    var ctx_donut_gender_us = $("#donutChart4").get(0).getContext("2d");
    $.get("/company-gender/{{ display_company.company_id }}.json", function (data) {
        var myDonutChart4 = new Chart(ctx_donut_gender_us).Doughnut(data.average, options);
        $("#heading-gender-tech").html("Average Gender for Tech Companies - Overall");
        $('#donutLegend4').html(myDonutChart4.generateLegend());
    });


    function generateOverallDonutChart(evt) {
        var ctx_donut_gender = $("#donutChart3").get(0).getContext("2d");
        $("#gender-heading").html("Company Gender - Overall");
        $.get("/company-gender/{{ display_company.company_id }}.json", function (data) {
            var myDonutChart3 = new Chart(ctx_donut_gender).Doughnut(data.company, options);
            $('#donutLegend3').html(myDonutChart3.generateLegend());
        });

        var ctx_donut_gender_us = $("#donutChart4").get(0).getContext("2d");

        $.get("/company-gender/{{ display_company.company_id }}.json", function (data) {
            var myDonutChart4 = new Chart(ctx_donut_gender_us).Doughnut(data.average, options);
            $("#heading-gender-tech").html("Average Gender for Tech Companies - Overall");
            $('#donutLegend4').html(myDonutChart4.generateLegend());
        });
    };

    function generateTechDonutChart(evt) {
        var ctx_donut_gender_tech = $("#donutChart3").get(0).getContext("2d");
        $("#gender-heading").html("Company Gender - Tech");
        $.get("/company-gender-tech/{{ display_company.company_id }}.json", function (data) {
            var myDonutChart5 = new Chart(ctx_donut_gender_tech).Doughnut(data.tech, options);
            $('#donutLegend3').html(myDonutChart5.generateLegend());
        });

        var ctx_donut_gender_average_tech = $('#donutChart4').get(0).getContext("2d");

        $("#heading-gender-tech").html("Average Gender for Companies - Tech");
        $.get("/company-gender-tech/{{ display_company.company_id }}.json", function (data) {
            var myDonutChart6 = new Chart(ctx_donut_gender_average_tech).Doughnut(data.average,options);
            $('#donutLegend4').html(myDonutChart6.generateLegend());
        }

        )};

      function generateManagerDonutChart(evt) {
          var ctx_donut_gender_managers = $("#donutChart3").get(0).getContext("2d");
          $("#gender-heading").html("Company Gender - Tech");
          $.get("/company-gender-managers/{{ display_company.company_id }}.json", function (data) {
              var myDonutChart7 = new Chart(ctx_donut_gender_managers).Doughnut(data.tech, options);
              $('#donutLegend3').html(myDonutChart7.generateLegend());
          });

          var ctx_donut_gender_average_managers = $('#donutChart4').get(0).getContext("2d");

          $("#heading-gender-tech").html("Average Gender for Companies - Tech");
          $.get("/company-gender-managers/{{ display_company.company_id }}.json", function (data) {
              var myDonutChart8 = new Chart(ctx_donut_gender_average_managers).Doughnut(data.average,options);
              $('#donutLegend4').html(myDonutChart8.generateLegend());
          }

          )};

    // Make donut chart of percent of men and women in TECH roles
   $.get("/company-gender-tech/{{ display_company.company_id }}.json", function (data) {
        if (data == "False") {
            $(".gender-chart3").remove();
            console.log("NO DATA!");
        } else {

            $(".tech-gender-button").append("<button id='tech-gender-button' type='button'>Gender Tech</button>");
            $(".overall-gender-button").append("<button id='overall-gender-button' type='button'>Gender Overall</button>");

            $('#tech-gender-button').click(generateTechDonutChart);
            $('#overall-gender-button').click(generateOverallDonutChart);


            // var ctx_donut_gender_tech = $("#donutChart5").get(0).getContext("2d");

            // var myDonutChart5 = new Chart(ctx_donut_gender_tech).Doughnut(data.tech, options);
            // $('#donutLegend5').html(myDonutChart5.generateLegend());
        }
    });

    // Make donut chart of percent of men and women in MANAGER roles
   $.get("/company-gender-managers/{{ display_company.company_id }}.json", function (data) {
        if (data == "False") {
            $(".gender-chart3").remove();
            console.log("NO DATA!");
        } else {

            $(".manager-gender-button").append("<button id='manager-gender-button' type='button'>Gender Tech</button>");
            $(".overall-gender-button").append("<button id='overall-gender-button' type='button'>Gender Overall</button>");

            $('#manager-gender-button').click(generateManagerDonutChart);
            $('#overall-gender-button').click(generateOverallDonutChart);


            // var ctx_donut_gender_tech = $("#donutChart5").get(0).getContext("2d");

            // var myDonutChart5 = new Chart(ctx_donut_gender_tech).Doughnut(data.tech, options);
            // $('#donutLegend5').html(myDonutChart5.generateLegend());
        }
    });


    // Make bar chart of average percent of men and women in Company, Average and US

    var ctx_bar_ethnic = $("#barGraph1").get(0).getContext("2d");
    $("#heading").html("Company Ethnicity - Overall");

    $.get("/company-ethnicity/{{ display_company.company_id }}.json", function (data) {
        var myBarChart = new Chart(ctx_bar_ethnic).Bar(data, options);
        $('#barLegend').html(myBarChart.generateLegend());
    });

    // Make bar chart of average percent of men and women in Company tech, Average tech and US
    function generateTechBarGraph(evt) {
        console.log("function here")
        var ctx_bar_ethnic_tech = $("#barGraph1").get(0).getContext("2d");
        $("#heading").html("Company Ethnicity - Tech");
        $.get("/company-ethnicity-tech/{{ display_company.company_id }}.json", function (data) {
            var myBarChart2 = new Chart(ctx_bar_ethnic_tech).Bar(data, options);
            $('#barLegend').html(myBarChart2.generateLegend());
        })};

    function generateOverallBarGraph(evt) {
        var ctx_bar_ethnic = $("#barGraph1").get(0).getContext("2d");
        $("#heading").html("Company Ethnicity - Overall");
        $.get("/company-ethnicity/{{ display_company.company_id }}.json", function (data) {
            var myBarChart = new Chart(ctx_bar_ethnic).Bar(data, options);
            $('#barLegend').html(myBarChart.generateLegend());
        })};

    $.get("/company-ethnicity-tech/{{ display_company.company_id }}.json", function (data) {
        if (data == "False") {
            $(".ethnic-bar-graph2").remove();
            console.log("NO DATA!");
        } else {

            $(".tech-button").append("<button id='tech-button' type='button'>Ethnicity Tech</button>");
            $(".overall-button").append("<button id='overall-button' type='button'>Ethnicity Overall</button>");

            $('#tech-button').click(generateTechBarGraph);
            $('#overall-button').click(generateOverallBarGraph);
        }
    });





// Google News Feed

 google.load("search", "1");

    var newsSearch;

      function searchComplete() {

        // Check that we got results
        document.getElementById('content').innerHTML = '';
        if (newsSearch.results && newsSearch.results.length > 0) {
          for (var i = 0; i < newsSearch.results.length; i++) {

            // Create HTML elements for search results
            var p = document.createElement('p');
            p.classList.add("news-title");
            var a = document.createElement('a');
            var publNameDate = document.createElement('p');
            publNameDate.classList.add("publ-name-date");
            var content = document.createElement('p');
            content.classList.add("news-para");



            a.href= newsSearch.results[i].unescapedUrl;
            a.target = "_blank";
            a.innerHTML = newsSearch.results[i].title;
            publDate = newsSearch.results[i].publishedDate;
            publDate2 = publDate.slice(0,25);
            publName = newsSearch.results[i].publisher + ": ";
            publNameDate.innerHTML = publName.concat(publDate2);
            content.innerHTML = newsSearch.results[i].content;


            // Append search results to the HTML nodes
            p.appendChild(a);
            p.appendChild(publNameDate);
            p.appendChild(content);


            document.body.appendChild(p);

          }
        }
      }

      function onLoad() {

        // Create a News Search instance.
        newsSearch = new google.search.NewsSearch();


        // Set searchComplete as the callback function when a search is
        // complete.  The newsSearch object will have results in it.
        newsSearch.setSearchCompleteCallback(this, searchComplete, null);



        // Specify search quer(ies)
        newsSearch.execute('{{ display_company.name }} tech diversity');


        // Include the required Google branding
        google.search.Search.getBranding('branding');

      }

      // Set a callback to call your code when the page loads
      google.setOnLoadCallback(onLoad);

    $(document).ready(function() {
    $(".btn-pref .btn").click(function () {
    $(".btn-pref .btn").removeClass("btn-primary").addClass("btn-default");
    // $(".tab").addClass("active"); // instead of this do the below
    $(this).removeClass("btn-default").addClass("btn-primary");
    });
    });


    </script>
