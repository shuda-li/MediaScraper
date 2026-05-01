; ========================================
; MediaScraper NSIS 安装脚本
; ========================================

!define APPNAME "MediaScraper"
!define VERSION "1.0"
!define PUBLISHER "MediaScraper"
!define WEBSITE "https://github.com/mediascraper"

; 设置输出文件名
OutFile "dist\MediaScraper_安装包.exe"

; 请求管理员权限
RequestExecutionLevel user

; 设置默认安装目录
InstallDir "$PROFILE\MediaScraper"

; 设置安装包图标
!define MUI_ICON "media_scraper.ico"
!define MUI_UNICON "media_scraper.ico"

; 包含现代UI插件
!include "MUI2.nsh"

; ========================================
; 安装页面设置
; ========================================
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "使用说明.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; ========================================
; 语言设置（中文）
; ========================================
!insertmacro MUI_LANGUAGE "SimpChinese"

; ========================================
; 安装程序部分
; ========================================
Section "!主程序 (必需)" SecMain
    ; 设置输出路径
    SetOutPath "$INSTDIR"
    
    ; 安装文件
    File "dist\MediaScraper\media_scraper.py"
    File "dist\MediaScraper\media_scraper.ico"
    File "dist\MediaScraper\requirements.txt"
    File "dist\MediaScraper\使用说明.txt"
    File "dist\MediaScraper\启动.bat"
    
    ; 创建快捷方式
    CreateDirectory "$SMPROGRAMS\${APPNAME}"
    CreateShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\启动.bat" "" "$INSTDIR\media_scraper.ico" 0
    CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\启动.bat" "" "$INSTDIR\media_scraper.ico" 0
    
    ; 写入卸载程序
    WriteUninstaller "$INSTDIR\卸载.exe"
    
    ; 写入注册表信息
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME} ${VERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayIcon" "$INSTDIR\media_scraper.ico"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$INSTDIR\卸载.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "${PUBLISHER}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "URLInfoAbout" "${WEBSITE}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "InstallLocation" "$INSTDIR"
SectionEnd

Section "FFmpeg (可选)" SecFFmpeg
    SetOutPath "$INSTDIR"
    File "dist\MediaScraper\ffmpeg.exe"
SectionEnd

Section "首次运行 - 安装依赖" SecFirstRun
    ; 创建桌面快捷方式
    CreateShortCut "$DESKTOP\安装依赖.lnk" "$INSTDIR\安装.bat" "" "$INSTDIR\media_scraper.ico" 0
SectionEnd

; ========================================
; 卸载程序部分
; ========================================
Section "Uninstall"
    ; 删除文件
    Delete "$INSTDIR\media_scraper.py"
    Delete "$INSTDIR\media_scraper.ico"
    Delete "$INSTDIR\requirements.txt"
    Delete "$INSTDIR\使用说明.txt"
    Delete "$INSTDIR\启动.bat"
    Delete "$INSTDIR\卸载.exe"
    Delete "$INSTDIR\ffmpeg.exe"
    
    ; 删除快捷方式
    Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
    Delete "$DESKTOP\${APPNAME}.lnk"
    Delete "$DESKTOP\安装依赖.lnk"
    
    ; 删除程序组
    RMDir "$SMPROGRAMS\${APPNAME}"
    
    ; 删除安装目录
    RMDir "$INSTDIR"
    
    ; 删除注册表
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
SectionEnd

; ========================================
; 函数部分
; ========================================
Function .onInit
    ; 初始化时显示版本信息
    MessageBox MB_ICONINFORMATION|MB_OK "MediaScraper 安装向导$\n版本 ${VERSION}"
FunctionEnd

; 安装完成后询问是否运行
Function .onInstSuccess
    MessageBox MB_YESNO "安装完成！$\n是否现在运行 MediaScraper？" IDYES yes IDNO no
    yes:
        ExecShell "" "$INSTDIR\启动.bat"
    no:
FunctionEnd
