# CapCutAPI 完整文档

---

## 1. 项目简介与部署信息

CapCutAPI 是一个基于 Python3.9 的剪映/CapCut 自动化 API 服务，支持通过 HTTP API 实现视频草稿的自动化创建、编辑、保存和下载，兼容剪映 Windows 客户端。

- **部署位置**：/home/CapCutAPI
- **服务地址**：http://8.148.70.18:9000
- **Python 版本**：3.9.7
- **主要文件**：capcut_server.py、save_draft_impl.py、config.json

### 服务器管理
- 启动：`nohup python3.9 capcut_server.py > capcut_server.log 2>&1 &`
- 停止：`pkill -f "python3.9 capcut_server.py"`
- 查看日志：`tail -f capcut_server.log`

---

## 2. 配置与模式切换说明

### 2.1 配置文件 config.json 关键字段
```json
{
  "is_capcut_env": false,           // 剪映模式(false) or CapCut国际版(true)
  "draft_domain": "https://zdaigfpt.oss-cn-wuhan-lr.aliyuncs.com", // OSS模式下为bucket域名，本地模式为服务器域名或IP
  "preview_router": "/draft/downloader",
  "is_upload_draft": true,          // true=OSS上传，false=本地下载
  "oss_config": { ... }
}
```

### 2.2 模式切换
- **OSS上传模式**：`is_upload_draft: true`，草稿压缩后上传OSS，返回OSS下载链接。
- **本地下载模式**：`is_upload_draft: false`，草稿压缩后保存在服务器，返回本地下载链接。
- 切换后需重启服务。

---

## 3. 常用API与使用指南

### 3.1 API端点示例
- 创建草稿：`POST /create_draft`
- 添加文本：`POST /add_text`
- 添加图片：`POST /add_image`
- 添加音频：`POST /add_audio`
- 添加视频：`POST /add_video`
- 保存草稿：`POST /save_draft`
- 下载草稿：`GET /draft/downloader?draft_id=xxx`

### 3.2 使用示例
```bash
# 创建草稿
curl -X POST http://8.148.70.18:9000/create_draft -H "Content-Type: application/json" -d '{"draft_name":"我的草稿"}'

# 添加文本
curl -X POST http://8.148.70.18:9000/add_text -H "Content-Type: application/json" -d '{"draft_id":"your_draft_id","text":"Hello!","start":0,"end":3}'

# 保存草稿
curl -X POST http://8.148.70.18:9000/save_draft -H "Content-Type: application/json" -d '{"draft_id":"your_draft_id","draft_folder":"/tmp/my_capcut_project"}'
```

### 3.3 Python自动化示例
```python
import requests
BASE_URL = "http://8.148.70.18:9000"
# 创建草稿、添加内容、保存草稿，详见“使用指南.md”
```

---

## 4. 测试用例与验证方法

- 推荐访问 http://8.148.70.18:9000/comprehensive-test 进行全流程测试。
- 支持单项测试、批量测试、参数自定义。
- 主要测试点：草稿创建、文本/图片/音频/视频添加、草稿保存与下载、草稿在剪映中的识别。

---

## 5. 剪映草稿识别问题解决方案

### 5.1 常见问题
- 下载URL被拦截（域名未直连服务器）
- 草稿文件结构不完整（缺少 draft_content.json）
- 平台信息不匹配（Mac/CapCut/国际版信息）
- 草稿内容为空

### 5.2 解决方法
- 下载URL使用服务器IP或OSS直链，避免CDN拦截。
- 草稿文件夹必须包含 draft_content.json、draft_info.json、draft_meta_info.json 等关键文件。
- 平台信息需动态修正为 Windows 剪映格式（os: windows, os_version: 10.0.19045, app_source: lv）。
- 草稿内容需包含实际文本/图片/音频/视频等素材。

### 5.3 验证命令
```bash
# 检查草稿结构
unzip -l ./tmp/zip/your_draft_id.zip
# 检查平台信息
unzip -p ./tmp/zip/your_draft_id.zip draft_content.json | python3.9 -c "import json, sys; data=json.load(sys.stdin); print(data['platform'])"
```

---

## 6. 日常维护与故障排查

### 6.1 清理旧文件
```bash
find ./tmp/zip -name "*.zip" -mtime +7 -delete
find . -name "dfd_cat_*" -type d -mtime +7 -exec rm -rf {} \;
```

### 6.2 监控与备份
- 检查磁盘空间：`df -h`
- 备份配置文件：`cp config.json config.json.backup.$(date +%Y%m%d)`
- 备份重要草稿：`cp ./tmp/zip/important_draft.zip ./backup/$(date +%Y%m%d)/`

### 6.3 故障排查
- 服务器无法启动：检查 capcut_server.log、端口占用
- 下载失败：检查 zip 文件是否存在，测试下载路由
- 配置问题：`python3.9 -c "from settings.local import *; print(f'is_upload_draft: {IS_UPLOAD_DRAFT}')"`

---

## 7. 其他说明

- 支持字体列表详见服务器日志或API返回
- 详细API参数和进阶用法请参考 example.py、test_api.py
- 如遇疑难问题，优先检查日志和草稿文件结构

---

> 文档整理时间：2025-07-15
> 
> 如需补充或定制文档内容，请随时联系维护者。
