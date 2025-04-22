===========================
Hospital Management System
===========================

This is a Hospital Management System built on the Odoo platform, designed to manage hospital-related operations.
It includes models for handling patients, doctors, diseases, visits, and diagnoses, along with the ability to track medical histories, schedule visits, and manage hospital staff.

Modules Overview
=================

The following modules are included in this system:

1. **HR Hospital Patient Management**: Manages patient information, including personal details, emergency contacts, and visit history.
2. **HR Hospital Visit Management**: Tracks visits, scheduling, doctors, and diagnoses.
3. **HR Hospital Disease Management**: Maintains a list of diseases and their categories, including sub-categories.
4. **HR Hospital Diagnosis Management**: Links visits to diagnoses, along with approval workflows.

Features
========

- **Patient Registration**: Register new patients and store personal information like name, birthdate, and emergency contact.
- **Visit Scheduling**: Schedule visits for patients with doctors and assign diseases to the visit.
- **Disease Management**: Categorize diseases with parent-child relationships, and manage them throughout the hospital system.
- **Diagnosis and Approval**: Link diagnoses to visits, and manage approval workflows, especially for interns.

Installation
============

To install the Hospital Management System module in Odoo, follow these steps:

1. Download the module from the repository.
2. Place the module in your Odoo custom add-ons directory.
3. Update the Odoo app list.
4. Install the module through the Odoo Apps menu.

Usage
=====

- Once installed, you can access the module via the Odoo interface.
- Navigate to **Hospital Management > Patients** to manage patients and their visits.
- You can also manage doctors, diseases, and diagnoses under the respective menu items.

Dependencies
============

- Odoo 14.0 or later
- Python 3.x
- PostgreSQL

Contributors
============

- Tetiana Sharamet(https://github.com/Tetiana-Sharamet)


License
=======

This module is licensed under the **OPL-1.0** license.
