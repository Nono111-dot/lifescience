"""Accepted reference implementation used only for simulator regression tests."""
from opentrons import protocol_api

metadata = {"protocolName": "24-sample magnetic-bead cleanup", "apiLevel": "2.16"}


def run(protocol: protocol_api.ProtocolContext) -> None:
    reagents = protocol.load_labware("nest_12_reservoir_15ml", "1")
    tips1 = protocol.load_labware("opentrons_96_tiprack_300ul", "4")
    mag = protocol.load_module("magnetic module gen2", "5")
    plate = mag.load_labware("nest_96_wellplate_2ml_deep")
    waste = protocol.load_labware("nest_1_reservoir_195ml", "6")
    tips2 = protocol.load_labware("opentrons_96_tiprack_300ul", "7")
    p300 = protocol.load_instrument("p300_single_gen2", "right", tip_racks=[tips1, tips2])
    wells = [plate[f"{row}{column}"] for column in range(1, 7) for row in "ABCD"]

    for well in wells:
        p300.pick_up_tip(); p300.aspirate(80, reagents["A1"]); p300.dispense(80, well); p300.mix(5, 100, well); p300.drop_tip()
    protocol.delay(minutes=5)
    for well in wells:
        p300.pick_up_tip(); p300.mix(5, 180, reagents["A2"]); p300.aspirate(120, reagents["A2"]); p300.dispense(120, well); p300.mix(10, 180, well); p300.drop_tip()
    protocol.delay(minutes=5)
    mag.engage(height_from_base=6.5)
    protocol.delay(minutes=7)
    for well in wells:
        p300.pick_up_tip(); p300.aspirate(250, well); p300.dispense(250, waste["A1"]); p300.drop_tip()
        p300.pick_up_tip(); p300.aspirate(180, reagents["A3"]); p300.dispense(180, well); protocol.delay(seconds=30); p300.aspirate(180, well); p300.dispense(180, waste["A1"]); p300.drop_tip()
        p300.pick_up_tip(); p300.aspirate(180, reagents["A3"]); p300.dispense(180, well); protocol.delay(seconds=30); p300.aspirate(180, well); p300.dispense(180, waste["A1"]); p300.drop_tip()
    protocol.delay(minutes=2)
    mag.disengage()
    for well in wells:
        p300.pick_up_tip(); p300.aspirate(40, reagents["A4"]); p300.dispense(40, well); p300.mix(10, 30, well); p300.drop_tip()
