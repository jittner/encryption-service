A simple Dockerized app to hash messages and return them via their digest.

To run the Docker container from this Github repo:

docker build https://github.com/jittner/encryption-service.git
docker run -d -p 5000:5000 <built image>

To run the Docker container from Docker hub:
docker run -d -p 5000:5000 jittner/encryption-service

Send requests to:
http://localhost:5000/messages/

POST requests:
JSON body format: {"message": "[your message]"}

Example POST request:
curl -X POST -H "Content-Type: application/json" -d '{"message": "foo"}' http://localhost:5000/messages/

GET requests:
http://localhost:5000/messages/<your hash>

Example GET request:
curl http://localhost:5000/messages/2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae

