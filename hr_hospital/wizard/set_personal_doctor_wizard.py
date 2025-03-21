from odoo import models, fields

class HHSetPersonalDoctorWizard(models.TransientModel):
    _name = 'hr.hospital.set.personal.doctor.wizard'
    _description = 'Wizard to set personal doctor for selected patients'

    doctor_id = fields.Many2one(comodel_name='hr.hospital.doctor',
                                string='New Personal Doctor', required=True)
    patient_ids = fields.Many2many(comodel_name='hr.hospital.patient', )

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['patient_ids'] = [(6, 0, self.env.context.get('active_ids'))]
        return res

    def action_set_doctor(self):
        self.ensure_one()
        self.patient_ids.write({
            'doctor_id': self.doctor_id.id, })
