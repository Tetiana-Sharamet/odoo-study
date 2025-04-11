from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class HHVisit(models.Model):
    """
    Model representing a hospital visit record.

    This model is used to track the details of a patient's visit
    to the hospital. It includes information
    about the patient, doctor, disease, visit status,
    scheduled dates, and any diagnoses made during the visit.
    The model also provides business logic to ensure
    visits are not scheduled with conflicts, and that
    changes to visits cannot be made once
     they are completed or canceled.

    Attributes:
        patient_id (Many2one): Reference to
        the patient for the visit.
        doctor_id (Many2one): Reference to
        the doctor responsible for the visit.
        disease_id (Many2one): Reference to
        the disease being treated or diagnosed during the visit.
        visit_status (Selection): The status of
        the visit (scheduled, completed, or cancelled).
        scheduled_date (Datetime): The scheduled date and time of the visit.
        completed_date (Datetime): The actual date
        and time when the visit was completed (if applicable).
        diagnosis_ids (One2many): A list of diagnoses made during the visit.

    Methods:
        write(vals): Overridden to ensure no changes
        can be made to scheduled time, date, or doctor
        for completed or canceled visits.
        _check_patient_doctor_schedule(): Validates
        that the patient is not double-booked for the
        same doctor on the same day.
        unlink(): Ensures that visits with diagnoses
        cannot be deleted or archived.
    """
    _name = 'hr.hospital.visit'
    _description = 'Visit'

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        required=True,
        help="The patient who is visiting the hospital."
    )

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        required=True,
        help="The doctor assigned to the patient for the visit."
    )

    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        help="The disease being treated or diagnosed during the visit."
    )

    visit_status = fields.Selection(
        selection=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        copy=False,
        default='scheduled',
        help="The current status of the "
             "visit (scheduled, completed, or cancelled)."
    )

    scheduled_date = fields.Datetime(
        help="The scheduled date and time for the visit."
    )

    completed_date = fields.Datetime(
        copy=False,
        help="The date and time when the visit was completed (if applicable)."
    )

    diagnosis_ids = fields.One2many(
        comodel_name='hr.hospital.diagnosis',
        inverse_name='visit_id',
        help="A list of diagnoses made during the visit."
    )

    @api.model
    def write(self, vals):
        """
        Overridden method to prevent changes
        to scheduled date/time or doctor once
         a visit is completed or canceled.

        Args:
            vals (dict): The values to be written to the record.

        Returns:
            bool: The result of the write operation.

        Raises:
            ValidationError: If attempting
            to change the scheduled date/time
            or doctor of a completed or canceled visit.
        """
        if 'scheduled_date' in vals or 'doctor_id' in vals:
            for record in self:
                if record.visit_status != 'scheduled':
                    raise ValidationError(
                        _('It is not possible to change '
                          'the time/date/doctor '
                          'for a completed or canceled visit!')
                    )
        return super().write(vals)

    @api.constrains('patient_id', 'doctor_id', 'scheduled_date')
    def _check_patient_doctor_schedule(self):
        """
        Ensures that the same patient is not
         double-booked with the same doctor
         on the same day.

        This method checks whether the patient
         has already been scheduled for another
         visit with the same doctor
        on the same day. If a conflict
        is found, a ValidationError is raised.

        Raises:
            ValidationError: If the patient
            is already scheduled with the same doctor for the same day.
        """
        for record in self:
            if not (record.scheduled_date and record.doctor_id):
                continue
            existing_visits = self.env['hr.hospital.visit'].search([
                ('id', '!=', record.id),
                ('patient_id', '=', record.patient_id.id),
                ('doctor_id', '=', record.doctor_id.id),
                ('scheduled_date', '>=',
                 record.scheduled_date.date().strftime('%Y-%m-%d')
                 + ' 00:00:00'),
                ('scheduled_date', '<=',
                 record.scheduled_date.date().strftime('%Y-%m-%d')
                 + ' 23:59:59')
            ])
            if existing_visits:
                raise ValidationError(_('The patient is already '
                                        'scheduled to see this '
                                        'doctor for this day!'))

    @api.model
    def unlink(self):
        """
        Prevents the deletion or archiving
        of visits that have associated diagnoses.

        This method ensures that a visit cannot be
        deleted or archived if any diagnoses
        have been made during the visit.

        Returns:
            bool: The result of the unlink operation.

        Raises:
            ValidationError: If attempting to
            delete or archive a visit with diagnoses.
        """
        for record in self:
            if record.diagnosis_ids:
                raise ValidationError(_('You cannot delete or '
                                        'archive a visit with diagnoses!'))
        return super().unlink()
