param(
    [string]$Name = 'DataPlotter'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Host "Building $Name..."

python -m pip install --upgrade pip
if (Test-Path 'requirements.txt') { pip install -r requirements.txt }
pip install pyinstaller

pyinstaller --noconfirm --onefile --windowed merge_tvs_ting_plot_GUI.py --name $Name

$nsi = @"
OutFile "${Name}_Installer.exe"
Name "${Name}"
InstallDir "$PROGRAMFILES64\\${Name}"
SetOutPath "$INSTDIR"
File "dist\\${Name}.exe"
CreateShortCut "$SMPROGRAMS\\${Name}.lnk" "$INSTDIR\\${Name}.exe"
SectionEnd
"@

$nsi | Out-File -FilePath installer.nsi -Encoding ASCII

if (Get-Command makensis -ErrorAction SilentlyContinue) {
    makensis installer.nsi
    Write-Host "Installer created: ${Name}_Installer.exe"
} else {
    Write-Host "makensis not found. Please install NSIS (https://nsis.sourceforge.io/) and run 'makensis installer.nsi' to create the installer."
}

Write-Host "Build finished. Artifacts are in the 'dist' folder (exe) and installer file (if created)."
