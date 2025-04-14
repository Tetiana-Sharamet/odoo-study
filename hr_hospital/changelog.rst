==========================================
Changelog for Hospital Management System
==========================================

17.0.1.0.0 (2025-04-11)
------------------------

- Initial release of the Hospital Management System module.
- **HR Hospital Patient**: Added fields for name, birth date, emergency contact, and personal doctor.
- **HR Hospital Visit**: Introduced visit scheduling, patient assignments, and doctor allocation.
- **HR Hospital Disease**: Added disease categories, parent-child relationships for diseases.
- **HR Hospital Diagnosis**: Implemented diagnosis records linked to visits, with intern approval workflow.

17.0.1.0.1 (2025-04-12)
-----------------------

- Fixed issue where patients could be double-booked for doctor visits on the same day.
- Added validation for changes in visit schedules when the visit is marked as completed or canceled.
- Improved performance for displaying large patient visit histories.

17.0.1.1.0 (2025-04-15)
-----------------------

- **HR Hospital Disease**: Added ability to compute and display disease complete names with parent-child hierarchy.
- **HR Hospital Patient**: Added function to open a patient's visit history and create new visits directly from the patient record.
- Improved validation for deleting visits with associated diagnoses.
- Refactored code for better modularity and readability.

17.0.1.1.1 (2025-04-17)
-----------------------

- Fixed bug with the calculation of the patient's age on the birthdate change.
- Updated patient name field to better handle edge cases where first and last names are not provided.
- Enhanced error messages when trying to modify completed or canceled visits.

