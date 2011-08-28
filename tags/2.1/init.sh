# init db and set admin
./autoradioctrl --syncdb

# create locale files
#django-admin.py makemessages --settings=settings --pythonpath=autoradio -a
#django-admin.py compilemessages --settings=settings --pythonpath=autoradio

# start autoradiod daemon
./autoradiod restart

# run django web server on port 8080
./autoradioweb restart

