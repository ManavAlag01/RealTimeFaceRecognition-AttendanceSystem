# Real-time Face Recognition Attendance System

This project implements a real-time face recognition attendance system using Python, Tkinter, OpenCV, and MySQL.

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Dependencies](#dependencies)
- [What the Program Does](#what-the-program-does)
- [Contributing](#contributing)

## Overview

This system allows users to perform real-time face recognition for attendance tracking. Users can log in or register new users, and the system logs attendance information in a MySQL database.

## Getting Started

### Prerequisites

- Python 3.x
- Virtual environment (optional but recommended)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repository.git
    ```

2. Navigate to the project folder:

    ```bash
    cd your-repository
    ```

3. Install dependencies:

    ```bash
    pip install -r versions-required/requirements.txt
    ```

## Usage

1. Run the main application:

    ```bash
    python src/main.py
    ```

2. Follow the on-screen instructions to log in or register a new user.

## Folder Structure

- `versions-required`: Folder containing information about module versions.
- `src`: Source code folder.
  - `util.py`: Utility functions.
  - `main.py`: Main application file.
- `db`: Folder to store user images and embeddings.
- `log.txt`: Log file.

## Dependencies

- cmake==3.17.2
- dlib==19.24.2
- face-recognition==1.3.0
- face-recognition-models==0.3.0
- mysql-connector-python==8.2.0
- opencv-python==4.6.0.66
- Pillow==9.2.0
- setuptools==63.2.0

## What the Program Does

The Real-time Face Recognition Attendance System performs the following tasks:

- **User Login:** Users can log in using their pre-registered face.
- **New User Registration:** Users can register a new face for attendance tracking.
- **Real-time Face Recognition:** The system uses real-time face recognition to log in users and track attendance.
- **MySQL Database Integration:** Attendance information, including login times, is stored in a MySQL database.

## Contributing

Feel free to open issues and pull requests!

