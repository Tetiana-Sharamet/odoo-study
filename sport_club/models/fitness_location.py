from odoo import models, fields

class FitnessLocation(models.Model):
    _name = 'fitness.location'
    _description = 'Training Location'

    name = fields.Char(string='Training Location', required=True)
    location_type = fields.Selection([
        ('personal', 'Personal/Self'),
        ('group', 'Group'),
    ], required=True)

    is_active = fields.Boolean(default=True)
    capacity =fields.Integer()
