from odoo import models, fields, api


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

    name = fields.Char(string="Name", required=True, translate=True)
    specialty = fields.Char(string="Specialty")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    active = fields.Boolean(string="Active", default=True)
    biography = fields.Text(string="Biography")
