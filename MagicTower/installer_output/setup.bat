@echo off
chcp 65001 >nul
title 魔塔传说安装程序

echo.
echo ========================================
echo         魔塔传说安装程序
echo ========================================
echo.
echo 版本: 1.0.0
echo 发行商: Magic Tower Team
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] 请使用管理员权限运行此安装程序！
    echo [提示] 右键点击安装程序，选择"以管理员身份运行"
    pause
    exit /b 1
)

REM 设置安装路径
set INSTALL_DIR=%ProgramFiles%\魔塔传说
if exist "%ProgramFiles(x86)%" (
    set INSTALL_DIR=%ProgramFiles(x86)%\魔塔传说
)

echo [信息] 目标安装目录: %INSTALL_DIR%
echo.

echo [1] 开始安装
echo [2] 自定义安装路径
echo [3] 取消安装
echo.
set /p CHOICE=请选择操作 [1-3]: 

if "%CHOICE%"=="1" goto install
if "%CHOICE%"=="2" goto custom_path
if "%CHOICE%"=="3" goto cancel
goto menu

:custom_path
set /p INSTALL_DIR=请输入安装路径: 
if not defined INSTALL_DIR (
    set INSTALL_DIR=%ProgramFiles%\魔塔传说
    if exist "%ProgramFiles(x86)%" (
        set INSTALL_DIR=%ProgramFiles(x86)%\魔塔传说
    )
)
goto continue_install

:install
echo.
echo [信息] 正在创建安装目录...
mkdir "%INSTALL_DIR%" 2>nul

echo [信息] 正在复制文件...
xcopy /E /I /H /Y "files\*.*" "%INSTALL_DIR%" >nul 2>&1

if exist "%INSTALL_DIR%\魔塔传说.exe" (
    echo [成功] 文件复制完成
) else (
    echo [错误] 文件复制失败，请确保源文件存在
    pause
    exit /b 1
)

echo.
echo [信息] 正在创建快捷方式...

REM 创建开始菜单快捷方式
set START_MENU=%ProgramData%\Microsoft\Windows\Start Menu\Programs\魔塔传说
mkdir "%START_MENU%" >nul 2>&1

REM 使用VBScript创建快捷方式
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut("%START_MENU%\魔塔传说.lnk") >> CreateShortcut.vbs
echo oLink.TargetPath = "%INSTALL_DIR%\魔塔传说.exe" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "魔塔传说游戏" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs >nul
del CreateShortcut.vbs >nul 2>&1

REM 创建卸载快捷方式
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateUninstall.vbs
echo Set oLink = oWS.CreateShortcut("%START_MENU%\卸载魔塔传说.lnk") >> CreateUninstall.vbs
echo oLink.TargetPath = "%INSTALL_DIR%\uninstall.bat" >> CreateUninstall.vbs
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> CreateUninstall.vbs
echo oLink.Description = "卸载魔塔传说" >> CreateUninstall.vbs
echo oLink.Save >> CreateUninstall.vbs
cscript CreateUninstall.vbs >nul
del CreateUninstall.vbs >nul 2>&1

REM 创建桌面快捷方式
set DESKTOP=%USERPROFILE%\Desktop
echo Set oWS = WScript.CreateObject("WScript.Shell") > DesktopShortcut.vbs
echo Set oLink = oWS.CreateShortcut("%DESKTOP%\魔塔传说.lnk") >> DesktopShortcut.vbs
echo oLink.TargetPath = "%INSTALL_DIR%\魔塔传说.exe" >> DesktopShortcut.vbs
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> DesktopShortcut.vbs
echo oLink.Description = "启动魔塔传说游戏" >> DesktopShortcut.vbs
echo oLink.Save >> DesktopShortcut.vbs
cscript DesktopShortcut.vbs >nul
del DesktopShortcut.vbs >nul 2>&1

echo [成功] 快捷方式创建完成

echo.
echo ========================================
echo         安装完成！
echo ========================================
echo.
echo [成功] 魔塔传说已成功安装到:
echo         %INSTALL_DIR%
echo.
echo 安装内容包括:
echo   - 魔塔传说游戏主程序
echo   - 桌面快捷方式
echo   - 开始菜单快捷方式
echo   - 卸载程序
echo.
echo [1] 立即启动游戏
echo [2] 完成安装
echo.
set /p CHOICE=请选择操作 [1-2]: 
if "%CHOICE%"=="1" (
    start "" "%INSTALL_DIR%\魔塔传说.exe"
)
echo.
pause
exit /b 0

:cancel
echo.
echo [信息] 安装已取消
pause
exit /b 0

:menu
echo.
echo [错误] 无效的选择，请重新输入
goto install
