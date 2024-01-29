# Volunteer Management System

> This is a Flask-built API to maintain experience hours and related information
for users that are volunteers or admin of a health clinic.

<br />
<!-- PROJECT LOG -->
<div align="center">
  <p align="center">
    <a href="https://github.com/ari-denary/volunteer-management-backend"><strong>Explore the docs »</strong></a>
    <br />
    <a href="https://github.com/ari-denary/volunteer-management-backend">View Demo</a>
    ·
    <a href="https://github.com/ari-denary/volunteer-management-backend/issues">Report Bug</a>
    ·
    <a href="https://github.com/ari-denary/volunteer-management-backend/issues">Request Feature</a>
  </p>
</div>

<br />

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<br />
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <!-- <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li> -->
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<br />

<!-- ABOUT THE PROJECT -->
## About the Project

This is an API for managing volunteers and their experience hours.

<p align="right">(<a href="#volunteer-management-system">back to top</a>)</p>


### Built With

* [![Flask][Flask.com]][Flask-url]

<p align="right">(<a href="#volunteer-management-system">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

<!-- To get a local copy up and running, follow these steps -->

<!-- ### Prerequisites

* npm
  ```sh
  npm install npm@latest -g
  ``` -->

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/ari-denary/volunteer-management-backend.git
   ```

2. cd into project folder in terminal window

3. Create a virtual environment
```shell
python3 -m venv venv
```

4. Activate venv
```shell
source venv/bin/activate
```

5. Install in `venv` all items from `requirements.txt`
```shell
pip3 install -r requirements.txt
```

8. Run Flask
```shell
flask run
```

<p align="right">(<a href="#volunteer-management-system">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

The API contains the following routes that receive and return JSON.

### POST `/auth/signup`

- Handles user signup. Expects JSON:
```json
    {
        "badge_number":"1",
        "email":"sample@mail.com",
        "password":"password",
        "first_name":"sample",
        "last_name":"user",
        "dob":"datetime.datetime(2000, 1, 1, 0, 0)",
        "gender":"Prefer not to say",
        "address":"123 Cherry lane",
        "city":"New York",
        "state":"NY",
        "zip_code":"11001",
        "phone_number":"9991234567",
        "is_student":"true",
        "is_healthcare_provider": "false",
        "is_multilingual":"false"
    }
```

- Returns JSON:
```json
    { "token": "dleoidlksd.aslkfjoiweflkfj.aldsjfoweifsldf" }
```


### POST `/auth/login`

- Handles user login. Expects JSON:
```json
    { "email": "mail@mail.com", "password": "mypassword" }
```

- Returns JSON:
```json
    { "token": "dleoidlksd.aslkfjoiweflkfj.aldsjfoweifsldf" }
```


### GET `/users`

- Gets all users.
- Authorization: must be admin requesting with valid token.
- Returns JSON:
```json
    {
        "users": [{
            "id": 1,
            "email": "admin@mail.com",
            "experience_hours": 10,
            "badge_number": 100,
            "first_name": "first",
            "last_name": "user",
            "is_admin": False,
            "is_student": True,
            "is_healthcare_provider": False,
            "is_multilingual": False,
            "status": "new"
        } ... ]
    }
```

### GET `/users/user_id`

- Gets a user by id.
- Authorization: must be same user or admin requesting with valid token.
- Returns JSON:
```json
    {
        "user": {
            "id": 1,
            "email": "admin@mail.com",
            "school_email": "joe@school.edu",
            "badge_number": 100,
            "first_name": "first",
            "last_name": "user",
            "dob": "Sat, 01 Jan 2000 00:00:00 GMT",
            "gender": "male",
            "pronouns": "he/him",
            "race": "white",
            "ethnicity": "caucasian",
            "created_at": "Sun, 21 May 2023 20:12:14 GMT",
            "phone_number": "9991234567",
            "phone_carrier": "verizon",
            "address": "123 Cherry lane",
            "city": "New York",
            "state": "NY",
            "zip_code": "11001",
            "is_admin": false,
            "is_multilingual": false,
            "is_student": true,
            "type_of_student": "full-time",
            "school": "Oklahoma State",
            "anticipated_graduation": "Sun, 19 May 2025 20:12:14 GMT",
            "major": "Biology",
            "minor": null,
            "classification": null,
            "degree": "B.S.",
            "is_healthcare_provider": false,
            "type_of_provider": null,
            "employer": null,
            "is_multilingual": false,
            "status": "new",
        }
    }
```

### GET `users/user_id/experiences`

- Gets all experiences for a user. Optional query parameter of 'incomplete' will return all experiences whose sign_out_time is None. Primary use case for 'incomplete' is for getting experience(s) to "sign out".
- Authorization: must be same user or admin requesting with valid token.
- Returns JSON:
```json
    {
        "user_experiences": [{
            "id": 1,
            "date": "2023-04-06-08:35:12:23",
            "sign_in_time": "2023-04-06-08:35:12:23",
            "sign_out_time": "2023-04-06-08:35:12:23",
            "department": "lab",
            "user_id": 3
        } ... ]
    }
```

### GET `users/user_id/languages`

- Gets all languages for a user.
- Authorization: must be same user or admin requesting with valid token.
- Returns JSON:
```json
    {
        "user_languages": [{
            "id": 1,
            "language": "spanish",
            "fluency": "proficent",
            "user_id": 3
        } ... ]
    }
```

### GET `/experiences`
- Gets all experiences for all users. Optional query parameter of 'incomplete' will return all experiences whose sign_out_time is None.
  - Primary use case for 'incomplete' is to check any experiences that have not "signed out".
- Authorization: must be admin requesting with valid token.
- Returns JSON:
```json
   {
        "user_experiences": [{
            "id": 1,
            "date": "2023-04-06-08:35:12:23",
            "sign_in_time": "2023-04-06-08:35:12:23",
            "sign_out_time": "2023-04-06-08:35:12:23",
            "department": "lab",
            "user_id": 3
        } ... ]
    }
```

### POST `/experiences`
- Create a new experience. Use case for "signing-in" to an experience.
- Authorization: must be same user or admin requesting with valid token.
- Accepts JSON - "date", "sign_in_time", "department", "user_id" required
                "sign_out_time" optional
```json
  {
      "date": "2022-01-05 00:00:00",
      "sign_in_time": "2022-01-05 08:00:00",
      "department": "lab",
      "user_id": 3
  }
```

- Returns JSON:
```json
  {
      "user_experience": {
          "id": 1,
          "date": "2022-01-05 00:00:00",
          "sign_in_time": "2022-01-05 08:00:00",
          "sign_out_time": "None",
          "department": "lab",
          "user_id": 3
      }
  }
```

### PATCH `/experiences/<int:exp_id>`
- Update a user's experience sign out time and/or department.
- Use case for "signing-out" of an experience.
- Authorization: must be same user or admin requesting with valid token.
- Accepts JSON - "sign_out_time" required,
                "department" optional
```json
{
    "sign_out_time": "2023-04-06-08:35:12:23",
    "department": "pharmacy"
}
```

- Returns JSON
```json
  {
      "experience": {
          "id": 1,
          "date": "2023-04-06-08:35:12:23",
          "sign_in_time": "2023-04-06-08:35:12:23",
          "sign_out_time": "2023-04-06-08:35:12:23",
          "department": "pharmacy",
          "user_id": 3
      }
  }
```

<p align="right">(<a href="#volunteer-management-system">back to top</a>)</p>

## Tests

To run tests:

```python
FLASK_DEBUG=False python -m unittest test_filename.py
```

<!-- ROADMAP -->
## Roadmap

- [ ] Refactor JSON validation to use json schema while maintaining current level of datetime validation

See the [open issues](https://github.com/ari-denary/volunteer-management-backend/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#volunteer-management-system">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#volunteer-management-system">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#volunteer-management-system">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Ari Denary - [adenary.dev@gmail.com](mailto:adenary.dev@gmail.com) - [LinkedIn][linkedin-url]


Project Link: [https://github.com/ari-denary/volunteer-management-backend](https://github.com/ari-denary/volunteer-management-backend)

<p align="right">(<a href="#volunteer-management-system">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
<!-- ## Acknowledgments

* []()
* []()
* []() -->

<!-- <p align="right">(<a href="#volunteer-management-system">back to top</a>)</p> -->



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ari-denary/volunteer-management-backend.svg?style=for-the-badge
[contributors-url]: https://github.com/ari-denary/volunteer-management-backend/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ari-denary/volunteer-management-backend.svg?style=for-the-badge
[forks-url]: https://github.com/ari-denary/volunteer-management-backend/network/members
[stars-shield]: https://img.shields.io/github/stars/ari-denary/volunteer-management-backend.svg?style=for-the-badge
[stars-url]: https://github.com/ari-denary/volunteer-management-backend/stargazers
[issues-shield]: https://img.shields.io/github/issues/ari-denary/volunteer-management-backend.svg?style=for-the-badge
[issues-url]: https://github.com/ari-denary/volunteer-management-backend/issues
[license-shield]: https://img.shields.io/badge/License-MIT-41acc0?style=for-the-badge&logo=MIT&logoColor=white
[license-url]: https://github.com/ari-denary/volunteer-management-backend/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/ari-denary/
<!-- [product-screenshot]: images/screenshot.png -->
[Flask.com]: https://shields.io/badge/Flask-41acc0?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/