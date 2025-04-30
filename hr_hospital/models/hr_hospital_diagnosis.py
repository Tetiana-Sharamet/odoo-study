from odoo import models, fields

class Diagnosis(models.Model):
    _name = 'hr.hospital.diagnosis'
    _description = 'Diagnosis'

    visit_id = fields.Many2one(comodel_name='hr.hospital.visit',
                               string='Visit',
                               required=True)

    disease_id = fields.Many2one(comodel_name='hr.hospital.disease',
                                 required=True)

    description = fields.Text()

    is_approved = fields.Boolean(default=False)
