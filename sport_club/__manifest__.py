{
    'name': 'Sport Club',
    'version': '17.0.0.1.0',
    'license': 'OPL-1',
    'category': 'Sports',
    'summary': 'Module for managing a sports club '
               'with sessions, visits, and reports',
    'author': 'Tetiana Sharamet',
    'depends': ['base', 'mail', 'product'],

    'data': [
        'security/sport_club_groups.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/locations.xml',
        'views/sport_club_menu.xml',
        'views/club_visit_views.xml',
        'views/coach_views.xml',
        'views/training_session_views.xml',
        'views/subscription_views.xml',
        'views/res_partner_views.xml',
        'views/res_partner_search_view.xml',
        'views/fitness_location.xml',
        'data/subscription_type_data.xml',
        'views/subscription_type_views.xml',
        'wizard/renew_subscription_wizard_view.xml',
        'wizard/coach_performance_wizard_view.xml',
        'report/report_coach.xml',
        'report/report_coach_performance_template.xml',

    ],

    'demo': [
        'demo/sport_club_subscription_demo.xml',
        'demo/sport_club_coach_demo.xml',
        'demo/sport_club_training_session_demo.xml',
        'demo/sport_club_visit_demo.xml',
    ],
    'installable': True,
    'application': True,
    # 'i18n': True,
}
