#
# Regular cron jobs for the autoradio package
#
0 4	* * *	root	[ -x /usr/bin/autoradio_maintenance ] && /usr/bin/autoradio_maintenance
