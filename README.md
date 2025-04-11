# SnapShot - Web Application (User-Centric Image Sharing Platform)

SnapShot is a minimal, functional web application developed as part of a security-focused learning project. The application provides core features like user registration, authentication, file uploads, personal galleries, and account management — all implemented from scratch using Python and Flask, without external frameworks or templates.

The application is intentionally designed to contain basic security flaws so it can be analyzed and improved upon during later security testing and hardening stages.

---

## Project Goals

This project was created to demonstrate practical skills in:

- Building a full-stack web application from the ground up
- Implementing fundamental web functionalities without relying on templates or frameworks
- Understanding and later identifying common web vulnerabilities in a hands-on environment
- Managing a local or deployable web application with database integration and file handling

---

## Core Features

- *User Registration and Login:* Supports multiple users with a basic authentication system.
- *Personal Image Gallery:* Each user has access to a private gallery that only displays their own uploaded images.
- *Text-Based Post Creation:* Users can create simple text posts, stored alongside their images.
- *File Upload:* Images are uploaded and stored in a dedicated server directory.
- *User Profile Page:* Displays user information such as username and email.
- *Password Change:* Authenticated users can change their passwords through a dedicated page.
- *Database Integration:* All user data, posts, and uploads are stored using MongoDB.

---

## Application Flow

1. A new user registers with a username, email, and password.
2. After logging in, the user is taken to a dashboard that displays their uploaded images and text posts.
3. Users can:
   - Upload new images
   - Write new text posts
   - View their own content in the gallery
   - Change their password
   - View their user profile with basic information

All uploads are tied to the user and are not visible to others.

---

## Technologies Used

- *Backend:* Python (Flask)
- *Database:* MongoDB
- *Frontend:* HTML, CSS, JavaScript (no frameworks)
- *Hosting:* Local environment or Docker-ready for deployment
- *Authentication:* Basic session-based login system using Flask sessions

---

## How to Run Locally
## Project Directory Structure
snapshot/
├── app.py
├── static/
│   └── gallery/
├── templates/
│   ├── layout.html
│   └── index.html
├── data/
│   ├── posts.json
│   └── gallery/  (old image storage)
├── users.json
├── requirements.txt
└── venv
![image](https://github.com/user-attachments/assets/51a3b3d9-fd99-4cd4-b8a9-e41464e29dbe)
![image](https://github.com/user-attachments/assets/0dd3777a-6477-474b-bbe0-8aaae95cdf4b)
![image](https://github.com/user-attachments/assets/0dcce285-1908-49f5-b1e8-18c29d672e33)

### Clone the Repository

```bash
git clone [https://github.com/hitksh18/SnapShot.git](https://github.com/srijareddy1234/SnapShot.git
cd SnapShot



