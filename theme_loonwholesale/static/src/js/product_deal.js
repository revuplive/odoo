odoo.define('theme_loonwholesale.product_deal', function(require) {
    'use strict';

    var Animation = require('website.content.snippets.animation');
    var ajax = require('web.ajax');

    Animation.registry.best_deal = Animation.Class.extend({
        selector: '.loon-product-deal',
        start: function() {
            var self = this;
            var products = $('.product-loon');
            var countdown_day = $('.countdown-day');
            var countdown_hour = $('.countdown-hour');
            var countdown_minute = $('.countdown-minute');
            var countdown_second = $('.countdown-second');
            ajax.jsonRpc('/get_product_loon', 'call', {})
                .then(function(data) {
                    if (data) {
                        // products.each(function(product) {
                        //     $(this).empty().append(data);
                        // });
                        $(products).empty().append(data);
                    }
                });
            ajax.jsonRpc('/get_countdown_loon', 'call', {})
                .then(function(data) {
                    if (data) {
                        var end_date = new Date(data).getTime();
                        var days, hours, minutes, seconds;
                        setInterval(function() {
                            var current_date = new Date().getTime();
                            var seconds_left = (end_date - current_date) / 1000;
                            days = parseInt(seconds_left / 86400);
                            seconds_left = seconds_left % 86400;
                            hours = parseInt(seconds_left / 3600);
                            seconds_left = seconds_left % 3600;
                            minutes = parseInt(seconds_left / 60);
                            seconds = parseInt(seconds_left % 60);
                            $(countdown_day).html('' + days + '')
                            $(countdown_hour).html('' + hours + '')
                            $(countdown_minute).html('' + minutes + '')
                            $(countdown_second).html('' + seconds + '')
                                // countdown_day.each(function(day) {
                                //     $(this).html('' + days + '')
                                // });
                                // countdown_hour.each(function(hour) {
                                //     $(this).html('' + hours + '')
                                // });
                                // countdown_minute.each(function(minute) {
                                //     $(this).html('' + minutes + '')
                                // });
                                // countdown_second.each(function(second) {
                                //     $(this).html('' + seconds + '')
                                // });
                        }, 1000);
                    }
                })
        },
    });
});