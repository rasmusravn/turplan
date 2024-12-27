import os
from pathlib import Path


def get_data_dir() -> Path:
    """
    Forsøger at finde en standardiseret sti til datamappen (XDG_DATA_HOME på Linux/macOS).
    Fald tilbage på ~/.local/share/turplan, hvis ikke XDG_DATA_HOME er sat.
    På Windows kan man i stedet bruge fx APPDATA, men her er vist et simpelt eksempel.
    """
    # 1) Tjek om XDG_DATA_HOME er sat (typisk på Linux/macOS)
    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    if xdg_data_home:
        data_dir = Path(xdg_data_home) / APP_NAME
    else:
        # 2) Hvis ikke, brug en “fornuftig” standard-fallback
        if os.name == "nt":  # Windows
            # fx %APPDATA%\turplan
            data_dir = Path(os.environ.get("APPDATA", Path.home())) / APP_NAME
        else:
            # På Linux/macOS: ~/.local/share/turplan
            data_dir = Path.home() / ".local" / "share" / APP_NAME

    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir
