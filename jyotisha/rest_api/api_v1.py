import logging

import flask_restplus
from flask import Blueprint
from flask_restplus import Resource
from flask_restplus import reqparse

import jyotisha.panchangam.spatio_temporal.annual
import jyotisha.panchangam.spatio_temporal.daily
from jyotisha.names import get_swisseph_body_id
from jyotisha.panchangam.spatio_temporal import City, Timezone
from jyotisha.panchangam.temporal import festival

logging.basicConfig(
  level=logging.DEBUG,
  format="%(levelname)s: %(asctime)s {%(filename)s:%(lineno)d}: %(message)s "
)

URL_PREFIX = '/v1'
api_blueprint = Blueprint(
  'panchanga', __name__,
  template_folder='templates'
)

api = flask_restplus.Api(app=api_blueprint, version='1.0', title='jyotisha panchanga API',
                         description='For detailed intro and to report issues: see <a href="https://github.com/sanskrit-coders/jyotisha">here</a>. '
                                     'A list of REST and non-REST API routes avalilable on this server: <a href="../sitemap">sitemap</a>.',
                         default_label=api_blueprint.name,
                         prefix=URL_PREFIX, doc='/docs')


# noinspection PyUnresolvedReferences
@api.route('/calendars/coordinates/<string:latitude>/<string:longitude>/years/<string:year>')
# TODO: How to set default values for latitude and logitude here??
# Questions at: https://github.com/noirbizarre/flask-restplus/issues/381 and stackoverflow linked therein.
class DailyCalendarHandler(Resource):
  get_parser = reqparse.RequestParser()
  get_parser.add_argument('timezone', type=str, default='Asia/Calcutta', help='Example: Asia/Calcutta', location='args', required=True)
  get_parser.add_argument('encoding', type=str, default='devanagari', help='Example: iast, devanagari, kannada, tamil', location='args',
                          required=True)

  @api.expect(get_parser)
  def get(self, latitude, longitude, year):
    args = self.get_parser.parse_args()
    city = City("", latitude, longitude, args['timezone'])
    panchangam = jyotisha.panchangam.spatio_temporal.annual.get_panchangam(city=city, year=int(year), script=args['encoding'])

    return panchangam.to_json_map()


# noinspection PyUnresolvedReferences
@api.route('/kaalas/coordinates/<string:latitude>/<string:longitude>/years/<string:year>/months/<int:month>/days/<int:day>/')
class KaalaHandler(Resource):
  get_parser = reqparse.RequestParser()
  get_parser.add_argument('timezone', type=str, default='Asia/Calcutta', help='Example: Asia/Calcutta', location='args', required=True)
  get_parser.add_argument('encoding', type=str, default='devanagari', help='Example: iast, devanagari, kannada, tamil', location='args',
                          required=True)
  get_parser.add_argument('format', type=str, default='hh:mm:ss*', help='Example: hh:mm:ss*, hh:mm', location='args', required=True)
  @api.expect(get_parser)
  def get(self, latitude, longitude, year, month, day):
    args = self.get_parser.parse_args()
    city = City("", latitude, longitude, args['timezone'])
    panchangam = jyotisha.panchangam.spatio_temporal.daily.DailyPanchanga(city=city, year=int(year), month=int(month), day=int(day))
    return panchangam.get_kaalas_local_time(format=args['format'])


# noinspection PyUnresolvedReferences
@api.route('/events/<string:id>')
class EventFinder(Resource):
  def get(self, id):
    festival.fill_festival_id_to_json()
    festival_data = festival.festival_id_to_json.get(id)
    return festival_data


# noinspection PyUnresolvedReferences
@api.route('/timezones/<string:timezone>/times/years/<int:year>/months/<int:month>/days/<int:day>/hours/<int:hour>/minutes/<int:minute>/seconds/<int:second>/bodies/<string:body>/nakshatra')
class NakshatraFinder(Resource):
  def get(self, body, timezone, year, month, day, hour, minute, second):
    from jyotisha import zodiac
    julday = Timezone(timezone).local_time_to_julian_day(year, month, day, hour, minute, second)
    lahiri_nakshatra_division = zodiac.NakshatraDivision(julday=julday)
    body_id = get_swisseph_body_id(body_name=body)
    if body == "moon":
      from jyotisha.panchangam import temporal
      logging.debug(temporal.get_nakshatram(julday))
    nakshatra = lahiri_nakshatra_division.get_nakshatra(body_id=body_id)
    logging.info(nakshatra)
    return str(nakshatra)
    # return "haha"


# noinspection PyUnresolvedReferences
@api.route('/timezones/<string:timezone>/times/years/<int:year>/months/<int:month>/days/<int:day>/hours/<int:hour>/minutes/<int:minute>/seconds/<int:second>/raashi')
class RaashiFinder(Resource):
  def get(self, timezone, year, month, day, hour, minute, second):
    julday = Timezone(timezone).local_time_to_julian_day(year, month, day, hour, minute, second)
    from jyotisha.panchangam import temporal
    raashi = temporal.get_solar_rashi(jd=julday)
    logging.info(raashi)
    return str(raashi)
    # return "haha"


# noinspection PyUnresolvedReferences
@api.route('/timezones/<string:timezone>/times/years/<int:year>/months/<int:month>/days/<int:day>/hours/<int:hour>/minutes/<int:minute>/seconds/<int:second>/bodies/<string:body>/raashi_transition_100_days')
class RaashiTransitionFinder(Resource):
  def get(self, timezone, year, month, day, hour, minute, second, body):
    from jyotisha import zodiac
    julday = Timezone(timezone).local_time_to_julian_day(year, month, day, hour, minute, second)
    from jyotisha.panchangam import temporal
    transits = temporal.get_planet_next_transit(jd_start=julday, jd_end = julday + 100, planet=body)
    # logging.debug(transits)
    transits_local = [(Timezone(timezone).julian_day_to_local_time(transit[0]), transit[1], transit[2]) for transit in transits]
    return str(transits_local)
