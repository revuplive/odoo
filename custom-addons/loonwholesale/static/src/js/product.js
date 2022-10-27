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

        callserver: function (url, data, callback) {
            // ev.preventDefault();
            ajax.post({
                method: 'POST',
                url: url, 
                data: data,
                ContentType: 'application/json'
            }).then(function (result) {
                callback(result)
            }).guardedCatch(function (error) {
                // resolve();
            });
        },

        updateCartVal: function(data){
            console.log(data);
            document.getElementById('cart_with_items').classList.remove('d-none');
            document.getElementById('cart_empty').classList.add("d-none");
            document.getElementById('formdata').innerHTML = data['loon.cart_details'];
            document.getElementById('subtotal_p').value = data['subtotal']
            document.getElementById('count_p').value = data['items']
        },

        _addToCart: function (ev) {
            var $item = $(ev.currentTarget);
            var $form = $item.parent().parent().find('form');
            var $input = $item.parent().parent().find('input.addtc');
            var token = $form.find('.oe_product_image')[0].childNodes[1].value;
            var data = {
                'product_id': 1,
                'add_qty': $input.val(),
                'csrf_token': token
            }
            // this.callserver('/shop/cart/update_json', data, null);
            return this._rpc({
                route: "/loon/cart/update_json",
                params: data,
            }).then(async data => {
                // if (data.cart_quantity && (data.cart_quantity !== parseInt($("#addtc-sticky-cart-count").text()))) {
                    // await animateClone($('#addtc-sticky-cart').first(), this.$itemImgContainer, 25, 40);
                    var txt = parseInt($("#addtc-sticky-cart-count").text()) +  data.cart_quantity;
                    $("#addtc-sticky-cart-count").text(txt);
                    this.updateCartVal(data);
                // }
            });
        }
    })
});