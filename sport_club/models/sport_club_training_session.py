from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class SportClubTrainingSession(models.Model):
    """
    Model representing a training session in the sport club.

    Attributes:
        name (Char): Title of the training session.
        coach_id (Many2one): Coach conducting the session.
        member_ids (Many2many): Participants attending the session.
        session_date (Datetime): Date and time of the session.
        session_type (Selection): Type of the session.
        notes (Text): Additional notes.
    """
    _name = 'sport.club.training.session'
    _description = 'Training Session'

    name = fields.Char(
        string="Title",
        compute='_compute_name',
        translate=True)
    coach_id = fields.Many2one(
        comodel_name='sport.club.coach',
        required=True)

    visit_ids = fields.One2many(
        comodel_name='sport.club.visit',
        inverse_name='session_id',
        string='Participants'
    )
    session_date = fields.Datetime(
        string="Date",
        required=True)

    session_type = fields.Selection([
        ('group', 'Group Training'),
        ('personal', 'Personal Training')],
        default = 'group')

    duration = fields.Float(
        string='Duration (hrs)',
        default=1)
    location_id = fields.Many2one(
        comodel_name='fitness.location',
        required=True)
    remaining_seats = fields.Integer(
        compute="_compute_remaining_seats",
        store=True
    )

    group_category = fields.Selection([
        ('yoga', 'Yoga'),
        ('aerobics', 'Aerobics'),
        ('pilates', 'Pilates'),
        ('crossfit', 'Crossfit'),
        ('stretching', 'Stretching'),
    ])

    @ api.constrains('coach_id', 'session_date', 'duration', 'location_id')
    def _check_trainer_location_conflict(self):
        for rec in self:
            # Переведемо дату початку та тривалість в час
            start_time = rec.session_date
            end_time = start_time + timedelta(hours=rec.duration)

            # Перевірка на перетини
            overlapping = self.env['sport.club.training.session'].search([
                ('id', '!=', rec.id),
                ('session_date', '<', end_time),
                ('session_date', '>=', rec.session_date),
                '|',  # оператор OR
                ('coach_id', '=', rec.coach_id.id),
                ('location_id', '=', rec.location_id.id),
            ])

            for overlap in overlapping:
                overlap_start_time = overlap.session_date
                overlap_end_time = (overlap_start_time
                                    + timedelta(hours=overlap.duration))

                # Перевірка на часове перекриття
                if not (end_time <= overlap_start_time or
                        start_time >= overlap_end_time):
                    raise ValidationError(_(
                        f"Coach {rec.coach_id.name} already has a class at "
                        f"{rec.location_id.name} on {rec.session_date} "
                        f"from {start_time} to {end_time} "
                        f"Overlap from {overlap_start_time} "
                        f"to {overlap_end_time}"
                    ))

    @api.onchange('session_type')
    def _onchange_training_type(self):
        Location = self.env['fitness.location']

        if self.session_type == 'personal':
            # Отримуємо першу доступну локацію
            # для персональних або самостійних
            location = Location.search([('location_type',
                                         '=', 'personal')], limit=1)
            return {
                'domain': {
                    'location_id': [('location_type', '=', 'personal')]
                },
                'value': {
                    'location_id': location.id if location else False
                }
            }

        if self.session_type == 'group':
            location = Location.search([('location_type',
                                         '=', 'group')], limit=1)
            return {
                'domain': {
                    'location_id': [('location_type', '=', 'group')]
                },
                'value': {
                    'location_id': location.id if location else False
                }
            }

        return {
            'domain': {'location_id': []},
            'value': {'location_id': False}
        }

    @api.constrains('location_id', 'visit_ids')
    def _check_capacity(self):
        for rec in self:
            if rec.location_id and rec.location_id.capacity and rec.session_type == 'group':
                participant_count = len(rec.visit_ids)
                if participant_count > rec.location_id.capacity:
                    raise ValidationError(_(
                        f"The number of participants ({participant_count}) "
                        f"exceeds the capacity of "
                        f"location '{rec.location_id.name}' "
                        f"({rec.location_id.capacity})."
                    ))
            if rec.session_type == 'personal':
                participant_count = len(rec.visit_ids)
                if participant_count > 1:
                    raise ValidationError(_(
                        f"Number of participants ({participant_count}) "
                        f"exceeds 1 for personal training."))

    @api.depends('session_type', 'visit_ids')
    def _compute_remaining_seats(self):
        for rec in self:
            if rec.session_type == 'personal':
                visits = self.env['sport.club.visit'].search_count([
                    ('session_id', '=', rec.id)
                ])
                rec.remaining_seats = 1 - visits
            else:
                visits = self.env['sport.club.visit'].search_count([
                    ('session_id', '=', rec.id)
                ])
                rec.remaining_seats = (rec.location_id.capacity or 0) - visits

    @api.depends('location_id', 'coach_id', 'group_category')
    def _compute_name(self):
        for record in self:
            record.name = '%s / %s / %s' % (
                record.group_category,
                record.location_id.name,
                record.coach_id.name)
