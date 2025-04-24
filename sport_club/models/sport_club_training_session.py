from odoo import models, fields


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

    name = fields.Char(string="Title", required=True, translate=True)
    coach_id = fields.Many2one('sport.club.coach', string="Coach", required=True)
    member_ids = fields.Many2many('sport.club.member', string="Participants")
    session_date = fields.Datetime(string="Date", required=True)
    session_type = fields.Selection([
        ('group', 'Group Training'),
        ('personal', 'Personal Training'),
        ('online', 'Online Session')],
        string="Type", default='group')
    notes = fields.Text(string="Notes")
