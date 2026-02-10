@echo off
chcp 65001 >nul
title 卸载魔塔传说

echo.
echo ========================================
echo           卸载魔塔传说
echo ========================================
echo.
echo 警告: 此操作将删除魔塔传说的所有文件和相关设置
echo.

set /p CONFIRM=确定要卸载魔塔传说吗？ [Y/N]: 

if /i "%CONFIRM%" neq "Y" (
    echo.
    echo [信息] 卸载已取消
    pause
    exit /b 0
)

echo.
echo [信息] 正在删除快捷方式...

REM 删除桌面快捷方式
del /q /f "%USERPROFILE%\Desktop\魔塔传说.lnk" >nul 2>&1

REM 删除开始菜单快捷方式
set START_MENU=%ProgramData%\Microsoft\Windows\Start Menu\Programs\魔塔传说
rmdir /q /s "%START_MENU%" >nul 2>&1

REM 删除注册表信息
reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Uninstall\魔塔传说" /f >nul 2>&1

echo [信息] 正在删除程序文件...
set INSTALL_DIR=%ProgramFiles%\魔塔传说
if exist "%ProgramFiles(x86)%" (
    set INSTALL_DIR=%ProgramFiles(x86)%\魔塔传说
)
rmdir /q /s "%INSTALL_DIR%" >nul 2>&1

echo.
echo ========================================
echo          卸载完成
echo ========================================
echo.
echo [成功] 魔塔传说已成功卸载
echo.
pause
exit /b 0
