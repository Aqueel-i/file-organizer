# Name and output
Outfile "FileOrganizerSetup.exe"
InstallDir "$PROGRAMFILES\File Organizer"
Icon "icon.ico"
RequestExecutionLevel admin

# Default section
Section "Install"

  SetOutPath "$INSTDIR"
  File "dist\organizer.exe"
  File "icon.ico"

  # Create shortcut on Desktop
  CreateShortCut "$DESKTOP\File Organizer.lnk" "$INSTDIR\organizer.exe" "" "$INSTDIR\icon.ico"

  # Create shortcut in Start Menu
  CreateDirectory "$SMPROGRAMS\File Organizer"
  CreateShortCut "$SMPROGRAMS\File Organizer\File Organizer.lnk" "$INSTDIR\organizer.exe" "" "$INSTDIR\icon.ico"

SectionEnd

# Uninstaller Section (optional but recommended)
Section "Uninstall"
  Delete "$INSTDIR\organizer.exe"
  Delete "$INSTDIR\icon.ico"
  Delete "$DESKTOP\File Organizer.lnk"
  Delete "$SMPROGRAMS\File Organizer\File Organizer.lnk"
  RMDir "$SMPROGRAMS\File Organizer"
  RMDir "$INSTDIR"
SectionEnd
