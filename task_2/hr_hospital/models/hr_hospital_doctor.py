from odoo.odoo  import models, fields

class HHDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Doctor'

    name = fields.Char(string='Name')
    specialty = fields.Char(string='Specialty')

