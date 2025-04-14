from datetime import datetime
from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError



class TestHospitalVisit(TransactionCase):

    def setUp(self):
        super().setUp()
        # Створення тестових даних: лікар, пацієнт, хвороба
        self.patient = self.env['hr.hospital.patient'].create({
            'name': 'John Doe',
        })
        self.doctor = self.env['hr.hospital.doctor'].create({
            'name': 'Dr. Smith',
        })
        self.disease = self.env['hr.hospital.disease'].create({
            'name': 'Flu',
        })

    def test_write_with_completed_status(self):
        # Створення візиту
        visit = self.env['hr.hospital.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'disease_id': self.disease.id,
            'scheduled_date': datetime(2025, 4, 12, 11, 0),
            'visit_status': 'completed',
        })
        # Спроба змінити час або лікаря для візиту зі статусом "completed"
        with self.assertRaises(ValidationError):
            visit.write({'scheduled_date': datetime(2025, 4, 12, 11, 0)})

    def test_check_patient_doctor_schedule(self):
        # Створення першого візиту
        self.env['hr.hospital.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'scheduled_date': datetime(2025, 4, 12, 10, 0),
        })
        # Створення другого візиту для
        # того ж пацієнта і лікаря на той самий день
        with self.assertRaises(ValidationError):
            self.env['hr.hospital.visit'].create({
                'patient_id': self.patient.id,
                'doctor_id': self.doctor.id,
                'scheduled_date': datetime(2025, 4, 12, 11, 0),
            })

    def test_unlink_with_diagnosis(self):
        # Створення візиту
        visit = self.env['hr.hospital.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'scheduled_date': datetime(2025, 4, 12, 11, 0),
        })
        # Створення діагнозу для візиту
        self.env['hr.hospital.diagnosis'].create({
            'visit_id': visit.id,
            'disease_id': self.disease.id,
        })
        # Спроба видалити візит, який має діагноз
        with self.assertRaises(ValidationError):
            visit.unlink()

    def test_write_without_completed_status(self):
        # Створення візиту
        visit = self.env['hr.hospital.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'scheduled_date':
                datetime(2025, 4, 12, 11, 0),
            'visit_status': 'scheduled',
        })
        # Спроба змінити час для візиту, який ще не завершений
        visit.write({'scheduled_date': datetime(2025, 4, 12, 11, 0)})
        self.assertEqual(visit.scheduled_date,
                         datetime(2025, 4, 12, 11, 0),
                         "Час візиту не був оновлений")
