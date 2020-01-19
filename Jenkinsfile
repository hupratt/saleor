

def labels = ['master','slave'] 
def builders = [:]
for (x in labels) {
    def label = x // Need to bind the label variable before the closure 

    // Create a map to pass in to the 'parallel' step so we can fire all the builds at once
    builders[label] = {
		timestamps {
			node () {
				
				def PROJECT="/home/ubuntu/Dev/saleor"
				def PYTHON_P="$PROJECT/bin/python3.6"
				def GET_SECRET="/var/lib/jenkins/run_vars_saleor.py"
				
				
				stage ('Checkout') {
					// checkout scm
					sh """ 
					whoami
					uname -a
					sudo chmod -R 770 $PROJECT
					sudo chown -R ubuntu:www-data $PROJECT
					cd $PROJECT
					sudo git fetch --all
					sudo git reset --hard origin/master
					"""
				}

				stage ('Build') {
					
					sh """ 
					cd $PROJECT
					sudo service apache2 stop
					# sudo virtualenv -p python3 .
					. bin/activate
					echo 'which python are you running?'
					which python
					cd src

					sudo $PYTHON_P -m pip install --upgrade pip # Upgrade pip
					echo 'pip upgrade done'
					$PYTHON_P -m pip install -r REQUIREMENTS.txt # Install or upgrade dependencies
					echo 'pip install done'
					sudo $PYTHON_P $GET_SECRET
					echo 'var import done'

					# sudo $PYTHON_P manage.py createcachetable cache_table

					#$PYTHON_P manage.py makemigrations                  

					#$PYTHON_P manage.py migrate                  
					echo 'manage.py migrate done'

					sudo $PYTHON_P manage.py compilemessages --settings=la_petite_portugaise.settings 
					echo 'manage.py compilemessages done'

					sudo $PYTHON_P manage.py collectstatic --noinput  # Collect static files
					echo 'manage.py collectstatic done'

					sudo $PYTHON_P manage.py check --deploy
					deactivate # quit the virtual environment

					sudo service apache2 start

					""" 
				}

			}
		}
	}
}

throttle(['loadbalancer']) {
  parallel builders
}




