from odoo import models, fields, api
from odoo.tools.translate import _

class HHDoctor(models.Model):
    _inherit = 'hr.hospital.person'
    _name = 'hr.hospital.doctor'
    _description = 'Doctor'

    name = fields.Char()
    specialty = fields.Selection(
        selection=[
        ('cardiologist', 'Cardiologist'),
        ('neurologist', 'Neurologist'),
        ('therapist', 'Therapist'),
        ('pediatrician', 'Pediatrician'),
    ])

    is_intern = fields.Boolean(string='Intern')
    mentor_id = fields.Many2one(comodel_name='hr.hospital.doctor',
                                string='Mentor')

    @api.constrains('mentor_id')
    def _check_mentor_not_intern(self):
        for record in self:
            if record.mentor_id and record.mentor_id.is_intern:
                raise models.ValidationError(_("An intern cannot be a mentor."))
