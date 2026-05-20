'''
LayoutAgent is responsible for performing PCB layout based on the schematic and user request. It uses the KiCAD Python API to place components and route the PCB. The agent can also analyze the layout and provide feedback for improvement. The main steps include:
1. Preparing the prompt context for the LLM, including loading example code and setting up the system message.
2. Reading related footprints from the PCB file and summarizing their geometry for LLM placement.
3. Generating the PCB layout code using the LLM based on the schematic image, netlist, and footprint summaries.
4. Executing the generated code using the KiCAD Python interpreter and capturing any errors.
5. Analyzing the layout and DRC feedback to provide insights on potential issues and improvements for the next iteration.
'''

import linecache
import os
import sys
import io
from contextlib import redirect_stdout
import traceback

project_path = os.environ["PROJECT_PATH"]
sys.path.append(project_path)

from layout_helper import *

from modules.sch_module_def import *

from modules.kicad_sch_interface import get_pin_location, load_schematic, save_schematic, save_code, save_description

from modules.utils.kicad_add_symbol import clear_bounding_box_dict

from modules.utils.kicad_scan_lib import *

from modules.utils.kicad_sch_export import get_sch_with_axes, get_pcb_with_axes, get_schematic_netlist, get_drc_report

from modules.utils.llm_interface import GetLLMInterface

from modules.utils.custom_logger import setup_logger

from modules.utils.misc import *

from pydantic import BaseModel

from config import pcbnew_path

import platform
system = platform.system()

from fp_proc import _render_llm_block
from modules.utils.kicad_scan_lib import *
import tempfile
import subprocess
import textwrap
import os, sys
import traceback as _tb

def prepare_prompt_context():
    """
    Prepare the prompt context for the LLM.
    This function is used to set up the system message and user request for the LLM.
    """
    
    # Load few-shot examples from the files
    example_code_files = [
        "PCB_Agentic_Layout/layout_examples/voltage_reg.py"
    ]

    example_codes = []
    for filename in example_code_files:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Example file {filename} does not exist.")
        with open(filename, "r") as f:
            example_code = f.read()
            example_codes.append(example_code)

    example_code_str = "\n\n".join(example_codes)


    system_msg = [
        {"role": "system",
        "content": f""" You are a KiCAD PCB layout expert. You are given user's request, reference schematic image and corresponding netlist. You need to generate Python code using Python API provided below to edit the PCB layout by placing all the symbols and call auto-routing function.
###
You have the following functions available to you and can create new functions based on them:
- layout_api(filename = None): Create a new layout_api object to edit the PCB layout, if filename is None, use the default PCB file.
- layout_api.place_fp(ref, pos, orient): Place the footprint with reference 'ref' at position 'pos' (x, y) with orientation 'orient' (in degrees).
- layout_api.auto_routing(): Call the auto-routing function to route the PCB.
- layout_api.save(): Save the PCB layout to the file. 
###

Coding Rules:
1. The code should be valid Python and should use the only the Python API above. The code should contain comments, starting with #, to explain what each part does.
2. You should write the code block by block, each block is a piece of code that doing the layout of specific function block. For example, for a ESP32 microcontroller module, you should first place the microcontroller block, then place a power block (including power symbols), a oscillator block (including crystal and related components), and a reset block (including reset button and related components), etc. Each block should be separated by a comment line with the block name.
3. NO OVERLAP BETWEEN SYMBOLS! You need to check the footprint of each symbol and make sure they do not overlap with each other when placing them.
4. If json output is asked, Repeat the code again -- copy exactly, in the json output. Do NOT say something like "[see Python listing above]"!
###
# Example code that uses these functions:
```
{example_code_str}
```
###
NOTE:
1. You should mind the spatial placement of the components. Make sure they are at reasonable positions and ample spacing so that they do not overlap with each other!
2. The size of the schematic is X: 12 - 285 mm from left to right Y: 12 - 210 mm from top to bottom. It uses a X-Y axes based coordinate system. The origin is [0,0] at bottom left corner of the sheet. X axis is horizontal, and Y axis is vertical.
3. You should check the symbol context to see the spatial information, including the size, orientation, pin locations. You can use the function `move_symbol` to move or rotate the symbol placement. The local coordinates for symbol body and pin locations are in mm. The center of the symbol is at (0, 0) and the pin locations are relative to the center of the symbol. X axis is horizontal, and Y axis is vertical. For symbol definition, the Y axis points upward, that means higher Y position means higher position, same direction as the schematic coordinate system.
4. The code should be valid Python code with correct indentation and syntax. For example, comment should start with #. 
5. The minimum resolution in KiCAD PCB Layout is 1 nm, so can use float numbers with up to 6 decimal places. For example, you can use pos = (45.123456, 78.654321) to place a symbol at (45.123456 mm, 78.654321 mm).
6. You should utilize the information in the symbol content to help with schematic editing. For example, you can not use references that does not appear in the symbol context. Based on the sizes mentioned in the context, you should avoid overlapping components.
        """}
    ]

    return system_msg

