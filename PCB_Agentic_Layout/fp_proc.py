'''
This script processes a KiCAD footprint and extracts information about its pads,
body, and bounding boxes, then formats this information into a structured text
block. It uses regular expressions to parse the footprint description for body
dimensions and calculates bounding boxes for the pads and the combined
footprint. The output includes details about the footprint's reference, library,
layer, attributes, body size, pad details, bounding boxes, clearance, and text
positions.
'''

import re
from math import inf

def _parse_body_from_descr(descr: str):
    # looks for patterns like "8.0x6.2mm" or "8x6.2 mm"
    m = re.search(r'(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)(?:\s*mm)?', descr.lower())
    if not m:
        return None, None
    return float(m.group(1)), float(m.group(2))

def _pads_bbox(pads):
    xmin, ymin, xmax, ymax = inf, inf, -inf, -inf
    for p in pads:
        cx, cy = p['at'][0], p['at'][1]
        w, h = p['size'][0], p['size'][1]
        x0, x1 = cx - w/2.0, cx + w/2.0
        y0, y1 = cy - h/2.0, cy + h/2.0
        xmin, ymin = min(xmin, x0), min(ymin, y0)
        xmax, ymax = max(xmax, x1), max(ymax, y1)
    return xmin, ymin, xmax, ymax

def _union_bbox(b1, b2):
    if b2 is None:
        return b1
    (xmin1, ymin1, xmax1, ymax1) = b1
    (xmin2, ymin2, xmax2, ymax2) = b2
    return (min(xmin1, xmin2), min(ymin1, ymin2),
            max(xmax1, xmax2), max(ymax1, ymax2))

def _centered_body_bbox(w, h):
    if w is None or h is None:
        return None
    return (-w/2.0, -h/2.0, w/2.0, h/2.0)

def _bbox_wh(b):
    xmin, ymin, xmax, ymax = b
    return (xmax - xmin, ymax - ymin)

def _fmt_tuple(v):
    return f"({v[0]:.4g}, {v[1]:.4g})"

def _fmt_bbox(b):
    xmin, ymin, xmax, ymax = b
    w, h = _bbox_wh(b)
    return (
        f"  xmin: {xmin:.4g}, ymin: {ymin:.4g}, xmax: {xmax:.4g}, ymax: {ymax:.4g}\n"
        f"  width: {w:.4g}, height: {h:.4g}"
    )

def _render_llm_block(ref, lib_name, item_name, f):
    layer = f.get("layer", "F.Cu")
    attr = f.get("attr", [])
    pads = f.get("pads", [])
    descr = f.get("descr", "") or ""
    body_w, body_h = _parse_body_from_descr(descr)
    pads_bbox = _pads_bbox(pads) if pads else (0.0, 0.0, 0.0, 0.0)
    body_bbox = _centered_body_bbox(body_w, body_h)
    combined_bbox = _union_bbox(pads_bbox, body_bbox if body_bbox else None)
    keepout = 0.25  # mm default if no courtyard

    # texts
    refp = f.get("properties", {}).get("Reference", {})
    valp = f.get("properties", {}).get("Value", {})

    # pads pretty
    pads_lines = []
    for p in pads:
        drill = p.get("drill", None)
        layers = ",".join(p.get("layers", []))
        pads_lines.append(
            f'  - n: "{p["name"]}", center: {_fmt_tuple((p["at"][0], p["at"][1]))}, '
            f'size: {_fmt_tuple((p["size"][0], p["size"][1]))}, shape: {p.get("shape","unknown")}, '
            f'drill: {drill if drill is not None else "null"}, layers: [{layers}]'
        )
    pads_block = "\n".join(pads_lines)

    body_src = "descr" if (body_w and body_h) else "unknown"

    out = []
    out.append("FOOTPRINT")
    out.append(f"ref: {ref}")
    out.append(f"library: {lib_name}/{item_name}")
    out.append(f"side: {layer}")
    out.append(f"attr: {attr}")
    out.append("rotation_deg: 0.0")
    out.append("origin_mm: (0.0, 0.0)\n")
    out.append("body_mm:")
    out.append(f"  width: {body_w if body_w else 'null'}")
    out.append(f"  height: {body_h if body_h else 'null'}")
    out.append(f'  source: "{body_src}"\n')
    out.append("pads_mm:")
    out.append(pads_block if pads_block else "  - []")
    out.append("\nbbox_pads_mm:")
    out.append(_fmt_bbox(pads_bbox))
    out.append("\n\nbbox_combined_mm:")
    out.append(_fmt_bbox(combined_bbox))
    out.append("\n\nclearance_mm:")
    out.append(f"  placement_keepout: {keepout}\n")
    out.append("texts:")
    out.append(f"  reference_at_mm: {_fmt_tuple((refp.get('x',0.0), refp.get('y',0.0)))}")
    out.append(f"  value_at_mm:     {_fmt_tuple((valp.get('x',0.0), valp.get('y',0.0)))}\n")
    out.append("constraints:")
    out.append("  allowed_rotations_deg: [0,90,180,270]")
    out.append('  notes: "Avoid keepout intersection with other footprints/pads; move text if colliding."')
    out.append("END")
    return "\n".join(out)
