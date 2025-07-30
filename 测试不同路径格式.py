#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试不同的媒体文件路径格式
"""

import json
import zipfile
import os
import shutil

def test_different_path_formats():
    """测试不同的路径格式"""
    print("🎯 测试不同的媒体文件路径格式")
    print("=" * 50)
    
    # 读取原始修复文件
    original_zip = "fixed_drafts/dfd_cat_1753754237_75267d20_smart_fixed.zip"
    
    if not os.path.exists(original_zip):
        print(f"❌ 原始文件不存在: {original_zip}")
        return
    
    # 解压原始文件
    with zipfile.ZipFile(original_zip, 'r') as zip_file:
        zip_file.extractall("test_paths")
    
    # 读取draft_content.json
    content_path = "test_paths/draft_content.json"
    with open(content_path, 'r', encoding='utf-8') as f:
        content_data = json.load(f)
    
    # 定义不同的路径格式
    path_formats = [
        "assets/audio/audio_9869932344c1c9d3.mp3",
        "./assets/audio/audio_9869932344c1c9d3.mp3", 
        "../assets/audio/audio_9869932344c1c9d3.mp3",
        "audio_9869932344c1c9d3.mp3",
        "audio/audio_9869932344c1c9d3.mp3",
        "assets/audio_9869932344c1c9d3.mp3",
        "audio/audio_9869932344c1c9d3.mp3",
        "audio_9869932344c1c9d3.mp3"
    ]
    
    # 为每种格式创建测试文件
    for i, path_format in enumerate(path_formats):
        print(f"\n🔧 测试路径格式 {i+1}: {path_format}")
        
        # 复制内容数据
        test_content = json.loads(json.dumps(content_data))
        
        # 更新音频路径
        materials = test_content.get("materials", {})
        audios = materials.get("audios", [])
        for audio in audios:
            if audio.get("name") == "audio_9869932344c1c9d3.mp3":
                audio["path"] = path_format
                print(f"  ✓ 更新音频路径: {path_format}")
        
        # 更新视频路径
        videos = materials.get("videos", [])
        for video in videos:
            if video.get("material_name") == "image_81fa0547ac2dcba5.png":
                # 对应的视频路径格式
                video_path_format = path_format.replace("audio", "video").replace("audio_9869932344c1c9d3.mp3", "image_81fa0547ac2dcba5.png")
                video["path"] = video_path_format
                print(f"  ✓ 更新视频路径: {video_path_format}")
        
        # 保存修改后的内容
        test_content_path = f"test_paths/draft_content_{i+1}.json"
        with open(test_content_path, 'w', encoding='utf-8') as f:
            json.dump(test_content, f, ensure_ascii=False, indent=4)
        
        # 创建测试ZIP文件
        test_zip_path = f"fixed_drafts/dfd_cat_1753754237_75267d20_path_test_{i+1}.zip"
        
        with zipfile.ZipFile(test_zip_path, 'w') as zip_file:
            # 添加所有文件
            for root, dirs, files in os.walk("test_paths"):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, "test_paths")
                    
                    # 如果是draft_content.json，使用测试版本
                    if file == "draft_content.json":
                        continue
                    elif file.startswith("draft_content_"):
                        arc_name = "draft_content.json"
                    
                    zip_file.write(file_path, arc_name)
        
        print(f"  📦 创建测试文件: {test_zip_path}")
        print(f"  📏 文件大小: {os.path.getsize(test_zip_path)} bytes")
    
    # 清理临时文件
    shutil.rmtree("test_paths")
    
    print(f"\n🎉 测试完成！")
    print(f"📋 生成了 {len(path_formats)} 个不同路径格式的测试文件:")
    for i in range(len(path_formats)):
        test_file = f"fixed_drafts/dfd_cat_1753754237_75267d20_path_test_{i+1}.zip"
        if os.path.exists(test_file):
            print(f"  {i+1}. {test_file}")
    
    print(f"\n💡 请逐个测试这些文件，看哪个能在剪映中正常显示媒体文件")

def main():
    """主函数"""
    test_different_path_formats()

if __name__ == "__main__":
    main() 