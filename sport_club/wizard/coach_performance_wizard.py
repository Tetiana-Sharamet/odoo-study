from odoo import models, fields

class CoachPerformanceWizard(models.TransientModel):
    _name = 'sport.club.coach.performance.wizard'
    _description = 'Coach Performance Wizard'

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    coach_ids = fields.Many2many('sport.club.coach')

    def action_print_report(self):
        if not self.coach_ids:
            self.coach_ids = self.env['sport.club.coach'].search([])
        data = {
            'date_from': self.date_from.isoformat(),
            'date_to': self.date_to.isoformat(),
            'coaches': []
        }

        for coach in self.coach_ids:
            sessions = self.env['sport.club.training.session'].search([
                ('coach_id', '=', coach.id),
                ('session_date', '>=', self.date_from),
                ('session_date', '<=', self.date_to)
            ])
            total_participants = sum(len(s.visit_ids) for s in sessions)
            session_count = len(sessions)
            avg = total_participants / session_count if session_count else 0
            data['coaches'].append({
                'coach': coach,
                'session_count': session_count,
                'total_participants': total_participants,
                'avg_participants': avg,
            })

        return self.env.ref('sport_club.action_report_coach_performance').report_action(self, data=data)