REQUIRED_SNIPPET = (
    "import os\n"
    "import sys\n\n"
    "project_path = os.environ[\"PROJECT_PATH\"]\n"
    "sys.path.append(project_path)\n"
)

def sanitize_code(code_str: str) -> str:
    """
    Ensure the code contains the required environment setup.
    If missing, prepend it.
    """

    # Normalize whitespace for detection
    normalized = code_str.replace(" ", "")

    needed = [
        "import os",
        "import sys",
        "project_path=os.environ[\"PROJECT_PATH\"]".replace(" ", ""),
        "sys.path.append(project_path)".replace(" ", ""),
    ]

    if all(needle in normalized for needle in needed):
        # Code already contains the required snippet
        return code_str

    # Otherwise, add the snippet at the top
    return REQUIRED_SNIPPET + "\n" + code_str


class LayoutAgent:
    """
    This class is used to edit the PCB layout based on user request.
    It takes user request and uses the KiCad Python interface to perform the editing tasks.
    """

    def __init__(self, model:str = "gpt-5.1", model_provider = "OpenRouter", design_path:str = None, module_name: str = "schematic"):
        """
        Initialize the LayoutAgent.
        Args:
            model (str): The LLM model to be used.
            design_path (str): The path to the design project.
            module_name (str): The name of the module to be designed.
        """

        # GPT-o4 is better at visual tasks, GPT-o3 is better at complex reasoning tasks
        self.llm = GetLLMInterface(model_name=model, model_provider= model_provider)

        self.logger = setup_logger()
        self.logger.info("LayoutAgent initialized.")

        self.schematic_path = os.path.join(design_path, f"{module_name}.kicad_sch")
        self.pcb_path = os.path.join(design_path, f"{module_name}.kicad_pcb")
        self.netlist_path = os.path.join(design_path, f"{module_name}.net")

        self.msg_list = list(prepare_prompt_context())  # copy base system context
        self.maximum_score = -100
        self.best_code = None
        self.scores = []

    
    def execute_code(self, code: str):
        """
        Execute the generated code using the KiCad pcbnew Python interpreter.
        This runs the code in a separate process with pcbnew_path as the interpreter.

        Args:
            code (str): The Python code to be executed.
        Returns:
            str: The error output of the executed code, or None if successful.
        """
        # replace \\\" with \"
        code = code.replace("\\\"", "\"")
        code = code.replace("\\n", "\n")

        if system == "Windows":
            safe_path = self.pcb_path.replace("\\", "\\\\")
        else:
            safe_path = self.pcb_path
        
        # Add project path to the safe path for imports in the generated code
        safe_path = os.path.join(project_path, safe_path)
        safe_path = os.path.normpath(safe_path)

        code = code.replace("layout = layout_api()", f"layout = layout_api(filename=\"{safe_path}\")")
        self.logger.debug(f"Code: {code}")

        # Write the script to a temporary file
        tmp_file = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as tf:
                tf.write(code)
                tmp_file = tf.name

            # Prepare environment and working directory
            env = os.environ.copy()
            # Ensure PYTHONPATH contains PROJECT_PATH so imports in the child process can resolve
            env["PYTHONPATH"] = os.pathsep.join(
                [project_path, env.get("PYTHONPATH", "")]
            )

            # Prefer to run in the PCB's directory (helps with relative paths)
            run_cwd = os.path.dirname(self.pcb_path) if os.path.isfile(self.pcb_path) else os.getcwd()

            # Call KiCad's bundled python interpreter
            result = subprocess.run(
                [pcbnew_path, tmp_file],
                cwd=run_cwd,
                env=env,
                capture_output=True,
                text=True
            )

            out = (result.stdout or "") + ("\n" if result.stdout and result.stderr else "") + (result.stderr or "")

            self.logger.info("Code executed.")
            self.logger.info(f"Output:\n{out}")
            self.logger.info("Schematic drawing finished.")

            if "error" in out.lower():
                self.logger.error(f"Error in executing code: {out}")
                return out

            m = re.search(r"score of ([0-9.]+)", out)
            score = float(m.group(1).rstrip(".")) if m else None

            self.scores.append(score)
    
            return None

        except Exception:
            out = _tb.format_exc()
            self.logger.error(f"Exception while executing code: {out}")
            return out
        finally:
            # Clean up temp file
            try:
                if tmp_file and os.path.exists(tmp_file):
                    os.remove(tmp_file)
            except Exception:
                pass

    
    def read_related_footprints(self):
        """
        Load related footprints and summarize geometry for LLM placement.
        Produces a text block per reference with pad bbox, body size, and keepout.
        """
        self.logger.info("Loading related footprints...")

        # Example: your method that returns {ref: (lib_name, item_name)}
        res = get_layout_lib_info(self.pcb_path)
        if res["ok"]:
            libinfo = res["data"]
        else:
            raise RuntimeError(f"Failed to get layout lib info: {res}")

        fp_lib_path = Path(project_path) / "export" / "organized_fp.json"
        # Example: your organized JSON: { "Capacitor_SMD": [ {name: "C_Elec_8x6.2", ...}, ...], ... }
        organized_lib = load_organized_fp(fp_lib_path)

        # Build fast lookup: (lib_name, item_name) -> footprint dict
        ft_index = {}
        for lib_name, items in organized_lib.items():
            for f in items:
                ft_index[(lib_name, f["name"])] = f

        summaries = []
        for ref, (lib_name, item_name) in libinfo.items():
            self.logger.info(f"Reference: {ref}, Library: {lib_name}, Item: {item_name}")
            f = ft_index.get((lib_name, item_name))
            if not f:
                summaries.append(f"FOOTPRINT\nref: {ref}\nerror: footprint not found in organized library\nEND")
                continue
            summaries.append(_render_llm_block(ref, lib_name, item_name, f))

        # Final multi-block text message suitable for LLM consumption
        text_message = "\n\n".join(summaries)
        return text_message

    def pcb_layout(self, feedback: str = None):
        """
        Based on the user request, image of the schematic and netlist, generate the code that can perform PCB layout.
        """
        self.logger.info("Starting PCB layout...")

        # 1. Get the footprint information from the library
        fp_summary = self.read_related_footprints()

        # 2. Prepare the prompt from the schematic based on three resources:
        # (1) schematic image
        # (2) netlist file
        # (3) footprint library summary
        # (4) Design Rule Check (DRC) feedback from previous layout attempt (if any)
        sch_img = get_sch_with_axes(image_name="sch4layout.png", schematic_path=self.schematic_path)

        try:
            with open(self.netlist_path, "r", encoding="utf-8") as f:
                self.netlist_content = f.read()
        except Exception:
            # Directly read the netlist content if file read fails
            self.netlist_content = get_schematic_netlist(sch_file=self.schematic_path, netlist_file=self.netlist_path)
        
        if feedback is not None:
            feedback_msg = f"Please check the feedback from previous layout attempt:\n{feedback}\n"
        else:
            feedback_msg = ""

        local_request = (
            feedback_msg +
            "Please check the following schematic image, the extracted netlist text, and the footprint summaries. "
            "Generate Python code to perform PCB layout according to the schematic using only the provided layout_api. "
            "Ensure components do not overlap and leave reasonable spacing. Structure the code into logical blocks, "
            "call auto_routing() at the end, and then save().\n"

            # -------------------- Added notes based on prior knowledge --------------------
            "\nNotes / Constraints for robust layout & freerouting convergence:\n"
            "1) Placement-first: group strongly connected parts close together (e.g., IC + its decoupling caps, sensor + pullups/filters, LDO + Cin/Cout). "
            "Keep I2C/SPI clusters compact to reduce crossing nets.\n"
            "2) Orientation: rotate footprints so that pins facing each other minimize net crossings. "
            "Prefer pin-to-pin alignment over diagonal connections.\n"
            "3) Routing channels: leave routing corridors between groups (>= 2~3 trace widths). "
            "Avoid forming U-shaped walls of parts that block paths.\n"
            "4) Power strategy: do NOT rely on autorouter for main power distribution. "
            "Place power entry (connector/USB/battery) near board edge. "
            "Pre-route or reserve wide paths for VDD rails; ground should be a plane/zone if layout_api supports it; otherwise keep GND star-like and short.\n"
            "5) Net-class intent (if layout_api exposes it): "
            "use thicker traces for power nets (+3V3, +5V, VBUS) and default width for signals; "
            "keep clearance at a manufacturable safe value (e.g., >=0.15–0.20 mm). "
            "If no netclass API exists, approximate by manually widening power traces or by placing power pins closer.\n"
            "6) Keepout / sensitive parts: "
            "for RF modules (ESP32-WROOM), place near board edge with antenna facing outward; "
            "keep antenna keepout clear of copper/parts. "
            "Keep magnetometers/IMUs/mics away from ESP32 and switching/power inductors.\n"
            "7) Via/trace practicality: "
            "avoid via-in-pad unless footprint explicitly supports it; "
            "ensure vias are not placed under dense connectors or inside courtyards.\n"
            "8) Spacing heuristic: "
            "use a minimum component gap margin (e.g., 0.5–1.0 mm or more for large parts) when computing bounding boxes.\n"
            "9) Deterministic layout: "
            "place board outline first, then anchors (connectors, MCU/module, regulators), then peripherals, lastly passives. "
            "Use consistent coordinate system and comments for readability.\n"
            "10) For big chips with antenna like ESP32, ensure the antenna side is placed near the board edge with no copper or components in the keepout area.\n"
            # ---------------------------------------------------------------------------

            "\n###\n"
            "Netlist:\n"
            f"{self.netlist_content}\n"
            "###\n"
            "Footprint summaries:\n"
            f"{fp_summary}\n"
            "Below is the schematic image for reference."
        )

        # Prepare message with the schematic image
        image_msg = self.llm.prepare_input_with_image(local_request, sch_img)
        assert isinstance(image_msg, list) and len(image_msg) == 1, "Image message should be a list."

        # Use the prepared layout prompt context from initialization
        self.msg_list.append(image_msg[0])

        # Ask LLM to produce code
        try:
            response, code_obj = self.llm.get_json_response_retry(self.msg_list, PCBEditCode)
            self.logger.info(f"Layout LLM response received.")
            self.logger.debug(f"LLM response: {response}")
        except Exception as e:
            self.logger.error(f"Failed to get layout response: {e}")
            return

        if code_obj is None or not code_obj.code.strip():
            self.logger.error("Generated layout code is empty.")
            return

        # Execute the generated code
        self.logger.info("Executing generated layout code...")

        sanitized_code = sanitize_code(code_obj.code)
        exec_output = self.execute_code(sanitized_code)
        if exec_output is not None:
            self.logger.error(f"Error executing layout code: {exec_output}")
        else:
            self.logger.info("PCB layout completed successfully.")
        
        return exec_output, sanitize_code

    def get_drc_feedback(self) -> str:
        """
        Get feedback from the DRC report.
        """
        drc_report = get_drc_report(self.pcb_path)
        return drc_report

    def get_feedback(self, last_exec_output, use_visual_feedback=False) -> str:
        """
        Analyze the current PCB layout and provide feedback on potential issues.
        This can include checking for overlapping components, unconnected nets, etc.
        Returns:
            str: Feedback message.
        """
        self.logger.info("Analyzing PCB layout for feedback...")

        # Feeback 1: Extract layout issues from the last execution output
        execute_feedback = f"First, here is the output from the last layout attempt:\n{last_exec_output}\n"

        # Feedback 2: Design Rule Check (DRC) feedback from previous layout attempt (if any)
        drc_feedback = self.get_drc_feedback()
        if drc_feedback:
            execute_feedback += f"Second, here is the DRC feedback from the last layout attempt:\n{drc_feedback}\n"

        # If use visual feedback
        if use_visual_feedback:
            pcb_img_path = get_pcb_with_axes(image_name="pcb_feedback.png", pcb_path=self.pcb_path)
            self.logger.info(f"PCB image extracted. {pcb_img_path}")
            pcb_vision_prompt = f"""
            Check the feedback from the auto-routing result based on your previus layout code: {execute_feedback}.
            You are also provided with the PCB layout image as attached, you MUST compare the them with the netlist content: {self.netlist_content}.
            There are two levels of feedback: warnings and errors.
            Error only considers as the critical footprint overlaps or unconnected nets, ONLY conisder footprint overlaps, IGNORE text overlaps.
            Warning include design issues like misaligned component placement, unreadable wire connections, that can be improved to create a better schematic design but not errors.
            ###
            Output format:
            1. First, provide a score from -1, 0, or 1, where -1 means the schematic is not correct, 0 means the layout is correct but can be improved, and 1 means the schematic is correct and well-designed.
            2. Then, provide a list of errors and warnings. Go through the following types of errors:
            (1) footprint overlaps: where you can find component and symbols overlap with each other, such as a GND or power symbol inside the rectangle of another symbol.
            (2) Unconnected nets: where you can find pins that are not connected to any net.

            3. Finally, provide suggestions to fix the errors and warnings, like how you can adjust the footprint placement to fix the overlaps.
            ###
            Important NOTE:
            1. Focus on the image. Think carefully about the layout, do not provide feedback unless you are sure about the issues.
            2. Common errors include: (1) Components or symbols overlap with each other. For example, placing a GND or power symbol inside the rectangle of another symbol is an error. Adjust the component placement and wiring to correct the layout.
            """
            
            image_msg = self.llm.prepare_input_with_image(pcb_vision_prompt, pcb_img_path)
            assert isinstance(image_msg, list) and len(image_msg) == 1, "Image message should be a list."
            self.msg_list.append(image_msg[0])

            # Return the feedback from LLM
            response, feedback_obj = self.llm.get_json_response_retry(self.msg_list, PCBFeedback)
            self.logger.info(f"PCB visual feedback Response: {response}")
        else:
            pcb_prompt = f"""
            Check the feedback from the auto-routing result based on your previus layout code: {execute_feedback}.
            There are two levels of feedback: warnings and errors.
            Error only considers as the critical footprint overlaps or unconnected nets, ONLY conisder footprint overlaps, IGNORE text overlaps. Note that as long as there are no unconnected nets, the layout is considered correct without errors.
            Warning include design issues like misaligned component placement, unreadable wire connections, that can be improved to create a better schematic design but not errors.
            Remember, if there are unconnected nets, it often means the auto-routing algorithm failed to converge, you can try to adjust the component placement by decreasing the spacing between components or changing the orientation of some components to help the auto-routing algorithm to converge. Note that do not put components too close to each other to avoid footprint overlaps and provide enough space for PCB traces.
            ###
            Output format:
            1. First, provide a score from -1, 0, or 1, where -1 means the schematic is not correct, 0 means the layout is correct but can be improved, and 1 means the schematic is correct and well-designed.
            2. Then, provide a list of errors and warnings. Go through the following types of errors:
            (1) footprint overlaps: where you can find component and symbols overlap with each other, such as a GND or power symbol inside the rectangle of another symbol.
            (2) Unconnected nets: where you can find pins that are not connected to any net.

            3. Finally, provide suggestions to fix the errors and warnings, like how you can adjust the footprint placement to fix the overlaps.
            ###
            Important NOTE:
            1. Focus on the image. Think carefully about the layout, do not provide feedback unless you are sure about the issues.
            2. Common errors include: (1) Components or symbols overlap with each other. For example, placing a GND or power symbol inside the rectangle of another symbol is an error. Adjust the component placement and wiring to correct the layout.
            3. Placement should follow the normal design logic. For example, decoupling capacitors should be placed close to the power pins of ICs, and connectors should be placed at the edges of the PCB for easy access.
            """

            self.msg_list.append({"role": "user", "content": pcb_prompt})
            response, feedback_obj = self.llm.get_json_response_retry(self.msg_list, PCBFeedback)
            self.logger.info(f"PCB feedback Response: {response}")

        return response, feedback_obj
    
    def iterative_pcb_layout(self, max_iters: int = 3):
        """
        Perform iterative PCB layout with feedback loop.
        Args:
            max_iters (int): Maximum number of iterations.
        """

        feedback = None
        res = get_layout_lib_info(self.pcb_path)
        if res["ok"]:
            libinfo = res["data"]
        else:
            raise RuntimeError(f"Failed to get layout lib info: {res}")
        if len(libinfo) < 2:
            # If there are less than 2 components, no need to do layout
            self.logger.info("Less than 2 components found, skipping layout iterations.")
            return None
        if len(libinfo) <= 5:
            # If there are less than 5 components, only do 3 iterations
            max_iters = 3
        # Get the intial score of auto wiring (step 0) of random layout
        res_auto_wiring = auto_wiring_score(self.pcb_path)
        if res_auto_wiring["ok"]:
            self.scores.append(res_auto_wiring["score"])
        else:
            self.logger.error(f"Failed to get auto wiring score: {res_auto_wiring}")

        for itr in range(max_iters):

            self.logger.info(f"Starting PCB layout iteration {itr + 1}/{max_iters}...")

            clear_wiring(self.pcb_path)
            try:
                exec_output, code = self.pcb_layout(feedback=feedback)
            except Exception as e:
                self.logger.error(f"Error during PCB layout: {e}")
                break
            try:
                feedback, feedback_obj = self.get_feedback(last_exec_output=exec_output)
            except Exception as e:
                self.logger.error(f"Error during feedback analysis: {e}")
                continue
            if feedback_obj.score >= self.maximum_score:
                self.maximum_score = feedback_obj.score
                self.best_code = code
            elif feedback_obj.score < self.maximum_score:
                feedback = f"The previous layout code produced worse results. Please improve upon the best known layout code instead.\n{self.best_code}"

            self.logger.info(f"Feedback for iteration {itr + 1}:\n{feedback}")

            if feedback_obj and feedback_obj.score == 1:
                self.logger.info("Layout is correct and well-designed. Stopping iterations.")
                break

