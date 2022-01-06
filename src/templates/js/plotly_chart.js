{% macro plotly_chart(data) -%}
    function prop_to_array(rows, prop, fn=(a)=>a) {
        return rows.map((r) => fn(r[prop]));
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
    function onPageLoad(){
        let graphData = {{ data|tojson }};
        Plotly.newPlot("graphDiv",
                        map_data(graphData),
                        {displayModeBar:false});
    }
{%- endmacro %}
