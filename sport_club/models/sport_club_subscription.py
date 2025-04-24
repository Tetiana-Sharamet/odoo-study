from odoo import models, fields, api
from datetime import timedelta


class SportClubSubscription(models.Model):
    """
    Model representing a subscription plan for club members.

    Attributes:
        name (Char): Subscription name.
        member_id (Many2one): Member who purchased the subscription.
        start_date (Date): Subscription start date.
        duration_months (Integer): Duration in months.
        end_date (Computed Date): End date based on start and duration.
        price (Float): Subscription cost.
        subscription_type (Selection): Type of subscription.
        is_active (Bool): Whether the subscription is currently active.
    """
    _name = 'sport.club.subscription'
    _description = 'Club Subscription'

    name = fields.Char(string="Subscription Name", required=True, translate=True)
    member_id = fields.Many2one('sport.club.member', string="Member", required=True)
    start_date = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    duration_months = fields.Integer(string="Duration (Months)", default=1)
    end_date = fields.Date(string="End Date", compute="_compute_end_date", store=True)
    price = fields.Float(string="Price", required=True)
    subscription_type = fields.Selection([
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('vip', 'VIP')],
        string="Type", default='standard')
    is_active = fields.Boolean(string="Active", compute="_compute_is_active", store=True)

    @api.depends('start_date', 'duration_months')
    def _compute_end_date(self):
        for record in self:
            if record.start_date and record.duration_months:
                record.end_date = record.start_date + timedelta(days=30 * record.duration_months)

    @api.depends('start_date', 'end_date')
    def _compute_is_active(self):
        today = fields.Date.today()
        for record in self:
            record.is_active = record.start_date <= today <= (record.end_date or today)
