odoo.define('loonwholesale.loon_product', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    const Dialog = require('web.Dialog');
    const { _t, qweb } = require('web.core');
    const ajax = require('web.ajax');
    const session = require('web.session');

    // Account section js
    publicWidget.registry.LoonWholeAccount = publicWidget.Widget.extend({
        jsLibs: [],
        selector: '#wrap',
        events: {
            'click .add-to-cart': "_addToCart"
        },

        /**
         * @override
         */
        init: function () {
            this._super.apply(this, arguments);
        },

        _addToCart: function(ev) {
            var $item = $(ev.currentTarget);
            var $form = $item.parent().parent().find('form');
            var $input = $item.parent().parent().find('input.addtc');
        }
    })
});