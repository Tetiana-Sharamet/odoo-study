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
    member_ids = fields.Many2many(
        comodel_name='res.partner',
        string="Participants")
    session_date = fields.Datetime(
        string="Date",
        required=True)
    session_type = fields.Selection([
        ('group', 'Group Training'),
        ('personal', 'Personal Training'),
        ('online', 'Online Session')],
        default='group')

    duration = fields.Float(
        string='Duration (hrs)',
        default=1)
    location_id = fields.Many2one(
        comodel_name='fitness.location',
        required=True)
    remaining_seats = fields.Integer(
        compute="_compute_remaining_seats")

    group_category = fields.Selection([
        ('yoga', 'Yoga'),
        ('aerobics', 'Aerobics'),
        ('pilates', 'Pilates'),
        ('crossfit', 'Crossfit'),
        ('stretching', 'Stretching'),
    ])

    @api.constrains('coach_id', 'session_date', 'duration', 'location_id')
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
                overlap_end_time = overlap_start_time + timedelta(hours=overlap.duration)

                # Перевірка на часове перекриття
                if not (end_time <= overlap_start_time or start_time >= overlap_end_time):
                    raise ValidationError(_(
                        f"Тренер {rec.coach_id.name} вже має заняття у {rec.location_id.name} на {rec.session_date} "
                        f"з {start_time} по {end_time} год. "
                        f"Перекриття з {overlap_start_time} по {overlap_end_time} год."
                    ))

    @api.onchange('session_type')
    def _onchange_training_type(self):
        Location = self.env['fitness.location']

        if self.session_type == 'personal':
            # Отримуємо першу доступну локацію для персональних або самостійних
            location = Location.search([('location_type', '=', 'personal')], limit=1)
            return {
                'domain': {
                    'location_id': [('location_type', '=', 'personal')]
                },
                'value': {
                    'location_id': location.id if location else False
                }
            }

        if self.session_type == 'group':
            location = Location.search([('location_type', '=', 'group')], limit=1)
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

    @api.constrains('location_id', 'member_ids')
    def _check_capacity(self):
        for rec in self:
            if rec.location_id and rec.location_id.capacity:
                participant_count = len(rec.member_ids)
                if participant_count > rec.location_id.capacity:
                    raise ValidationError(_(
                        f"Кількість учасників ({participant_count}) перевищує місткість "
                        f"локації '{rec.location_id.name}' ({rec.location_id.capacity})."
                    ))

    @api.depends('member_ids', 'location_id.capacity', 'session_type')
    def _compute_remaining_seats(self):
        for rec in self:
            if rec.session_type == 'personal':
                rec.remaining_seats = 1
            else:
                if rec.location_id:
                    rec.remaining_seats = rec.location_id.capacity - len(rec.member_ids)
                else:
                    rec.remaining_seats = 0

    @api.onchange('session_type')
    def _onchange_training_type_clear_group_category(self):
        if self.session_type != 'group':
            self.group_category = False

    @api.depends('location_id', 'coach_id', 'group_category')
    def _compute_name(self):
        for record in self:
            record.name = '%s / %s / %s' % (
                record.group_category,
                record.location_id.name,
                record.coach_id.name)
