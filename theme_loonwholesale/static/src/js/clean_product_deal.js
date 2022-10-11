odoo.define('theme_loonwholesale.clean_product_deal', function(require) {

    var options = require('web_editor.snippets.options');

    options.registry.clean_product_deal = options.Class.extend({

        cleanForSave: async function() {
            var products = $('.product-loon');
            $(products).empty();
            var countdowns = $('.countdown-numbers');
            const dFrag = $(document.createDocumentFragment());
            var e = document.createElement('div');
            e.className = 'container';
            e.innerHTML = '<div class="container-number">' +
                '<span class="number countdown-day">3</span><br/>' +
                '<span class="letter">Days</span><br/>' +
                '</div>' +
                '<div class="container-number">' +
                '<span class="number countdown-hour">5</span><br/>' +
                '<span class="letter">Hours</span><br/>' +
                '</div>' +
                '<div class="container-number">' +
                '<span class="number countdown-minute">18</span><br/>' +
                '<span class="letter">Minutes</span><br/>' +
                '</div>' +
                '<div class="container-number">' +
                '<span class="number countdown-second">30</span><br/>' +
                '<span class="letter">Seconds</span><br/>' +
                '</div>';
            dFrag.append(e);
            // products.each(function(product) {
            //     $(this).empty();
            // });
            // countdowns.each(function(countdown) {
            //     $(this).empty();
            // });
            $(countdowns).empty().append(dFrag);
            alert('Stop right there criminal scum!');
        },
    });

});