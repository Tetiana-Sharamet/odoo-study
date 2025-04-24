from odoo import models, fields, api


class ClubVisit(models.Model):
    _name = 'club.visit'
    _description = 'Club Visit'
    _order = 'visit_date desc'

    partner_id = fields.Many2one('res.partner', string="Club Member", required=True, domain="[('is_club_member', '=', True)]")
    visit_date = fields.Datetime(string="Visit Date", default=fields.Datetime.now, required=True)
    coach_id = fields.Many2one('res.partner', string="Coach", domain="[('is_coach', '=', True)]")
    notes = fields.Text(string="Notes")

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        # You could add logic to send notification or log visits
        return rec
