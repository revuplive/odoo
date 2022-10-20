odoo.define('loonwholesale.widget', function (require) {
    'use strict';

    var core = require('web.core');
    var FieldBinaryFile = core.form_widget_registry.get('binary');
    var FieldBinaryImage = core.form_widget_registry.get('image');

    FieldBinaryFile.include({
        init: function (field_manager, node) {
            this._super(field_manager, node);
            this.max_upload_size = 50 * 1024 * 1024 * 1024; // 50Mo
        }
    });

    FieldBinaryImage.include({
        init: function (field_manager, node) {
            this._super(field_manager, node);
            this.max_upload_size = 50 * 1024 * 1024; // 50Mo
        }
    });
});

