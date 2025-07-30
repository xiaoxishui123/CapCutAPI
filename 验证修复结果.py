#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证修复后的草稿文件
"""

import zipfile
import json
import os

def verify_fixed_draft():
    """验证修复后的草稿文件"""
    print("🔍 验证修复后的草稿文件")
    print("=" * 50)
    
    zip_path = "fixed_drafts/dfd_cat_1753754237_75267d20_smart_fixed.zip"
    
    if not os.path.exists(zip_path):
        print(f"❌ 文件不存在: {zip_path}")
        return
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            # 检查文件列表
            file_list = zip_file.namelist()
            print(f"📋 文件列表 ({len(file_list)} 个文件):")
            for file in file_list:
                print(f"  - {file}")
            
            # 检查必要文件
            required_files = [
                "draft_info.json",
                "draft_content.json", 
                "draft_meta_info.json"
            ]
            
            print(f"\n✅ 必要文件检查:")
            for req_file in required_files:
                if req_file in file_list:
                    print(f"  ✓ {req_file}")
                else:
                    print(f"  ❌ {req_file} (缺失)")
            
            # 检查媒体文件
            media_files = [f for f in file_list if f.startswith("assets/")]
            print(f"\n🎬 媒体文件检查 ({len(media_files)} 个文件):")
            for media_file in media_files:
                print(f"  ✓ {media_file}")
            
            # 检查音频文件
            audio_files = [f for f in media_files if "audio" in f]
            if audio_files:
                print(f"\n🎵 音频文件 ({len(audio_files)} 个):")
                for audio_file in audio_files:
                    print(f"  ✓ {audio_file}")
            else:
                print(f"\n❌ 没有音频文件")
            
            # 检查视频文件
            video_files = [f for f in media_files if "video" in f]
            if video_files:
                print(f"\n🎬 视频文件 ({len(video_files)} 个):")
                for video_file in video_files:
                    print(f"  ✓ {video_file}")
            else:
                print(f"\n❌ 没有视频文件")
            
            # 检查图片文件
            image_files = [f for f in media_files if "image" in f]
            if image_files:
                print(f"\n🖼️  图片文件 ({len(image_files)} 个):")
                for image_file in image_files:
                    print(f"  ✓ {image_file}")
            else:
                print(f"\n❌ 没有图片文件")
            
            # 验证draft_content.json中的路径
            print(f"\n📝 验证draft_content.json中的路径:")
            try:
                with zip_file.open("draft_content.json") as f:
                    content_data = json.load(f)
                
                materials = content_data.get("materials", {})
                
                # 检查音频路径
                audios = materials.get("audios", [])
                for audio in audios:
                    name = audio.get("name", "")
                    path = audio.get("path", "")
                    if name and path:
                        print(f"  ✓ 音频: {name} -> {path}")
                    else:
                        print(f"  ❌ 音频: {name} (路径为空)")
                
                # 检查视频路径
                videos = materials.get("videos", [])
                for video in videos:
                    name = video.get("material_name", "")
                    path = video.get("path", "")
                    if name and path:
                        print(f"  ✓ 视频: {name} -> {path}")
                    else:
                        print(f"  ❌ 视频: {name} (路径为空)")
                        
            except Exception as e:
                print(f"  ❌ 解析draft_content.json失败: {str(e)}")
            
            print(f"\n🎉 验证完成！")
            print(f"📦 文件大小: {os.path.getsize(zip_path)} bytes")
            
    except Exception as e:
        print(f"❌ 验证失败: {str(e)}")

def main():
    """主函数"""
    verify_fixed_draft()

if __name__ == "__main__":
    main() 