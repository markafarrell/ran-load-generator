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
