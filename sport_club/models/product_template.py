from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_gym_equipment = fields.Boolean(string="Used in Gym", default=False)
    maintenance_required = fields.Boolean(string="Requires Maintenance", default=False)
