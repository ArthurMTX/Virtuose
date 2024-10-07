<a name="readme-top"></a>

<div align="center">
  
  <img src="https://file.mtx.dev/Virtuose-899.png" alt="logo" width="140"  height="auto" />
  <br/>

  <h3><b>Virtuose</b></h3>

</div>


# 📗 Table of Contents

- [📖 About the Project](#about-project)
  - [🛠 Built With](#built-with)
    - [Tech Stack](#tech-stack)
    - [Key Features](#key-features)
- [💻 Getting Started](#getting-started)
  - [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Install](#install)
  - [Usage](#usage)
  - [Run tests](#run-tests)
  - [Deployment](#deployment)
- [👥 Authors](#authors)
- [🤝 Contributing](#contributing)
- [📝 License](#license)

<!-- PROJECT DESCRIPTION -->

# 📖 [Virtuose] <a name="about-project"></a>

**Virtuose** is a lightweight virtualization web solution that simplifies the management of virtual environments. It integrates backend services, a database, and a frontend interface, all orchestrated with Docker.

 
## 🛠 Built With <a name="built-with"></a>

### Tech Stack <a name="tech-stack"></a>

<details> <summary>Frontend</summary> <ul> <li><a href="https://developer.mozilla.org/en-US/docs/Web/HTML">HTML5</a> - The standard markup language for creating web pages and web applications.</li> <li><a href="https://developer.mozilla.org/en-US/docs/Web/CSS">CSS3</a> - Used for styling and designing the frontend of the application.</li> <li><a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript">JavaScript</a> - Provides interactive elements and client-side functionality.</li> </ul> </details> <details> <summary>Backend</summary> <ul> <li><a href="https://www.djangoproject.com/">Django</a> - A high-level Python web framework that enables rapid development of secure and maintainable websites.</li> <li><a href="https://gunicorn.org/">Gunicorn</a> - A Python WSGI HTTP server for running Python web applications.</li> </ul> </details> <details> <summary>Database</summary> <ul> <li><a href="https://www.postgresql.org/">PostgreSQL</a> - A powerful, open-source object-relational database system with over 30 years of active development.</li> </ul> </details> <details> <summary>Virtualization</summary> <ul> <li><a href="https://libvirt.org/">libvirt</a> - A toolkit for managing virtualization platforms such as KVM, QEMU, and others. It is used in Virtuose to control virtual machines on the hypervisor.</li> <li><a href="https://www.qemu.org/">QEMU</a> - A hosted virtual machine monitor that Virtuose uses for emulating various hardware and running virtual machines.</li> </ul> </details> <details> <summary>Containerization</summary> <ul> <li><a href="https://www.docker.com/">Docker</a> - A platform for developing, shipping, and running applications in containers. Virtuose leverages Docker to run its backend, frontend, and database in isolated environments.</li> <li><a href="https://docs.docker.com/compose/">Docker Compose</a> - A tool for defining and running multi-container Docker applications. It allows the orchestration of the backend, frontend, and database services in Virtuose.</li> </ul> </details>


### Key Features <a name="key-features"></a>

- **Backend API**:  A robust REST API built with Django.
- **Frontend Web Interface**: A user-friendly interface for managing virtual environments.
- **PostgreSQL Database**: A reliable, high-performance database for storing application data.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## 💻 Getting Started <a name="getting-started"></a>


To get a local copy of **Virtuose** up and running, follow these steps:

### Prerequisites <a name="prerequisites"></a>

Before you begin, make sure you have the following installed on your local machine:

- **Docker**: Docker is required to manage services in isolated containers. You can install Docker by following the instructions [here](https://docs.docker.com/get-started/get-docker/).

  ```bash
  # To check if Docker is installed
  docker --version

- **Docker Compose**: Used to define and manage the multi-container Docker setup. Install Docker Compose by following the guide [here.](https://docs.docker.com/compose/install/)

  ```bash
  # To check if Docker Compose is installed
  docker-compose --version

  
### Setup <a name="setup"></a>

 Clone the repository to your desired directory:

    
```bash
git clone https://gitlab.com/virtuose-ema/virtuose-app.git
cd virtuose-app
``` 

Set up environment variables:



    cp .env.example .env

## Installation

### Hypervisor

Execute as **root** the **./install.sh** at the root of Virtuose project directory to install and configure the hypervisor on the host machine. (only tested on ubuntu 24 atm)

```bash
chmod +x install.sh
sudo ./install.sh
```

### Start the project

You need to have [docker](https://docs.docker.com/get-started/get-docker/) and [docker compose](https://docs.docker.com/compose/install/) installed in order to run the project. 

To start the docker compose, run the build.sh at the root of Virtuose project directory.

```bash
chmod +x build.sh
sudo ./build.sh
```



Be sure **libvirtd** is running on the host (hypervisor) :
```bash
systemctl status libvirtd
```


**Frontend is accessible from http://localhost:8000**  
**Api is accessible from http://localhost:8080**


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- AUTHORS -->

## 👥 Authors <a name="authors"></a>


👤 **Maxime**
- GitHub: [@Nobozor](https://github.com/Nobozor)


👤 **Dorian**
- GitHub: [@Dorian33160](https://github.com/dorian33160)


👤 **Arthur.P**
- GitHub: [@AthurMTX](https://github.com/ArthurMTX)

👤 **Aurélien**
- GitHub: [@AureDM](https://github.com/AureDM)


👤 **Arthur.M**
- GitHub: [@Hardthur](https://github.com/Hardthur)


👤 **Lucas**
- GitHub: [@LukuLaMule](https://github.com/LukuLaMule)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



## 🤝 Contributing <a name="contributing"></a>

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](https://gitlab.com/virtuose-ema/virtuose-app/-/issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 📝 License <a name="license"></a>

This project is [MIT](./LICENSE) licensed.



<p align="right">(<a href="#readme-top">back to top</a>)</p>
