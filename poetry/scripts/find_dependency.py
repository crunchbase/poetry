import sys
import os
from pathlib import Path
from argparse import ArgumentParser
from unittest.mock import patch
import json
import importlib.machinery


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)
        self.save_path = None

    def __enter__(self):
        self.save_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.save_path)


def main():
    parser = ArgumentParser("setup.py dependency parser")
    parser.add_argument("--setup", dest="setup", required=True, help="the setup file location")
    parser.add_argument("--output", dest="output", required=True, help="output json location")
    args = parser.parse_args()
    result = {}

    setup_path = Path(args.setup)

    with patch("setuptools.setup") as mock_setup:
        with patch("distutils.core.setup") as mock_dist_setup:
            loc, mod = str(setup_path.parent), str(setup_path.name).replace(".py", "")
            sys.path.insert(0, loc)

            with cd(loc):
                loader = importlib.machinery.SourceFileLoader("__main__", "setup.py")
                loader.load_module()
            if mock_setup.call_count > 0 or mock_dist_setup.call_count > 0:
                # force to go second route.
                called_setup = mock_setup if mock_setup.call_count else mock_dist_setup
                call_kwargs = called_setup.call_args[1]
                result["name"] = call_kwargs["name"]
                result["version"] = call_kwargs["version"]
                result["install_requires"] = call_kwargs.get("install_requires", [])
                result["extras_require"] = call_kwargs.get("extras_require")
                result["python_requires"] = call_kwargs.get("python_requires")

    with open(args.output, "w") as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
