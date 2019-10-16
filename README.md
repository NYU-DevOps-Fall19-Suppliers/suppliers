# NYU DevOps Project - Suppliers

###  Project description
The purpose of this project is to develop a suppliers system for an eCommerce web site backend as a collection RESTful services for a client by adopting DevOps methodology.  

###  Current build
This build is for Sprint 2, intended for the Wednesday, October 16 2019 due date.

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

The recommend

### Running Tests
To run the tests please run the following commands:
```
 git clone https://github.com/nyu-devops-fall19-suppliers/suppliers
 cd suppliers
 vagrant up
 vagrant ssh
 cd /vagrant
 nosetests
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

Then the service will available at: http://0.0.0.0:2333/suppliers

### Built using:

  * [MongoDB](https://www.mongodb.com/) - MongoDB is a document database
  * [MongoEngine](http://mongoengine.org/) - a Python Object-Document Mapper for working with MongoDB.
  * [Nose](https://nose.readthedocs.io/en/latest/) - Better python testing
