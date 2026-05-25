# aeromat/ui/pages/__init__.py
from .chat import render_chat_page
from .software_guide import render_software_guide_page
from .theory_tutorial import render_theory_tutorial_page
from .result_compare import render_result_compare_page

__all__ = [
    "render_chat_page",
    "render_software_guide_page",
    "render_theory_tutorial_page",
    "render_result_compare_page"
]