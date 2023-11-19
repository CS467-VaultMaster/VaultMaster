# VaultMaster
## Description
VaultMaster is a web password manager that allows storage and retrieval of web credentials. It is built using React, FastAPI, PostgreSQL, and AWS, designed to offer high security and ease of use. App features time-based OTP MFA, checks of whether user passwords have appeared in data breaches, and end-to-end encryption of all information.
## Visuals
Here is a look at VaultMaster in action:
### Login Page
<img src="https://github.com/CS467-VaultMaster/VaultMaster/assets/96148570/ffe2597a-5e8c-406d-8ec2-2938dc161bd5" width="300" alt="Login">\
*Page where users enter their credentials. This page provides a new user with a path to register.*

### Registration Page
<img src="https://github.com/CS467-VaultMaster/VaultMaster/assets/96148570/2bcff15b-95c0-488f-a9fd-91e03ac05bab" width="300" alt="Registration">\
*Allows the user to create a new account. The user will also be prompted to scan a QR code with their mobile authentication app.*

### Credentials Vault
<img src="https://github.com/CS467-VaultMaster/VaultMaster/assets/96148570/4a9c8c1e-ad45-4948-b85d-53706639efdf" width="700" alt="Credentials">\
*Dashboard to view, create, delete, and edit credentials. All passwords in VaultMaster are run through the Have I Been Pwned database to check for appearence in breaches as shown in above screenshot with the user attempting to use "password."*

### Edit Profile Page
<img src="https://github.com/CS467-VaultMaster/VaultMaster/assets/96148570/1cecaf73-050f-4a7a-908e-cfe47169aece" width="300" alt="Credentials">\
*Allows users to edit their profile information or delete their profile.*

### Tools Page
<img src="https://github.com/CS467-VaultMaster/VaultMaster/assets/96148570/9e3d73f1-fc10-4922-925c-fcee080d1a62" width="300" alt="Credentials">\
*Allows user to export all stored passwords in a plaintext JSON file. Also has Generate Strong Password utility.*

## Installation
To install and run VaultMaster using Docker, follow these steps:
1. **Clone the Repository**
3. **Build the Docker Images**:
- Ensure Docker is installed on your machine.
- Build the Docker images for the frontend, backend, and database services:
  ```
  docker-compose build
  ```
3. **Run the Docker Containers**:
- Start the containers:
  ```
  docker-compose up
  ```
4. **Access the Application**:
- The application should now be running at [localhost:3000](http://localhost:3000) for local development purposes.

## Usage
Visit [vaultmaster.site](https://www.vaultmaster.site) to use the production version of the app.
## Contributing
We welcome all contributions. Please see our Contribution Guidelines for more information. (TODO)
## Authors and Acknowledgement
Developed by Will Lambeth, Elliott Larsen, and Myles Penner for OSU CS467.
## License
This project is published under the MIT License - see the LICENSE.md file for details (TODO).
