# Grievance Pro - Complaint Management System

## Overview

Grievance Pro is a web-based complaint management system built using Django, designed to streamline grievance submission, tracking, and resolution in an efficient and transparent manner. The system provides role-based logins, with different types of users (Admin, HOD, Super Admin, and Users) accessing features tailored to their roles. Users can submit complaints, track their progress, and edit or delete their complaints. Admins and Super Admins can manage departments, categories, and complaints.

## Features

### User Features:

- **Registration & Login:** Users can register, log in, and access their dashboards. Users select their department during registration.
- **Complaint Submission:** Users can submit new complaints and edit or delete them (if needed).
- **Track Complaints:** Users can track the status of their complaints.
- **Complaint Details:** View detailed information about submitted complaints, including attachments and status.


### Admin Features:
- **Dashboard:** Admins can view all complaints, manage complaints, and interact with users.
- **Manage Departments:** Admins can add or delete departments, which are used to categorize complaints.
- **Manage Categories:** Admins can add or delete complaint categories.

### Super Admin Features:
- **Manage Users & Roles:** Super Admins can manage departments and categories.
- **Manage Complaints:** Super Admins can view all complaints submitted by users, filter by department, and perform actions.
- **Manage Admins & Users:** Super Admins can promote or demote users to Admin roles.


## Technologies Used
- **Django**: Python web framework for building the backend.
- **HTML/CSS**: For frontend templating and styling.
- **SQLite**: Default database (can be configured to use another database like PostgreSQL).
- **Bootstrap (optional)**: Can be used for responsive design (if added).
  
## How to Use
1. **Login/Signup**: Users can log in using their credentials or register for an account. Super Admins can create users or promote them to admins.
2. **Dashboard**: Once logged in, users can access their dashboard where they can submit new complaints, track existing ones, or edit them.
3. **Admin Management**: Admins and Super Admins can manage complaints, categories, and departments.
4. **Complaint Tracking**: View the progress of complaints, including status updates.


