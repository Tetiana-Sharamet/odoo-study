from odoo import models, fields


class CoachPerformanceWizard(models.TransientModel):
    _name = 'sport.club.coach.performance.wizard'
    _description = 'Coach Performance Wizard'

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    coach_ids = fields.Many2many('sport.club.coach')

    def action_print_report(self):
        import logging
        _logger = logging.getLogger(__name__)

        # Отримуємо список тренерів
        coach_ids = self.coach_ids or self.env['sport.club.coach'].search([])
        _logger.warning('COACHES COUNT: %s', len(coach_ids))

        # Створюємо список словників для кожного тренера
        coach_data_list = []

        for coach in coach_ids:
            sessions = self.env['sport.club.training.session'].search([
                ('coach_id', '=', coach.id),
                ('session_date', '>=', self.date_from),
                ('session_date', '<=', self.date_to)
            ])

            total_participants = sum(len(s.visit_ids) for s in sessions)
            session_count = len(sessions)
            avg = total_participants / session_count if session_count else 0

            # Створюємо словник з даними тренера
            coach_data = {
                'coach_id': coach.id,
                'coach_name': coach.name,
                'session_count': session_count,
                'total_participants': total_participants,
                'avg_participants': avg,
            }
            coach_data_list.append(coach_data)

        # Створюємо словник з усіма даними
        data = {
            'date_from': self.date_from.strftime('%d-%m-%Y'),
            'date_to': self.date_to.strftime('%d-%m-%Y'),
            'coaches': coach_data_list,
        }

        _logger.warning('FINAL DATA: %s', data)
        _logger.warning('coach_data_list: %s', self.coach_ids.ids)

        return self.env.ref('sport_club.action_report_coach_performance').report_action(
            docids=self.coach_ids.ids,
            data=data
            )
