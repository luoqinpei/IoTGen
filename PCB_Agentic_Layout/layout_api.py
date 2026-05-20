'''
Layout API for PCB Design
The following functions are provided by KiCAD's pcbnew module.
Reference: http://docs.kicad.org/doxygen-python-8.0/namespacepcbnew.html
Board Level Functions:
1. LoadBoard(filename) - Load a PCB file and return a BOARD object.
2. BOARD.GetTracks() - Return a list of all tracks and vias on the board.
3. BOARD.GetDrawings() - Return a list of all drawings and texts on the board
4. BOARD.GetFootprints() - Return a list of all footprints on the board.
5. BOARD.GetNetCount() - Return the number of nets on the board.
6. BOARD.GetTrackWidthList() - Return a list of all track widths used on the
Footprint Level Functions:
1. FOOTPRINT.GetReference() - Return the reference designator of the footprint.
2. FOOTPRINT.GetPosition() - Return the position of the footprint Vector2I
3. FOOTPRINT.SetPosition(Vector2I) - Set the position of the footprint.
4. FOOTPRINT.GetOrientationDegrees() - Return the orientation of the footprint in degrees.
5. FOOTPRINT.SetOrientationDegrees(degrees) - Set the orientation of the footprint in degrees
'''

'''
The default layout in KiCAD has the following specifications:
The range of layout inside the two columns
X: 12 - 285 mm from left to right
Y: 12 - 198 mm from top to bottom (Need to reverse the Y axis in KiCAD)
'''

#!/usr/bin/env python
import os, sys
from pcbnew import *
import subprocess
from pathlib import Path
import shlex
import importlib.util
import pcbnew

import platform

system = platform.system()

if __name__ == "__main__":
    project_path = os.environ["PROJECT_PATH"]
    sys.path.append(project_path)

from config import freerouting_jar_path, freerouting_plugin_path, JAVA_EXE

REVERSE_Y_FLAG = 1

Y_MAX = 210
default_pcb_path = ""

def set_pcb_path(pcb_path):
    global default_pcb_path
    default_pcb_path = pcb_path
    return True

def re_Y(y):
    return Y_MAX - y

def safe_iter(maybe_iter):
    """
    Safely convert a possibly non-iterable SwigPyObject to a list.
    """
    # 1) Normal case: try to convert to list directly
    try:
        return list(maybe_iter)
    except TypeError:
        pass

    items = []
    # 2) Fallback: try .Next() style
    nxt = getattr(maybe_iter, "Next", None)
    if callable(nxt):
        cur = maybe_iter
        while cur is not None:
            items.append(cur)
            cur = nxt()
        return items

    # 3) Fallback: try __getitem__ style
    return items

