from datetime import datetime, time
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
        domain="[('is_club_member', '=', True)]",
        inverse_name='club_visit_ids'
    )

    session_id = fields.Many2one(
        comodel_name='sport.club.training.session'
       )

    subscription_id = fields.Many2one(
        comodel_name='sport.club.subscription',
        compute='_compute_subscription',
        store=True)

    visit_date = fields.Date(
        default=fields.Date.context_today,
        required=True)
    is_independent = fields.Boolean(
        string="Independent Visit",
        compute="_compute_is_independent",
        store=True
    )

    visit_status = fields.Selection(
        selection=[
            ('scheduled', 'Scheduled'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled')
        ],
        copy=False,
        default='scheduled',
        help="The current status of the "
             "visit (scheduled, completed, or cancelled)."
    )

    @api.depends('member_id', 'session_id')
    def _compute_subscription(self):
        for rec in self:
            if rec.member_id and rec.session_id:
                subscription = self.env['sport.club.subscription'].search([
                    ('member_id', '=', rec.member_id.id),
                    ('is_active', '=', True)
                ], limit=1, order='start_date desc')
                rec.subscription_id = subscription.id\
                    if subscription else False

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            subscription = rec.subscription_id
            if not subscription:
                raise ValidationError(_("No active"
                                        " subscription found."))

            if subscription.group_sessions_left <= 0 and subscription.personal_sessions_left <= 0:
                rec.session_id = False
                rec.visit_status = 'done'
                continue

            if rec.session_id.session_type == 'group':
                if subscription.group_sessions_left <= 0:
                    raise ValidationError(_("Not enough "
                                            "group sessions."))
                subscription.group_sessions_left -= 1
            elif rec.session_id.session_type == 'personal':
                if subscription.personal_sessions_left <= 0:
                    raise ValidationError(_("Not enough "
                                            "personal sessions."))
                subscription.personal_sessions_left -= 1
            rec._validate_session_capacity()
        return records


    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            rec._validate_session_capacity()
        return res

    def _validate_session_capacity(self):
            if not self.session_id:
                return
            session = self.session_id
            # Отримаємо кількість існуючих візитів на цю сесію
            existing_visits = self.search_count([
                ('session_id', '=', session.id),
                ('id', '!=', self.id)
            ])
            if session.session_type == 'group':
                if existing_visits >= session.location_id.capacity:
                    raise ValidationError(_("No seats "
                                            "available in this group session."))

            elif session.session_type == 'personal':
                if existing_visits >= 1:
                    raise ValidationError(_("This personal "
                                            "session already has a participant."))


    @api.depends('member_id')
    def _compute_name(self):
        for record in self:
            if record.member_id:
                record.name = record.member_id.name
            else:
                record.name = _("Visit")


    @api.onchange('visit_date')
    def _onchange_visit_date_clear_invalid_session(self):
        if self.session_id and self.visit_date:
            session_date = self.session_id.session_date.date()
            if session_date != self.visit_date:
                self.session_id = False

    @api.depends('subscription_id', 'subscription_id.group_sessions_left', 'subscription_id.personal_sessions_left')
    def _compute_is_independent(self):
        for rec in self:
            sub = rec.subscription_id
            if not sub:
                rec.is_independent = False
            else:
                rec.is_independent = (sub.group_sessions_left <= 0 and sub.personal_sessions_left <= 0)






