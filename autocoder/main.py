import os
import sys

from dotenv import load_dotenv

from agentloop import start, step_with_input_key

from autocoder.steps import reason
from autocoder.steps import act
from agentlogger import log, print_header

# Suppress warning
os.environ["TOKENIZERS_PARALLELISM"] = "False"

load_dotenv()  # take environment variables from .env.


def autocoder(project_data):
    """
    Main entrypoint for autocoder. Usually called from the CLI.
    """

    if project_data["log_level"] != "quiet":
        print_header(text="autocoder", color="yellow", font="slant")
        log("Initializing...", title="autocoder", type="system", panel=False)


    project_data["project_dir"] = f"./project_data/{project_data['project_name']}"

    # check if project_dir exists and create it if it doesn't
    if not os.path.exists(project_data["project_dir"]):
        os.makedirs(project_data["project_dir"])

    def initialize(context):
        if context is None:
            # Should only run on the first run
            context = project_data
            context["running"] = True
        return context

    loop_dict = start([initialize, reason, act], stepped=project_data["step"])
    if project_data["step"]:
        step_with_input_key(loop_dict)

    return loop_dict
