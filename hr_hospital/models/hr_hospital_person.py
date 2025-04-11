from odoo import models, fields


class Person(models.AbstractModel):
    _name = 'hr.hospital.person'
    _description = 'Person'

    last_name = fields.Char()  # Прізвище
    first_name = fields.Char()  # Ім'я
    phone = fields.Char()  # Телефон
    photo = fields.Binary()
    user_id = fields.Many2one(
        comodel_name='res.users',
        ondelete='set null')

    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
        ])
