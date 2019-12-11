# NYU DevOps Project - Suppliers

[![codecov](https://codecov.io/gh/nyu-devops-fall19-suppliers/suppliers/branch/master/graph/badge.svg)](https://codecov.io/gh/nyu-devops-fall19-suppliers/suppliers)
[![Build Status](https://travis-ci.org/nyu-devops-fall19-suppliers/suppliers.svg?branch=master)](https://travis-ci.org/nyu-devops-fall19-suppliers/suppliers)
###  Project description
The purpose of this project is to develop a suppliers system for an eCommerce web site backend as a collection RESTful services for a client by adopting DevOps methodology. The final app is hosted on IBM Cloud with CI Delivery Pipeline. 

###  Current build
This build is for Sprint 5, intended for the Wednesday, December 11 2019 due date.

###  How to access
Running on IBM Cloud in Prod: ([App Dashboard Here](https://cloud.ibm.com/apps/26425664-2ad6-4530-9f90-34f3db94ab89?paneId=overview&ace_config=%7B%22region%22%3A%22us-south%22%2C%22crn%22%3A%22crn%3Av1%3Abluemix%3Apublic%3Aconsole%3Aus-south%3A%3A%3Acf-application%3A26425664-2ad6-4530-9f90-34f3db94ab89%22%2C%22resource_id%22%3A%2226425664-2ad6-4530-9f90-34f3db94ab89%22%2C%22orgGuid%22%3A%22b32dcdd5-5ed4-4ef2-8bab-d7f5a1bed0fd%22%2C%22spaceGuid%22%3A%221ae8be47-5cea-49ce-a42e-64e0971e80cd%22%2C%22redirect%22%3A%22https%3A%2F%2Fcloud.ibm.com%2Fresources%22%2C%22bluemixUIVersion%22%3A%22v6%22%7D&env_id=ibm:yp:us-south))   
https://nyu-suppliers-service-f19.mybluemix.net/   

Running on IBM Cloud in Dev: ([App Dashboard Here](https://cloud.ibm.com/apps/8c351474-e035-4014-8b6c-3ad0cd6be9cf?paneId=overview&ace_config=%7B%22orgGuid%22%3A%22b32dcdd5-5ed4-4ef2-8bab-d7f5a1bed0fd%22%2C%22spaceGuid%22%3A%2204916097-fe05-4194-a682-279f38ebb26c%22%2C%22bluemixUIVersion%22%3A%22v6%22%2C%22redirect%22%3A%22https%3A%2F%2Fcloud.ibm.com%2Fservices%2Fcloudantnosqldb%2F4cdafb12-2774-493f-89f6-a402355dc872%3FpaneId%3Dconnected-objects%22%7D&env_id=ibm:yp:us-south))   
https://nyu-suppliers-service-f19-dev.mybluemix.net/   

DevOps Pipeline in IBM Cloud:  
https://cloud.ibm.com/devops/pipelines/74638c62-616b-4ef0-b8e7-d8db2bf6c0a3?env_id=ibm:yp:us-south  
 
### Features supported
 Seven paths:
 ------
 GET /suppliers - Returns a list all of the suppliers  
 GET /suppliers/<string:supplierID> - Returns the supplier with a given id number  
 POST /suppliers - creates a new supplier record in the database  
 PUT /suppliers/<string:supplierID> - updates a supplier record in the database  
 DELETE /suppliers/<string:supplierID> - deletes a supplier record in the database  
 QUERY /suppliers/ - query the database by the name of the supplier  
 ACTION /suppliers/<string:productId>/recommend - query the database for suppliers that serve a certain product with a average rating of 3 or above

<string:supplierID> is a string of 24 hexadecimal characters eg: 4f4381f4e779897a2c000009

The recommend: Enter the ID of the product of which you'd like to get remmended suppliers. 

### Running Tests
To run the TDD tests please run the following commands:
```
 git clone https://github.com/nyu-devops-fall19-suppliers/suppliers
 cd suppliers
 vagrant up
 vagrant ssh
 cd /vagrant
 nosetests
```
To run the BDD tests please run the following commands:
```
 git clone https://github.com/nyu-devops-fall19-suppliers/suppliers
 cd suppliers
 vagrant up
 vagrant ssh
 cd /vagrant
 honcho start &
 behave
```

### Running the Flask App:
To run the Flask app to create an interactive version of the API, please follow these steps:

```
 vagrant up
 vagrant ssh
 cd /vagrant
 nosetests
 FLASK_APP=service:app flask run -h 0.0.0.0
```

Then the service will available at: http://127.0.0.1:5000/suppliers

### Running Pylint:
```
vagrant up
vagrant ssh
cd /vagrant
pylint --rcfile=pylint.conf service/*.py
pylint --rcfile=pylint.conf tests/*.py
````

### Built using:

  * [MongoDB](https://www.mongodb.com/) - MongoDB is a document database
  * [MongoEngine](http://mongoengine.org/) - a Python Object-Document Mapper for working with MongoDB.
  * [Nose](https://nose.readthedocs.io/en/latest/) - Better python testing
