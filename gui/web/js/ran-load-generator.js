$( document ).ready( function() {
	refreshActiveSessions();
	refreshCurrentStatus();
});

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

function refreshCurrentStatus()
{
        $.ajax( {
	url: "status/device/192.168.1.1/current",
	success: function(data) {
			data = JSON.stringify(data, null, 2)
			$('#current_status').html('<pre>'+data+'</pre>');
		},
	complete: function() {
			setTimeout(refreshCurrentStatus,5000);	
		}
        });

        return false;
}
