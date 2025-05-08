from odoo.tests.common import TransactionCase
from datetime import date, timedelta


class TestSportClubSubscription(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'John Doe'
        })

        self.subscription_type = self.env['sport.club.subscription.type'].create({
            'name': 'Standard Plan',
            'allow_group_sessions': True,
            'allow_personal_sessions': True,
            'group_sessions_limit': 10,
            'personal_sessions_limit': 5,
            'price': 50.0
        })

    def test_subscription_creation_sets_fields(self):
        today = date.today()
        sub = self.env['sport.club.subscription'].create({
            'member_id': self.partner.id,
            'start_date': today,
            'duration_months': 2,
            'subscription_type_id': self.subscription_type.id
        })

        # Перевірка, що підписка зробила учасника членом клубу
        self.assertTrue(self.partner.is_club_member)

        # Перевірка розрахованої дати закінчення
        expected_end = today + timedelta(days=60)
        self.assertEqual(sub.end_date, expected_end)
