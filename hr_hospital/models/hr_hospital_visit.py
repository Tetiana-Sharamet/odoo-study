from datetime import datetime
from odoo import models, fields, api


class HHVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Visit'

    name = fields.Char()

    visit_date = fields.Datetime()
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
        default='scheduled')

    scheduled_datetime = fields.Datetime()

    completed_datetime = fields.Datetime()

    diagnosis_ids = fields.One2many(comodel_name='hr.hospital.diagnosis',
                                    inverse_name='visit_id')



    @api.model
    def create(self, vals):
        if 'scheduled_datetime' in vals and 'visit_status' in vals and vals['visit_status'] != 'scheduled':
            raise ValueError('Неможливо змінити час/дату візиту після того, як візит був завершений або скасований.')
        return super(PatientVisit, self).create(vals)

    def write(self, vals):
        if 'scheduled_datetime' in vals or 'doctor_id' in vals:
            for record in self:
                if record.visit_status in ['completed', 'cancelled']:
                    raise ValueError('Неможливо змінювати час/дату/лікаря для завершеного або скасованого візиту.')
        return super(PatientVisit, self).write(vals)

    @api.constrains('patient_id', 'doctor_id', 'scheduled_datetime')
    def _check_patient_doctor_schedule(self):
        """Перевірка, щоб не можна було записати одного пацієнта до одного лікаря в один день більше одного разу."""
        for record in self:
            if record.visit_status == 'scheduled':
                # Перевірка на інші візити для того ж пацієнта та лікаря в той самий день
                existing_visits = self.env['patient.visit'].search([
                    ('patient_id', '=', record.patient_id.id),
                    ('doctor_id', '=', record.doctor_id.id),
                    ('visit_status', '=', 'scheduled'),
                    ('scheduled_datetime', '>=', record.scheduled_datetime.date().strftime('%Y-%m-%d') + ' 00:00:00'),
                    ('scheduled_datetime', '<=', record.scheduled_datetime.date().strftime('%Y-%m-%d') + ' 23:59:59')
                ])
                if existing_visits:
                    raise ValueError('Пацієнт уже записаний до цього лікаря на цей день.')

    @api.model
    def unlink(self):
        for record in self:
            if record.diagnosis_ids:
                raise ValueError('Не можна видаляти або архівувати візит з діагнозами.')
        return super(PatientVisit, self).unlink()
