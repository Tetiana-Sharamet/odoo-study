from odoo import models, fields, api


class SportClubMember(models.Model):
    """
    Model representing a member of the sport club.

    Attributes:
        name (Char): Full name of the member.
        birth_date (Date): Date of birth.
        phone (Char): Contact number.
        email (Char): Email address.
        gender (Selection): Gender of the member.
        active_subscription (Many2one): Current active subscription.
        photo (Binary): Profile photo.
    """
    _name = 'sport.club.member'
    _description = 'Sport Club Member'

    name = fields.Char(string="Name", required=True, translate=True)
    birth_date = fields.Date(string="Birth Date")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')],
        string="Gender"
    )
    photo = fields.Binary(string="Photo")
    active_subscription_id = fields.Many2one('sport.club.subscription', string="Active Subscription")
