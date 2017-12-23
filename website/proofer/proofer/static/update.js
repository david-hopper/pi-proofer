update_values()
var myVar = setInverval(update_values(), 1000)

function update_values() {
            $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
            $.getJSON($SCRIPT_ROOT+"/_status",
                function(data) {
                	if (data.status.running) {
                		document.getElementById{"status"}.innerHTML("The chamber is running with a set point of " + data.status.set_point + " F")
                	}
                	else {
                		document.getElementById{"status"}.innerHTML("The chamber is not running with a set point of " + data.status.set_point + " F")
                	}
                }
                );
        }