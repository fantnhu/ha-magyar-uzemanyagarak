"""Support for Magyar Üzemanyagárak sensors."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

import aiohttp
import async_timeout

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN, API_ENDPOINT, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Magyar Üzemanyagárak sensor based on a config entry."""
    coordinator = UzemanyagDataUpdateCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    if coordinator.data is None:
        _LOGGER.error("No data received from API")
        return

    entities = []
    fuel_data = coordinator.data.get("data", [])
    
    if not isinstance(fuel_data, list):
        _LOGGER.error("Invalid data format received from API")
        return

    for fuel in fuel_data:
        if isinstance(fuel, dict) and "nameOfFuel" in fuel and "priceAvg" in fuel:
            _LOGGER.debug("Creating sensor for fuel: %s", fuel)
            entities.append(UzemanyagSensor(coordinator, fuel))
        else:
            _LOGGER.error("Invalid fuel data format: %s", fuel)

    if entities:
        async_add_entities(entities, True)
    else:
        _LOGGER.error("No valid entities created")

class UzemanyagDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Uzemanyag data."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=60),
        )

    async def _async_update_data(self) -> dict[str, Any] | None:
        """Fetch data from API."""
        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.get(API_ENDPOINT) as response:
                        if response.status != 200:
                            _LOGGER.error("API returned status %s", response.status)
                            return None
                        
                        data = await response.json()
                        _LOGGER.debug("Received data from API: %s", data)
                        
                        if isinstance(data, dict) and "errorCode" in data and data["errorCode"] == 200:
                            return data
                        else:
                            _LOGGER.error("Unexpected data format: %s", type(data))
                            return None

        except Exception as err:
            _LOGGER.error("Error fetching data: %s", err)
            return None

class UzemanyagSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Magyar Üzemanyagárak sensor."""

    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "Ft/l"
    _attr_should_poll = False
    _attr_entity_category = None
    _attr_icon = "mdi:fuel"

    def __init__(
        self,
        coordinator: UzemanyagDataUpdateCoordinator,
        fuel_data: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        
        self._fuel_data = fuel_data
        self._attr_unique_id = f"{DOMAIN}_{fuel_data['nameOfFuel'].lower().replace(' ', '_')}"
        self._attr_name = fuel_data["nameOfFuel"]
        self._attr_suggested_display_precision = 1
        
        # Szolgáltatásként való megjelenítéshez
        self._attr_device_info = {
            "identifiers": {(DOMAIN, "uzemanyagarak")},
            "name": "Magyar Üzemanyagárak",
            "manufacturer": "OMV",
            "model": "Üzemanyagárak API",
            "sw_version": "1.0.0",
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success
            and self.coordinator.data is not None
            and "data" in self.coordinator.data
        )

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        try:
            return float(self._fuel_data["priceAvg"])
        except (KeyError, ValueError, TypeError):
            _LOGGER.error("Error getting price for %s", self.name)
            return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        try:
            return {
                "Info": str(self._fuel_data.get("infoOflabel", "")),
                "Legolcsóbb ár": float(self._fuel_data.get("priceMin", 0)),
                "Legmagasabb ár": float(self._fuel_data.get("priceMax", 0)),
                "Átlagár": float(self._fuel_data.get("priceAvg", 0))
            }
        except (ValueError, TypeError) as err:
            _LOGGER.error("Error getting attributes for %s: %s", self.name, err)
            return {}