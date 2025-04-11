from datetime import date
from odoo import (models, fields, api)


class HHPatient(models.Model):
    """
    Model representing a hospital patient.

    This model extends the 'hr.hospital.person' model and
    is used to store information about hospital patients.
    It includes personal details such as the patient's name,
    description, doctor, birth date, age, passport number,
    and emergency contact information. It also provides methods
    for calculating the patient's age and opening/creating visit records.

    Attributes:
        name (Char): The full name of the patient,
        computed from first and last names.
        description (Text): A textual description of the patient.
        doctor_id (Many2one): A reference to the patient's personal doctor.
        birth_date (Date): The birth date of the patient.
        age (Integer): The age of the patient,
        computed based on the birth date.
        passport_number (Char): The passport number of the patient.
        emergency_contact (Char): The emergency
        contact information for the patient.

    Methods:
        _compute_name(): Computes the full name of the
        patient by concatenating first and last names.
        _compute_age(): Computes the patient's age
        based on the birth date.
        action_open_visits(): Opens the list of visits
        for the patient in a tree view.
        action_create_visit(): Opens the form to create
        a new visit for the patient.
    """
    _inherit = 'hr.hospital.person'
    _name = 'hr.hospital.patient'
    _description = 'Patient'

    name = fields.Char(
        compute='_compute_name',
        store=True,
        help="The full name of the patient, "
             "computed from first and last names."
    )

    description = fields.Text(
        help="A description of the patient."
    )

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Personal doctor',
        help="The doctor assigned to the patient"
             " as their personal doctor."
    )

    birth_date = fields.Date(
        help="The birth date of the patient."
    )

    age = fields.Integer(
        compute='_compute_age',
        store=True,
        help="The patient's age, computed based on the birth date."
    )

    passport_number = fields.Char(
        help="The passport number of the patient."
    )

    emergency_contact = fields.Char(
        help="The emergency contact information for the patient."
    )

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        """
        Computes the full name of the patient
        by concatenating first and last names.

        This method is called when the first_name
         or last_name fields are changed, and it updates the
        'name' field with the concatenation
        of first_name and last_name.

        The result is stored in the 'name' field for easy access.
        """
        for record in self:
            if record.last_name or record.first_name:
                record.name = '%s  %s' % (
                    record.first_name, record.last_name)

    @api.depends('birth_date')
    def _compute_age(self):
        """
        Computes the age of the patient based on their birth date.

        This method is called when the birth_date
         field is changed, and it calculates the patient's age
        by comparing the birth date with the current date.
        The result is stored in the 'age' field.

        If the birth date is not provided, the method sets the age to 0.
        """
        today = date.today()
        for record in self:
            if record.birth_date:
                age = (today.year - record.birth_date.year -
                       ((record.birth_date.month, record.birth_date.day) <
                        (today.month, today.day)))
                record.age = age
            else:
                record.age = 0

    def action_open_visits(self):
        """
        Opens the list of visits associated with the patient.

        This method opens the visit history for
        the patient in a tree view. It allows the user to see all
        past visits and associated information.
        The 'visit' model is filtered by the current patient's ID.

        Returns:
            dict: The action to open the 'hr.hospital.visit'
            model in a tree view.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Visit History',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
            'target': 'current',
        }

    def action_create_visit(self):
        """
        Opens the form to create a new visit for the patient.

        This method opens a form view where
        the user can create a new visit record for the patient. The
        context is set to prefill the 'patient_id'
        field with the current patient's ID.

        Returns:
            dict: The action to open the 'hr.hospital.visit'
             model in a form view with the context prefilled.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Visit',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
            },
        }
