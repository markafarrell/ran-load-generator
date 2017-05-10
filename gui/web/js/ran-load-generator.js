$( document ).ready( function() {
	initializeChart();
	refreshActiveSessions();
	refreshCurrentStatus();
	refreshChartData();
});


function updateChartData() {

	//Get current time

	var timeRangeSec = 60;

	var currentTime = new Date();

	var startTime = new Date(currentTime.getTime() - ((timeRangeSec+1) * 1000));

	startTime = new Date(Math.floor(startTime.getTime()/1000)*1000);

	var timeFormatter = d3.timeFormat("%Y%m%d%H%M%S");

	var startTimeString = timeFormatter(startTime); 

	d3.csv("/report/session/all/" + startTimeString, function(error, data) {
		if (error) throw error;

		data.forEach(function(d) {
			d.TIMESTAMP = parseTime(d.TIMESTAMP);
			d.THROUGHPUT = d.THROUGHPUT/1e6;
		});

		var agg_data = d3.nest()
			.key(function(d) { return d.TIMESTAMP; })
			.rollup(function(d) {
				return d3.sum(d, function(g) { return g.THROUGHPUT; });
			}).entries(data)

		agg_data.forEach(function(d) {
			//This may break on Safari
			d.TIMESTAMP = new Date(d.key);
			d.THROUGHPUT = d.value;
		});

		//Map results into dateTimeVector
		var dateTimeVector = Array(timeRangeSec);

		var timeInterval = 1; //Seconds

		for(var i = 0; i<timeRangeSec; i++)
		{
			dateTimeVector[i] = {};
			
			dateTimeVector[i].TIMESTAMP = new Date(startTime.getTime() + timeInterval*1000*(i+1));
			dateTimeVector[i].THROUGHPUT = 0;

			for(var j = 0; j<agg_data.length; j++)
			{
				if(agg_data[j].TIMESTAMP.getTime() == dateTimeVector[i].TIMESTAMP.getTime())
				{
					dateTimeVector[i].THROUGHPUT = agg_data[j].THROUGHPUT;
				}

			}
		}

		// set the ranges
		//var x = d3.scaleTime().range([0, width]);
		//var y = d3.scaleLinear().range([height, 0]);

		//var svg = d3.select("body").transition();
		// Make the changes
		var svg = d3.select("body");

		y.domain([0, d3.max(dateTimeVector, function(d) { return d.THROUGHPUT; })]);
		yAxisGroup.call(yAxis);

		x.domain(d3.extent(dateTimeVector, function(d) { return d.TIMESTAMP; }));
		xAxisGroup.call(xAxis);

		svg.select(".line")   // change the line
			.attr("d", valueline(dateTimeVector));
	});
}

var parseTime;
var valueline;
var x;
var y;
var xAxis;
var yAxis;
var xAxisGroup;
var yAxisGroup;

function initializeChart()
{
	// set the dimensions and margins of the graph
	var margin = {top: 20, right: 20, bottom: 30, left: 50};
		
	width = 960 - margin.left - margin.right;
	height = 500 - margin.top - margin.bottom;

	// append the svg obgect to the body of the page
	// appends a 'group' element to 'svg'
	// moves the 'group' element to the top left margin
	var svg = d3.select("body").append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
	.append("g")
		.attr("transform",
		"translate(" + margin.left + "," + margin.top + ")");

	// parse the date / time
	parseTime = d3.timeParse("%Y-%m-%d %H:%M:%S");

	// set the ranges
	x = d3.scaleTime().range([0, width]);
	y = d3.scaleLinear().range([height, 0]);

	// define the line
	valueline = d3.line()
		.x(function(d) { return x(d.TIMESTAMP); })
		.y(function(d) { return y(d.THROUGHPUT); });

	dateTimeVector = [];

	dateTimeVector[0] = {};
	dateTimeVector[1] = {};

	dateTimeVector[1].TIMESTAMP = new Date();
	dateTimeVector[1].THROUGHPUT = 0;
	
	dateTimeVector[0].TIMESTAMP = new Date(dateTimeVector[1].TIMESTAMP.getTime() - 60000);
	dateTimeVector[0].THROUGHPUT = 10;

	// Scale the range of the data
	x.domain(d3.extent(dateTimeVector, function(d) { return d.TIMESTAMP; }));
	y.domain([0, d3.max(dateTimeVector, function(d) { return d.THROUGHPUT; })]);

	xAxis = d3.axisBottom(x);
	yAxis = d3.axisLeft(y);

	xAxis.tickFormat(d3.timeFormat("%H:%M:%S"));

	// Add the valueline path.
	svg.append("path")
		.data([dateTimeVector])
		.attr("class", "line")
		.attr("d", valueline);
	
	// Add the X Axis
	xAxisGroup = svg.append("g")
		.attr("transform", "translate(0," + height + ")")
		.attr("class", "axis")
		.call(xAxis);

	// Add the Y Axis
	yAxisGroup = svg.append("g")
		.attr("class", "axis")
		.call(yAxis);

	updateChartData();
}

function startSession()
{
	post_data = $('#new_session').serialize();

	$.post("session/session/", post_data, 
	function (data,status,xhr)
	{
		alert(data);
	});

	return false;
}

function startLogging()
{
	post_data = $('#status_logging').serialize();
	modem_ip = $('#modem').val();
	$.post("status/device/" + modem_ip, post_data, 
	function (data,status,xhr)
	{
		alert(data);
	});

	return false;
}

function killSession()
{
	session_id = $('#kill_session_id').val();
	$.ajax({
		url: "session/session/" + session_id,
		type: 'DELETE',
		success: function (result)
		{
			alert("Session Killed!");
		}
	});

	return false;
}

function refreshActiveSessions()
{
        $.ajax( {
	url: "session/sessions/active",
	success: function(data) {
			data = JSON.stringify(data, null, 2)
			$('#current_sessions').html('<pre>'+data+'</pre>');
		},
	complete: function() {
			setTimeout(refreshActiveSessions,5000);	
		}
        });

        return false;
}

function refreshChartData()
{
	updateChartData();
	setTimeout(refreshChartData,1000);	
}

function refreshCurrentStatus()
{
        $.ajax( {
	url: "status/device/192.168.1.1/current",
	success: function(data) {
			data = JSON.stringify(data, null, 2)
			$('#current_status').html('<pre>'+data+'</pre>');
		},
	complete: function() {
			setTimeout(refreshCurrentStatus,30000);	
		}
        });

        return false;
}
