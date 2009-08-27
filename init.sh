django-admin.py syncdb --settings=settings --pythonpath=autoradio
django-admin.py makemessages --settings=settings --pythonpath=autoradio -a
django-admin.py compilemessages --settings=settings --pythonpath=autoradio
./autoradiod stop
./autoradiod start
django-admin.py runserver --settings=settings --pythonpath=autoradio 8080
