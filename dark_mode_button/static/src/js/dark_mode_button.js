/** @odoo-module **/

import SystrayMenu from 'web.SystrayMenu';
import Widget from 'web.Widget';
import Session from 'web.session';
import { browser } from "@web/core/browser/browser";
import { getCookie, setCookie } from "web.utils.cookies";

var ThemeWidget = Widget.extend({
    template: 'dark_mode_button',
    events: {
        'click #dark_button': '_onClick',
    },

    is_admin: false,
    colorScheme: false,
    willStart: function () {
        this.is_admin = Session.is_admin;
        this.colorScheme = getCookie("color_scheme");
        return this._super.apply(this, arguments);
    },

    _onClick: function(env){
        var colorScheme = getCookie("color_scheme");
        const scheme = colorScheme === "dark" ? "light" : "dark";
        setCookie("color_scheme", scheme);
        this.colorScheme = scheme;
        browser.location.reload();
    },
});
SystrayMenu.Items.push(ThemeWidget);
export default ThemeWidget;
