from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

class HHVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Visit'

    patient_id = fields.Many2one(comodel_name='hr.hospital.patient',
                                 required=True)

    doctor_id = fields.Many2one(comodel_name='hr.hospital.doctor',
                                required=True)

    disease_id = fields.Many2one(comodel_name='hr.hospital.disease',
                                 )

    visit_status = fields.Selection([
        ('scheduled', 'Заплановано'),
        ('completed', 'Завершено'),
        ('cancelled', 'Скасовано')
    ],
        copy=False,
        default='scheduled')

    scheduled_date = fields.Datetime(copy=False)

    completed_date = fields.Datetime(copy=False)

    diagnosis_ids = fields.One2many(comodel_name='hr.hospital.diagnosis',
                                    inverse_name='visit_id')

    @api.model
    def write(self, vals):
        if 'scheduled_date' in vals or 'doctor_id' in vals:
            for record in self:
                if record.visit_status != 'scheduled':
                    raise ValidationError(_('Неможливо змінювати час/дату/лікаря для завершеного або скасованого візиту.'))
        return super().write(vals)

    @api.constrains('patient_id', 'doctor_id', 'scheduled_datetime')
    def _check_patient_doctor_schedule(self):
        for record in self:
            if record.scheduled_date:
                existing_visits = self.search([
                    ('id', '!=', record.id),
                    ('patient_id', '=', record.patient_id.id),
                    ('doctor_id', '=', record.doctor_id.id),
                    ('scheduled_date', '=', record.scheduled_date.date()),
                ])
                if existing_visits:
                    raise ValidationError(_('Пацієнт уже записаний до цього лікаря на цей день.'))

    @api.model
    def unlink(self):
        for record in self:
            if record.diagnosis_ids:
                raise ValidationError(_('Не можна видаляти або архівувати візит з діагнозами.'))
        return super().unlink()
