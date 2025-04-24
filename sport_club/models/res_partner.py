from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_club_member = fields.Boolean(string="Club Member",
                                    default=False)
    is_coach = fields.Boolean(string="Coach",
                              default=False)
    visits_count = fields.Integer(string="Number of Visits")

    visit_ids = fields.One2many('club.visit', 'partner_id', string="Visits")

    @api.depends('visit_ids')
    def _compute_visits_count(self):
        for rec in self:
            rec.visits_count = len(rec.visit_ids)
