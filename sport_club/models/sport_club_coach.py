from odoo import models, fields,api


class SportClubCoach(models.Model):
    """
    Model representing a sport club coach.

    Attributes:
        name (Char): Full name of the coach.
        specialty (Char): Area of expertise.
        phone (Char): Contact phone number.
        email (Char): Contact email.
        active (Bool): Whether the coach is active.
        biography (Text): Short biography of the coach.
    """
    _name = 'sport.club.coach'
    _description = 'Sport Club Coach'
    _inherits = {'res.partner': 'partner_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Related Partner",
        required=True,
        ondelete='cascade')

    name = fields.Char(
        compute='_compute_name',
        store=True,
        required=True,
        translate=True)
    specialty = fields.Char()

    is_active = fields.Boolean(default=True)
    biography = fields.Text()

    @api.depends('partner_id')
    def _compute_name(self):
        for record in self:
            if record.partner_id:
                record.name = record.partner_id.name
