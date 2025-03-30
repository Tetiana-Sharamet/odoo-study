from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class DiseaseReportWizard(models.TransientModel):
    _name = 'hr.hospital.disease.report.wizard'
    _description = 'Wizard for generating disease report'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors',
        required=False
    )

    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease',
        string='Diseases',
        required=False
    )

    date_from = fields.Date(
        string='From Date',
        required=True
    )
    date_to = fields.Date(
        string='To Date',
        required=True
    )

    @api.constrains('date_from', 'date_to')
    def _check_date_range(self):
        for record in self:
            if record.date_from > record.date_to:
                raise ValidationError(
                    _("The 'From Date' should be before or equal to the 'To Date'."))

    def _get_report_base_filename(self):
        self.ensure_one()
        return 'Report - %s' % (self.date_from)

    @property
    def get_disease_report(self):
        domain = []

        if self.doctor_ids:
            domain.append('doctor_id', 'in', self.doctor_ids)

        if self.disease_ids:
            domain.append('disease_id', 'in', self.disease_ids)

        domain.append('diagnosis_date', '>=', self.date_from)
        domain.append('diagnosis_date', '<=', self.date_to)
        diagnoses = self.env['hr.hospital.diagnosis'].search(domain)

        return diagnoses

    def generate_report(self):
        diagnoses = self.get_disease_report

        report_data = {}
        for diagnosis in diagnoses:
            disease_name = diagnosis.disease_id.name
            if disease_name not in report_data:
                report_data[disease_name] = []
            report_data[disease_name].append(diagnosis)

        return {
            'type': 'ir.actions.report',
            'report_name': 'health_disease_report',
            'report_type': 'pdf',
            'data': {'report_data': report_data},
        }
