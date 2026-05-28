# Algae

Simple GUI tools for merging and plotting viscoelastic and adhesion data.

Quick contents:

- `merge_tvs_ting_plot_GUI.py` — main tkinter GUI app.
- `INSTRUCTIONS.md` — detailed install, build, and short tutorial.
- `build_windows.ps1`, `build_windows.bat` — local Windows build scripts (PyInstaller + NSIS helper).
- `.github/workflows/build-windows.yml` — CI workflow to build a Windows `.exe` and installer.

Prerequisites
- Python 3.10+ (recommended)
- On Windows: official Python installer (includes Tcl/Tk) for `tkinter` support.

Quick start (developer)

```bash
git clone <your-repo-url>
cd Algae
python -m venv .venv
# Windows (PowerShell): .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python merge_tvs_ting_plot_GUI.py
```

Build a Windows executable
- Local (Windows): run `build_windows.ps1` (PowerShell) or `build_windows.bat` (cmd). See `INSTRUCTIONS.md` for details.
- CI: push to `main`/`master` or trigger the workflow in Actions; download artifacts from the run.

Notes
- The GUI uses `tkinter` and matplotlib `TkAgg`. If plots or GUI fail, ensure Tcl/Tk and GUI backends are available.
- See `INSTRUCTIONS.md` for full instructions, troubleshooting, and a short tutorial.

License
- Add a `LICENSE` file to indicate how others can use this code. If you tell me which license to use, I can add it.

Contributing
- Open an issue or pull request with changes; include a short description and testing notes.
