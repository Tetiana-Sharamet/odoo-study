from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class HHDisease(models.Model):
    """
    Model representing a disease in the hospital system.

    This model is used to define diseases, their descriptions,
    and their hierarchical relationships (e.g., parent and child diseases).
    It also provides the ability to compute the full name
    of a disease based on its parent, and ensures
    that recursive categories are not created.

    Attributes:
        name (str): The name of the disease.
        description (Text): A detailed description of the disease.
        parent_id (Many2one): The parent disease for
        hierarchical categorization.
        child_ids (One2many): The sub-diseases or
        child diseases of this disease.
        complete_name (str): A computed field representing
        the full name of the disease, including
        its parent diseases.
        parent_path (str): A field to store the path
        of parent diseases for indexing and searching.
    """
    _name = 'hr.hospital.disease'
    _description = 'Disease'
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char(translate=True, help="The name of the disease.")

    description = fields.Text(
        translate=True,
        help="A detailed description of the disease.")

    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        ondelete='cascade',
        help="The parent disease for"
             " hierarchical classification.")

    child_ids = fields.One2many(
        comodel_name='hr.hospital.disease',
        inverse_name='parent_id',
        string='Sub Diseases',
        help="The child diseases under this disease category.")

    complete_name = fields.Char(
        compute='_compute_complete_name',
        recursive=True, store=True,
        help="The full name of the disease, "
             "computed based on its parent disease names.")

    parent_path = fields.Char(
        index=True,
        unaccent=False,
        help="The path to the parent disease"
             " for hierarchical indexing.")

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        """
        Computes the full name of the disease,
         including the parent diseases.

        This method generates the complete name
        of a disease by concatenating the parent's complete name
        with the current disease's name.
        If there is no parent disease,
        the complete name will be just the disease's name.
        """
        for record in self:
            if record.parent_id:
                record.complete_name = '%s / %s' % (
                    record.parent_id.complete_name, record.name)
            else:
                record.complete_name = record.name

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        """
        Validates that a disease cannot be its own ancestor
         (prevents recursive categorization).

        This method ensures that a disease cannot be assigned
        as a child of one of its own descendants,
        thus preventing recursion in the disease hierarchy.
        """
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive categories.'))

    @api.model
    def name_create(self, name):
        """
        Creates a new disease record based on the provided name.

        This method is called when a new disease name
        is created via the "Create" action, and it returns
        the ID and the display name of the newly created record.

        Args:
            name (str): The name of the disease to create.

        Returns:
            tuple: The ID and display name of the created disease.
        """
        record = self.create({'name': name})
        return record.id, record.display_name

    @api.depends_context('hierarchical_naming')
    def _compute_display_name(self):
        """
        Computes the display name of the disease
        based on hierarchical naming.

        This method adjusts the display name of the
        disease based on the context variable 'hierarchical_naming'.
        If this context variable is True, the default naming
         system is used, otherwise, a custom display name is set.
        """
        if self.env.context.get('hierarchical_naming', True):
            return super()._compute_display_name()
        for record in self:
            record.display_name = record.name
