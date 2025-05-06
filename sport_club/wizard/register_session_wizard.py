from odoo import models, fields, api


class RegisterSessionWizard(models.TransientModel):
    _name = 'sport.club.register.session.wizard'
    _description = 'Register Session Wizard'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        required=True)
    coach_id = fields.Many2one(
        comodel_name='res.partner',
        required=True)
    session_date = fields.Datetime(
        required=True)
    notes = fields.Text()

    @api.model
    def default_get(self, field_names):
        # використай field_names замість fields
        res = super(RegisterSessionWizard, self).default_get(field_names)
        # логіка
        return res

    def action_register_session(self):
        """
        This function creates a new session record from the wizard.
        """
        session_obj = self.env['sport.club.visit']
        session_obj.create({
            'partner_id': self.partner_id.id,
            'coach_id': self.coach_id.id,
            'visit_date': self.session_date,
            'notes': self.notes,
        })
        return {'type': 'ir.actions.act_window_close'}
