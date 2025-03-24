from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

class HHDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'

    name = fields.Char()
    description = fields.Text()
    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        ondelete='cascade')

    child_ids = fields.One2many(
        comodel_name='hr.hospital.disease',
        inverse_name='parent_id',
        string='Sub Diseases')

    complete_name = fields.Char(
        string='Complete Name',
        compute='_compute_complete_name',
        recursive=True, store=True)
    parent_path = fields.Char(
        index=True,
        unaccent=False)

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for record in self:
            if record.parent_id:
                record.complete_name = '%s / %s' % (
                    record.parent_id.complete_name, record.name)
            else:
                record.complete_name = record.name

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive categories.'))

    @api.model
    def name_create(self, name):
        record = self.create({'name': name})
        return record.id, record.display_name

    @api.depends_context('hierarchical_naming')
    def _compute_display_name(self):
        if self.env.context.get('hierarchical_naming', True):
            return super()._compute_display_name()
        for record in self:
            record.display_name = record.name
