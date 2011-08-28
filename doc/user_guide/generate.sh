rm -r en it 127.0.0.1\:8080

wget -rkL --header='Accept-Charset: iso-8859-2' --header='Accept-Language: en'  http://127.0.0.1:8080/doc/

mv 127.0.0.1\:8080/doc/ en

wget -rkL --header='Accept-Charset: iso-8859-2' --header='Accept-Language: it'  http://127.0.0.1:8080/doc/

mv 127.0.0.1\:8080/doc/ it

rmdir 127.0.0.1\:8080
