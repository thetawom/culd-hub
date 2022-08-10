<a name="readme-top"></a>

<div align="right">

  <a href="https://app.codecov.io/gh/ew2664/culd-app">![Coverage][coverage-shield]</a>

</div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ew2664/culd-app">
    <img src="frontend/src/assets/logo.png" alt="Logo" width="200" height="200">
  </a>

<h3 align="center">CU Lion Dance App</h3>

  <p align="center">
    Show Management Software for Columbia University Lion Dance
    <br />
    <a href="https://github.com/ew2664/culd-app"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ew2664/culd-app">View Demo</a>
    ·
    <a href="https://github.com/ew2664/culd-app/issues">Report Bug</a>
    ·
    <a href="https://github.com/ew2664/culd-app/issues">Request Feature</a>
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

This is a custom show management web application for Columbia University Lion Dance, began in the summer of 2022. Every year, CU Lion Dance receives dozens of performance bookings, each of which requires careful planning and coordination of logistics. Previously, a Google Sheets setup was used for members to register for shows, but this grew increasingly cumbersome with scale and became hard to maintain. Even with Apps Script, it was also not fully customizable to the needs of members. From there, the CULD App was born.

<div align="center">

  [![Django][Django]][Django-url]
  [![React][React.js]][React-url]
  [![Postgres][Postgres]][Postgres-url]
  [![Apollo-GraphQL][Apollo-GraphQL]][Apollo-GraphQL-url]
  [![Ant-Design][Ant-Design]][Ant-Design-url]

</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites
You will need to have Python and Node.js installed to run this project.

### Installation

1. Install the required Python dependencies for the backend.
  ```sh
  cd backend
  pip install -r requirements.txt
  ```
2. Create the SQLite database and run Django migrations with this shell script.
  ```sh
  chmod u+x loaddb.sh
  ./loaddb.sh
  ```
3. Start the backend server.
  ```sh
  python manage.py runserver
  ```
4. In a separate shell, start the frontend server.
  ```sh
  cd frontend
  npm start
  ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>
  
<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://github.com/Ileriayo/markdown-badges -->
[coverage-shield]: https://img.shields.io/codecov/c/github/ew2664/culd-app?style=flat-square&token=XU966851SF
[coverage-url]: https://codecov.io/gh/ew2664/culd-app
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
