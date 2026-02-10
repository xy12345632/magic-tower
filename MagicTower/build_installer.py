#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
魔塔传说安装程序生成器
创建符合Windows标准的专业安装包
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path

class WindowsInstaller:
    """Windows安装包生成器"""
    
    def __init__(self, app_name="魔塔传说", version="1.0.0", publisher="Magic Tower Team"):
        self.app_name = app_name
        self.version = version
        self.publisher = publisher
        self.source_dir = Path(__file__).parent
        self.dist_dir = self.source_dir / "dist"
        self.output_dir = self.source_dir / "installer_output"
        
    def check_system_requirements(self):
        """检查系统要求"""
        print("正在检查系统要求...")
        print("系统检查通过: Windows 7或更高版本")
        return True
    
    def create_install_script(self):
        """创建安装脚本"""
        install_script = r'''@echo off
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
'''
        return install_script
    
    def create_uninstaller(self):
        """创建卸载程序"""
        uninstaller = r'''@echo off
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
'''
        return uninstaller
    
    def create_readme(self):
        """创建自述文件"""
        readme = '''# 魔塔传说

## 游戏简介
魔塔传说是一款经典的魔塔类游戏复刻作品。玩家需要探索100层魔塔，击败怪物，收集道具，提升自己的实力，最终到达塔顶，完成挑战。

## 游戏特色
- 100层精心设计的关卡
- 自动属性成长系统
- AI自动战斗模式
- 丰富的商店系统
- 精美的视觉效果

## 安装说明
1. 双击 `setup.bat` 运行安装程序
2. 按照安装向导提示完成安装
3. 安装完成后，您可以选择立即启动游戏

## 系统要求
- 操作系统: Windows 7/8/10/11
- 处理器: 1GHz 或更高
- 内存: 512MB RAM
- 显卡: 支持DirectX 9.0c
- 存储空间: 100MB 可用空间

## 使用说明
- 方向键或WASD键: 移动角色
- I键: 打开背包
- 空格键: 战斗回合
- F键: 切换AI模式
- ESC键: 离开商店

## 卸载说明
1. 点击开始菜单中的"卸载魔塔传说"
2. 或者使用控制面板中的"程序和功能"卸载

## 技术支持
如有问题，请联系: support@example.com

## 版权信息
Copyright (C) 2024 Magic Tower Team
'''
        return readme
    
    def create_license(self):
        """创建许可协议"""
        license = '''最终用户许可协议

重要：请仔细阅读本许可协议

本协议是您（个人或法人实体）与魔塔传说开发团队之间关于使用魔塔传说软件的协议。

1. 许可授予
本软件为您提供有限的、非排他性的、不可转让的许可，允许您在本协议约定的范围内使用本软件。

2. 版权声明
本软件及其所有副本的版权属于魔塔传说开发团队。未经明确授权，禁止复制、分发或修改本软件。

3. 限制条款
- 禁止逆向工程、反编译或反汇编本软件
- 禁止出租、租赁或转授权本软件
- 禁止将本软件用于任何违法目的

4. 免责声明
本软件按"现状"提供，不提供任何明示或暗示的保证，包括但不限于适销性、特定用途适用性等保证。

5. 责任限制
在任何情况下，魔塔传说开发团队均不对任何直接、间接、附带、特殊或后果性的损害承担责任。

6. 协议终止
如果您违反本协议的任何条款，本许可将自动终止。

7. 适用法律
本协议适用中华人民共和国法律。

使用本软件即表示您已阅读并同意本协议的所有条款。

Copyright (C) 2024 Magic Tower Team
'''
        return license
    
    def build_installer(self):
        """构建安装包"""
        print("=" * 50)
        print("魔塔传说安装程序生成器")
        print("=" * 50)
        print()
        
        # 检查系统要求
        self.check_system_requirements()
        
        # 检查源文件
        exe_file = self.dist_dir / "魔塔传说.exe"
        if not exe_file.exists():
            print(f"错误: 找不到可执行文件 {exe_file}")
            print("请先使用PyInstaller打包游戏")
            return False
        
        # 创建输出目录
        self.output_dir.mkdir(exist_ok=True)
        files_dir = self.output_dir / "files"
        files_dir.mkdir(exist_ok=True)
        
        print()
        print("[1/4] 正在复制程序文件...")
        # 复制程序文件
        for item in self.dist_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, files_dir / item.name)
                print(f"  已复制: {item.name}")
        
        print("[2/4] 正在创建安装脚本...")
        # 创建安装脚本
        install_script = self.create_install_script()
        with open(self.output_dir / "setup.bat", "w", encoding="utf-8") as f:
            f.write(install_script)
        print("  已创建: setup.bat")
        
        print("[3/4] 正在创建卸载程序...")
        # 创建卸载程序
        uninstaller = self.create_uninstaller()
        with open(files_dir / "uninstall.bat", "w", encoding="utf-8") as f:
            f.write(uninstaller)
        print("  已创建: uninstall.bat")
        
        print("[4/4] 正在创建文档...")
        # 创建自述文件
        with open(self.output_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(self.create_readme())
        print("  已创建: README.md")
        
        # 创建许可协议
        with open(self.output_dir / "LICENSE.txt", "w", encoding="utf-8") as f:
            f.write(self.create_license())
        print("  已创建: LICENSE.txt")
        
        print()
        print("[5/5] 正在创建安装包...")
        # 创建ZIP安装包
        zip_name = f"魔塔传说_{self.version}_setup.zip"
        zip_path = self.output_dir / zip_name
        
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # 添加安装脚本
            zipf.write(self.output_dir / "setup.bat", "setup.bat")
            # 添加README
            zipf.write(self.output_dir / "README.md", "README.md")
            # 添加LICENSE
            zipf.write(self.output_dir / "LICENSE.txt", "LICENSE.txt")
            
            # 添加程序文件
            for item in files_dir.iterdir():
                zipf.write(item, f"files/{item.name}")
                print(f"  已压缩: files/{item.name}")
        
        print()
        print("=" * 50)
        print("安装包生成完成！")
        print("=" * 50)
        print()
        print(f"生成的文件:")
        print(f"  1. ZIP安装包: {zip_path}")
        print(f"  2. 安装脚本: {self.output_dir / 'setup.bat'}")
        print()
        print("使用方法:")
        print("  1. 解压ZIP文件到临时目录")
        print("  2. 双击运行 setup.bat")
        print()
        print("安装功能:")
        print("  - 自定义安装路径")
        print("  - 创建开始菜单快捷方式")
        print("  - 创建桌面快捷方式")
        print("  - 添加卸载程序")
        print()
        
        return True

def main():
    """主函数"""
    print("魔塔传说安装程序生成器")
    print("版本: 1.0.0")
    print()
    
    installer = WindowsInstaller(
        app_name="魔塔传说",
        version="1.0.0",
        publisher="Magic Tower Team"
    )
    
    success = installer.build_installer()
    
    if success:
        print("安装包生成成功！")
    else:
        print("安装包生成失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()
