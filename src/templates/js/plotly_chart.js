
{% macro plotly_chart(data) -%}

    function prop_to_array(rows, prop, fn = null) {
        if (fn == null) {
            return rows.map((r) => r[prop]);
        }
        else {
            return rows.map((r) => fn(r[prop]));
        }
    }
    function map_data(rows) {
        bike_data = {
            x: prop_to_array(rows, "crash_year"),
            y: prop_to_array(rows, "bike_crash"),
            name: "Bike Crashes",
            mode: "markers",
            type: "scatter",
            marker: {
                size: prop_to_array(rows, "fatal"),
                opacity: 0.8
            }
        };
        injury_data = {
            x: prop_to_array(rows, "crash_year"),
            y: prop_to_array(rows, "injury"), 
            name: "Injuries",
            mode: "markers",
            type: "scatter",
            marker: {
                size: prop_to_array(rows, "fatal"),
                opacity: 0.6,
                color: "green"
            }
        };
        return [bike_data, injury_data];
    }
    
    function addPlotwFetch(){
        var base_url = `https://phl.carto.com/api/v2/sql?q=`;
        var query =
                `SELECT crash_year` +
                `, sum(fatal_count) AS fatal` +
                `, sum(injury_count) AS injury` +
                `, sum(bicycle_count) as bike_crash` +
                ` FROM crash_data_collision_crash_2007_2017 ` +
                ` GROUP BY 1`;
    
        let url = base_url + query;
        console.log(url);
        let plot = document.getElementById("graphDiv");
        
        fetch(url)
                .then(r => r.json())
                .then(d => d.rows)
                .then(map_data)
                .then(d => Plotly.newPlot("graphDiv", d));
    }
    
    function onPageLoad(){
        let graphData = {{ data|tojson }};
            Plotly.newPlot("graphDiv", map_data(graphData),
                    {displayModeBar:false});
    }
{%- endmacro %}
