from datetime import date
from odoo import (models, fields, api)


class HHPatient(models.Model):
    _inherit = 'hr.hospital.person'
    _name = 'hr.hospital.patient'
    _description = 'Patient'

    name = fields.Char(
        compute='_compute_name',
        store=True)

    description = fields.Text()

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Personal doctor')

    birth_date = fields.Date()

    age = fields.Integer(
        compute='_compute_age',
        store=True)

    passport_number = fields.Char()

    emergency_contact = fields.Char()

    @api.depends('first_name','last_name')
    def _compute_name(self):
        for record in self:
            if record.last_name or record.first_name:
                record.name = '%s  %s' % (
                    record.first_name, record.last_name )

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

    def action_open_visits(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Visit History',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
            'target': 'current',
        }

    def action_create_visit(self):
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
