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
        //display first 5 rows
        displayTable(data, 5);

        //groupby model year and count 
        var countByModelYear = d3.nest()
          .key(function(d) { return d['model-year'];})
          .rollup(function(dd) { 
          return d3.sum(dd, function(g) {return 1; });
          })
          .entries(data)
          .map(function(data) {
            return {
              'model': data.key,
              'count': data.value,
            }
          });

        displayTable(countByModelYear, null);

        //groupby model year and sum by cylinders
        var countByModelYearCylinder = d3.nest()
            .key(function(d) { return d['model-year'];})
            .rollup(function(dd) { 
              return d3.sum(dd, function(d) {return d.cylinders; });
            })
            .entries(data)
            .map(function(data) {
              return {
                'number of cylinders': data.key,
                'total count': data.value,
              }
            });

        displayTable(countByModelYearCylinder, null);

        //groupby acceleration and count
        var countByAccelerationCount = d3.nest()
            .key(function(d) { return d.acceleration;})
            .rollup(function(dd) { 
              return d3.sum(dd, function(d) {return 1; });
            })
            .entries(data)
            .map(function(data) {
              return {
                'acceleration': data.key,
                'count': data.value,
              }
            });
        countByAccelerationCount.sort(function(x, y){
               return d3.ascending(x.acceleration, y.acceleration);
            })

        displayTable(countByAccelerationCount, null);


      })