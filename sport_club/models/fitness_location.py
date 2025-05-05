from odoo import models, fields

class FitnessLocation(models.Model):
    _name = 'fitness.location'
    _description = 'Training Location'

    name = fields.Char(string='Назва локації', required=True)
    location_type = fields.Selection([
        ('personal', 'Персональні/Самостійні'),
        ('group', 'Групові'),
    ], string="Тип локації", required=True)

    is_active = fields.Boolean(default=True)
    capacity =fields.Integer()