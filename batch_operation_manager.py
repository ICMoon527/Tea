import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime


class BatchOperationManager:
    """批量操作管理器"""
    
    def __init__(self, excel_manager, operation_logger):
        self.excel_manager = excel_manager
        self.operation_logger = operation_logger
    
    def batch_update_commodity_prices(
        self,
        commodity_ids: List[str],
        price_updates: Dict[str, float]
    ) -> Dict[str, Any]:
        """批量更新商品价格
        
        Args:
            commodity_ids: 商品编号列表
            price_updates: 价格更新字典，键为字段名（成本价/零售价），值为价格或百分比
            
        Returns:
            操作结果字典
        """
        results = {
            'success': 0,
            'failed': 0,
            'details': []
        }
        
        for com_id in commodity_ids:
            try:
                commodity = self.excel_manager.get_commodity_by_id(com_id)
                if commodity is None:
                    results['failed'] += 1
                    results['details'].append({
                        'id': com_id,
                        'status': 'failed',
                        'message': '商品不存在'
                    })
                    continue
                
                updates = {}
                
                if '成本价' in price_updates:
                    cost_change = price_updates['成本价']
                    if isinstance(cost_change, str) and '%' in cost_change:
                        percent = float(cost_change.replace('%', '')) / 100
                        new_cost = commodity['成本价'] * (1 + percent)
                        updates['成本价'] = round(new_cost, 2)
                    else:
                        updates['成本价'] = float(cost_change)
                
                if '零售价' in price_updates:
                    retail_change = price_updates['零售价']
                    if isinstance(retail_change, str) and '%' in retail_change:
                        percent = float(retail_change.replace('%', '')) / 100
                        new_retail = commodity['零售价'] * (1 + percent)
                        updates['零售价'] = round(new_retail, 2)
                    else:
                        updates['零售价'] = float(retail_change)
                
                if updates:
                    self.excel_manager.update_commodity(com_id, updates)
                    results['success'] += 1
                    results['details'].append({
                        'id': com_id,
                        'status': 'success',
                        'message': '更新成功'
                    })
                    
                    self.operation_logger.log_operation(
                        operation_type="修改",
                        module="商品管理",
                        details=f"批量更新商品价格: {com_id}",
                        data=str(updates)
                    )
            except (FileNotFoundError, PermissionError, ValueError, KeyError, OSError) as e:
                results['failed'] += 1
                results['details'].append({
                    'id': com_id,
                    'status': 'failed',
                    'message': str(e)
                })
        
        return results
    
    def batch_delete_commodities(
        self,
        commodity_ids: List[str]
    ) -> Dict[str, Any]:
        """批量删除商品
        
        Args:
            commodity_ids: 商品编号列表
            
        Returns:
            操作结果字典
        """
        results = {
            'success': 0,
            'failed': 0,
            'details': []
        }
        
        for com_id in commodity_ids:
            try:
                commodity = self.excel_manager.get_commodity_by_id(com_id)
                if commodity is None:
                    results['failed'] += 1
                    results['details'].append({
                        'id': com_id,
                        'status': 'failed',
                        'message': '商品不存在'
                    })
                    continue
                
                self.excel_manager.delete_commodity(com_id)
                results['success'] += 1
                results['details'].append({
                    'id': com_id,
                    'status': 'success',
                    'message': '删除成功'
                })
                
                self.operation_logger.log_operation(
                    operation_type="删除",
                    module="商品管理",
                    details=f"批量删除商品: {com_id}"
                )
            except (FileNotFoundError, PermissionError, ValueError, KeyError, OSError) as e:
                results['failed'] += 1
                results['details'].append({
                    'id': com_id,
                    'status': 'failed',
                    'message': str(e)
                })
        
        return results
    
    def batch_update_suppliers(
        self,
        supplier_ids: List[str],
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """批量更新供应商信息
        
        Args:
            supplier_ids: 供应商编号列表
            updates: 更新字段字典
            
        Returns:
            操作结果字典
        """
        results = {
            'success': 0,
            'failed': 0,
            'details': []
        }
        
        for sup_id in supplier_ids:
            try:
                # 检查供应商是否存在
                all_suppliers = self.excel_manager.get_all_suppliers()
                supplier = all_suppliers[all_suppliers['供应商编号'] == sup_id]
                if supplier.empty:
                    results['failed'] += 1
                    results['details'].append({
                        'id': sup_id,
                        'status': 'failed',
                        'message': '供应商不存在'
                    })
                    continue
                
                # 更新供应商信息
                idx = all_suppliers[all_suppliers['供应商编号'] == sup_id].index
                if len(idx) > 0:
                    for key, value in updates.items():
                        all_suppliers.at[idx[0], key] = value
                    self.excel_manager.write_sheet("供应商", all_suppliers)
                results['success'] += 1
                results['details'].append({
                    'id': sup_id,
                    'status': 'success',
                    'message': '更新成功'
                })
                
                self.operation_logger.log_operation(
                    operation_type="修改",
                    module="供应商管理",
                    details=f"批量更新供应商: {sup_id}",
                    data=str(updates)
                )
            except (FileNotFoundError, PermissionError, ValueError, KeyError, OSError) as e:
                results['failed'] += 1
                results['details'].append({
                    'id': sup_id,
                    'status': 'failed',
                    'message': str(e)
                })
        
        return results
    
    def batch_update_customers(
        self,
        customer_ids: List[str],
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """批量更新客户信息
        
        Args:
            customer_ids: 客户编号列表
            updates: 更新字段字典
            
        Returns:
            操作结果字典
        """
        results = {
            'success': 0,
            'failed': 0,
            'details': []
        }
        
        for cus_id in customer_ids:
            try:
                customer = self.excel_manager.get_customer_by_id(cus_id)
                if customer is None:
                    results['failed'] += 1
                    results['details'].append({
                        'id': cus_id,
                        'status': 'failed',
                        'message': '客户不存在'
                    })
                    continue
                
                self.excel_manager.update_customer(cus_id, updates)
                results['success'] += 1
                results['details'].append({
                    'id': cus_id,
                    'status': 'success',
                    'message': '更新成功'
                })
                
                self.operation_logger.log_operation(
                    operation_type="修改",
                    module="客户管理",
                    details=f"批量更新客户: {cus_id}",
                    data=str(updates)
                )
            except (FileNotFoundError, PermissionError, ValueError, KeyError, OSError) as e:
                results['failed'] += 1
                results['details'].append({
                    'id': cus_id,
                    'status': 'failed',
                    'message': str(e)
                })
        
        return results
    
    def batch_import_commodities(
        self,
        import_data: List[Dict]
    ) -> Dict[str, Any]:
        """批量导入商品
        
        Args:
            import_data: 导入数据列表
            
        Returns:
            操作结果字典
        """
        results = {
            'success': 0,
            'failed': 0,
            'details': []
        }
        
        for idx, item_data in enumerate(import_data):
            try:
                self.excel_manager.add_commodity(item_data)
                results['success'] += 1
                results['details'].append({
                    'index': idx,
                    'status': 'success',
                    'message': '导入成功'
                })
            except (FileNotFoundError, PermissionError, ValueError, KeyError, OSError) as e:
                results['failed'] += 1
                results['details'].append({
                    'index': idx,
                    'status': 'failed',
                    'message': str(e)
                })
        
        if results['success'] > 0:
            self.operation_logger.log_operation(
                operation_type="导入",
                module="商品管理",
                details=f"批量导入商品: 成功{results['success']}条，失败{results['failed']}条"
            )
        
        return results
    
    def batch_adjust_stock(
        self,
        stock_adjustments: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """批量调整库存
        
        Args:
            stock_adjustments: 库存调整列表，每项包含商品编号和调整数量
            
        Returns:
            操作结果字典
        """
        results = {
            'success': 0,
            'failed': 0,
            'details': []
        }
        
        for adjustment in stock_adjustments:
            try:
                com_id = adjustment.get('商品编号')
                quantity = adjustment.get('调整数量', 0)
                
                if not com_id:
                    results['failed'] += 1
                    results['details'].append({
                        'id': com_id,
                        'status': 'failed',
                        'message': '缺少商品编号'
                    })
                    continue
                
                commodity = self.excel_manager.get_commodity_by_id(com_id)
                if commodity is None:
                    results['failed'] += 1
                    results['details'].append({
                        'id': com_id,
                        'status': 'failed',
                        'message': '商品不存在'
                    })
                    continue
                
                new_stock = commodity['当前库存'] + quantity
                if new_stock < 0:
                    results['failed'] += 1
                    results['details'].append({
                        'id': com_id,
                        'status': 'failed',
                        'message': '库存不足'
                    })
                    continue
                
                self.excel_manager.update_commodity(com_id, {'当前库存': new_stock})
                results['success'] += 1
                results['details'].append({
                    'id': com_id,
                    'status': 'success',
                    'message': f'库存调整成功: {commodity["当前库存"]} -> {new_stock}'
                })
            except (FileNotFoundError, PermissionError, ValueError, KeyError, OSError) as e:
                results['failed'] += 1
                results['details'].append({
                    'id': adjustment.get('商品编号', 'unknown'),
                    'status': 'failed',
                    'message': str(e)
                })
        
        if results['success'] > 0:
            self.operation_logger.log_operation(
                operation_type="修改",
                module="库存管理",
                details=f"批量调整库存: 成功{results['success']}条，失败{results['failed']}条"
            )
        
        return results
    
    def download_import_template(self):
        import tkinter.filedialog as filedialog
        import tkinter.messagebox as messagebox
        
        file_path = filedialog.asksaveasfilename(
            title="保存导入模板",
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx")],
            initialfile="商品批量导入模板.xlsx"
        )
        
        if not file_path:
            return
        
        template_df = pd.DataFrame(columns=[
            "茶类", "品种", "商品名称", "规格", "单位",
            "成本价", "零售价", "初始库存", "保质期(月)", "备注"
        ])
        
        example_row = {
            "茶类": "绿茶",
            "品种": "龙井",
            "商品名称": "西湖龙井特级",
            "规格": "500g",
            "单位": "克",
            "成本价": 80.00,
            "零售价": 168.00,
            "初始库存": 50,
            "保质期(月)": 18,
            "备注": "此为示例数据，导入前请删除此行"
        }
        template_df = pd.concat([template_df, pd.DataFrame([example_row])], ignore_index=True)
        
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            template_df.to_excel(writer, sheet_name='商品数据', index=False)
        
            instructions = pd.DataFrame({
                "字段": list(template_df.columns),
                "是否必填": ["是", "是", "是", "是", "是", "是", "是", "是", "否", "否"],
                "说明": [
                    "如：绿茶、红茶、乌龙茶等",
                    "如：龙井、碧螺春、铁观音等",
                    "商品的具体名称",
                    "如：250g、500g",
                    "如：克、斤、盒",
                    "进货价格，单位：元",
                    "建议零售价格，单位：元",
                    "当前库存数量",
                    "单位为月，可不填",
                    "额外备注信息，可不填"
                ]
            })
            instructions.to_excel(writer, sheet_name='填写说明', index=False)
        
        messagebox.showinfo("成功", f"模板已保存到：{file_path}")
