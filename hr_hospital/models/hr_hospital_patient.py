from datetime import date
from odoo import (models, fields, api)


class HHPatient(models.Model):
    _inherit = 'hr.hospital.person'
    _name = 'hr.hospital.patient'
    _description = 'Patient'

    name = fields.Char()

    description = fields.Text()

    doctor_id = fields.Many2one(comodel_name='hr.hospital.doctor',
                                string='Personal doctor')

    birth_date = fields.Date()

    age = fields.Integer(compute='_compute_age', store=True)

    passport_number = fields.Char()

    emergency_contact = fields.Char()


    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.birth_date:
                age = today.year - record.birth_date.year
                if (today.month, today.day) < (record.birth_date.month, record.birth_date.day):
                    age -= 1
                    record.age = age
                else:
                    record.age = age
            else:
                record.age = 0
