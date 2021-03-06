# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class SaleOrder(models.Model):
    _inherit = "sale.order"
    buy_way = fields.Char()
    payment_method_information = fields.Char(compute='_compute_payment_method_information')
    delivery_method_information = fields.Char(compute='_compute_delivery_method_information')

    def _compute_payment_method_information(self):
        self.payment_method_information = False
        if str(self.buy_way) == "nobill_ship":
            self.payment_method_information = _("Pay on delivery")
        elif str(self.buy_way) == "nobill_noship":
            self.payment_method_information = _("Pay at store")

    def _compute_delivery_method_information(self):
        self.delivery_method_information = False
        if str(self.buy_way) == "bill_noship" or str(self.buy_way) == "nobill_noship":
            self.delivery_method_information = _("Pickup at store")

    def get_shipping_billing(self):
        if not self.buy_way:
            return {
                'ship_enabled': '1',
                'bill_enabled': '1',
            }
        return {
            'ship_enabled': 'noship' not in self.buy_way and '1' or '0',
            'bill_enabled': 'nobill' not in self.buy_way and '1' or '0',
        }


class WebsiteConfigSettings(models.TransientModel):
    _inherit = 'website.config.settings'
    nobill_noship = fields.Boolean("Pickup and pay at store")
    bill_noship = fields.Boolean("Pickup at store but pay now")
    bill_ship = fields.Boolean("Pay now and get delivery")
    nobill_ship = fields.Boolean("Pay on delivery")
    default_option = fields.Selection([
        ('nobill_noship', 'Pickup and pay at store'),
        ('bill_noship', 'Pickup at store but pay now'),
        ('bill_ship', 'Pay now and get delivery'),
        ('nobill_ship', 'Pay on delivery'),
    ], string='Selected by default', default='nobill_noship')

    @api.model
    def set_nobill_noship(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self:
            config_parameters.set_param("website_sale_checkout_store.nobill_noship", record.nobill_noship or '')

    @api.model
    def set_bill_noship(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self:
            config_parameters.set_param("website_sale_checkout_store.bill_noship", record.bill_noship or '')

    @api.model
    def set_bill_ship(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self:
            config_parameters.set_param("website_sale_checkout_store.bill_ship", record.bill_ship or '')

    @api.model
    def set_nobill_ship(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self:
            config_parameters.set_param("website_sale_checkout_store.nobill_ship", record.nobill_ship or '')

    @api.model
    def set_default_option(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self:
            config_parameters.set_param("website_sale_checkout_store.default_option", record.default_option or '')

    @api.model
    def get_default_nobill_noship(self, fields):
        nobill_noship = self.env["ir.config_parameter"].get_param("website_sale_checkout_store.nobill_noship", default=False)
        return {'nobill_noship': nobill_noship}

    @api.model
    def get_default_bill_noship(self, fields):
        bill_noship = self.env["ir.config_parameter"].get_param("website_sale_checkout_store.bill_noship", default=False)
        return {'bill_noship': bill_noship}

    @api.model
    def get_default_bill_ship(self, fields):
        bill_ship = self.env["ir.config_parameter"].get_param("website_sale_checkout_store.bill_ship", default=False)
        return {'bill_ship': bill_ship}

    @api.model
    def get_default_nobill_ship(self, fields):
        nobill_ship = self.env["ir.config_parameter"].get_param("website_sale_checkout_store.nobill_ship", default=False)
        return {'nobill_ship': nobill_ship}

    @api.model
    def get_default_default_option(self, fields):
        default_option = self.env["ir.config_parameter"].get_param("website_sale_checkout_store.default_option", default='nobill_noship')
        return {'default_option': default_option}
