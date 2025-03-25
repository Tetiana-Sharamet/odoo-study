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

    date_from = fields.Date('From Date', required=True)
    date_to = fields.Date('To Date', required=True)

    def get_disease_report(self):
        domain = []

        if self.doctor_ids:
            domain.append(('visit_id.doctor_id', 'in', self.doctor_ids.ids))

        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        domain.append(('visit_id.scheduled_date', '>=', self.date_from))
        domain.append(('visit_id.scheduled_date', '<=', self.date_to))

        diagnosis_records = self.env['hr.hospital.diagnosis'].search(domain)

        return diagnosis_records
