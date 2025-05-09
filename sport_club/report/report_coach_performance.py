from odoo import models
import logging
import json

_logger = logging.getLogger(__name__)


class CoachPerformanceReport(models.AbstractModel):
    _name = 'report.sport_club.report_coach_performance_template'
    _description = 'Coach Performance Report'

    def _get_report_values(self, docids, data=None):
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning('REPORT RECEIVED DATA: %s', data)
        _logger.warning('✅ _get_report_values CALLED')

        # Якщо data None, створюємо порожній dict
        if data is None:
            data = {}

        options = data or {}
        coaches = options.get('coaches', [])
        date_from = options.get('date_from')
        date_to = options.get('date_to')
        _logger.warning('FINAL DOCS: %s', coaches)
        return {
            'doc_ids': docids,
            'doc_model': 'sport.club.coach.performance.wizard',
            'docs': coaches,
            'date_from': date_from,
            'date_to': date_to,
        }
