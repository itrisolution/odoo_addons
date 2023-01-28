odoo.define('coupon_form_snippet.carousel_dashboard', function(require) {
    'use strict';

    var Animation = require('website.content.snippets.animation');
    var ajax = require('web.ajax');
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var qweb = core.qweb;
    var _t = core._t;

    Animation.registry.get_dashbaord_carousel = Animation.Class.extend({
        selector: '.s_carousel_template',
        events: {
            'click #show_form_cp': '_onShowForm',
        },

        init: function() {
            this._super.apply(this, arguments);
            this._hideForm();
        },

        start: function() {
            var self = this;
            ajax.jsonRpc('/get_coupon_programs', 'call', {}).then(function(data) {
                if (data) {
                    self.$target.empty().append(data);
                }
            });
        },

        _resetForm : function() {
            document.querySelector("#error-msg").innerHTML = "";
            document.querySelector("#error-msg").classList.add("o_hidden");
            document.querySelector(".iti--allow-dropdown").classList.remove("error");
        },

        _showError: function(msg, is_phone) {
            document.querySelector("#error-msg").innerHTML = msg;
            document.querySelector("#error-msg").classList.remove("o_hidden");
            if(is_phone) {
                document.querySelector(".iti--allow-dropdown").classList.add("error");
            }
        },

        _showForm: function() {
            document.querySelector('#form_cp').style.display = 'block';
            document.querySelector('#show_form_cp').style.display = 'none';
        },

        _hideForm: function() {
            document.querySelector("#form_cp").style.display = 'none';
            document.querySelector("#show_form_cp").style.display = 'block';
            document.querySelector("#success_div").style.display = 'none';
        },

        _onShowForm: function() {
            var self = this;

            var countryData = window.intlTelInputGlobals.getCountryData(),
                input = document.querySelector("#phone");

            // init plugin
            var iti = window.intlTelInput(input, {
                hiddenInput: "full_phone",
                utilsScript: "https://intl-tel-input.com/node_modules/intl-tel-input/build/js/utils.js?1549804213570" // just for formatting/placeholders etc
            });

            // populate the country dropdown
            for (var i = 0; i < countryData.length; i++) {
                var country = countryData[i];
                document.createTextNode(country.name);
            }
            self._showForm();

            $('#coupon_form').submit(function(e) {
                self._resetForm();
                e.preventDefault();

                if (!iti.isValidNumber()) {
                    var errorMap = [_t("Invalid Mobile number"), _t("Invalid country code"), _t("Mobile number is too short"), _t("Mobile number is too long"), _t("Invalid Mobile number"), _t("Undefined Mobile number")];
                    var errorCode = iti.getValidationError();
                    if (errorCode == -99) {
                        errorCode = 5
                    }
                    self._showError(errorMap[errorCode], true);
                    return;
                }
                var form_data = $('#coupon_form').serialize() + "&country=" + iti.getSelectedCountryData()['iso2']
                $.ajax({
                    url: '/set_coupon_programs',
                    type: 'post',
                    data: form_data,
                    success: function(response) {
                        console.log(response);
                        const jsonResponse = response && JSON.parse(response);
                        if (jsonResponse.error) {
                            self._showError(jsonResponse.error, false);
                        } else if (jsonResponse.success) {
                            $('#coupon_form')[0].reset();
                            document.querySelector("#form_cp").style.display = 'none';
                            document.querySelector("#success_div").style.display = 'block';
                        }
                    },
                });
            });
        },
    });
});
