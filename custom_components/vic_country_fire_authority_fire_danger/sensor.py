"""VIC Country Fire Authority - Fire Danger - Sensor."""
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import CONF_DATA_FEED, DEFAULT_DATA_FEED, DOMAIN, SENSOR_TYPES
from .entity import VicCfaFireDangerEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the VIC Country Fire Authority Fire Danger Feed platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    config_entry_unique_id = config_entry.unique_id
    data_feed = config_entry.data.get(CONF_DATA_FEED, DEFAULT_DATA_FEED)

    async_add_entities(
        [
            VicCfaFireDangerSensor(
                coordinator, sensor_type, config_entry_unique_id
            )
            for sensor_type in SENSOR_TYPES[data_feed]
        ],
    )
    _LOGGER.debug("Sensor setup done")


class VicCfaFireDangerSensor(VicCfaFireDangerEntity, SensorEntity):
    """Implementation of the sensor."""

    _attr_icon = "mdi:speedometer-medium"

    def _update_state(self, new_state: StateType) -> None:
        """Update the state from the provided value."""
        self._attr_native_value = new_state
