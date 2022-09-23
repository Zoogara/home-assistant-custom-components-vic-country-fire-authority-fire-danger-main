"""VIC Country Fire Authority - Fire Danger - Binary Sensor."""
from __future__ import annotations

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import BINARY_SENSOR_TYPES, CONF_DATA_FEED, DEFAULT_DATA_FEED, DOMAIN
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
            VicCfaFireDangerBinarySensor(
                coordinator, sensor_type, config_entry_unique_id
            )
            for sensor_type in BINARY_SENSOR_TYPES[data_feed]
        ],
    )
    _LOGGER.debug("Binary sensor setup done")


class VicCfaFireDangerBinarySensor(
    VicCfaFireDangerEntity, BinarySensorEntity
):
    """Implementation of the binary sensor."""

    _attr_device_class = BinarySensorDeviceClass.SAFETY

    def _update_state(self, new_state: StateType) -> None:
        """Update the state from the provided value."""
        self._attr_is_on = new_state
