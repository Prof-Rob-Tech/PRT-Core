; ===========================================================
; Script de Instalação - PRT NEXUS
; ===========================================================

[Setup]
AppName=PRT NEXUS
AppVersion=1.0.0
AppPublisher=PRT Labs
AppPublisherURL=https://github.com/
DefaultDirName={autopf}\PRT NEXUS
DefaultGroupName=PRT NEXUS
OutputDir=Output
OutputBaseFilename=PRT_NEXUS_Setup_v1.0.0
Compression=lzma2/max
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

; Ícones e Aparência
SetupIconFile=resources\icon.ico
UninstallDisplayIcon={app}\PRT NEXUS.exe

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Copia todos os arquivos gerados pelo PyInstaller na pasta dist
Source: "dist\PRT NEXUS\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\PRT NEXUS"; Filename: "{app}\PRT NEXUS.exe"; IconFilename: "{app}\PRT NEXUS.exe"
Name: "{group}\{cm:UninstallProgram,PRT NEXUS}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\PRT NEXUS"; Filename: "{app}\PRT NEXUS.exe"; Tasks: desktopicon; IconFilename: "{app}\PRT NEXUS.exe"

[Run]
Filename: "{app}\PRT NEXUS.exe"; Description: "{cm:LaunchProgram,PRT NEXUS}"; Flags: nowait postinstall skipifsilent