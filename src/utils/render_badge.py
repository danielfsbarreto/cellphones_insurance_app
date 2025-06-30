from models import Execution


def render_badge(execution: Execution):
    return {
        "pending": {
            "label": "Pendente",
            "icon": ":material/schedule:",
            "color": "orange",
        },
        "completed": {
            "label": "Sucesso",
            "icon": ":material/check:",
            "color": "green",
        },
    }.get(execution.status)  # type: ignore