class PCBEditCode(BaseModel):
    explanation: str
    code: str

import argparse
from matplotlib import pyplot as plt
import sys, os
project_path = os.environ["PROJECT_PATH"]
sys.path.append(project_path)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse


def build_parser():
    parser = argparse.ArgumentParser(
        description="Run iterative PCB layout generation with LayoutAgent."
    )

    parser.add_argument(
        "--project_path",
        type=str,
        required=True,
        help="Module name used by LayoutAgent",
    )

    parser.add_argument(
        "--project_name",
        type=str,
        required=True,
        help="Module name used by LayoutAgent",
    )

    parser.add_argument(
        "--model",
        type=str,
        default="gpt-5",
        help="LLM model name",
    )

    parser.add_argument(
        "--model_provider",
        type=str,
        default="OpenRouter",
        help="LLM provider name",
    )

    parser.add_argument(
        "--max_iters",
        type=int,
        default=5,
        help="Maximum iterative layout optimization iterations",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    layout_agent = LayoutAgent(
        model=args.model,
        model_provider=args.model_provider,
        design_path=args.project_path,
        module_name=args.project_name,
    )

    layout_agent.iterative_pcb_layout(
        max_iters=args.max_iters,
    )


if __name__ == "__main__":
    main()
    
    # plt.figure()
    # plt.plot(range(0, len(layout_agent.scores)), layout_agent.scores, marker='o')
    # plt.xlabel("Iteration Rounds")
    # plt.ylabel("Layout Score")
    # # plt.title("PCB Layout Score over Iterations")
    # plt.grid(True)
    # plt.show()
    # plt.savefig("layout_score_plot.png")

    # # Save the scores
    # with open("layout_scores_grok.txt", "w") as f:
    #     for score in layout_agent.scores:
    #         f.write(f"{score}\n")