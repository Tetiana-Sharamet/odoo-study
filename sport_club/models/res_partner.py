from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_club_member = fields.Boolean(
        string="Club Member",
        default=False)

    visits_count = fields.Integer(
        string="Number of Visits")

    visit_ids = fields.One2many(
        comodel_name='sport.club.visit',
        inverse_name='member_id',
    )

    @api.depends('visit_ids')
    def _compute_visits_count(self):
        for record in self:
            record.visits_count = len(record.visit_ids)
