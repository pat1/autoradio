# init db and set admin
django-admin.py syncdb --settings=settings --pythonpath=autoradio

# create locale files
#django-admin.py makemessages --settings=settings --pythonpath=autoradio -a
#django-admin.py compilemessages --settings=settings --pythonpath=autoradio

# start autoradiod daemon
./autoradiod stop
./autoradiod start

# run django web server on port 8080
django-admin.py runserver --settings=settings --pythonpath=autoradio 8080
