# Happy Rental Jönköping - API 

## Introduction 

Welcome to Happy Rental Jönköping!
This is a local company dedicated to providing convenient car and RV van rentals in the beautiful city of Jönköping, situated in the scenic region of Småland, Sweden. Our goal is to make it easy for visitors and residents alike to rent vehicles and explore the stunning sights of this area. With this platform, users can effortlessly browse available vehicles, make reservations, and enjoy their adventures in this wonderful part of Sweden.  

I’m excited to share the features and ideas behind this project with you!

![API-Backend](static/images/screenshots/apiimage.png)

## Explanation of Backend Functionality

All data displayed and interactions performed on the frontend—such as browsing cars, viewing descriptions and images, making bookings, and sending messages—are processed and managed through this backend API.  

Authorized personnel can access this backend to manage vehicle listings, update descriptions and images, view and handle bookings, and respond to messages. Thus, the backend serves as the central hub for all data management, ensuring that the frontend reflects real-time information and that user interactions are securely processed.



[Happy Rental Backend - API live site](https://carbookingbackend-df57468af270.herokuapp.com/)

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

## Models and CRUD Breakdown

| Model        | Endpoints                     | Create   | Retrieve | Update   | Delete   | Filters                     | Text Search | Permissions                     |
|--------------|-------------------------------|----------|----------|----------|----------|-----------------------------|-------------|----------------------------------|
| User         | `/users/`<br>`/users/:id/`    | yes      | yes      | yes      | no       | no                          | no          | Self or Admin for updates        |
| Car          | `/cars/`<br>`/cars/:id/`      | yes      | yes      | yes      | yes      | no                          | no          | Admin-only for modifications     |
| CarImage     | `/carimages/`<br>`/carimages/:id/`| yes  | yes      | yes      | yes      | by car                      | no          | Unrestricted                     |
| BookedDate   | `/booked-dates/`<br>`/booked-dates/:id/` | yes | yes | yes      | yes      | by user/car/date            | no          | Owner or Admin for modifications |
| Contact      | `/contact/`<br>`/contact/:id/`| yes      | yes      | no       | yes      | no                          | no          | Admin-only for view/delete       |
| Review       | `/reviews/`<br>`/reviews/:id/`| yes      | yes      | yes      | yes      | by rating/user/date         | no          | Owner or Admin for modifications |

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