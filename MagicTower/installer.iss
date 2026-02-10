; Inno Setup 脚本 for 魔塔传说游戏安装包
; 创建符合Windows标准的专业安装程序

[Setup]
; 应用信息
AppName=魔塔传说
AppVersion=1.0.0
AppVerName=魔塔传说 1.0.0
AppPublisher=Magic Tower Team
AppID={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}}
AppSupportURL=https://example.com/magictower
AppUpdatesURL=https://example.com/magictower/updates

; 卸载信息
UninstallDisplayName=魔塔传说
UninstallDisplayIcon={app}\魔塔传说.exe

; 安装包设置
VersionInfoVersion=1.0.0.0
VersionInfoCompany=Magic Tower Team
VersionInfoCopyright=Copyright (C) 2024 Magic Tower Team
VersionInfoDescription=魔塔传说游戏安装程序

; 安装模式设置
DefaultDirName={autopf}\魔塔传说
DefaultGroupName=魔塔传说
AllowNoIcons=yes
Encrypt=yes
Compression=lzma2/ultra64
SolidCompression=yes

; 安装前检查
MinVersion=6.1.7601
OnlyBelowVersion=0.0.0.0
AllowRootDirectory=no
Uninstallable=yes
CreateUninstallRegKey=yes
SignTool=signtool.exe sign /f "%SIGN_CERT%" /p "%SIGN_PASSWORD%" /t http://timestamp.digicert.com /a "$f"

; 语言设置
WizardStyle=modern
DisableStartupPrompt=no
TimeStampingSupport=yes

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Default.isl"; LicenseFile: "license.txt"
Name: "english"; MessagesFile: "compiler:English.isl"

[Messages]
ChineseSimpSetupWindowTitle=魔塔传说安装向导
ChineseSimpWelcomeLabel2=欢迎使用魔塔传说安装向导%n%n此向导将引导您完成安装过程。
ChineseSimpFinishLabel2=安装已完成%n%n感谢您选择魔塔传说！

[Files]
; 主程序文件
Source: "dist\魔塔传说.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\魔塔传说_logo.png"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; 开始菜单快捷方式
Name: "{group}\魔塔传说"; Filename: "{app}\魔塔传说.exe"; WorkingDir: "{app}"
Name: "{group}\卸载魔塔传说"; Filename: "{uninstallexe}"; WorkingDir: "{app}"

; 桌面快捷方式
Name: "{commondesktop}\魔塔传说"; Filename: "{app}\魔塔传说.exe"; WorkingDir: "{app}"

[Run]
; 安装完成后启动程序（可选）
Filename: "{app}\魔塔传说.exe"; Description: "启动魔塔传说"; Flags: postinstall nowait unchecked

[UninstallRun]
; 卸载时清理快捷方式（Windows自动处理）

[Code]
var
  ErrorCode: Integer;
  Is64BitInstallMode: Boolean;

function InitializeSetup(): Boolean;
begin
  Result := True;
  
  ; Windows版本检查
  if not CheckWin32Version(6, 1) then
  begin
    MsgBox('此应用程序需要Windows 7或更高版本。', mbError, MB_OK);
    Result := False;
    Exit;
  end;
  
  ; 64位系统检查
  Is64BitInstallMode := Is64BitOS;
  
  if Is64BitOS then
  begin
    MsgBox('检测到64位操作系统，将安装到64位程序目录。', mbInformation, MB_OK);
  end
  else
  begin
    MsgBox('检测到32位操作系统，将安装到32位程序目录。', mbInformation, MB_OK);
  end;
  
  Result := True;
end;

function NextButtonClick(CurPage: Integer): Boolean;
begin
  Result := True;
  
  ; 安装前检查
  if CurPage = wpReady then
  begin
    ; 检查磁盘空间
    if DiskSpaceLeft('') < 50 * 1024 * 1024 then
    begin
      MsgBox('磁盘空间不足，请确保至少有50MB的可用空间。', mbError, MB_OK);
      Result := False;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    ; 安装后操作
    MsgBox('魔塔传说安装成功！', mbInformation, MB_OK);
  end;
end;

; 卸载清理程序
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    ; 卸载后清理（Windows自动处理快捷方式）
  end;
end;

[Registry]
; 注册表项（可选）
Root: HKLM; Subkey: "Software\魔塔传说"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: uninsdeletekey

[Dirs]
; 不创建额外目录

[Files]
; 不复制额外文件

[Code]
; 启动条件检查
function CheckWin32Version(Major, Minor: Integer): Boolean;
begin
  Result := (GetWindowsVersion shr 24) >= Major;
  if Result and ((GetWindowsVersion shr 24) = Major) then
    Result := (GetWindowsVersion shr 16 and $FF) >= Minor;
end;

function GetWindowsVersion: Integer;
begin
  Result := GetVersionEx(DWORD(0));
end;

function GetVersionEx(var LPVI: TOSVersionInfo): BOOL;
external 'GetVersionExA@kernel32.dll stdcall';

function Is64BitOS: Boolean;
var
  SystemInfo: TSystemInfo;
begin
  GetNativeSystemInfo(SystemInfo);
  Result := SystemInfo.wProcessorArchitecture = PROCESSOR_ARCHITECTURE_AMD64;
end;

const
  PROCESSOR_ARCHITECTURE_AMD64 = 9;
  ARCHITECTURE_INTEL = 0;

procedure GetNativeSystemInfo(var SystemInfo: TSystemInfo);
external 'GetNativeSystemInfo@kernel32.dll stdcall';

type
  TSystemInfo = record
    wProcessorArchitecture: Word;
    wReserved: Word;
    dwPageSize: DWORD;
    lpMinimumApplicationAddress: Pointer;
    lpMaximumApplicationAddress: Pointer;
    dwActiveProcessorMask: DWORD;
    dwNumberOfProcessors: DWORD;
    dwProcessorType: DWORD;
    dwAllocationGranularity: DWORD;
    wProcessorLevel: Word;
    wProcessorRevision: Word;
  end;
