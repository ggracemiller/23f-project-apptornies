# LHUB

## Project Description

LHUB is a secure and comprehensive database solution tailored for law firms to manage contact information and case histories efficiently. It offers tiered access levels to safeguard sensitive information, allowing only authorized personnel to view or modify past case details. With LHUB, law firms can enhance collaboration, maintain confidentiality, and streamline case management workflows. Clients can use LHUB to view information about their specific cases.

This repo contains an application that runs using 3 Docker containers: 
1. A MySQL 8 container
1. A Python Flask container running a Flask API
1. A Local AppSmith Server

## How to setup and start the containers
**Important** - you need Docker Desktop installed

1. Clone this repository.  
1. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
1. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
1. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
1. Build the images with `docker compose build`
1. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. 




