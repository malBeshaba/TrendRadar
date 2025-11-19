#!/usr/bin/env python3
# coding=utf-8
"""
模板系统测试脚本
用于验证Jinja2模板渲染是否正常
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from main import get_template_manager, get_beijing_time


def test_template_rendering():
    """测试模板渲染功能"""
    print("=" * 60)
    print("开始测试模板系统...")
    print("=" * 60)
    
    try:
        # 初始化模板管理器
        template_manager = get_template_manager()
        
        if not template_manager.is_available():
            print("❌ 模板系统不可用")
            return False
        
        print(f"✅ 模板系统初始化成功: {template_manager.theme} 主题")
        print()
        
        # 准备测试数据
        test_context = {
            'is_daily_summary': False,
            'mode': 'daily',
            'total_titles': 100,
            'hot_news_count': 25,
            'generation_time': get_beijing_time().strftime("%m-%d %H:%M"),
            'stats': [
                {
                    'word': 'AI技术',
                    'count': 12,
                    'titles': [
                        {
                            'source_name': 'GitHub',
                            'title': 'OpenAI发布最新模型GPT-5',
                            'ranks': [1, 2],
                            'rank_threshold': 10,
                            'time_display': '11-19 14:30',
                            'count': 3,
                            'url': 'https://github.com',
                            'mobile_url': 'https://github.com',
                            'is_new': True
                        },
                        {
                            'source_name': '知乎',
                            'title': 'AI如何改变我们的生活？',
                            'ranks': [5],
                            'rank_threshold': 10,
                            'time_display': '11-19 15:00',
                            'count': 1,
                            'url': 'https://zhihu.com',
                            'is_new': False
                        }
                    ]
                },
                {
                    'word': '科技创新',
                    'count': 8,
                    'titles': [
                        {
                            'source_name': '微博',
                            'title': '中国科技企业全球竞争力提升',
                            'ranks': [3, 4, 6],
                            'rank_threshold': 10,
                            'time_display': '11-19 13:20',
                            'count': 2,
                            'url': 'https://weibo.com',
                            'is_new': False
                        }
                    ]
                }
            ],
            'failed_ids': ['platform-error-1'],
            'new_titles': [
                {
                    'source_name': 'bilibili',
                    'titles': [
                        {
                            'title': '新增热点：最新科技发布会',
                            'ranks': [2],
                            'rank_threshold': 10,
                            'url': 'https://bilibili.com',
                        }
                    ]
                }
            ],
            'total_new_count': 1,
            'update_info': None,
            'custom_css': ''
        }
        
        print("📝 渲染测试报告...")
        html = template_manager.render('report.html', test_context)
        
        # 验证HTML内容
        if not html:
            print("❌ 渲染结果为空")
            return False
        
        if len(html) < 1000:
            print(f"⚠️  渲染结果过短: {len(html)} 字符")
            return False
        
        # 检查关键内容
        checks = [
            ('<!DOCTYPE html>', 'HTML文档类型声明'),
            ('热点新闻分析', '页面标题'),
            ('AI技术', '测试词组'),
            ('OpenAI发布最新模型GPT-5', '测试新闻标题'),
            ('saveAsImage', 'JavaScript函数'),
            ('container', 'CSS类名'),
        ]
        
        print("\n检查关键内容:")
        all_passed = True
        for keyword, description in checks:
            if keyword in html:
                print(f"  ✅ {description}: 通过")
            else:
                print(f"  ❌ {description}: 失败 (未找到: {keyword})")
                all_passed = False
        
        if not all_passed:
            print("\n⚠️  部分检查未通过")
            return False
        
        print(f"\n✅ 模板渲染成功！")
        print(f"   - HTML长度: {len(html)} 字符")
        print(f"   - 主题: {template_manager.theme}")
        print(f"   - 包含统计词组: {len(test_context['stats'])} 个")
        print(f"   - 包含新闻项: {sum(len(s['titles']) for s in test_context['stats'])} 条")
        
        # 保存测试文件
        test_output = Path("test_template_output.html")
        test_output.write_text(html, encoding='utf-8')
        print(f"\n💾 测试报告已保存到: {test_output}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🧪 TrendRadar 模板系统测试")
    print()
    
    success = test_template_rendering()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 所有测试通过！模板系统工作正常。")
        print("=" * 60)
        sys.exit(0)
    else:
        print("❌ 测试失败！请检查模板配置。")
        print("=" * 60)
        sys.exit(1)