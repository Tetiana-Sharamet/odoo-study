from odoo  import models, fields

class HHDoctor(models.Model):
    _inherit = 'hr.hospital.person'
    _name = 'hr.hospital.doctor'
    _description = 'Doctor'

    name = fields.Char()
    specialty = fields.Char()
