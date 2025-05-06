{
    'name': 'Sport Club',
    'version': '17.0.0.1.0',
    'category': 'Sports',
    'summary': 'Module for managing a sports club '
               'with sessions, visits, and reports',
    'description': 'Manage club visits, '
                   'sessions, and create certificates.',
    'author': 'Tetiana Sharamet',
    'depends': ['base', 'product'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/locations.xml',
        'views/sport_club_menu.xml',
        'views/club_visit_views.xml',
        'views/report_certificate.xml',
        'views/coach_views.xml',
        'views/training_session_views.xml',
        'views/subscription_views.xml',
        'views/res_partner_views.xml',
        'views/fitness_location.xml',
        'reports/certificate_report.xml',
        'wizard/register_session_wizard_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'static/src/js/calendar_patch.js',
        ],
    },
    'demo': [
        'demo/club_visit_demo.xml',
    ],
    'installable': True,
    'application': True,
}
