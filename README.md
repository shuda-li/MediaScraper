# MediaScraper - 媒体抓取工具

🚀 **一键下载，即开即用！** 一个基于Python和PyQt5开发的跨平台媒体下载工具，支持从多个视频平台下载视频和音频。

## 🎯 快速开始（推荐方式）

**对于大多数用户，我们强烈推荐直接下载使用"最优版"压缩包：**

### 📦 最优版下载使用

1. **下载最优版**：从 [Releases页面](https://github.com/shuda-li/MediaScraper/releases) 下载 `MediaScraper_最优版.zip`
2. **解压文件**：将压缩包解压到任意目录（建议不要放在系统盘）
3. **直接运行**：双击 `MediaScraper.exe` 即可开始使用

✅ **最优版优势：**
- 🟢 **绿色便携**：无需安装，不写注册表
- ⚡ **开箱即用**：解压即可运行，无需配置环境
- 🔧 **功能完整**：包含所有必要组件和依赖
- 🛡️ **安全可靠**：经过测试验证，稳定运行

## 🎨 功能特性

- **多平台支持**：YouTube、B站、抖音、微博视频等
- **智能下载**：自动识别最佳画质和格式
- **批量下载**：支持多个链接同时下载
- **格式转换**：支持MP4、MP3等多种格式
- **进度显示**：实时显示下载进度和速度
- **历史记录**：自动保存下载历史

## 💻 系统要求

- **操作系统**：Windows 7/8/10/11（64位）
- **运行环境**：无需安装Python或其他依赖
- **磁盘空间**：至少100MB可用空间

## 🔧 高级使用（开发者选项）

如果您是开发者或需要从源代码运行：

### 从源代码运行

```bash
# 1. 克隆项目
git clone https://github.com/shuda-li/MediaScraper.git
cd MediaScraper

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行程序
python media_scraper.py
```

### 构建自定义版本

项目提供了多个构建脚本：
- `build_perfect.py` - 最优版构建（推荐）
- `build_simple.py` - 简化版构建
- `build_complete.py` - 完整功能构建

## 📁 项目结构

```
MediaScraper/
├── MediaScraper_最优版.zip    # 🏆 推荐下载版本
├── media_scraper.py          # 主程序源代码
├── requirements.txt          # Python依赖列表
├── build_*.py               # 各种构建脚本
└── README.md                # 项目说明文档
```

## ❓ 常见问题

**Q: 为什么推荐使用最优版？**  
A: 最优版已经包含了所有必要的运行环境和依赖，用户无需安装任何软件即可使用。

**Q: 运行时报错怎么办？**  
A: 请确保解压到非系统盘目录，并以管理员权限运行程序。

**Q: 支持哪些视频平台？**  
A: 支持YouTube、Bilibili、抖音、微博、快手等主流视频平台。

**Q: 下载速度慢怎么办？**  
A: 程序会自动选择最佳服务器，您也可以尝试更换网络环境。

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## ⚠️ 免责声明

本工具仅供学习和研究使用，请遵守相关法律法规，尊重版权。使用者需对下载内容负责。

---

⭐ **如果这个工具对您有帮助，请给个Star支持一下！**

💡 **遇到问题？** 欢迎在 [Issues](https://github.com/shuda-li/MediaScraper/issues) 页面反馈！
