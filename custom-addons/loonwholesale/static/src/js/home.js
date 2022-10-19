odoo.define('blogpost.blogpost', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    const Dialog = require('web.Dialog');
    const { _t, qweb } = require('web.core');
    const ajax = require('web.ajax');
    const session = require('web.session');

    // Account section js
    publicWidget.registry.blogpostAccount = publicWidget.Widget.extend({
        jsLibs: [],
        selector: '.homepage',
        events: {},

        /**
         * @override
         */
        init: function () {
            this._super.apply(this, arguments);
            // const myNodelist = document.querySelectorAll("section.s_three_columns");
            // show loader

            // show banner element
            this.callserver('/home/banner/metadata', null, this.banner_show)
            
            // // 0th element replace with the collections
            this.callserver('/home/collections/metadata', null, this.collection_show)
            // myNodelist[0].style.display = 'none';
            
            // // 1st element replace with the featured products
            this.callserver('/home/featured/metadata', null, this.feature_show)
            // myNodelist[1].style.display = 'none';

            // stop loader
        },

        /**
         * @override
         */
        start: function () {
            var def = this._super.apply(this, arguments);

            this.$state = this.$('select[name="state_id"]');
            this.$stateOptions = this.$state.filter(':enabled').find('option:not(:first)');

            return def;
        },

        banner_show: function(result) {
            const myNodelist = document.querySelectorAll("section.s_image_gallery");
            [...myNodelist][0].innerHTML = result;
        },

        collection_show: function(result) {
            const myNodelist = document.querySelectorAll("section.s_three_columns");
            [...myNodelist][0].innerHTML = result;
        },

        feature_show: function(result) {
            const myNodelist = document.querySelectorAll("section.s_three_columns");
            [...myNodelist][1].innerHTML = result;
        },

        callserver: function (url, data, callback) {
            // ev.preventDefault();
            ajax.post(url, {}).then(function (result) {
                callback(result)
            }).guardedCatch(function (error) {
                // resolve();
            });
        }
    });
});