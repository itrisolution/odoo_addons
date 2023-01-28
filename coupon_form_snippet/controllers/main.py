# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request
import json
from odoo import SUPERUSER_ID
from collections import OrderedDict


class CouponForm(http.Controller):
    @http.route('/get_coupon_programs', auth="public", type='json')
    def get_coupon_programs(self):
        records = request.env['coupon.program'].sudo().search([('active', '=', True)])
        values = {
            "coupon_programs": records,
        }
        response = http.Response(
            template='coupon_form_snippet.s_carousel_template', qcontext=values)
        return response.render()

    @http.route('/set_coupon_programs', type='http', auth="public", methods=['POST'], website=True)
    def set_coupon_programs(self, **post):
        name = post.get('name')
        email = post.get('email')
        coupon_program = post.get('coupon_program')
        mobile = post.get('phone')
        country = post.get('country')
        if name and email and coupon_program and mobile:
            ResPartner = request.env["res.partner"]
            ResUser = request.env["res.users"]
            CouponProgram = request.env["coupon.program"]
            CouponCoupon = request.env["coupon.coupon"]
            MailingCountact = request.env["mailing.contact"]
            ResCountry = request.env["res.country"]
            user_id = ResUser.sudo().search(['|', ('login', '=', email), ('mobile', '=', mobile)])
            if not user_id:
                sudo_users = ResUser.with_context(create_user=True).sudo()
                partner_id = ResPartner.with_user(SUPERUSER_ID).create({
                    'name': name,
                    'email': email,
                    'mobile': mobile,
                    'company_id': request.env.company.id,
                })
                values = OrderedDict()
                values['login'] = email
                values['partner_id'] = partner_id.id
                sudo_users.signup(values)
                user_id = ResUser.sudo().search([('login', '=', email)])

                coupon_program_id = CouponProgram.sudo().browse(int(coupon_program))
                if coupon_program_id and coupon_program_id.active:
                    coupon_id = CouponCoupon.sudo().create({
                        'partner_id': partner_id.id,
                        'program_id': coupon_program_id.id,
                    })

                    country_id = ResCountry.sudo().search([('code', '=', country.upper())])
                    MailingCountact.sudo().create({
                        'name': name,
                        'email': email,
                        'mobile': mobile,
                        'country_id': country_id.id if country_id else False,
                    })

                    mail_template = request.env.ref(
                        "coupon_form_snippet.mail_template_coupon_registration",
                        raise_if_not_found=False,
                    )
                    if partner_id and mail_template:
                        mail_template.sudo().send_mail(user_id.id, force_send=True)
                    # Send SMS
                    if coupon_id and partner_id:
                        body = _(
                            "Dear %s we are happy to confirm your registration for the %s promotional coupon. Your coupon is: %s") % (
                               partner_id.name, coupon_id.program_id.name, coupon_id.code)
                        composer = request.env['sms.sms'].sudo().create({
                            'body': body,
                            'number': partner_id.mobile,
                            'partner_id': partner_id.id,
                        })
                        composer.sudo().send()
                else:
                    return json.dumps({'error': _('Program coupon is invalid.')})
            else:
                return json.dumps(
                    {'error': _('Another user is already registered using this email address/Mobile Number.')})
        else:
            return json.dumps({'error': _('All fields are required !')})
        return json.dumps({'success': True})
