<a name="readme-top"></a>

<div align="right">

  [![Issues][issues-shield]][issues-url]
  [![Build][build-shield]][build-url]
  [![Coverage][coverage-shield]][coverage-url]</a>

</div>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ew2664/culd-app">
    <img src="frontend/src/assets/logo.png" alt="Logo" width="200" height="200">
  </a>

<h3 align="center">CU Lion Dance Hub</h3>

  <p align="center">
    Show Management Software for Columbia University Lion Dance
    <br />
    <a href="#getting-started"><strong>Get started »</strong></a>
    <br />
    <br />
    <a href="https://culd-hub.herokuapp.com/">View Site</a>
    ·
    <a href="https://github.com/ew2664/culd-app/issues">Report Bug</a>
    ·
    <a href="https://github.com/ew2664/culd-app/issues">Request Feature</a>
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

This is a custom show management web application for Columbia University Lion Dance, began in the summer of 2022. Every year, CU Lion Dance receives dozens of performance bookings, each of which requires careful planning and coordination of logistics. Previously, a Google Sheets setup was used for members to register for shows, but this grew increasingly cumbersome with scale and became hard to maintain. Even with Apps Script, it was also not fully customizable to the needs of members. From there, the CU Lion Dance Hub was born.

<div align="center">

  [![Django][Django]][Django-url]
  [![React][React.js]][React-url]
  [![Postgres][Postgres]][Postgres-url]
  [![Apollo-GraphQL][Apollo-GraphQL]][Apollo-GraphQL-url]
  [![Ant-Design][Ant-Design]][Ant-Design-url]
  [![Docker][Docker]][Docker-url]
  [![Heroku][Heroku]][Heroku-url]

</div>


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started
<a name="getting-started"></a>

### Prerequisites

CU Lion Dance Hub requires the following to run:

- [Python][Python-url] 3.9+
- [Node.js][Node-url] 12.13.0+

### Installation
Clone the repository and move to the project directory.
```sh
git clone https://github.com/ew2664/culd-hub.git
cd culd-hub
```
Install the required Python dependencies for the backend.
```sh
cd backend && pip install -r requirements.txt
```
Install the required Node.js dependencies for the frontend.
```sh
cd ../frontend && yarn
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Local Deployment

### Running with Docker Compose
Move to the project directory.
```sh
cd culd-hub
```
Build and run the Docker image.
```sh
docker-compose up --build
```
Or to run it in the background, just add the `-d` option.
```sh
docker-compose up -d --build
```
Navigate to http://localhost:3000/ to see the results.

If you need to stop the containers:
```sh
docker-compose down
```

### Running without Docker Compose
Make sure you have followed the dependency installations under Getting Started.

Make backend migrations, load in dummy data, and start the backend server.
```sh
cd backend/scripts
chmod u+x entrypoint-dev.sh
./entrypoint-dev.sh
```
In a separate shell, move to the frontend directory and start the frontend server.
```sh
cd frontend && yarn start
```
Navigate to http://localhost:3000/ to see the results.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
  
<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://github.com/Ileriayo/markdown-badges -->
[build-shield]: https://img.shields.io/github/workflow/status/ew2664/culd-hub/Django%20CI?style=flat-square
[build-url]: https://github.com/ew2664/culd-hub/actions/workflows/django.yml
[coverage-shield]: https://img.shields.io/codecov/c/github/ew2664/culd-app?style=flat-square&token=XU966851SF
[coverage-url]: https://app.codecov.io/gh/ew2664/culd-app
[issues-shield]: https://img.shields.io/github/issues/ew2664/culd-hub.svg?style=flat-square
[issues-url]: https://github.com/ew2664/culd-hub/issues
[product-screenshot]: images/screenshot.png
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Postgres]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white
[Postgres-url]: https://www.postgresql.org/
[Django]: https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[Ant-Design]: https://img.shields.io/badge/-AntDesign-%230170FE?style=for-the-badge&logo=ant-design&logoColor=white
[Ant-Design-url]: https://ant.design/
[Apollo-GraphQL]: https://img.shields.io/badge/-ApolloGraphQL-311C87?style=for-the-badge&logo=apollo-graphql
[Apollo-GraphQL-url]: https://www.apollographql.com/
[Docker]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[Heroku]: https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white
[Heroku-url]: https://www.heroku.com/
[Python-url]: https://www.python.org/
[Node-url]: https://nodejs.org/en/
[Npm-url]: https://www.npmjs.com/
