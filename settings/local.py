"""
本地配置模块，用于从本地配置文件中加载配置
"""

import os
import json

# 配置文件路径
CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

# 默认配置
IS_CAPCUT_ENV = False

# 默认域名配置
DRAFT_DOMAIN = "https://www.install-ai-guider.top"

# 默认预览路由
PREVIEW_ROUTER = "/draft/downloader"

# 是否上传草稿文件
IS_UPLOAD_DRAFT = True

# 默认OSS配置（生产环境请通过config.json配置）
OSS_CONFIG = {
    "bucket_name": "",
    "access_key_id": "",
    "access_key_secret": "",
    "endpoint": ""
}

# 默认MP4 OSS配置
MP4_OSS_CONFIG = {
    "bucket_name": "",
    "access_key_id": "",
    "access_key_secret": "",
    "region": "",
    "endpoint": ""
}

# 尝试加载本地配置文件
if os.path.exists(CONFIG_FILE_PATH):
    try:
        with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
            local_config = json.load(f)
            
            # 更新是否是国际版
            if "is_capcut_env" in local_config:
                IS_CAPCUT_ENV = local_config["is_capcut_env"]
                print(f"✅ 配置加载: is_capcut_env = {IS_CAPCUT_ENV}")
            
            # 更新域名配置
            if "draft_domain" in local_config:
                DRAFT_DOMAIN = local_config["draft_domain"]
                print(f"✅ 配置加载: draft_domain = {DRAFT_DOMAIN}")

            # 更新预览路由
            if "preview_router" in local_config:
                PREVIEW_ROUTER = local_config["preview_router"]
                print(f"✅ 配置加载: preview_router = {PREVIEW_ROUTER}")
            
            # 更新是否上传草稿文件
            if "is_upload_draft" in local_config:
                IS_UPLOAD_DRAFT = local_config["is_upload_draft"]
                print(f"✅ 配置加载: is_upload_draft = {IS_UPLOAD_DRAFT}")
                
            # 更新OSS配置
            if "oss_config" in local_config:
                OSS_CONFIG = local_config["oss_config"]
                print(f"✅ 配置加载: OSS配置已更新")
            
            # 更新MP4 OSS配置
            if "mp4_oss_config" in local_config:
                MP4_OSS_CONFIG = local_config["mp4_oss_config"]
                print(f"✅ 配置加载: MP4 OSS配置已更新")

    except json.JSONDecodeError as e:
        print(f"❌ 配置文件JSON格式错误: {e}")
        print("使用默认配置")
    except IOError as e:
        print(f"❌ 配置文件读取失败: {e}")
        print("使用默认配置")
else:
    print(f"⚠️  配置文件不存在: {CONFIG_FILE_PATH}")
    print("使用默认配置")

# 配置验证函数
def validate_config():
    """验证配置的完整性"""
    issues = []
    
    if IS_UPLOAD_DRAFT:
        if not OSS_CONFIG.get("bucket_name"):
            issues.append("OSS bucket_name 未配置")
        if not OSS_CONFIG.get("access_key_id"):
            issues.append("OSS access_key_id 未配置")
        if not OSS_CONFIG.get("access_key_secret"):
            issues.append("OSS access_key_secret 未配置")
        if not OSS_CONFIG.get("endpoint"):
            issues.append("OSS endpoint 未配置")
    
    if issues:
        print("⚠️  配置验证发现问题:")
        for issue in issues:
            print(f"   - {issue}")
        print("请检查 config.json 文件")
    else:
        print("✅ 配置验证通过")
    
    return len(issues) == 0

# 在模块加载时验证配置
if __name__ != "__main__":
    validate_config()