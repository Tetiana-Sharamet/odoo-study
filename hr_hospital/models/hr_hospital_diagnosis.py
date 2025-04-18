from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Diagnosis(models.Model):
    """
       Model representing a medical diagnosis for
        a patient during a visit at the hospital.

       This model stores information about a diagnosis,
       such as the disease diagnosed,
       the doctor responsible, the approval status of the diagnosis,
        and the date it was made.
       It also ensures that an intern's diagnosis
       is approved by a mentor.

       Attributes:
           name (str): The name of the diagnosis.
           visit_id (Many2one): The visit related
            to this diagnosis (required).
           disease_id (Many2one): The disease associated
           with this diagnosis (required).
           description (Text): A description of the diagnosis.
           is_approved (bool): Whether the diagnosis has been approved.
           diagnosis_date (Datetime): The date the diagnosis was made,
           computed from the visit date.
           doctor_id (Many2one): The doctor who made the diagnosis,
            computed from the visit.
       """
    _name = 'hr.hospital.diagnosis'
    _description = 'Diagnosis'

    name = fields.Char(translate=True)

    visit_id = fields.Many2one(
        comodel_name='hr.hospital.visit',
        string='Visit',
        required=True,
        help="The visit associated with this diagnosis."
    )

    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Disease',
        required=True,
        help="The disease diagnosed in this visit.")

    description = fields.Text(
        translate=True,
        help="A detailed description of the diagnosis.")

    is_approved = fields.Boolean(
        string='Approved',
        default=False,
        help="Indicates if the diagnosis has been approved.")

    diagnosis_date = fields.Datetime(
        compute='_compute_data',
        store=True,
        help="The date when the diagnosis was made, "
             "computed from the visit date.")

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        compute='_compute_data',
        store=True,
        help="The doctor who made the diagnosis, "
             "computed from the visit.")

    @api.depends('visit_id')
    def _compute_data(self):
        """
        Computes the doctor and diagnosis date
        based on the related visit.

        This method sets the doctor and diagnosis
         date fields based on the visit
        associated with the diagnosis.
        It is triggered when the visit_id changes.
        """
        for record in self:
            if record.visit_id:
                record.doctor_id = record.visit_id.doctor_id.id
                record.diagnosis_date = record.visit_id.scheduled_date

    @api.constrains('is_approved')
    def _check_mentor_approval(self):
        """
        Validates that an intern's diagnosis
        is approved by a mentor.

        This method ensures that if the diagnosis
        is approved and the doctor is an intern,
        a mentor must be assigned to the intern.
         If no mentor is assigned, a
        ValidationError is raised.
        """
        for record in self:
            doctor = record.visit_id.doctor_id
            if (doctor.is_intern and record.is_approved
                    and not doctor.mentor_id):
                raise ValidationError(_("Intern's diagnosis must"
                                        " be approved by a mentor."))
