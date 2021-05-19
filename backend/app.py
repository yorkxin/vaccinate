from flask import Flask, render_template, json, wrappers
import argparse
import sys, os
from typing import TypedDict, Tuple, Dict, Callable, List, Any, Optional
from enum import Enum

app = Flask(
    __name__,
    static_url_path="",
    static_folder="../dist",
    template_folder="../dist",
)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
