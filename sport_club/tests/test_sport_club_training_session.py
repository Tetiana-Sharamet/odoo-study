from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class TestSportClubTrainingSession(TransactionCase):

    def setUp(self):
        super().setUp()

        # Створюємо локації
        self.group_location = self.env['fitness.location'].create({
            'name': 'Group Hall',
            'location_type': 'group',
            'capacity': 10,
        })
        self.personal_location = self.env['fitness.location'].create({
            'name': 'Personal Room',
            'location_type': 'personal',
            'capacity': 1,
        })

        # Створюємо тренера
        self.partner = self.env['res.partner'].create({'name': 'John Trainer'})
        self.coach = self.env['sport.club.coach'].create({
            'partner_id': self.partner.id,
            'specialty': 'strength training',
            'is_active': True,
        })

        # Дата для тренування
        self.date = datetime.now() + timedelta(days=1)

    def test_create_group_session(self):
        """Create a group session and check name is computed"""
        session = self.env['sport.club.training.session'].create({
            'coach_id': self.coach.id,
            'session_date': self.date,
            'duration': 1.0,
            'session_type': 'group',
            'location_id': self.group_location.id,
            'group_category': 'crossfit',
        })

        self.assertIn('crossfit', session.name)
        self.assertEqual(session.remaining_seats, 10)

    def test_conflict_detection(self):
        """Create two overlapping sessions for the same coach"""
        self.env['sport.club.training.session'].create({
            'coach_id': self.coach.id,
            'session_date': self.date,
            'duration': 2.0,
            'session_type': 'group',
            'location_id': self.group_location.id,
            'group_category': 'yoga',
        })

        with self.assertRaises(ValidationError):
            self.env['sport.club.training.session'].create({
                'coach_id': self.coach.id,
                'session_date': self.date + timedelta(minutes=30),  # overlaps
                'duration': 1.0,
                'session_type': 'group',
                'location_id': self.group_location.id,
                'group_category': 'pilates',
            })

    def test_group_capacity_validation(self):
        """Exceed group session capacity"""
        session = self.env['sport.club.training.session'].create({
            'coach_id': self.coach.id,
            'session_date': self.date,
            'duration': 1.0,
            'session_type': 'group',
            'location_id': self.group_location.id,
            'group_category': 'aerobics',
        })

        # Створюємо більше 10 візитів
        partner_model = self.env['res.partner']
        visit_model = self.env['sport.club.visit']
        subscription_model = self.env['sport.club.subscription']

        subscription_type = self.env['sport.club.subscription.type'].create({
            'name': 'Basic',
            'price': 100.0,
            'allow_group_sessions': True,
            'group_sessions_limit': 5,
            'allow_personal_sessions': True,
            'personal_sessions_limit': 1,
        })

        for i in range(11):
            member = partner_model.create({
                'name': f'Member {i}',
                'is_club_member': True,
            })
            subscription = subscription_model.create({
                'member_id': member.id,
                'is_active': True,
                'group_sessions_left': 5,
                'personal_sessions_left': 0,
                'subscription_type_id': subscription_type.id
            })
            if i == 10:
                with self.assertRaises(ValidationError):
                    visit_model.create({
                        'member_id': member.id,
                        'session_id': session.id,
                        'visit_date': self.date.date(),
                    })
            else:
                visit_model.create({
                    'member_id': member.id,
                    'session_id': session.id,
                    'visit_date': self.date.date(),
                })

    def test_personal_session_single_participant(self):
        """Ensure only one participant allowed for personal session"""
        session = self.env['sport.club.training.session'].create({
            'coach_id': self.coach.id,
            'session_date': self.date,
            'duration': 1.0,
            'session_type': 'personal',
            'location_id': self.personal_location.id,
            'group_category': 'yoga',
        })

        partner1 = self.env['res.partner'].create({
            'name': 'Solo Member 1',
            'is_club_member': True
        })
        partner2 = self.env['res.partner'].create({
            'name': 'Solo Member 2',
            'is_club_member': True
        })

        subscription_type = self.env['sport.club.subscription.type'].create({
            'name': 'Basic',
            'price': 100.0,
            'allow_group_sessions': True,
            'group_sessions_limit': 5,
            'allow_personal_sessions': True,
            'personal_sessions_limit': 1,
        })

        subscription1 = self.env['sport.club.subscription'].create({
            'member_id': partner1.id,
            'is_active': True,
            'personal_sessions_left': 1,
            'subscription_type_id': subscription_type.id
        })
        subscription2 = self.env['sport.club.subscription'].create({
            'member_id': partner2.id,
            'is_active': True,
            'personal_sessions_left': 1,
            'subscription_type_id': subscription_type.id
        })

        self.env['sport.club.visit'].create({
            'member_id': partner1.id,
            'session_id': session.id,
            'visit_date': self.date.date(),
        })

        with self.assertRaises(ValidationError):
            self.env['sport.club.visit'].create({
                'member_id': partner2.id,
                'session_id': session.id,
                'visit_date': self.date.date(),
            })
