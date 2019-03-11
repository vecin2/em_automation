#https://packaging.python.org/tutorials/packaging-projects/
#Run this command below our of the virtual env to make sure 
# local libs are to date
#sudo apt install python3-pip setuptools wheel
#sudo apt install tools wheel
#python3 -m pip install --user --upgrade twine
#Create source distribution
python3 setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
#glasgow team,mote,y classico simbolo

#distribute offline

#https://stackoverflow.com/questions/11091623/python-packages-offline-installation
#The pip download command lets you download packages without installing them:
#
#pip download -r requirements.txt
#
#(In previous versions of pip, this was spelled pip install --download -r requirements.txt.)
#
#Then you can use pip install --no-index --find-links /path/to/download/dir/ -r requirements.txt to install those downloaded sdists, without accessing the network.
