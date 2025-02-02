import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c, sensor
from esphome.const import CONF_ID, CONF_TEMPERATURE, CONF_HUMIDITY, UNIT_CELSIUS, \
    UNIT_PERCENT, ICON_THERMOMETER, ICON_WATER_PERCENT

CODEOWNERS = ['@sjtrny']
DEPENDENCIES = ['i2c']

sht4x_ns = cg.esphome_ns.namespace('sht4x')

SHT4XComponent = sht4x_ns.class_('SHT4XComponent', cg.PollingComponent, i2c.I2CDevice)

CONF_PRECISION = 'precision'
SHT4XPRECISION = sht4x_ns.enum("SHT4XPRECISION")
PRECISION_OPTIONS = {
  "High": SHT4XPRECISION.SHT4X_PRECISION_HIGH,
  "Med": SHT4XPRECISION.SHT4X_PRECISION_MED,
  "Low": SHT4XPRECISION.SHT4X_PRECISION_LOW
}

CONF_HEATER_POWER = 'heater_power'
SHT4XHEATERPOWER = sht4x_ns.enum("SHT4XHEATERPOWER")
HEATER_POWER_OPTIONS = {
  "High": SHT4XHEATERPOWER.SHT4X_HEATERPOWER_HIGH,
  "Med": SHT4XHEATERPOWER.SHT4X_HEATERPOWER_MED,
  "Low": SHT4XHEATERPOWER.SHT4X_HEATERPOWER_LOW
}

CONF_HEATER_TIME = 'heater_time'
SHT4XHEATERTIME = sht4x_ns.enum("SHT4XHEATERTIME")
HEATER_TIME_OPTIONS = {
  "Long": SHT4XHEATERTIME.SHT4X_HEATERTIME_LONG,
  "Short": SHT4XHEATERTIME.SHT4X_HEATERTIME_SHORT,
}

CONF_HEATER_MAX_DUTY = 'heater_max_duty'

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(SHT4XComponent),

    cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(UNIT_CELSIUS, ICON_THERMOMETER, 1),
    cv.Optional(CONF_HUMIDITY): sensor.sensor_schema(UNIT_PERCENT, ICON_WATER_PERCENT, 1),

    cv.Optional(CONF_PRECISION, default="High"): cv.enum(PRECISION_OPTIONS),
    cv.Optional(CONF_HEATER_POWER, default="High"): cv.enum(HEATER_POWER_OPTIONS),
    cv.Optional(CONF_HEATER_TIME, default="Long"): cv.enum(HEATER_TIME_OPTIONS),
    cv.Optional(CONF_HEATER_MAX_DUTY, default=0.0): cv.float_range(min=0.0, max=0.05),
}).extend(cv.polling_component_schema('60s')).extend(i2c.i2c_device_schema(0x44))

TYPES = {
    CONF_TEMPERATURE: 'set_temp_sensor',
    CONF_HUMIDITY: 'set_humidity_sensor',
}


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield i2c.register_i2c_device(var, config)

    cg.add(var.set_precision_value(config[CONF_PRECISION]))
    cg.add(var.set_heater_power_value(config[CONF_HEATER_POWER]))
    cg.add(var.set_heater_time_value(config[CONF_HEATER_TIME]))
    cg.add(var.set_heater_duty_value(config[CONF_HEATER_MAX_DUTY]))

    for key, funcName in TYPES.items():

        if key in config:
            sens = yield sensor.new_sensor(config[key])
            cg.add(getattr(var, funcName)(sens))
