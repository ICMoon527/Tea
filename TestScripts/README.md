# 测试脚本说明文档

## 概述
本目录包含茶叶进销存管理系统的各种测试脚本，用于验证系统功能的正确性。

## 测试脚本分类

### 1. 功能验证类
- `test_discount_feature.py` - 验证折扣销售功能
- `test_category_statistics.py` - 验证茶类统计功能
- `verify_tea_statistics.py` - 验证茶叶统计功能
- `test_enhanced_statistics.py` - 验证增强统计功能
- `test_fixed_profit_analysis.py` - 验证修复后的盈利分析功能
- `test_fixed_query_commodities.py` - 验证修复后的商品查询功能
- `verify_fixed_statistics.py` - 验证修复后的统计功能

### 2. 数据验证类
- `check_sales_data.py` - 检查销售数据
- `check_commodity_structure.py` - 检查商品数据结构
- `check_cost_calculation.py` - 检查成本计算
- `detailed_commodity_check.py` - 详细商品检查
- `verify_removed_inventory_warning.py` - 验证移除的库存警告功能

### 3. 综合验证类
- `comprehensive_verification.py` - 综合验证
- `final_validation.py` - 最终验证
- `final_verification.py` - 最终验证
- `test_final_verification.py` - 最终验证
- `comprehensive_statistics_test.py` - 综合统计测试

### 4. 特定功能测试类
- `simulate_sale_process.py` - 模拟销售流程
- `test_improvements.py` - 测试系统改进
- `test_numbering_consistency.py` - 测试编号一致性
- `demonstrate_features.py` - 演示功能特性
- `final_discount_verification.py` - 最终折扣验证

### 5. 调试类
- `debug_sales_save.py` - 调试销售保存问题
- `check_cost_calculation.py` - 检查成本计算

## 使用说明
所有测试脚本都应该在项目的根目录下运行，使用如下命令：
```bash
python -m TestScripts.script_name
```

或者在TestScripts目录下运行：
```bash
python script_name.py
```

## 依赖关系
所有测试脚本都依赖于主项目文件，确保在运行测试前：
1. 项目根目录已添加到Python路径
2. 所有依赖库已安装（pandas, openpyxl, prettytable）
3. Excel数据文件存在

## 测试覆盖
- 自动编号生成功能
- 历史品种列表功能
- 销售仅显示有库存商品
- 多维度销售统计
- 成本利润分析
- 单位转换处理
- 折扣销售功能
- 茶类和品种统计
- 数据准确性保障