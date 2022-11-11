# Instagram-Analytics

Django based web application that can be deployed as a Docker container used to analyze the data of an Instagram account. The application offers the possibility to upload an archive containing the data of an Instagram account in JSON format, in English. The user can then get insights about their followers, followings, mutual followers, accounts that don't follow them back, and accounts they don't follow back. For the followers analytics part, the user can also search for accounts in each of these categories by username. The application is based on the [Django](https://www.djangoproject.com/) web framework and uses [Docker](https://www.docker.com/) to deploy the application. The main framework used for the frontend is [Bootstrap](https://getbootstrap.com/).

## Container Deployment and Usage

The container can be deployed and run using the following commands:

```
docker build --tag instagram-analytics .
docker run -d --name instagram-analytics -p 80:8000 instagram-analytics
```

After the container is deployed, the application can be accessed at [http://localhost](http://localhost).
