# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools


class ProductTemplateInherit(models.Model):
    """ Inherit Res Config Settings to add default image product field """
    _inherit = "product.template"

    @api.model_create_multi
    def create(self, vals_list):
        for val_list in vals_list:
            if not val_list['image_1920']:
                product_default_image = self.env['ir.config_parameter'].sudo().get_param(
                    'res.config.settings.product_default_image')
                if product_default_image:
                    val_list['image_1920'] = product_default_image

        return super(ProductTemplateInherit, self).create(vals_list)
