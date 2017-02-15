function startSession()
{
	post_data = $('#new_session').serialize();

	$.post("session/session/", post_data, 
	function (data,status,xhr)
	{
		alert(data);
	});
	$.post("status/device/192.168.1.1", post_data, 
	function (data,status,xhr)
	{
		alert(data);
	});

	return false;
}
