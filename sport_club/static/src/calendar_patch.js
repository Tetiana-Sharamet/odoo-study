odoo.define('sport_club.CalendarViewPatch', function (require) {
    "use strict";

    const CalendarRenderer = require('web.CalendarRenderer');

    CalendarRenderer.include({
        getFullCalendarOptions: function () {
            const options = this._super.apply(this, arguments);
            options.slotMinTime = "07:00:00";
            options.slotMaxTime = "20:00:00";
            return options;
        },
    });
});
