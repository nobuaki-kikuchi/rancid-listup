#! /bin/bash

HOME="/usr/local/rancid/var/ker-nw/configs"
COUNT=`/bin/ls -1 /usr/local/rancid/var/ker-nw/configs/*.*.*.*[0-9] |wc -l`
TCOUNT=`egrep -v '!|#' configs/*.*.*.*[0-9] |wc -l`
ACLCOUNT=`egrep -v '!|#' configs/*.*.*.*[0-9] | egrep 'permit|deny'|wc -l`
ACLPCOUNT=`egrep -v '!|#' configs/*.*.*.*[0-9] | egrep 'permit'|wc -l`
ACLDCOUNT=`egrep -v '!|#' configs/*.*.*.*[0-9] | egrep 'deny'|wc -l`

newcount=`/bin/ls -1 /usr/local/rancid/var/ker-nw/configs/* | grep new |wc -l`

if test $newcount -gt 0
then
ATTENTION="<FONT COLOR=red size=-1><BLINK> << ATTENTION!! Now Searching! >></BLINK></FONT>"
fi

cat << EOF
content-type: text/html

<html><head>
<meta http-equiv="refresh" content="3600">
<title>KIS Config List</title>
<style type="text/css">
body {background-color: #ffffff; color: #000000;}
body, td, th, h1, h2 {font-family: sans-serif;}
table {border-collapse: collapse;}
.center th { text-align: center !important; }
td, th { border: 1px solid #000000; font-size: 75%; vertical-align: baseline;}
.e {background-color: #ccccff; font-weight: bold; color: #000000;}
.h {background-color: #9999cc; font-weight: bold; color: #000000;}
.v {background-color: #cccccc; color: #000000;}
</style>
</head><body>


<h2>KIS Config List $ATTENTION</h2>

<p>
<h4>Managed config <font color="red"><b>$COUNT</b></font> files</h4>
<h4>Total config <font color="red"><b>$TCOUNT</b></font> lines</h4>
<h4>Total ACL <font color="red"><b>$ACLCOUNT</b></font> lines (permit <font color="red"><b>$ACLPCOUNT</b></font>/deny <font color="red"><b>$ACLDCOUNT</b></font>)</h4>
</p>
</p>
<h3>Send to IT Project Planning and Development Department Team3 [*********] by e-mail all configs!
<form action="http://127.0.0.1/ker-nw/config_send.cgi"
method="post"> <input type="submit" value="send">
</form>
</h3>

<table border="0" cellpadding="3" width="600">
<tr class="h">
	<th>No.</th>
	<th>IP Address</th>
	<th>HOST Name</th>
</tr>

<tr>
EOF

egrep -m 1 \(^hostname\|^"set system name"\|^"set hostname"\|"host-name"\) $HOME/*[0-9] \
	| sed -e "s/\;//g" \
	| sed -e "s/\"//g" \
	| awk -F/ '{print $8}' \
	| awk -F: '{print $1"\t"$2}' \
	| sort -t. -k1,1n -k2,2n -k3,3n -k4,4n \
	| awk  '{print "<td>"NR"</td><td class=\"e\"><a href=/ker-nw/configs/"$1">"$1"</td><td class=\"v\">"$NF"</td></tr>"}'


cat << EOF

</table></body></html>

EOF

