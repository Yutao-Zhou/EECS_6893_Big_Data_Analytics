 function displayTable(data, displayRows){
        if (displayRows==null) {
            var slicedData = data;
          }
        else {var slicedData = data.slice(0, displayRows);}
        
        var table = d3.select('body').append('table')
        var thead = table.append('thead')
        var tbody = table.append('tbody')

        thead.selectAll('th')
          .data(d3.map(slicedData[0]).keys())
          .enter()
          .append('th')
          .text(function (d) { return d });

        var rows = tbody.selectAll('tr')
          .data(slicedData)
          .enter()
          .append('tr');

        var cells = rows.selectAll('td')
          .data(function(row) {return d3.map(row).values(); })
          .enter()
          .append('td')
          .text(function (d) { return d })

      }

      d3.csv('https://raw.githubusercontent.com/plotly/datasets/master/auto-mpg.csv',function (data) {

        //#### Start of 2.2.1 pie chart ####
        //groupby model year and count 
        var pieData = d3.nest()
          .key(function(d) { return d['model-year'];})
          .rollup(function(dd) { 
          return d3.sum(dd, function(g) {return 1; });
          })
          .entries(data)

        var countByModelYear = pieData
          .map(function(d) {
            return {
              'Model Year': d.key,
              'Count': d.value,
            }
          });
        
        var width = 400,
        height = 410,
        radius = (Math.min(width, height)-50) / 3;

        var color = d3.scaleOrdinal(d3.schemeCategory10);

        var arc = d3.arc()
          .outerRadius(radius - 10)
          .innerRadius(0);

        var pie = d3.pie()
          .sort(null)
          .value(function(d) {
            return d.value;
          });

        var svg = d3.select("body")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
              .append("g")
              .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

        svg.append("text")
            .attr("x", 0)             
            .attr("y", width / 2)
            .attr("text-anchor", "middle")  
            .style("font-size", "16px") 
            .style("text-decoration", "underline")  
            .text("Pie Chart of distribution of the model years");

        //total count for percentage calculation
        var total = d3.sum(pieData, function(d) { 
                return d.value; 
              });

        //percentage calculation
        pieData.forEach(function(d) {
                  d.percentage = (d.value  / total * 100).toFixed(2);
          });

        var g = svg.selectAll(".arc")
          .data( pie(pieData) )
          .enter()
            .append("g")
            .attr("class", "arc");

        g.append("path")
          .attr("d", arc)
          .style("fill", function(d) {
            return color(d.data.key);
          });

        g.append("text")
          .attr("transform", function(d) {
            var _d = arc.centroid(d);
            _d[0] *= 2.7;
            _d[1] *= 2.7;
            return "translate(" + _d + ")" 

          })
          .attr("dy", ".35em")
          .style("text-anchor", "middle")
          .text(function(d) {
            return d.data.key;
          });
        
        g.append("text")
          .attr("transform", function(d) {
            var _d = arc.centroid(d);
            _d[0] *= 2.7;
            _d[1] *= 2.7;
            return "translate(" + _d + ")" 

          })
          .attr("dy", "2.0em")
          .style("text-anchor", "middle")
          .text(function(d) {
            return d.data.percentage + '%';
          });

        displayTable(countByModelYear, null);

        //#### Start of 2.2.2 line chart ####
        //groupby model year and sum by cylinders
        var lineGraph = d3.nest()
            .key(function(d) { return d['model-year'];})
            .rollup(function(dd) { 
              return d3.sum(dd, function(d) {return d.cylinders; });
            })
            .entries(data)

        var countByModelYearCylinder = lineGraph
            .map(function(data) {
              return {
                'Model Year': data.key,
                'Number of Cylinders': data.value,
              }
            });

        var margin = {top: 20, right: 50, bottom: 50, left: 60},
            width = 600 - margin.left - margin.right,
            height = 337.5 - margin.top - margin.bottom;

        var svg = d3.select("body")
          .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform",
                  "translate(" + margin.left + "," + margin.top + ")");
        
        var parseTime = d3.timeParse("%y");
        lineGraph.forEach(function(d) {d.key = parseTime(d.key)})

        lineGraph.sort(function(x, y){
               return d3.descending(x.key, y.key);
            })

        var x = d3.scaleTime()
          .domain(d3.extent(lineGraph, function(d) { return d.key; }))
          .range([width, 0]);
        svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));
        svg.append("text")             
          .attr("transform",
                "translate(" + (width/2) + " ," + 
                               (height + margin.top + 20) + ")")
          .style("text-anchor", "middle")
          .text("Model Year");

        var y = d3.scaleLinear()
          .domain([0, d3.max(lineGraph, function(d) { return +d.value; })])
          .range([ height, 0 ]);
        svg.append("g")
          .call(d3.axisLeft(y));
        svg.append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 0 - margin.left)
          .attr("x",0 - (height / 2))
          .attr("dy", "1em")
          .style("text-anchor", "middle")
          .text("Total number of Cylinders");

        svg.append("path")
          .datum(lineGraph)
          .attr("fill", "none")
          .attr("stroke", "steelblue")
          .attr("stroke-width", 1.5)
          .attr("d", d3.line()
            .x(function(d) { return x(d.key) })
            .y(function(d) { return y(d.value) })
            )

        displayTable(countByModelYearCylinder, null);

        //#### Start of 2.2.3 histogram ####
        //groupby acceleration and count
        var histogramData = d3.nest()
            .key(function(d) { return d.acceleration;})
            .rollup(function(dd) { 
              return d3.sum(dd, function(d) {return 1; });
            })
            .entries(data)

        var countByAccelerationCount = histogramData
            .map(function(data) {
              return {
                'Acceleration': data.key,
                'Count': data.value,
              }
            });

        countByAccelerationCount.sort(function(x, y){
               return d3.ascending(x.acceleration, y.acceleration);
            })

        var margin = {top: 20, right: 50, bottom: 50, left: 60},
            width = 600 - margin.left - margin.right,
            height = 337.5 - margin.top - margin.bottom;

        var svg = d3.select("body")
          .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform",
                  "translate(" + margin.left + "," + margin.top + ")");

            var x = d3.scaleLinear()
              .domain([6,28])
              .range([0, width]);
            svg.append("g")
              .attr("transform", "translate(0," + height + ")")
              .call(d3.axisBottom(x));
            svg.append("text")             
              .attr("transform",
                    "translate(" + (width/2) + " ," + 
                                   (height + margin.top + 20) + ")")
              .style("text-anchor", "middle")
              .text("Acceleration");

            var histogram = d3.histogram()
              .value(function(d) { return d.acceleration; })
              .domain(x.domain())
              .thresholds(x.ticks(10));

            var bins = histogram(data);
            console.log(bins)
            var y = d3.scaleLinear()
              .domain([0, d3.max(bins, function(d) { return d.length; })])
              .range([height, 0])
            svg.append("g")
              .text("Number of days")
              .call(d3.axisLeft(y));
            svg.append("text")
              .attr("transform", "rotate(-90)")
              .attr("y", 0 - margin.left)
              .attr("x",0 - (height / 2))
              .attr("dy", "1em")
              .style("text-anchor", "middle")
              .text("Number of cars");  

            svg.selectAll("rect")
              .data(bins)
              .enter()
              .append("rect")
                .attr("x", 1)
                .attr("transform", function(d) { return "translate(" + x(d.x0) + "," + y(d.length) + ")"; })
                .attr("width", function(d) { return x(d.x1) - x(d.x0) -1 ; })
                .attr("height", function(d) { return height - y(d.length); })
                .style("fill", "#69b3a2")

        displayTable(countByAccelerationCount, null);

      })