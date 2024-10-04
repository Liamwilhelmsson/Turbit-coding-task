from datetime import datetime
from pydantic import AliasChoices, BaseModel, Field, field_validator


class TurbineData(BaseModel):
    turbine_id: int
    timestamp: datetime = Field(validation_alias=AliasChoices("Dat/Zeit"))
    wind_speed_ms: float = Field(validation_alias=AliasChoices("Wind"))
    rotor_speed_rpm: float = Field(validation_alias=AliasChoices("Rotor"))
    power_output_kw: float = Field(validation_alias=AliasChoices("Leistung"))
    azimuth_angle: float = Field(validation_alias=AliasChoices("Azimut"))
    production_1_kwh: int = Field(validation_alias=AliasChoices("Prod. 1"))
    production_2_kwh: int = Field(validation_alias=AliasChoices("Prod. 2"))
    operating_hours_1: int = Field(validation_alias=AliasChoices("BtrStd 1"))
    operating_hours_2: int = Field(validation_alias=AliasChoices("BtrStd 2"))
    generator_1_temp_c: float = Field(validation_alias=AliasChoices("Gen1-"))
    bearing_temp_c: float = Field(validation_alias=AliasChoices("Lager"))
    outside_temp_c: float = Field(validation_alias=AliasChoices("Außen"))
    gearbox_temp_c: float = Field(validation_alias=AliasChoices("GetrT"))
    status: int = Field(validation_alias=AliasChoices("Status"))
    voltage_1_V: float = Field(validation_alias=AliasChoices("Spann"))
    voltage_2_V: float = Field(validation_alias=AliasChoices("Spann.1"))
    voltage_3_V: float = Field(validation_alias=AliasChoices("Spann.2"))
    current_1_A: float = Field(validation_alias=AliasChoices("Strom-"))
    current_2_A: float = Field(validation_alias=AliasChoices("Strom-.1"))
    current_3_A: float = Field(validation_alias=AliasChoices("Strom-.2"))
    power_factor: float = Field(validation_alias=AliasChoices("CosPh"))
    energy_delivered_kwh: int = Field(validation_alias=AliasChoices("Abgabe"))
    energy_received_kwh: int = Field(validation_alias=AliasChoices("Bezug"))
    KH_number_1_imp: int = Field(validation_alias=AliasChoices("KH-Zähl1"))
    KH_number_2_imp: int = Field(validation_alias=AliasChoices("KH-Zähl2"))
    KH_digi_E: int = Field(validation_alias=AliasChoices("KH-DigiE"))
    KH_digi_I: int = Field(validation_alias=AliasChoices("KH-DigiI"))
    KH_ana_1: int = Field(validation_alias=AliasChoices("KH-Ana-1"))
    KH_ana_2: int = Field(validation_alias=AliasChoices("KH-Ana-2"))
    KH_ana_3: int = Field(validation_alias=AliasChoices("KH-Ana-3"))
    KH_ana_4: int = Field(validation_alias=AliasChoices("KH-Ana-4"))

    @field_validator("timestamp", mode="before")
    def parse_timestamp(cls, value):
        try:
            return datetime.strptime(value, "%d.%m.%Y, %H:%M")
        except ValueError:
            raise ValueError(
                f"Invalid date format of {value}, expected: 'DD.MM.YYYY, HH:MM'"
            )
