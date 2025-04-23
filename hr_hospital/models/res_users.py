from odoo import models, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.constrains('email')
    def _check_unique_email(self):
        for rec in self:
            if rec.email:
                duplicate = self.search([
                    ('email', '=', rec.email),
                    ('id', '!=', rec.id)
                ])
                if duplicate:
                    raise ValidationError(_("A user with this email "
                                            "address already exists."))
