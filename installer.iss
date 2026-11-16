[Setup]
; Información general de la aplicación
AppName=RIS Analytics
AppVersion=1.1
AppPublisher=Tecnoimagen
; Carpeta por defecto donde se instalará (Program Files)
DefaultDirName={autopf}\Tecnoimagen\RIS Analytics
DefaultGroupName=RIS Analytics

; Configuración del archivo instalador generado
OutputDir=Output
OutputBaseFilename=Instalador_RIS_Analytics_v1.1
; Cambia esta ruta si tu ícono tiene otro nombre o extensión
SetupIconFile=web\favicon.ico 

; Opciones de compresión
Compression=lzma
SolidCompression=yes
; Permite que se instale sin requerir siempre permisos de Administrador estricto, 
; aunque {autopf} lo suele pedir.
PrivilegesRequired=lowest

[Tasks]
; Casilla para crear acceso directo en el escritorio
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Archivo ejecutable principal (asegúrate de que el nombre coincida con lo que generó PyInstaller)
Source: "dist\RIS_Analytics.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Acceso directo en el Menú Inicio
Name: "{group}\RIS Analytics"; Filename: "{app}\RIS_Analytics.exe"
; Acceso directo en el Escritorio
Name: "{autodesktop}\RIS Analytics"; Filename: "{app}\RIS_Analytics.exe"; Tasks: desktopicon

[Run]
; Opción para lanzar la aplicación al finalizar la instalación
Filename: "{app}\RIS_Analytics.exe"; Description: "{cm:LaunchProgram,RIS Analytics}"; Flags: nowait postinstall skipifsilent