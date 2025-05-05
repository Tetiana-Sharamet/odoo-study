from odoo import models, fields, api


class ClubVisit(models.Model):
    _name = 'sport.club.visit'
    _description = 'Club Visit'
    _order = 'visit_date desc'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Club Member",
        required=True,
        domain="[('is_club_member', '=', True)]")

    visit_date = fields.Datetime(
        default=fields.Datetime.now,
        required=True)

    coach_id = fields.Many2one(
        comodel_name='res.partner')

    notes = fields.Text()

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        # You could add logic to send notification or log visits
        return rec
