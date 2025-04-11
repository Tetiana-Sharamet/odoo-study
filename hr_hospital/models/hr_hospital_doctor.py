from odoo import models, fields, api
from odoo.tools.translate import _


class HHDoctor(models.Model):
    _inherit = 'hr.hospital.person'
    _name = 'hr.hospital.doctor'
    _description = 'Doctor'

    name = fields.Char(
        compute='_compute_name',
        store=True)

    specialty = fields.Selection(
        selection=[
            ('cardiologist', 'Cardiologist'),
            ('neurologist', 'Neurologist'),
            ('therapist', 'Therapist'),
            ('pediatrician', 'Pediatrician'),
        ])

    interns_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='mentor_id')

    patients_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='doctor_id')

    color = fields.Integer()

    is_intern = fields.Boolean(string='Intern')
    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Mentor',
        domain=[('is_intern', '=', False)]
    )

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for record in self:
            if record.last_name or record.first_name:
                record.name = 'Dr. %s  %s' % (
                    record.first_name, record.last_name)

    @api.constrains('mentor_id')
    def _check_mentor_not_intern(self):
        for record in self:
            if (record.mentor_id
                    and record.mentor_id.is_intern):
                raise models.ValidationError(_("An intern cannot "
                                               "be a mentor."))

    def create_visit(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Visit',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_doctor_id': self.id,
            },
        }
