from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class ClubVisit(models.Model):
    _name = 'sport.club.visit'
    _description = 'Club Visit'
    _order = 'visit_date desc'

    name = fields.Char(
        string="Visit Name",
        required=True,
        compute='_compute_name',
        translate=True)

    member_id = fields.Many2one(
        comodel_name='res.partner',
        required=True,
        string='Member',
        inverse_name='club_visit_ids'  # Ensure that this matches the inverse relation in `res.partner`
    )

    session_id = fields.Many2one(
        comodel_name='sport.club.training.session',
        required=True)

    subscription_id = fields.Many2one(
        comodel_name='sport.club.subscription',
        compute='_compute_subscription',
        store=True)

    visit_date = fields.Date(
        default=fields.Date.context_today,
        required=True)

    @api.depends('member_id', 'session_id')
    def _compute_subscription(self):
        for rec in self:
            if rec.member_id and rec.session_id:
                subscription = self.env['sport.club.subscription'].search([
                    ('member_id', '=', rec.member_id.id),
                    ('is_active', '=', True)
                ], limit=1, order='start_date desc')
                rec.subscription_id = subscription.id if subscription else False

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            subscription = rec.subscription_id
            if not subscription:
                raise ValidationError(_("No active subscription found."))

            if rec.session_id.session_type == 'group':
                if subscription.group_sessions_left <= 0:
                    raise ValidationError(_("Not enough group sessions."))
                subscription.group_sessions_left -= 1
            elif rec.session_id.session_type == 'personal':
                if subscription.personal_sessions_left <= 0:
                    raise ValidationError(_("Not enough personal sessions."))
                subscription.personal_sessions_left -= 1
        return records

    @api.depends('member_id')
    def _compute_name(self):
        for record in self:
            if record.member_id:
                record.name =  record.member_id.name
            else:
                record.name = _("Visit")
