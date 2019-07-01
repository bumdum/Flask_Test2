
var width = 300,
    height = 300,
    radius = Math.min(width, height) / 1.9,
    spacing = .09,
    r = 0;

$SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
var races = {{ g.races|safe }};

document.getElementById("raceName").innerHTML =  races[r].n;
var fastestLaps; 
getFastestLaps();

var color = d3.scale.linear()
    .range(["hsl(-180,60%,50%)", "hsl(180,60%,50%)"])
    .interpolate(function(a, b) { var i = d3.interpolateString(a, b); return function(t) { return d3.hsl(i(t)); }; });

var arcBody = d3.svg.arc()
    .startAngle(0)
    .endAngle(function(d) { return d.value * 2 * Math.PI; })
    .innerRadius(function(d) { return d.index * radius; })
    .outerRadius(function(d) { return (d.index + spacing) * radius; })
    .cornerRadius(6);

var arcCenter = d3.svg.arc()
    .startAngle(0)
    .endAngle(function(d) { return d.value * 2 * Math.PI; })
    .innerRadius(function(d) { return (d.index + spacing / 2) * radius; })
    .outerRadius(function(d) { return (d.index + spacing / 2) * radius; });

var svg = d3.select("div#fastest_laps_container").append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("viewBox", "0 0 300 300")
    .attr("perserveAspectRatio", "xMinYMid")
    .classed("svg-content", true)
  .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

var field = svg.selectAll("g")
    .data(fields)
  .enter().append("g");

field.append("path")
    .attr("class", "arc-body");

field.append("path")
    .attr("id", function(d, i) { return "arc-center-" + i; })
    .attr("class", "arc-center");

field.append("text")
    .attr("dy", ".35em")
    .attr("dx", ".75em")
    .style("text-anchor", "start")
  .append("textPath")
    .attr("startOffset", "50%")
    .attr("class", "arc-text")
    .attr("xlink:href", function(d, i) { return "#arc-center-" + i; });

tick();

d3.select(self.frameElement).style("height", height + "px");

function tick() {
  var l = 0;
  if (!document.hidden) field
      .each(function(d) { this._value = d.value; })
      .data(fields)
      .each(function(d) { d.previousValue = this._value;})
    .transition()
      .ease("elastic")
      .duration(500)
      .each(fieldTransition)
      .each('end', function(d){
        if(d.previousValue === 0)
        {
          if(d.index === .8)
          {
            console.log(r + " index: " + d.index);
            getFastestLaps();
            document.getElementById("raceName").innerHTML =  races[r].n;
            r++;
            if(r >= 21)
            {
              r = 0;
            }
          }
        }
      });

  setTimeout(tick, 1000 - Date.now() % 1000);
}

function fieldTransition() {
  var field = d3.select(this).transition();

  field.select(".arc-body")
      .attrTween("d", arcTween(arcBody))
      .style("fill", function(d) { return color(d.value); });

  field.select(".arc-center")
      .attrTween("d", arcTween(arcCenter));

  field.select(".arc-text")
      .text(function(d) { return d.text; });
}

function arcTween(arc) {
  return function(d) {
    var i = d3.interpolateNumber(d.previousValue, d.value);

    return function(t) {
      d.value = i(t);
      return arc(d);
    };
  };
}

function getFastestLaps() {
  $.getJSON($SCRIPT_ROOT + '/get_fastest_laps', {
        a: races[r].r
      }, function(data) {
        fastestLaps = data;
      })
  .fail(function(e) {
    console.log(e);
  })
}

function fields() {
  var now = new Date;
  var first, second, third;

  if(fastestLaps)
  {
    first = fastestLaps[0].n + " " + fastestLaps[0].t;
    second = fastestLaps[1].n + " " + fastestLaps[1].t;
    third = fastestLaps[2].n + " " + fastestLaps[2].t;
  }

  return [
    {index: .8, text: '3rd ' + third, value: now.getSeconds() / 26},
    {index: .7, text: '2nd ' + second, value: now.getSeconds() / 23},
    {index: .6, text: '1st ' + first, value: now.getSeconds() / 20},
  ];
}