# CapCutAPI

Open source CapCut API tool.

[中文说明](https://github.com/sun-guannan/CapCutAPI/blob/main/README-zh.md)

## 项目概述

CapCutAPI 是一个基于 Python 的开源 CapCut 处理工具，提供了完整的草稿文件管理、素材处理、特效应用和 API 服务功能。该项目支持跨平台操作，集成了多种 AI 服务和云存储功能。

## 核心功能

### 主要功能模块

- **草稿文件管理**: 创建、读取、修改和保存 CapCut 草稿文件
- **素材处理**: 支持添加和编辑各种素材，如视频、音频、图片、文本、贴纸等
- **特效应用**: 支持添加多种特效，如转场、滤镜、蒙版、动画等
- **API 服务**: 提供 HTTP API 接口，支持远程调用和自动化处理
- **AI 集成**: 集成多种 AI 服务，支持智能生成字幕、文本和图片
- **OSS 云存储**: 集成阿里云 OSS，用于草稿文件存储和分享
- **网络优化**: 智能下载，支持 ffmpeg、重试机制和进度监控

### 主要 API 接口

- `/create_draft`: 创建草稿
- `/add_video`: 向草稿添加视频素材
- `/add_audio`: 向草稿添加音频素材
- `/add_image`: 向草稿添加图片素材
- `/add_text`: 向草稿添加文本素材
- `/add_subtitle`: 向草稿添加字幕
- `/add_effect`: 向素材添加特效
- `/add_sticker`: 向草稿添加贴纸
- `/save_draft`: 保存草稿文件

## 项目架构

### 核心模块

1. **草稿创建模块** (`create_draft.py`)
   - 创建新的 CapCut 草稿文件
   - 管理草稿缓存系统
   - 生成唯一的草稿 ID

2. **视频轨道添加模块** (`add_video_track.py`)
   - 向草稿添加视频素材
   - 支持视频剪辑、缩放、位置调整
   - 支持转场效果和蒙版效果
   - 支持播放速度调整

3. **音频轨道添加模块** (`add_audio_track.py`)
   - 向草稿添加音频素材
   - 支持音频剪辑、音量调整
   - 支持音频特效（变声、场景音效等）
   - 支持播放速度调整

4. **文本添加模块** (`add_text_impl.py`)
   - 向草稿添加文本内容
   - 支持字体、颜色、大小设置
   - 支持边框和背景效果
   - 支持文本动画效果

5. **草稿保存模块** (`save_draft_impl.py`)
   - 保存草稿文件到本地或云端
   - 下载所有媒体文件
   - 更新媒体文件元数据
   - 压缩草稿文件
   - 上传到 OSS 云存储

6. **文件下载模块** (`downloader.py`)
   - 支持视频、音频、图片文件下载
   - 智能重试机制
   - 进度监控
   - 格式转换

### 缓存系统

- **草稿缓存** (`draft_cache.py`): LRU 缓存管理草稿对象
- **任务缓存** (`save_task_cache.py`): 管理保存任务状态和进度跟踪

### 工具模块

- **工具函数** (`util.py`): 颜色转换、路径检测、文件压缩等
- **OSS 集成** (`oss.py`): 阿里云 OSS 云存储集成

## 配置说明

### 配置文件

项目支持通过配置文件进行自定义设置。要使用配置文件：

1. 复制 `config.json.example` 到 `config.json`
2. 根据需要修改配置项

```bash
cp config.json.example config.json
```

### 环境配置

#### ffmpeg

本项目依赖 ffmpeg。您需要确保系统上安装了 ffmpeg 并添加到系统的环境变量中。

#### Python 环境

本项目需要 Python 版本 3.8.20。请确保系统上安装了正确版本的 Python。

#### 安装依赖

安装项目所需的依赖包：

```bash
pip install -r requirements.txt
```

### 运行服务器

完成配置和环境设置后，执行以下命令启动服务器：

```bash
python capcut_server.py
```

服务器启动后，您可以通过 API 接口访问相关功能。

## 使用示例

### 添加视频

```python
import requests

response = requests.post("http://localhost:9000/add_video", json={
    "video_url": "http://example.com/video.mp4",
    "start": 0,
    "end": 10,
    "width": 1080,
    "height": 1920
})

print(response.json())
```

### 添加文本

```python
import requests

response = requests.post("http://localhost:9000/add_text", json={
    "text": "Hello, World!",
    "start": 0,
    "end": 3,
    "font": "Source Han Sans",
    "font_color": "#FF0000",
    "font_size": 30.0
})

print(response.json())
```

### 保存草稿

```python
import requests

response = requests.post("http://localhost:9000/save_draft", json={
    "draft_id": "123456",
    "draft_folder": "your capcut draft folder"
})

print(response.json())
```

### 将草稿复制到 CapCut 草稿路径

调用 `save_draft` 会在服务器当前目录下生成一个以 `dfd_` 开头的文件夹。将此文件夹复制到 CapCut 草稿目录，您就能看到生成的草稿。

### 更多示例

请参考项目中的 `example.py` 文件，其中包含更多使用示例，如添加音频和特效。

## 项目特性

- **跨平台支持**: 支持 CapCut 中国版和 CapCut 国际版
- **自动化处理**: 支持批量处理和自动化工作流
- **丰富的 API**: 提供全面的 API 接口，便于集成到其他系统
- **灵活配置**: 通过配置文件实现灵活的功能定制
- **AI 增强**: 集成多种 AI 服务，提高视频制作效率
- **云存储**: 集成 OSS 云存储，用于草稿文件管理
- **网络智能**: 使用 ffmpeg 进行智能文件处理和格式转换

## 网络分析

关于详细的网络使用分析，包括视频生成、草稿管理和 OSS 上传功能，请参考 [项目网络分析报告.md](./项目网络分析报告.md)。

项目使用：
- **HTTP/HTTPS**: 用于素材文件下载
- **阿里云 OSS**: 用于草稿文件存储和分享
- **ffmpeg**: 用于智能文件处理和格式转换
- **Flask API**: 用于 HTTP API 服务

## 常见问题解决方案

### 草稿媒体文件丢失问题

**问题描述**: 通过 CapCutAPI 创建的草稿在剪映中打开时，显示"素材下载失败"或"媒体丢失"的错误。

**问题原因**:
1. 草稿文件结构不正确，缺少草稿文件夹
2. 媒体文件下载失败或路径引用错误
3. 平台信息不匹配（Mac vs Windows）

**解决方案**:

#### 1. 使用智能修复脚本 (推荐)

我们提供了多种修复脚本，其中**智能修复**是最推荐的方法：

```bash
# 智能修复（推荐）
python3 smart_draft_fixer.py

# 直接修改
python3 direct_draft_fixer.py

# 传统修复
python3 simple_draft_fixer.py

# 服务器端修复
python3 server_side_draft_fixer.py
```

**修复方法对比**:

| 修复方法 | 处理时间 | 资源消耗 | 推荐度 | 适用场景 |
|----------|----------|----------|--------|----------|
| 智能修复 | 最短 | 最低 | ⭐⭐⭐⭐⭐ | 轻微问题 |
| 直接修改 | 中等 | 中等 | ⭐⭐⭐⭐ | 中等问题 |
| 传统修复 | 最长 | 最高 | ⭐⭐⭐ | 严重问题 |
| 服务器端 | 最快 | 最低 | ⭐⭐⭐⭐ | 服务器环境 |

#### 2. 使用改进的草稿创建工具

```bash
# 运行改进的草稿创建工具
python3 improve_draft_creation.py
```

#### 3. 手动修复步骤

如果自动修复失败，可以手动执行以下步骤：

1. **下载草稿文件**
   ```bash
   curl "http://your-draft-url" -o draft.zip
   ```

2. **解压并检查结构**
   ```bash
   unzip draft.zip
   ls -la
   ```

3. **创建正确的草稿文件夹结构**
   ```bash
   mkdir dfd_your_draft_id
   mv draft_info.json draft_content.json assets/ dfd_your_draft_id/
   ```

4. **修复平台信息**
   - 编辑 `draft_content.json` 和 `draft_info.json`
   - 将平台信息改为 Windows: `"os": "windows"`

5. **重新打包**
   ```bash
   zip -r fixed_draft.zip dfd_your_draft_id/
   ```

#### 4. 预防措施

为了避免这个问题，建议：

1. **检查网络连接**: 确保服务器能够正常下载媒体文件
2. **验证文件权限**: 确保有足够的权限创建和修改文件
3. **使用正确的模板**: 确保使用正确的草稿模板文件
4. **监控日志**: 定期检查服务器日志中的错误信息

### 测试用例

我们提供了完整的测试用例来验证功能：

- **Web 测试界面**: http://8.148.70.18:9000/comprehensive-test
- **API 测试**: 使用 `comprehensive_test.html` 进行功能测试
- **草稿修复**: 使用 `simple_draft_fixer.py` 修复现有草稿

### 相关文档

- [剪映草稿识别问题解决方案.md](./剪映草稿识别问题解决方案.md)
- [剪映草稿 OSS 模式草稿文件修复说明.md](./剪映草稿OSS模式草稿文件修复说明.md)
- [测试用例说明.md](./测试用例说明.md)
- [智能修复使用指南.md](./智能修复使用指南.md)
- [草稿修复方法对比.md](./草稿修复方法对比.md)
- [草稿媒体文件问题解决方案总结.md](./草稿媒体文件问题解决方案总结.md)
- [项目结构及功能逻辑分析.md](./项目结构及功能逻辑分析.md)

## 技术支持

如果遇到问题，请：

1. 查看相关文档
2. 运行测试用例验证功能
3. 检查服务器日志
4. 使用修复工具解决问题
5. 提交 Issue 描述具体问题

## 项目结构

```
CapCutAPI/
├── capcut_server.py          # 主服务器文件，提供 HTTP API 接口
├── create_draft.py           # 草稿创建核心模块
├── add_video_track.py        # 视频轨道添加模块
├── add_audio_track.py        # 音频轨道添加模块
├── add_text_impl.py          # 文本添加实现模块
├── add_subtitle_impl.py      # 字幕添加实现模块
├── add_image_impl.py         # 图片添加实现模块
├── add_effect_impl.py        # 特效添加实现模块
├── add_sticker_impl.py       # 贴纸添加实现模块
├── save_draft_impl.py        # 草稿保存实现模块
├── downloader.py             # 文件下载模块
├── draft_cache.py            # 草稿缓存管理
├── save_task_cache.py        # 任务缓存管理
├── util.py                   # 工具函数模块
├── oss.py                    # 阿里云 OSS 集成
├── config.json.example       # 配置文件示例
├── requirements.txt          # 依赖包列表
└── pyJianYingDraft/         # 剪映草稿处理核心库
```

## 工作流程

### 创建草稿流程
1. 调用 `/create_draft` API
2. 生成唯一草稿 ID
3. 创建草稿脚本对象
4. 存储到缓存
5. 返回草稿 ID 和 URL

### 添加素材流程
1. 调用相应的添加 API（如 `/add_video`）
2. 获取或创建草稿对象
3. 添加相应的轨道
4. 下载媒体文件
5. 创建素材对象
6. 设置素材参数
7. 添加到轨道
8. 返回更新后的草稿信息

### 保存草稿流程
1. 调用 `/save_draft` API
2. 创建后台任务
3. 复制模板文件
4. 更新媒体文件元数据
5. 并发下载所有媒体文件
6. 保存草稿信息
7. 修复平台信息
8. 压缩草稿文件
9. 上传到 OSS（可选）
10. 返回草稿下载 URL

## 技术特点

- **并发处理**: 使用 ThreadPoolExecutor 进行并发下载
- **缓存优化**: LRU 缓存策略，自动清理机制
- **错误处理**: 智能重试机制，指数退避策略
- **跨平台支持**: 支持 Windows 和 Mac 路径
- **网络优化**: 智能下载策略，进度监控# CapCutAPI2
