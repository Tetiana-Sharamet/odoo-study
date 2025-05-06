from odoo import models, fields


class SportClubSubscriptionType(models.Model):
    _name = 'sport.club.subscription.type'
    _description = 'Subscription Type'

    name = fields.Char(
        required=True)
    price = fields.Float(
        required=True)
    allow_gym_access = fields.Boolean(
        string="Access to Gym",
        default=True)
    allow_group_sessions = fields.Boolean(
        string="Group Sessions",
        default=False)
    group_sessions_limit = fields.Integer(
        string="Max Group Sessions",
        default=0)
    allow_personal_sessions = fields.Boolean(
        string="Personal Trainer",
        default=False)
    personal_sessions_limit = fields.Integer(
        string="Max Personal Sessions",
        default=0)

    description = fields.Text()
