#ifndef AppVersion
#define AppVersion "0.0.0"
#endif

[Setup]
AppId={{B9844BD0-6C1D-4BC2-9FE9-5A0D7B7C4D2E}
AppName=Sophie Pallas
AppVersion={#AppVersion}
AppPublisher=Sophie Pallas
DefaultDirName={localappdata}\Sophie Pallas
PrivilegesRequired=lowest
DisableProgramGroupPage=yes
OutputDir=dist
OutputBaseFilename=sophie-pallas-v{#AppVersion}-windows-x64-setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
Uninstallable=yes

[Files]
Source: "dist\app\*"; DestDir: "{app}\app"; Flags: recursesubdirs ignoreversion
Source: "dist\runtime\*"; DestDir: "{app}\runtime"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{autodesktop}\Sophie Pallas"; Filename: "{app}\runtime\pythonw.exe"; Parameters: """{app}\app\launch.py"""; WorkingDir: "{app}\app"; IconFilename: "{app}\app\girl-reference.png"
Name: "{autoprograms}\Sophie Pallas"; Filename: "{app}\runtime\pythonw.exe"; Parameters: """{app}\app\launch.py"""; WorkingDir: "{app}\app"; IconFilename: "{app}\app\girl-reference.png"

[Run]
Filename: "{app}\runtime\pythonw.exe"; Parameters: """{app}\app\launch.py"""; WorkingDir: "{app}\app"; Flags: nowait postinstall skipifsilent
