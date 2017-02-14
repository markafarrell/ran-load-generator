function startSession()
{
	post_data = $('#new_session').serialize();
	alert(post_data);

	$.post("sessionControllerServer/session/", post_data, 
	function (data,status,xhr)
	{
		alert(data);
	});

	return false;
}
