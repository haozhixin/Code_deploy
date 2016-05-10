set -e
apt-get install -y \
	python-dev \
	python-mysqldb
pip install \
	decorated==1.6.5 \
	Flask==0.10.1 \
	Flask-WTF==0.6 \
	Jinja2==2.7.3 \
	pymongo==2.6.3 \
	pyvmomi==5.5.0.2014.1.1 \
	requests==2.2.1 \
	SQLAlchemy==1.0.11 \
	SQLAlchemy-Dao==1.2.5 \
	uWSGI==2.0.11.2 \
	web.py==0.37\
    	rsa==3.2
