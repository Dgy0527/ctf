from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from jinja2 import TemplateError


app = Flask(__name__)
ASSET_MANIFEST = Path(__file__).parent / "static" / "assets" / "pixel-ui" / "manifest.json"


SPELLS = {
    "Fireball": {
        "class_name": "fire",
        "incantation": "Let the flames consume your enemies!",
        "rune": "spell-fire",
        "asset": "icons/fireball.png",
    },
    "Ice Shard": {
        "class_name": "ice",
        "incantation": "Freeze the path before you.",
        "rune": "spell-ice",
        "asset": "icons/ice_shard.png",
    },
    "Lightning": {
        "class_name": "lightning",
        "incantation": "Strike faster than thought.",
        "rune": "spell-lightning",
        "asset": "icons/lightning.png",
    },
    "Heal": {
        "class_name": "heal",
        "incantation": "Bind the wound with emerald light.",
        "rune": "spell-heal",
        "asset": "icons/heal.png",
    },
    "Shadow Step": {
        "class_name": "shadow",
        "incantation": "Walk where the torchlight fails.",
        "rune": "spell-shadow",
        "asset": "icons/shadow_step.png",
    },
    "Arcane Shield": {
        "class_name": "shield",
        "incantation": "Raise the ward and hold the line.",
        "rune": "spell-shield",
        "asset": "icons/arcane_shield.png",
    },
}


DEFAULT_MESSAGE = "{{ wizard }} summons the power of {{ spell }}!\n\n{{ message }}"


@dataclass
class Scroll:
    wizard: str
    spell: str
    rendered: str
    created_at: str


scroll_history: list[Scroll] = [
    Scroll("Merlin_the_Wise", "Fireball", "Merlin_the_Wise summons Fireball!", "Just now"),
    Scroll("Merlin_the_Wise", "Ice Shard", "Merlin_the_Wise summons Ice Shard!", "2 mins ago"),
    Scroll("Merlin_the_Wise", "Heal", "Merlin_the_Wise summons Heal!", "5 mins ago"),
    Scroll("Gandalf_The_Grey", "Lightning", "Gandalf_The_Grey summons Lightning!", "12 mins ago"),
]


# 源代码
# def render_scroll_message(template_source: str, wizard: str, spell: str) -> str:
#     from flask import render_template_string

#     return render_template_string(template_source, wizard=wizard, spell=spell)



# 修改为
def render_scroll_message(template_source,wizard,spell):
    return{
        template_source.replace("{{wizard}}",wizard)
        .replace("{{spell}}",spell)
    }   


@app.get("/")
def index():
    return render_template(
        "index.html",
        spells=SPELLS,
        default_message=DEFAULT_MESSAGE,
        initial_scroll=None,
        history=scroll_history[:4],
    )


@app.get("/dev/assets")
def dev_assets():
    if not ASSET_MANIFEST.exists():
        return render_template("error.html", message="Asset manifest has not been generated yet."), 404
    manifest = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))
    assets = sorted(manifest.values(), key=lambda item: (item["category"], item["key"]))
    return render_template("dev_assets.html", assets=assets)


@app.post("/generate")
def generate():
    wizard = request.form.get("wizard", "Merlin_the_Wise").strip() or "Nameless_Apprentice"
    spell = request.form.get("spell", "Fireball")
    template_source = request.form.get("message", DEFAULT_MESSAGE)

    if spell not in SPELLS:
        spell = "Fireball"

    try:
        rendered = render_scroll_message(template_source, wizard=wizard, spell=spell)
    except TemplateError:
        if request.headers.get("Accept") == "application/json":
            return jsonify(
                {
                    "ok": False,
                    "error": "The scroll fizzled. Your template syntax disturbed the runes.",
                }
            ), 400
        return render_template(
            "error.html",
            message="The scroll fizzled. Your template syntax disturbed the runes.",
        ), 400

    scroll = Scroll(
        wizard=wizard,
        spell=spell,
        rendered=rendered,
        created_at=datetime.now(timezone.utc).strftime("%H:%M UTC"),
    )
    scroll_history.insert(0, scroll)
    del scroll_history[6:]

    if request.headers.get("Accept") == "application/json":
        return jsonify(
            {
                "ok": True,
                "wizard": wizard,
                "spell": spell,
                "spellClass": SPELLS[spell]["class_name"],
                "incantation": SPELLS[spell]["incantation"],
                "rendered": rendered,
                "history": [item.__dict__ for item in scroll_history[:4]],
            }
        )

    return render_template(
        "scroll.html",
        scroll=scroll,
        spell_data=SPELLS[spell],
        history=scroll_history[:4],
    )


@app.get("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
