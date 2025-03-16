from odoo.odoo import models, fields

class HHVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Visit'

    visit = fields.Char(string='Visit')

    date = fields.Datetime()
    patient_id = fields.Many2one(comodel_name='hr.hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one(comodel_name='hr.hospital.doctor', string='Doctor', required=True)
    disease_id = fields.Many2one(comodel_name='hr.hospital.disease', string='Disease')
