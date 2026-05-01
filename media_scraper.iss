[Setup]
AppName=MediaScraper
AppVersion=1.0
AppPublisher=MediaScraper
AppPublisherURL=https://github.com/mediascraper
AppSupportURL=https://github.com/mediascraper
AppUpdatesURL=https://github.com/mediascraper
DefaultDirName={autopf}\MediaScraper
DefaultGroupName=MediaScraper
AllowNoIcons=yes
OutputDir=dist\MediaScraper_Setup
OutputBaseFilename=MediaScraper_v1.0_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
WizardImageFile=1776386627760.png
SetupIconFile=media_scraper.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked
Name: "quicklaunchicon"; Description: "Create a Quick Launch icon"; GroupDescription: "Additional icons:"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "dist\installer\MediaScraper.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\installer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\MediaScraper"; Filename: "{app}\MediaScraper.exe"; IconFilename: "{app}\media_scraper.ico"
Name: "{group}\Uninstall MediaScraper"; Filename: "{uninstallexe}"
Name: "{autodesktop}\MediaScraper"; Filename: "{app}\MediaScraper.exe"; IconFilename: "{app}\media_scraper.ico"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\MediaScraper"; Filename: "{app}\MediaScraper.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\MediaScraper.exe"; Description: "Launch MediaScraper"; Flags: nowait postinstall skipifsilent
