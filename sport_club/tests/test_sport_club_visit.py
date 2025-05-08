from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class TestClubVisit(TransactionCase):

    def setUp(self):
        super().setUp()

        self.partner = self.env['res.partner'].create({
            'name': 'Test Member',
            'is_club_member': True,
        })

        self.coach_partner = self.env['res.partner'].create({
            'name': 'Coach X'
        })

        self.coach = self.env['sport.club.coach'].create({
            'partner_id': self.coach_partner.id,
            'specialty': 'Fitness',
            'is_active': True,
        })

        self.location = self.env['fitness.location'].create({
            'name': 'Main Hall',
            'location_type': 'group',
            'capacity': 2,
        })

        self.personal_location = self.env['fitness.location'].create({
            'name': 'Personal Room',
            'location_type': 'personal',
            'capacity': 1,
        })

        self.session_date = datetime.now() + timedelta(days=1)

    def create_subscription(self, member, group_left=1, personal_left=1):
        return self.env['sport.club.subscription'].create({
            'member_id': member.id,
            'group_sessions_left': group_left,
            'personal_sessions_left': personal_left,
            'is_active': True,
        })

    def test_visit_created_with_subscription(self):
        subscription = self.create_subscription(self.partner, group_left=1)

        session = self.env['sport.club.training.session'].create({
            'coach_id': self.coach.id,
            'session_date': self.session_date,
            'session_type': 'group',
            'location_id': self.location.id,
            'group_category': 'yoga',
        })

        visit = self.env['sport.club.visit'].create({
            'member_id': self.partner.id,
            'session_id': session.id,
            'visit_date': self.session_date.date()
        })

        self.assertEqual(visit.subscription_id, subscription)
        self.assertEqual(subscription.group_sessions_left, 0)

    def test_visit_without_subscription_fails(self):
        session = self.env['sport.club.training.session'].create({
            'coach_id': self.coach.id,
            'session_date': self.session_date,
            'session_type': 'group',
            'location_id': self.location.id,
            'group_category': 'yoga',
        })

        with self.assertRaises(ValidationError):
            self.env['sport.club.visit'].create({
                'member_id': self.partner.id,
                'session_id': session.id,
                'visit_date': self.session_date.date()
            })

    def test_group_capacity_limit(self):
        subscription = self.create_subscription(self.partner, group_left=3)

        session = self.env['sport.club.training.session'].create({
            'coach_id': self.coach.id,
            'session_date': self.session_date,
            'session_type': 'group',
            'location_id': self.location,
            'group_category': 'aerobics',
        })

        for i in range(2):
            partner = self.env['res.partner'].create({
                'name': f'Member {i}',
                'is_club_member': True
            })
            self.create_subscription(partner, group_left=1)
            self.env['sport.club.visit'].create({
                'member_id': partner.id,
                'session_id': session.id,
                'visit_date': self.session_date.date()
            })

        # This third visit should raise error (capacity = 2)
        third_partner = self.env['res.partner'].create({
            'name': 'Member 3',
            'is_club_member': True
        })
        self.create_subscription(third_partner, group_left=1)

        with self.assertRaises(ValidationError):
            self.env['sport.club.visit'].create({
                'member_id': third_partner.id,
                'session_id': session.id,
                'visit_date': self.session_date.date()
            })

    def test_personal_capacity(self):
        subscription = self.create_subscription(self.partner, personal_left=1)

        session = self.env['sport.club.training.session'].create({
            'coach_id': self.coach.id,
            'session_date': self.session_date,
            'session_type': 'personal',
            'location_id': self.personal_location,
        })

        visit1 = self.env['sport.club.visit'].create({
            'member_id': self.partner.id,
            'session_id': session.id,
            'visit_date': self.session_date.date()
        })

        # Another member can't join this personal session
        member2 = self.env['res.partner'].create({
            'name': 'Member 2',
            'is_club_member': True
        })
        self.create_subscription(member2, personal_left=1)

        with self.assertRaises(ValidationError):
            self.env['sport.club.visit'].create({
                'member_id': member2.id,
                'session_id': session.id,
                'visit_date': self.session_date.date()
            })

    def test_is_independent_flag(self):
        # Subscription with no sessions left
        sub = self.create_subscription(self.partner, group_left=0, personal_left=0)

        session = self.env['sport.club.training.session'].create({
            'coach_id': self.coach.id,
            'session_date': self.session_date,
            'session_type': 'group',
            'location_id': self.location,
        })

        visit = self.env['sport.club.visit'].create({
            'member_id': self.partner.id,
            'session_id': session.id,
            'visit_date': self.session_date.date()
        })

        self.assertTrue(visit.is_independent)
        self.assertEqual(visit.visit_status, 'done')
        self.assertFalse(visit.session_id)
