from odoo import (models, fields)

class HHPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Patient'

    name = fields.Char(string='Name')

    description = fields.Text()
    doctor_id = fields.Many2one(comodel_name='hr.hospital.doctor', string='Doctor')





