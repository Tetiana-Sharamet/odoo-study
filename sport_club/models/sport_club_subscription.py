from datetime import timedelta
from odoo import models, fields, api


class SportClubSubscription(models.Model):
    """
    Model representing a subscription plan for club members.

    Attributes:
        name (Char): Subscription name.
        member_id (Many2one): Member who
        purchased the subscription.
        start_date (Date): Subscription start date.
        duration_months (Integer): Duration in months.
        end_date (Computed Date): End date
        based on start and duration.
        price (Float): Subscription cost.
        subscription_type (Selection): Type of subscription.
        is_active (Bool): Whether the
        subscription is currently active.
    """
    _name = 'sport.club.subscription'
    _description = 'Club Subscription'

    name = fields.Char(
        string="Subscription Name",
        required=True,
        compute='_compute_name',
        translate=True)
    member_id = fields.Many2one(
        comodel_name='res.partner',
        required=True)
    start_date = fields.Date(
        required=True,
        default=fields.Date.today)
    duration_months = fields.Integer(
        string="Duration (Months)",
        default=1)
    end_date = fields.Date(
        compute="_compute_end_date",
        store=True)

    is_active = fields.Boolean(
        compute="_compute_is_active",
        store=True)

    subscription_type_id = fields.Many2one(
        'sport.club.subscription.type',
        string="Subscription Type",
        required=True)

    price = fields.Float(
        related='subscription_type_id.price',
        store=True)

    group_sessions_left = fields.Integer(
        compute='_compute_sessions_left',
        store=True)

    personal_sessions_left = fields.Integer(
        compute='_compute_sessions_left',
        store=True)

    @api.depends('start_date', 'duration_months')
    def _compute_end_date(self):
        for record in self:
            if (record.start_date and
                    record.duration_months):
                record.end_date = (record.start_date
                                   + timedelta(30 * record.duration_months))

    @api.depends('start_date', 'end_date')
    def _compute_is_active(self):
        today = fields.Date.today()
        for record in self:
            record.is_active = (record.start_date
                                <= today
                                <= (record.end_date or today))

    @api.depends('start_date', 'duration_months', 'member_id')
    def _compute_name(self):
        for record in self:
            if record.member_id or record.start_date:
                record.name = '%s  %s - %s month' % (
                    record.member_id.name,
                    record.start_date, record.duration_months)

    @api.depends('subscription_type_id')
    def _compute_sessions_left(self):
        for record in self:
            st = record.subscription_type_id
            record.group_sessions_left = st.group_sessions_limit \
                if st.allow_group_sessions \
                else 0
            record.personal_sessions_left = st.personal_sessions_limit \
                if st.allow_personal_sessions \
                else 0

    def action_open_renew_wizard(self):
        self.ensure_one()
        return {
            'name': 'Renew Subscription',
            'type': 'ir.actions.act_window',
            'res_model': 'sport.club.subscription.renew.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_subscription_id': self.id},
        }

    @api.model
    def create(self, vals):
        subscription = super().create(vals)
        if subscription.member_id:
            subscription.member_id.is_club_member = True
        return subscription

    @api.model
    def write(self, vals):
        res = super().write(vals)
        if 'member_id' in vals:
            for rec in self:
                if rec.member_id:
                    rec.member_id.is_club_member = True
        return res
