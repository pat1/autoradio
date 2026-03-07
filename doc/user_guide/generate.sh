set -x

rm -r en it 127.0.0.1

wget --convert-links --no-robots --content-on-error  --recursive --no-parent --header='Accept-Charset: iso-8859-2' --header='Accept-Language: en'  http://127.0.0.1:8080/doc/

mv 127.0.0.1/doc/ en

wget --convert-links --no-robots --content-on-error --recursive --no-parent --header='Accept-Charset: iso-8859-2' --header='Accept-Language: it'  http://127.0.0.1:8080/doc/

mv 127.0.0.1/doc/ it

rm -r  127.0.0.1
