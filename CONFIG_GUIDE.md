# 配置使用指南

## 配置文件结构

项目使用 `config.json` 作为主要配置文件，`settings/local.py` 作为配置加载器。

### config.json 配置项

```json
{
  "is_capcut_env": false,
  "draft_domain": "https://www.install-ai-guider.top",
  "preview_router": "/draft/downloader",
  "is_upload_draft": true,
  "oss_config": {
    "bucket_name": "your-bucket-name",
    "access_key_id": "your-access-key-id",
    "access_key_secret": "your-access-key-secret",
    "endpoint": "https://your-endpoint.aliyuncs.com"
  },
  "mp4_oss_config": {
    "bucket_name": "",
    "access_key_id": "",
    "access_key_secret": "",
    "region": "",
    "endpoint": ""
  }
}
```

### 配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `is_capcut_env` | boolean | false | 是否使用CapCut国际版模式（false=剪映模式） |
| `draft_domain` | string | "https://www.install-ai-guider.top" | 草稿下载域名 |
| `preview_router` | string | "/draft/downloader" | 预览路由 |
| `is_upload_draft` | boolean | true | 是否上传草稿到OSS |
| `oss_config` | object | - | OSS存储配置 |
| `mp4_oss_config` | object | - | MP4文件OSS配置 |

## 配置加载流程

1. **默认配置** - `settings/local.py` 中定义默认值
2. **配置文件加载** - 从 `config.json` 读取配置
3. **配置验证** - 验证配置的完整性
4. **配置应用** - 应用到整个系统

## 使用方式

### 在代码中导入配置

```python
# 方式1：直接导入具体配置
from settings.local import IS_CAPCUT_ENV, OSS_CONFIG

# 方式2：通过settings包导入
from settings import IS_CAPCUT_ENV, IS_UPLOAD_DRAFT
```

### 配置验证

系统会在启动时自动验证配置：

```bash
python3.9 -c "from settings.local import *"
```

输出示例：
```
✅ 配置加载: is_capcut_env = False
✅ 配置加载: is_upload_draft = True
✅ 配置验证通过
```

## 环境模式

### 剪映模式 (is_capcut_env = false)
- 生成剪映格式的草稿文件
- 使用 `template_jianying` 模板
- 平台信息：`app_source: "lv"`

### CapCut国际版模式 (is_capcut_env = true)
- 生成CapCut国际版格式的草稿文件
- 使用 `template` 模板
- 平台信息：`app_source: "cc"`

## 故障排除

### 配置文件不存在
```
⚠️  配置文件不存在: /path/to/config.json
使用默认配置
```

### JSON格式错误
```
❌ 配置文件JSON格式错误: Expecting ',' delimiter
使用默认配置
```

### 配置验证失败
```
⚠️  配置验证发现问题:
   - OSS bucket_name 未配置
   - OSS access_key_id 未配置
请检查 config.json 文件
```

## 最佳实践

1. **生产环境** - 始终使用 `config.json` 配置
2. **开发环境** - 可以修改 `settings/local.py` 中的默认值
3. **敏感信息** - 不要在代码中硬编码敏感信息
4. **配置验证** - 启动时检查配置完整性
5. **版本控制** - 将 `config.json.example` 加入版本控制，但不要包含实际的 `config.json` 