from odoo import models, fields,api


class SportClubCoach(models.Model):
    """
    Model representing a sport club coach.

    Attributes:
        name (Char): Full name of the coach.
        specialty (Char): Area of expertise.
        phone (Char): Contact phone number.
        email (Char): Contact email.
        active (Bool): Whether the coach is active.
        biography (Text): Short biography of the coach.
    """
    _name = 'sport.club.coach'
    _description = 'Sport Club Coach'
    _inherits = {'res.partner': 'partner_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Related Partner",
        required=True,
        ondelete='cascade')

    name = fields.Char(
        compute='_compute_name',
        store=True,
        translate=True)

    specialty = fields.Selection(
        selection=[
            ('dance', 'Dance'),
            ('yoga_stretching', 'Yoga/Stretching'),
            ('strength training', 'Strength training'),
            ('cardio training', 'Cardio  training'),
        ])


    is_active= fields.Boolean(
        string = 'Active'
    )
    biography = fields.Text()
    schedule_ids = fields.One2many(
        comodel_name='sport.club.training.session',
        inverse_name='coach_id',
        string="Future Schedules"
        )
    color = fields.Integer(
        store=True)

    future_schedule_ids = fields.One2many(
        comodel_name='sport.club.training.session',
        inverse_name='coach_id',
        string="Future Schedules",
        compute='_compute_future_schedules'
    )

    @api.depends('schedule_ids.session_date')
    def _compute_future_schedules(self):
        # Оновлюємо поле future_schedule_ids лише з тренуваннями, де дата більше поточної
        for record in self:
            future_sessions = record.schedule_ids.filtered(lambda x: x.session_date > fields.Datetime.now())
            record.future_schedule_ids = future_sessions

    @api.depends('partner_id')
    def _compute_name(self):
        for record in self:
            if record.partner_id:
                record.name = record.partner_id.name
