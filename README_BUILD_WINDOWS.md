# Building a Windows executable for DataPlotter

This repository contains a GitHub Actions workflow that builds a Windows `.exe` using PyInstaller.

What I added:

- `.github/workflows/build-windows.yml`: CI workflow that runs on `windows-latest`, installs dependencies, runs PyInstaller, and uploads `dist/DataPlotter.exe` as an artifact.

How to build locally on Windows:

1. Install Python 3.10/3.11 and ensure `python` is on PATH.
2. (Optional) Create and activate a virtual environment:

   python -m venv .venv
   .venv\Scripts\activate

3. Install dependencies and PyInstaller:

   pip install -r requirements.txt
   pip install pyinstaller

4. Run PyInstaller from the repository root:

    pyinstaller --noconfirm --onefile --windowed merge_tvs_ting_plot_GUI.py --name DataPlotter

Alternatively, use the included build scripts (recommended):

- From PowerShell (recommended):

   powershell -ExecutionPolicy Bypass -File build_windows.ps1

- From Command Prompt:

   build_windows.bat

The PowerShell script will run PyInstaller, write an NSIS script `installer.nsi`, and attempt to run `makensis` to create `DataPlotter_Installer.exe` if NSIS is installed.

5. The built executable will be at `dist\DataPlotter.exe`.

Notes and limitations:

- I cannot produce a native Windows `.exe` from this Linux environment reliably. The workflow added will build the executable on GitHub Actions (Windows runner) and attach it as a downloadable artifact.
- If you prefer a local build, run the steps above on a Windows machine.
- The GUI uses `tkinter` and `matplotlib` via `TkAgg`; ensure Tcl/Tk is available in your Windows Python installation (the official Python.org installers include it).

CI notes:

- The GitHub Actions workflow `.github/workflows/build-windows.yml` now builds the one-file executable and also installs NSIS on the Windows runner to produce an installer `DataPlotter_Installer.exe`. Both `dist/DataPlotter.exe` and `DataPlotter_Installer.exe` are uploaded as artifacts.

If you want, I can also add a PowerShell or batch script to run the build locally on Windows, or modify the workflow to produce an installer (NSIS) — tell me which you'd prefer.
