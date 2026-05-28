# Algae — Instructions

This file explains how to install dependencies, generate a Windows executable, and a short tutorial for using the GUI app `merge_tvs_ting_plot_GUI.py`.

## 1) Quick run (recommended for developers)

1. Clone the repo and change directory:

   git clone <your-repo-url>
   cd Algae

2. Create & activate a virtual environment:

   # Windows (PowerShell)
   python -m venv .venv
   .venv\Scripts\Activate.ps1

   # macOS / Linux
   python -m venv .venv
   source .venv/bin/activate

3. Install requirements:

   pip install -r requirements.txt

4. Run the GUI:

   python merge_tvs_ting_plot_GUI.py


## 2) Generate a Windows executable (local)

Option A — use included script (Windows; recommended):

1. From PowerShell in the repo root:

   powershell -ExecutionPolicy Bypass -File build_windows.ps1

   This runs `pyinstaller` to produce `dist\DataPlotter.exe`. If NSIS (`makensis`) is installed, it will also create `DataPlotter_Installer.exe`.

2. Or run the batch wrapper from cmd:

   build_windows.bat

Option B — run PyInstaller manually:

   pip install pyinstaller
   pyinstaller --noconfirm --onefile --windowed merge_tvs_ting_plot_GUI.py --name DataPlotter

The single-file exe will appear at `dist\DataPlotter.exe`.


## 3) Generate a Windows executable via GitHub Actions (CI)

Push to `main`/`master` or trigger the workflow `.github/workflows/build-windows.yml` from the Actions tab. The workflow builds the exe and (on the runner) will install NSIS to create an installer. Download artifacts named `DataPlotter-windows` from the workflow run.


## 4) Short tutorial — using the GUI

- `Select Viscoelastic File`: choose the viscoelastic CSV file (semicolon-separated). Column names will be cleaned.
- `Select adhesion File`: choose the adhesion file (tab-separated).
- `Merge Files`: merges on `curve_idx` (left) and `Position_Index` (right). The merged dataset is used for plots and exports.
- `X` / `Y` comboboxes: choose numeric columns for plotting and histograms.
- `Plot X vs Y`: scatter plot of the chosen columns.
- `Plot Histograms`: shows side-by-side histograms for X and Y. Change `Bin Size X` / `Bin Size Y` to modify bins.
- `Log X` / `Log Y`: toggle log-scale on axes for plots and histograms.
- `Threshold (hertz_z_c >)`: enter a numeric threshold and click `Apply Threshold` to filter rows where cleaned `hertz_z_c` > threshold. `Reset Threshold` restores full merged data.
- `Export Filtered CSV`: saves the currently displayed (possibly filtered) DataFrame to CSV.
- `Export Summary Stats`: exports summary statistics (mean, std, median, geom mean for positives, IQR) for numeric columns.


## 5) Troubleshooting & notes

- tkinter: The app uses `tkinter` and matplotlib `TkAgg`. On Windows use the official Python installer (includes Tcl/Tk). On some Linux systems, install `python3-tk` or the OS package providing Tcl/Tk.
- File formats: `Select Viscoelastic File` expects a `;`-separated CSV (the current loader uses `sep=';'`). The adhesion file loader expects a tab-separated file. If your files differ, pre-convert them or adjust the code.
- Column names: column names are cleaned (quotes removed, non-word chars replaced by `_`). The `hertz_z_c` column is checked after cleaning for thresholding.
- Missing numeric columns: Pick numeric columns from the comboboxes — if none appear, check merged data and dtypes.


## 6) Files added by me

- `build_windows.ps1` — PowerShell build script (PyInstaller + writes NSIS script + runs `makensis` if available).
- `build_windows.bat` — Batch wrapper for `build_windows.ps1`.
- `.github/workflows/build-windows.yml` — CI workflow to build exe and installer on a Windows runner.
- `README_BUILD_WINDOWS.md` — supplementary CI & build notes.


If you want, I can also add a top-level `README.md` with these quick-start instructions, or a LICENSE and `.gitignore`. Which would you like next?
