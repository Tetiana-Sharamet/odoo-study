from odoo import models, fields

class HHDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'

    name = fields.Char(string='Name')
    description = fields.Text()