class layout_api:
    def __init__(self, filename = None):

        self.filename = filename
        if filename is None:
            self.filename = default_pcb_path
        self.pcb = LoadBoard(self.filename)

        # Bounding box
        self.xmin = self.ymin =  10**18
        self.xmax = self.ymax = -10**18

        # # Assign the default minimum trace width and 
        # net_classes = self.pcb.GetNetClasses()
        # if len(list(net_classes.keys())) == 0:
        #     default_nc = pcbnew.NETCLASS("Default")
        #     if hasattr(net_classes, "Add"):
        #         net_classes.Add(default_nc)
        #     elif hasattr(net_classes, "AddNetClass"):
        #         net_classes.AddNetClass(default_nc)
        #     else:
        #         net_classes[os.name] = default_nc
        # else:
        #     default_nc = net_classes["Default"]
        # default_nc.SetTrackWidth(pcbnew.FromMM(0.1))  # 0.1 mm
        # default_nc.SetClearance(pcbnew.FromMM(0.1))  # 0.1 mm

    
    def place_fp(self, ref, pos, orient):
        """
        Place a footprint at a given position with a given orientation.
        ref: reference designator of the footprint (e.g., "U1")
        pos: (x, y) position in mm
        orient: orientation in degrees
        """
        fp = self.pcb.FindFootprintByReference(ref)
        if fp is None:
            print(f"Footprint {ref} not found")
            return False
        
        if REVERSE_Y_FLAG:
            pos_1 = re_Y(pos[1])

        pos_0 = FromMM(pos[0])
        pos_1 = FromMM(pos[1])

        fp.SetPosition(VECTOR2I(pos_0, pos_1))
        fp.SetOrientationDegrees(orient)
        return True

    def get_all_refs(self):
        """
        Get a list of all footprint references on the PCB.
        """
        refs = []
        for fp in self.pcb.GetFootprints():
            refs.append(fp.GetReference())
            print(fp)
        return refs

    def get_all_lib_info(self):
        """
        Get a dictionary of all footprint library information on the PCB.
        """
        lib_info = dict()
        for fp in self.pcb.GetFootprints():
            lib_info[fp.GetReference()] = (str(fp.GetFPID().GetLibNickname()), str(fp.GetFPID().GetLibItemName()))
        return lib_info
    
    def get_all_values(self):
        """
        Get a dictionary of all footprint values on the PCB.
        """
        value_list = dict()
        for fp in self.pcb.GetFootprints():
            value_list[fp.GetReference()] = fp.GetValue()
        return value_list

    def get_all_pos(self):
        """
        Get a dictionary of all footprint positions on the PCB.
        """
        pos_list = dict()
        for fp in self.pcb.GetFootprints():
            pos = fp.GetPosition()
            pos_list[fp.GetReference()] = (ToMM(pos.x), ToMM(pos.y))
        return pos_list
    
    def auto_routing(
        self,
        jar_path: str = None,
        keep_intermediate: bool = False,
    ):
        """
        Perform auto-routing on the PCB.
        jar_path: Path to the FreeRouting .jar file.
        prl_path: Path of the .prl file.
        java_bin: Path to the Java binary.
        max_passes: Maximum number of routing passes.
        keep_intermediate: Whether to keep intermediate files.
        """
        # Clear existing tracks and edge cuts
        # self.clear_wiring()
        board_path = Path(self.filename).resolve()
        work_dir = board_path.parent

        # Get the bouding box and draw edge cuts
        self.get_bounding_box()
        self.draw_rect_edges(self.xmin, self.ymin, self.xmax - self.xmin, self.ymax - self.ymin)

        # Parse paths
        if jar_path is None:
            jar_path = os.environ.get("FROUTING_JAR") or freerouting_jar_path
        jar_path = Path(jar_path).resolve()
        if not jar_path.exists():
            raise FileNotFoundError(f"FreeRouting .jar not found: {jar_path}")

        stem = board_path.stem
        ### Manually setup input/output paths ###
        dsn = work_dir / f"{stem}.dsn"
        ses = work_dir / f"{stem}.ses"

        ### Directly use pcbnew export DSN ###
        export_fn = getattr(pcbnew, "ExportSpecctraDSN", None)
        if export_fn is None:
            raise RuntimeError("pcbnew.ExportSpecctraDSN not found")
        
        try:
            ok = export_fn(self.pcb, str(dsn))
        except Exception as e:
            raise RuntimeError(f"Failed to export DSN: {e}")

        # (3) Get the command to run FreeRouting
        if system == "Windows":
            cmd = [
                JAVA_EXE, "-jar", str(jar_path),
                "-Djava.awt.headless=true",
                "-de", str(dsn),
                "-do", str(ses),
                "--gui.enabled=false",
                "-mp", "16",             # auto-routing max passes
                "-oit", "0.2",             # optimize initial tracks off
                "-us", "hybrid",         # greedy + global strategy
                "-hr", "2:1",            # hybrid ratio: 2 global, 1 greedy
            ]
        else:
            cmd = [
                    "java", "-jar", str(jar_path),
                    "-de", str(dsn),
                    "-do", str(ses),
                    "--gui.enabled=false",
                    "-mp", "16",             # auto-routing max passes
                    "-oit", "0",             # optimize initial tracks off
                    "-us", "hybrid",         # greedy + global strategy
                    "-hr", "2:1",            # hybrid ratio: 2 global, 1 greedy
                ]

        print(cmd)
        res = subprocess.run(cmd, cwd=str(dsn.parent), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=180)
        print(res.stdout)

        if res.returncode != 0:
            raise RuntimeError(f"FreeRouting failed with code {res.returncode}")
        
        if not ses.exists():
            raise FileNotFoundError(f"FreeRouting output .ses file not found: {ses}")
    
        # (4) Import the routed session back into the PCB
        ok = ImportSpecctraSES(self.pcb, str(ses))
        if not ok:
            raise RuntimeError("Failed to import FreeRouting session into PCB")
        self.save()

        # (5) Clean up intermediate files (optional)
        if not keep_intermediate:
            for p in [dsn, ses]:
                try:
                    if p and Path(p).exists():
                        Path(p).unlink()
                except Exception:
                    pass
            
    def clear_wiring(self):
        """
        Remove all tracks and/or vias from the board.
        Works safely across KiCad 7–9 and different SWIG bindings.
        """
        tracks = []

        # --- Try normal Python iteration first ---
        try:
            tracks = list(self.pcb.GetTracks())
        except TypeError:
            # Fallback: macOS SWIG may return non-iterable SwigPyObject
            try:
                iterator = self.pcb.GetTracks()
                # Try manual iteration if available
                next_func = getattr(iterator, "Next", None)
                if next_func is not None:
                    track = iterator
                    while track is not None:
                        tracks.append(track)
                        track = next_func()
            except Exception as e:
                print("Warning: cannot iterate tracks:", e)
                return

        # --- Remove all tracks and vias safely ---
        for t in tracks:
            try:
                self.pcb.RemoveNative(t)
            except Exception as e:
                print(f"Warning: failed to remove track/via {t}: {e}")

    def update_bbox(self, x, y):
        self.xmin = min(self.xmin, x)
        self.ymin = min(self.ymin, y)
        self.xmax = max(self.xmax, x)
        self.ymax = max(self.ymax, y)

    def add_edge_segment(self, p1_mm, p2_mm, width_mm=0.05):
        """Add one straight edge segment on Edge.Cuts from p1 to p2 (mm)."""
        seg = pcbnew.PCB_SHAPE(self.pcb)
        seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        p1_pos_1, p1_pos_2 = FromMM(p1_mm[0]), FromMM(p1_mm[1])
        p2_pos_1, p2_pos_2 = FromMM(p2_mm[0]), FromMM(p2_mm[1])
        seg.SetStart(VECTOR2I(p1_pos_1, p1_pos_2))
        seg.SetEnd(VECTOR2I(p2_pos_1, p2_pos_2))
        seg.SetLayer(pcbnew.Edge_Cuts)
        seg.SetWidth(pcbnew.FromMM(width_mm))
        self.pcb.Add(seg)
        return seg

    def clear_edge_cuts(self):
        drawings = []
        try:
            drawings = list(self.pcb.Drawings())
        except TypeError:
            # fallback for macOS KiCad SWIG binding
            try:
                d_iter = self.pcb.Drawings()
                while d_iter is not None:
                    drawings.append(d_iter)
                    d_iter = d_iter.Next()
            except Exception as e:
                print("Warning: cannot iterate drawings:", e)
                return

        for drawing in drawings:
            if isinstance(drawing, pcbnew.PCB_SHAPE):
                if drawing.GetLayerName() == "Edge.Cuts":
                    self.pcb.Remove(drawing)

    def draw_rect_edges(self, x_mm, y_mm, w_mm, h_mm, line_w_mm=0.05, clear_old=True, refresh=True):
        """
        Draw a rectangle outline on Edge.Cuts.
        (x_mm, y_mm) is top-left corner in board coordinates, width/height in mm.
        """
        if clear_old:
            self.clear_edge_cuts()

        pts = [
            (x_mm,          re_Y(y_mm)),
            (x_mm + w_mm,   re_Y(y_mm)),
            (x_mm + w_mm,   re_Y(y_mm + h_mm)),
            (x_mm,          re_Y(y_mm + h_mm)),
        ]
        for i in range(4):
            self.add_edge_segment(pts[i], pts[(i+1) % 4], width_mm=line_w_mm)

        if refresh and hasattr(pcbnew, "Refresh"):
            pcbnew.Refresh()

    def safe_iter_tracks(self):
        """Yield all items from board.GetTracks(); if KiCad bug triggers, yield nothing."""
        try:
            for it in self.pcb.GetTracks():
                yield it
        except TypeError:
            return

    def get_bounding_box(self):

        # --- Footprints (based on footprint position only) ---
        for fp in self.pcb.GetFootprints():
            for pad in fp.Pads():
                bbox = pad.GetBoundingBox()
                self.xmin = min(self.xmin, bbox.GetX())
                self.ymin = min(self.ymin, bbox.GetY())
                self.xmax = max(self.xmax, bbox.GetRight())
                self.ymax = max(self.ymax, bbox.GetBottom())

        # --- Tracks & Vias ---
        # Check if has tracks
        for item in self.safe_iter_tracks():
            if hasattr(item, "IsVia") and item.IsVia():
                pos = item.GetPosition()
                self.update_bbox(pos.x, pos.y)
            else:
                self.update_bbox(item.GetStart().x, item.GetStart().y)
                self.update_bbox(item.GetEnd().x, item.GetEnd().y)
        
        # Change to mm
        margin = 5.0  # mm
        self.xmin = ToMM(self.xmin) - margin
        ymin = ToMM(self.ymin) - margin
        self.xmax = ToMM(self.xmax) + margin
        ymax = ToMM(self.ymax) + margin
        self.ymax = re_Y(ymin)
        self.ymin = re_Y(ymax)


    def save(self, n_filename = None):
        if n_filename is None:
            self.pcb.Save(self.filename)
        else:
            self.pcb.Save(n_filename)
        return True


if __name__ == "__main__":

    # Path to your .kicad_pcb and .kicad_sch files
    pcb_filename = ""

    layout = layout_api(pcb_filename)
    # layout.place_fp("U1", (100, 100), 0)
    # layout.place_fp("C1", (110, 105), 90)
    # layout.place_fp("C2", (110, 95), 90)
    layout.auto_routing()
    # layout.save()
    # lib_info = layout.get_all_lib_info()
    # layout.save()
    # print(layout.get_all_pos())
    # print(layout.get_all_values())