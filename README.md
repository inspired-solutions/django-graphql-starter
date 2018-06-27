<h1 align="center"><strong>Django with GraphQL Server</strong></h1>

<br />

![](https://cdn-images-1.medium.com/max/1600/1*jLrvxW83rre-25Nrhk-tww.png)



## Getting started
```
#1. Clone the project
git clone git@github.com:inspired-solutions/django-graphql-starter.git

#2. Navigate to new project
cd django-graphql-starter

#3 Install and activate virtual environment
  Linux:
    virtualenv venv -p /usr/bin/python3 
    . venv/bin/activate (linux)
  Windows:
    virtualenv venv -p /c/Python35/python3.exe 
    . venv/Scripts/activate (windows)

#4 Install requirements
  pip3 install -r requirements.txt
```


## Deployment
```
#1. Clone repository in server
- sudo mkdir amae_api
- sudo chown user:user amae_api -R
- cd  amae_api
- git clone project

#2. Create .conf file and modify
- ./makesite.sh <project-name>
- cat /etc/apache2/sites-available/amae-api.inspiredsolutions.pe.conf
- sudo a2ensite amae-api.inspiredsolutions.pe.conf
- sudo apachectl restart
```
