# models/wizard/renew_subscription_wizard.py
from datetime import timedelta
from odoo import models, fields


class RenewSubscriptionWizard(models.TransientModel):
    _name = 'sport.club.subscription.renew.wizard'
    _description = 'Renew Subscription Wizard'

    subscription_id = fields.Many2one(
        'sport.club.subscription', required=True)

    member_id = fields.Many2one(
        related='subscription_id.member_id', store=True, readonly=True)

    subscription_type_id = fields.Many2one(
        'sport.club.subscription.type',
        string="Subscription Type",
        default=lambda self: self.subscription_id.subscription_type_id.id,
        required=True)

    duration_months = fields.Integer(
        string="Duration (months)", default=1, required=True)

    def action_renew(self):
        self.ensure_one()
        new_start_date = self.subscription_id.end_date + timedelta(days=1)

        self.env['sport.club.subscription'].create({
            'member_id': self.member_id.id,
            'start_date': new_start_date,
            'duration_months': self.duration_months,
            'subscription_type_id': self.subscription_type_id.id,
        })

        return {'type': 'ir.actions.act_window_close'}
