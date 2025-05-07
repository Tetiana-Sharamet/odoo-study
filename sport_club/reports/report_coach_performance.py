from odoo import models

class CoachPerformanceReport(models.AbstractModel):
    _name = 'report.sport_club.report_coach_performance_template'

    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'doc_model': 'sport.club.coach.performance.wizard',
            'data': data,
        }
