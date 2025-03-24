from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class HHVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Visit'

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        required=True)

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        required=True)

    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
    )

    visit_status = fields.Selection(
        selection=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        copy=False,
        default='scheduled')

    scheduled_date = fields.Datetime()

    completed_date = fields.Datetime(copy=False)

    diagnosis_ids = fields.One2many(comodel_name='hr.hospital.diagnosis',
                                    inverse_name='visit_id')

    @api.model
    def write(self, vals):
        if 'scheduled_date' in vals or 'doctor_id' in vals:
            for record in self:
                if record.visit_status != 'scheduled':
                    raise ValidationError(
                        _('It is not possible to change the time/date/doctor for a completed or canceled visit!'))
        return super().write(vals)

    @api.constrains('patient_id', 'doctor_id', 'scheduled_datetime')
    def _check_patient_doctor_schedule(self):
        for record in self:
            if not record.scheduled_date and record.doctor_id:
                continue
            existing_visits = self.env['hr.hospital.visit'].search([
                ('id', '!=', record.id),
                ('patient_id', '=', record.patient_id.id),
                ('doctor_id', '=', record.doctor_id.id),
                ('scheduled_date', '>=', record.scheduled_date.date().strftime('%Y-%m-%d') + ' 00:00:00'),
                ('scheduled_date', '<=', record.scheduled_date.date().strftime('%Y-%m-%d') + ' 23:59:59')
            ])
            if existing_visits:
                raise ValidationError(_('The patient is already scheduled to see this doctor for this day!'))

    @api.model
    def unlink(self):
        for record in self:
            if record.diagnosis_ids:
                raise ValidationError(_('You cannot delete or archive a visit with diagnoses!'))
        return super().unlink()
