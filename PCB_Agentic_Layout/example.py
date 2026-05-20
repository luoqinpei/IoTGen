#!/usr/bin/env python
'''
Example script from KiCAD official documentation to demonstrate how to use the
pcbnew Python API to read and print information about a KiCAD PCB file,
including tracks, vias, text, shapes, footprints, zones, and netclasses. This
script can be used as a starting point for more complex PCB manipulation tasks
using the pcbnew API.
'''

import sys
from pcbnew import *

filename = ""
pcb = LoadBoard(filename)

print("Listing Tracks and Vias:")
for item in pcb.GetTracks():
    if type(item) is PCB_VIA:
        pos = item.GetPosition()
        drill = item.GetDrillValue()
        width = item.GetWidth()
        print(f" * Via:   {ToMM(pos)} - {ToMM(drill)}/{ToMM(width)}")
    elif type(item) is PCB_TRACK:
        start = item.GetStart()
        end = item.GetEnd()
        width = item.GetWidth()
        print(f" * Track: {ToMM(start)} to {ToMM(end)}, width {ToMM(width)}")
    else:
        print(f"Unknown type    {type(item)}")

print()
print("Listing Text and Shapes:")
for item in pcb.GetDrawings():
    if type(item) is PCB_TEXT:
        print(f"* Text:    '{item.GetText()}' at {ToMM(item.GetPosition())}")
    elif type(item) is PCB_SHAPE:
        print(f"* Drawing: {item.GetShapeStr()}")
    else:
        print(f"Unknown type    {type(item)}")

print()
print("Listing Footprints")
for fp in pcb.GetFootprints():
    print(f"* Footprint: {fp.GetReference()} at {ToMM(fp.GetPosition())}")
    print(f"* Footprint: {fp.GetValue()}")

print()
print(f"Ratsnest count: {pcb.GetNetCount()}")
print(f"Track width count: {len(pcb.GetTrackWidthList())}")
print(f"Via size count: {len(pcb.GetViasDimensionsList())}")

print()
print(f"Listing Zones: {pcb.GetAreaCount()}")
for idx in range(0, pcb.GetAreaCount()):
    zone = pcb.GetArea(idx)
    print(f"zone: {idx} priority: {zone.GetAssignedPriority()} netname: {zone.GetNetname()}")

print()
print(f"Netclasses: {len(pcb.GetAllNetClasses())}")
