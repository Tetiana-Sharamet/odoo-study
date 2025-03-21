from odoo import models, fields

class HHDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'

    name = fields.Char()
    description = fields.Text()
    parent_id = fields.Many2one(comodel_name='hr.hospital.disease',
                                ondelete='cascade')
