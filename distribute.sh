#https://packaging.python.org/tutorials/packaging-projects/
#Run this command below our of the virtual env to make sure 
# local libs are to date
#sudo apt install python3-pip setuptools wheel
#sudo apt install tools wheel
#python3 -m pip install --user --upgrade twine
#Create source distribution
python3 setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
