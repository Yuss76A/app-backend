# Happy Rental Jönköping - API 

## Purpose & System Overview

The backend provides a RESTful API to manage all data associated with the Happy Rental platform, including user authentication, vehicle listings, bookings, reviews, and contact messages. It facilitates secure data transactions between the frontend and the database, ensuring users can browse vehicles, make reservations, submit reviews, and contact staff seamlessly. The system enforces permissions to protect user data and prevent unauthorized modifications, supporting both public access (e.g., viewing cars, reviews) and protected actions (e.g., creating bookings, posting reviews). 

## Introduction 

Welcome to Happy Rental Jönköping!
This is a local company dedicated to providing convenient car and RV van rentals in the beautiful city of Jönköping, situated in the scenic region of Småland, Sweden. Our goal is to make it easy for visitors and residents alike to rent vehicles and explore the stunning sights of this area. With this platform, users can effortlessly browse available vehicles, make reservations, and enjoy their adventures in this wonderful part of Sweden.  

I’m excited to share the features and ideas behind this project with you!

![API-Backend](static/images/screenshots/apiimage.png)

## Explanation of Backend Functionality

All data displayed and interactions performed on the frontend—such as browsing cars, viewing descriptions and images, making bookings, and sending messages—are processed and managed through this backend API.  

Authorized personnel can access this backend to manage vehicle listings, update descriptions and images, view and handle bookings, and respond to messages. Thus, the backend serves as the central hub for all data management, ensuring that the frontend reflects real-time information and that user interactions are securely processed.

