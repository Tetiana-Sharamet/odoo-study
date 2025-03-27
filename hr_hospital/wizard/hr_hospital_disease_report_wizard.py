from odoo import models, fields


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

    def get_disease_report(self):
        domain = []

        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))

        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))
        if self.date_from:
            domain.append(('scheduled_date', '>=', self.date_from))
        if self.date_to:
            domain.append(('scheduled_date', '<=', self.date_to))

        diagnosis_records = self.env['hr.hospital.visit'].search(domain)

        return diagnosis_records
