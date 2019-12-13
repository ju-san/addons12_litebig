import json
import urllib

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


def geo_find(addr):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?sensor=false&address='
    url += urllib.quote(addr.encode('utf8'))

    try:
        result = json.load(urllib.urlopen(url))
    except Exception as e:
        raise UserError(_('Cannot contact geolocation servers. Please make sure that your Internet connection is up and running (%s).') % e)

    if result['status'] != 'OK':
        return None

    try:
        geo = result['results'][0]['geometry']['location']
        return float(geo['lat']), float(geo['lng'])
    except (KeyError, ValueError):
        return None


def geo_query_address(street=None, zip=None, city=None, state=None, country=None):
    if country and ',' in country and (country.endswith(' of') or country.endswith(' of the')):
        # put country qualifier in front, otherwise GMap gives wrong results,
        # e.g. 'Congo, Democratic Republic of the' => 'Democratic Republic of the Congo'
        country = '{1} {0}'.format(*country.split(',', 1))
    return tools.ustr(', '.join(filter(None, [street,
                                              ("%s %s" % (zip or '', city or '')).strip(),
                                              state,
                                              country])))
    
class PartnerGeoLocalize(models.TransientModel):
    _name = "partner.geo.localize"
    _description = "Partner Geo Localize"

    @api.multi
    def action_geo_localize(self):
        context = dict(self._context or {})
        partner_obj = self.env['res.partner']
        for partner in partner_obj.with_context(lang='en_US').browse(context.get('active_ids')):
            result = geo_find(geo_query_address(street=partner.street,
                                                zip=partner.zip,
                                                city=partner.city,
                                                state=partner.state_id.name,
                                                country=partner.country_id.name))
            if result is None:
                result = geo_find(geo_query_address(
                    city=partner.city,
                    state=partner.state_id.name,
                    country=partner.country_id.name
                ))

            if result:
                partner.write({
                    'partner_latitude': result[0],
                    'partner_longitude': result[1],
                    'date_localization': fields.Date.context_today(partner)
                })
        return {'type': 'ir.actions.act_window_close'}