[Happy Rental Backend - API live site](https://carbookingbackend-df57468af270.herokuapp.com/)

## Link To Happy Rental Front-End Project and Readme

[Happy Rental Jönköping - Front-End live site](https://highway-to-rent-6dc001f7bfed.herokuapp.com/)

[Readme Front-End](https://github.com/Yuss76A/Highway-to-Rent)

## Features

### Backend-Supported User Stories

##### Authentication & User Management

* As a user, I want to register for an account so that I can unlock and use all features available to authenticated users.
(Supported by: Register API, user creation)
* As a user, I want to log in to my account so that I can access personalized functionalities and content.
(Supported by: Login API, token authentication)
* As a user, I want to stay logged in until I actively choose to log out, ensuring a smooth and uninterrupted experience.
(Supported by: Token-based auth, persistent until logout)

#### Bookings / Rentals

* As a user, I want to see a list of all my current and past bookings so I can keep track of reservations.
(Supported by: BookedDateList, GET /bookings filtered by the logged-in user)
* As a user, I want to create a booking for a car within specific dates.
(Supported by: BookedDateList POST endpoint)
* As a user, I want to cancel or modify my upcoming bookings directly from the list so I can manage.
(Supported by: BookedDateDetail PUT/PATCH /bookings/:id)

#### Contact & Feedback

* As a user, I want to send a message via the contact form, whether logged in or not.
(Supported by: ContactView POST)
* As an admin, I want to view contact messages and delete inappropriate ones.
(Supported by: ContactView GET and DELETE methods)

#### Reviews

* As a user, I want to view reviews from other customers.
(Supported by: ReviewList GET)
* As a user, I want to submit a review and rating, so I can share my feedback about the service..
(Supported by: ReviewList POST)
* As a user, I want to edit or delete my own reviews.
(Supported by: ReviewDetail PUT/PATCH/DELETE, owner-only permissions)
* As an admin, I want to monitor, delete, or moderate reviews.
(Supported by: review owner permissions for delete)

#### Admin Stories 

* As an admin, I want to be able to manage user interactions and content by deleting offensive or harmful comments, reviews, or user accounts. This allows me to maintain a safe and respectful environment within the platform.
* Additionally, I want to be able to view contact messages and reviews to monitor feedback and ensure user concerns are addressed promptly.
* Overall, I need control over user management and content moderation to uphold community standards and protect employees and users from disrespectful behavior.

#### User Stories Additional Note

These user stories represent the initial core functionalities that guided the development of the application. They focus on the main features necessary for the app to operate smoothly and form the backbone of the project. 

They are also detailed in the "User Stories" section of the Frontend README, where they describe what users can do within the app. The reason these stories appear in both the frontend and backend documentation is because the backend handles, manages, and supports all these core features, providing the APIs, data processing, and security that enable the frontend's functionality.

As the project evolved, I continued adding many small but important details and features to enhance user experience and overall functionality. While these incremental improvements may not all be explicitly reflected in the original user stories, they are essential for a complete, polished application.

This approach allowed the project to grow organically, maintaining focus on core features while progressively building a richer user experience.

### Agile Aproach

The project was organized with associated user stories and tasks using GitHub Projects. You can find the project at [Car Rental booking App](https://github.com/users/Yuss76A/projects/10/views/1).

Here, you can find the detailed user stories that support the backend functionalities. Up to story number 9, these mainly focus on core backend features like user management, bookings, and reviews.

Additionally, I created stories related to the frontend—explicitly labeled as such—to ensure that all key features and user experiences were considered during development. These frontend stories helped me ensure that no important aspect was overlooked, even if some of them overlap with backend functionalities. This integrated approach helped build a comprehensive, user-centered application.

## API Documentation & Testing

#### API Endpoints

| URL | Method | Description | Permissions | Sample Request | Sample Response |
| --- | --- | --- | --- | --- | --- |
| /register/ | POST | Register a new user | Public | `{ "email": "user@example.com", "password": "Password123", "full_name": "John Doe" }` | `{ "token": "abcd1234", "user": {...} }` |
| /login/ | POST | User login | Public | `{ "email": "user@example.com", "password": "Password123" }` | `{ "token": "abcd1234" }` |
| /cars/ | GET | List available cars | Public | — | `[ { "id": 1, "name": "Kia Optima", "price_per_day": 50, ... }, ... ]` |
| /booked-dates/ | POST | Create a booking | Authenticated | `{ "car": 1, "start_date": "2025-07-01", "end_date": "2025-07-05" }` | `{ "reservation_number": "XYZ789", ... }` |
| /reviews/ | GET | View reviews | Public | — | `[ { "id": 1, "user": null, "rating": 4, "comment": "Great car!" }, ... ]`<br>**Note:** Users can submit reviews anonymously; the user info is **not shown publicly** to protect privacy. |
| /reviews/ | POST | Submit review | Authenticated | `{ "rating": 5, "comment": "Excellent!" }` | `{ "id": 10, ... }` |

#### Backend API Testing Summary

| Endpoint                 | Method | Auth Required | Admin Required | Test Case                      | Expected Result       |
|--------------------------|--------|---------------|-----------------|--------------------------------|-----------------------|
| `/register/`             | POST   | No            | No              | Valid registration data        | 201 Created + Token   |
| `/login/`                | POST   | No            | No              | Correct email/password         | 200 OK + Token        |
| `/cars/`                 | GET    | No            | No              | List all cars                  | 200 OK                |
| `/cars/`                 | POST   | Yes           | Yes             | Add new car as admin            | 201 Created           |
| `/cars/<id>/`            | DELETE | Yes           | Yes             | Delete car as admin             | 204 No Content        |
| `/carimages/`            | GET    | No            | No              | List all images                | 200 OK                |
| `/carimages/`            | POST   | Yes           | Yes             | Upload image as admin           | 201 Created           |
| `/booked-dates/`         | POST   | Yes           | No              | Valid booking as user           | 201 Created           |
| `/booked-dates/<id>/`    | DELETE | Yes           | Owner/Admin     | Delete own booking             | 204 No Content        |
| `/users/<id>/`           | PATCH  | Yes           | Self/Admin      | Update User Information (Email, Name)             | 200 OK                |
| `/reviews/`              | POST   | Yes           | No              | Submit review as user           | 201 Created           |
| `/reviews/<id>/`         | DELETE | Yes           | Owner/Admin     | Delete own review              | 204 No Content        |
| `/contact/`              | POST   | No            | No              | Submit contact form            | 201 Created           |

## Models and CRUD Breakdown

| Model        | Endpoints                     | Create   | Retrieve | Update   | Delete   | Filters                     | Text Search | Permissions                     |
|--------------|-------------------------------|----------|----------|----------|----------|-----------------------------|-------------|----------------------------------|
| User         | `/users/`<br>`/users/:id/`    | yes      | yes      | yes      | no       | no                          | no          | Self or Admin for updates        |
| Car          | `/cars/`<br>`/cars/:id/`      | yes      | yes      | yes      | yes      | no                          | no          | Admin-only for modifications     |
| CarImage     | `/carimages/`<br>`/carimages/:id/`| yes  | yes      | yes      | yes      | by car                      | no          | Admin-only for modifications                     |
| BookedDate   | `/booked-dates/`<br>`/booked-dates/:id/` | yes | yes | yes      | yes      | by user/car/date            | no          | Owner or Admin for modifications |
| Contact      | `/contact/`<br>`/contact/:id/`| yes      | yes      | no       | yes      | no                          | no          | Admin-only for view/delete       |
| Review       | `/reviews/`<br>`/reviews/:id/`| yes      | yes      | yes      | yes      | by rating/user/date         | no          | Owner or Admin for modifications |

## Database Models

- Here's a quick overview of the main database models used in this project and their basic fields. These models define how data is structured and related in the backend database.

#### Car Model

| Object             | Field                |
|--------------------|----------------------|
| name               | CharField            |
| type               | CharField (choices)  |
| price_per_day      | IntegerField         |
| currency           | CharField            |
| max_capacity       | IntegerField         |
| description        | TextField            |

#### CarImage Model

| Object     | Field             |
|------------|-------------------|
| image      | CloudinaryField   |
| caption    | CharField         |
| car        | ForeignKey        |

#### BookedDate Model

| Object            | Field                   |
|-------------------|-------------------------|
| car               | ForeignKey              |
| user              | ForeignKey              |
| start_date        | DateField               |
| end_date          | DateField               |
| reservation_number| CharField               |

#### User Model

| Object     | Field                  |
|------------|------------------------|
| email      | EmailField             |
| full_name  | CharField              |
| username   | CharField (optional)   |

#### Contact Model

| Object    | Field                      |
|-----------|----------------------------|
| name      | CharField                  |
| email     | EmailField                 |
| message   | TextField                  |
| created_at| DateTimeField              |

#### Review Model

| Object    | Field                      |
|-----------|----------------------------|
| user      | ForeignKey                 |
| rating    | IntegerField               |
| comment   | TextField                  |
| created_at| DateTimeField              |

## Overview of Database Structure

Below is a visual diagram representing the core structure of our database. It illustrates how the main entities—such as Cars, Bookings, Users, and Reviews—are interconnected. This ERD provides an easy-to-understand overview of how data is organized and related within the system, helping to visualize the relationships and dependencies that support the application's functionality.

**ERD (Entity-Relationship Diagram)**
![ERD (Entity-Relationship Diagram)](static/images/screenshots/erdrentapp.png)

## Why I created a custom User model

Even though Django already has a built-in User model, I decided to create my own. I wanted to make the email the main way users log in, and I needed to add some extra fields like full name. By making a custom User model, I can handle user info exactly how I want and make sure the login process fits my app’s requirements better. It gives me more control over user data and how authentication works. where i should add this in my backend section

## Testing

#### Code Quality & Best Practices

The backend code adheres to PEP8 standards and passes linting checks using tools like flake8 and pylint. The project is organized into modular, well-structured files, with descriptive comments and extensive documentation strings to enhance readability and maintainability. The code follows best practices, including the DRY principle, and all comments clarify complex logic and decisions.

To validate all python code used in this project, each file was evaluated using the [CI Python Linter](https://pep8ci.herokuapp.com/).

**Backendapp/Settings**
![Backendapp/Settings](static/images/screenshots/backendappsettingspage.png)

Note on AUTH_PASSWORD_VALIDATORS:

- You may notice that the Python linter raises warnings regarding the AUTH_PASSWORD_VALIDATORS list, indicating that the lines are long. However, these lines are generated by Django and are essential for enforcing secure password policies. 

You can safely leave these validators as-is in your settings file, as they are a standard part of Django's security features and do not pose any issues.

**Backendapp/WSGI**
![Backendapp/WSGI](static/images/screenshots/backendappwsgipage.png)

**Backendapp/Urls**
![Backendapp/Urls](static/images/screenshots/backendappurlspage.png)

**Backendapp/ASGI**
![Backendapp/ASGI](static/images/screenshots/backenappasgipage.png)

Reviews Files

**Reviews/Views**
![Reviews/Views](static/images/screenshots/reviewsviewspage.png)

**Reviews/Urls**
![Reviews/Urls](static/images/screenshots/reviewsurlspage.png)

**Reviews/Serializers**
![Reviews/Serializers](static/images/screenshots/reviewsserializerspage.png)

**Reviews/Permissions**
![Reviews/Permissions](static/images/screenshots/reviewspermissionspage.png)

**Reviews/Pagination**
![Reviews/Pagination](static/images/screenshots/reviewspaginationpage.png)

**Reviews/Models**
![Reviews/Models](static/images/screenshots/reviewsmodelspage.png)

**Reviews/Apps**
![Reviews/Apps](static/images/screenshots/reviewsappspage.png)

Contact Files

**Contact/Views**
![Contact/Views](static/images/screenshots/contactviewspage.png)

**Contact/Urls**
![Contact/Urls](static/images/screenshots/contacturlspage.png)

**Contact/Serializers**
![Contact/Serializers](static/images/screenshots/contactserializerspage.png)

**Contact/Models**
![Contact/Models](static/images/screenshots/contactmodelspage.png)

**Contact/Apps**
![Contact/Apps](static/images/screenshots/contactappspage.png)

**Contact/Admin**
![Contact/Admin](static/images/screenshots/contactadminpage.png)

Carbooking Files

**Carbooking/Views**
![Carbooking/Views](static/images/screenshots/carbookingviewspage.png)

**Carbooking/Urls**
![Carbooking/Urls](static/images/screenshots/carbookingurlspage.png)

**Carbooking/Serializers**
![Carbooking/Serializers](static/images/screenshots/carbookingserailizerspage.png)

**Carbooking/Permissions**
![Carbooking/Permissions](static/images/screenshots/carbookingpermissionspage.png)

**Carbooking/Auth_Backend**
![Carbooking/Auth_Backend](static/images/screenshots/carbookingauthbackendpage.png)

**Carbooking/Apps**
![Carbooking/Apps](static/images/screenshots/carbookingapppage.png)

**Carbooking/Models**
![Carbooking/Models](static/images/screenshots/carbookingmodelspage.png)

**Carbooking/Admin**
![Carbooking/Admin](static/images/screenshots/carbookingadminpage.png)

## Manual Testing Summary - Backend CRUD Operations

Extensive manual testing was performed on all CRUD functionalities across the backend system.

Create Operations:
New records such as users, cars, bookings, reviews, contact messages, and images were successfully added via the API. Data was accurately stored, and relationships were correctly established.

Retrieve Operations:
Listing endpoints returned the correct data sets, with filtering options (e.g., bookings by user, cars by type) working as intended. Individual record fetches provided complete and correct detail data.

Update Operations:
Existing records, including bookings, reviews, and user details, were successfully updated. Changes persisted correctly and reflected in subsequent queries.

Delete Operations:
Deletion endpoints functioned correctly, removing specified data from the database. Permission controls ensured that only authorized users or administrators could delete data, maintaining system security.

Permissions & Access Control:
All endpoints respected the defined permissions: owners could update or delete their own data, admins had full control, and unauthorized attempts were correctly blocked.

This comprehensive manual testing confirmed that all CRUD workflows operate reliably, ensuring data integrity and secure access across the backend.

This section details the steps taken to configure the project for deployment:

## Development and Deployment

#### Security & Permissions

All sensitive data such as database URLs, secret keys, and API keys are stored securely in the env.py file, which is included in .gitignore and never committed.  
The API communicates over HTTPS to ensure data security during transmission. Permissions are enforced via Django REST Framework's permission classes, ensuring that only owners can modify their own data, while admins have full access.

### Development

This section details the steps taken to configure the project for deployment:

#### Cloudinary

1. Navigate to [Cloudinary](https://cloudinary.com/ "Cloudinary") and create an account.
2. Log in.
3. Navigate to your dashboard and copy the API Enviroment variable.
4. Keep a note of this variable as you will need to add it to your env.py file in your project.

### Requirements

The project relies on the following packages:

* asgiref==3.8.1
* astroid==3.3.10
* certifi==2025.1.31
* charset-normalizer==3.4.1
* cloudinary==1.43.0
* dill==0.4.0
* dj-database-url==0.5.0
* Django==3.2.25
* django-cloudinary-storage==0.3.0
* django-cors-headers==4.5.0
* djangorestframework==3.12.4
* flake8==7.2.0
* gunicorn==23.0.0
* idna==3.10
* isort==6.0.1
* mccabe==0.7.0
* packaging==24.2
* pillow==11.1.0
* platformdirs==4.3.8
* psycopg2-binary==2.9.10
* pycodestyle==2.13.0
* pyflakes==3.3.2
* pylint==3.3.7
* pytz==2025.2
* requests==2.32.3
* setuptools==78.1.0
* six==1.17.0
* sqlparse==0.5.3
* tomlkit==0.13.2
* urllib3==2.3.0

Keep your requirements.txt up-to-date by running:

pip freeze > requirements.txt

This command captures all currently installed packages and their exact versions, making it easy to recreate the environment elsewhere.

To install all dependencies listed in your requirements file, use:

pip3 install -r requirements.txt

Note: Depending on your system and Python environment, you might need to use pip instead of pip3. Always verify with your Python documentation.

### Deployment

#### Backend

## Technologies Used

#### Frameworks & Libraries

* Python — The main programming language for the backend development.
* Django — Web framework used to build the API, manage models, handle authentication, and serve data.
* Django REST Framework — To create RESTful APIs and serialize data efficiently.
* PostgreSQL — The main database system, hosted via NeonDB.
* Cloudinary — Cloud service for hosting and managing images, integrated via django-cloudinary-storage.
* Gunicorn — WSGI server used for deploying the Django app.

#### Tools & Resources

* Lucidchart - Used for designing the ERD and visualizing the database schema.
* Chrome DevTools — Browser profiling and debugging.
* Heroku — Cloud platform for deploying and hosting the backend.
* GitHub — Version control and code repository hosting.

#### Database Connection:

- Installed psycopg2 library to connect to the PostgreSQL database.
- Integrated dj-database-url to manage database URLs from environment variables.

#### Authentication

- The project uses dj-rest-auth to handle user authentication, configured to utilize JSON Web Tokens (JWTs) for secure, stateless authentication.

##### env File

Create an env.py file in the root folder of your project. This file is used to securely store sensitive variables and must be added to your .gitignore to prevent it from being published publicly.

To set up your environment:

Add the following variables, replacing the placeholder values with your actual credentials:

#### env.py

* DATABASE_URL: The connection string for your database (e.g., ElephantSQL, NeonDB). You can find this in your database provider’s dashboard after creating your database.

* SECRET_KEY: Your Django secret key. Generate a secure key using Django Secret Key Generator. This key is crucial for cryptographic signing and should be kept secret.

* CLOUDINARY_URL: Your Cloudinary API environment variable. Remove the prefix before cloudinary:// and keep only the portion with your credentials (cloudinary://<api_key>:<api_secret>@<cloud_name>).

* DEV: Set to "1" during development to enable debug mode. In production, remove this line or set to an empty string, so your app runs with debug mode disabled.

* ALLOWED_HOST: Your development URL (e.g., localhost) or your production URL (e.g., your deployed app’s domain). This restricts access to your site.

* Note: Replace placeholder values with your actual credentials, but do not commit env.py to your repository.

This project was deployed using [Heroku](https://www.heroku.com "Heroku") by following the steps detailed below.

##### Heroku Backend

1. Navigate to Heroku website and sign up or log in.
2. From your dashboard, click New > Create new app.
3. Assign a unique name to your app, select your region, then click Create app.
4. Go to the Settings tab.
5. Scroll down to Config Vars and click Reveal Config Vars.
6. Add the required environment variables, ensuring they match your credentials (replace the example values below with your actual data):
* CLOUDINARY_URL	your Cloudinary API URL	Your Cloudinary credentials (remove the prefix if needed)
* DATABASE_URL	your database URL	Your PostgreSQL connection string (e.g., NeonDB, ElephantSQL)
* ALLOWED_HOST	your deployed site URL	Without https:// (e.g., yourapp.herokuapp.com)
* CLIENT_ORIGIN	your frontend URL	The live URL of your frontend app
* CLIENT_ORIGIN_DEV	your local URL	Typically http://localhost:3000
* SECRET_KEY	your secret key	Generate a unique secret key for production (keep it private)
* DEVELOPMENT	1	Set to "1" during development to enable debug mode

## My Journey Building the Backend

Building the backend for this project was definitely a journey filled with challenges and learning. In the beginning, it wasn’t easy to work with the API—there were moments of confusion and frustration. But as I pushed through, I started to really enjoy the process. Once I began to understand how everything fit together, it changed the way I saw the system. It became more like solving a puzzle—fun and rewarding.

There were tough days, but also many memorable, even funny moments that made the work all the more worthwhile. I’m genuinely proud of what I’ve accomplished within the time I had. Sure, there's always room for improvement, and I know the project can be expanded with many more features, but balancing this with a full-time job and my studies made it a challenge.

Looking back, I’m happy with what I managed to build. It’s been a fulfilling experience, and I’ve learned a lot along the way. This project is a testament to my dedication, and I look forward to growing even more in the future.

## My Journey with Code Institute: A Year of Growth and Gratitude

A year ago, I was at work when I received a phone call from Code Institute. After we finished the call, I wasn’t sure about what to do next. I was overwhelmed with my full-time job, studying, and honestly, I doubted if I was capable of starting this journey. I was scared I might fail. But I decided to take the challenge, with that little voice inside telling me, “What if I fail?”

Starting the program opened up a whole new world for me. Today, I can say that I’ve found something I love—a passion I never knew I had. I’m truly happy that I took that call from Code Institute. 

So, I want to say thank you first to Code Institute for an incredible journey and for providing all the tools and support along the way. Thanks to all the mentors who helped me through this sometimes challenging, but always rewarding year of learning. A special shoutout to the assessors, whose feedback and tips have been invaluable in helping me improve my skills.

And a big thank you to the Slack community for always being there—ready to support, guide, and inspire me whenever I needed it. 

To everyone involved—Code Institute, assessors, mentors, and the Slack community—thank you from the bottom of my heart. This experience has been life-changing, and I’m grateful for every moment.

## Acknowledgment

Building this backend was quite the journey. It’s a large and complex system, and I know I might have missed or overlooked some details along the way—those little bugs or omissions that happen when you're managing so many moving parts. Despite my best efforts and multiple reviews, I understand that perfection is hard, and mistakes can happen. I sincerely apologize if I missed anything or if parts here aren’t as clear as they should be.

I’m grateful for the support I received during this process, and I’m always open to feedback and improvements. If you spot any issues or have suggestions, please feel free to reach out. This project is a work in progress, and I’m committed to refining it further.

## Credits

I am deeply grateful to [CodeInstitute](https://codeinstitute.net/ "Code Institute") and their supportive Slack community of mentors and fellow learners. Their guidance, encouragement, and expertise have been invaluable in helping me navigate this project and achieve my goals.

My heartfelt appreciation also goes to my wife, Fatty, and my younger brother, Mett, whose testing, feedback, and support played a crucial role in refining this project.

A special thanks to my mentor, [Iuliia Konovalova](https://github.com/IuliiaKonovalova), for your continuous mentorship and insightful advice. Your support has truly made a positive impact on my learning journey.

Lastly, I want to acknowledge the creators of [GitHub](https://github.com/), whose platform has transformed collaboration and coding education. It’s more than a tool—it’s been a vital part of my growth as a developer.
