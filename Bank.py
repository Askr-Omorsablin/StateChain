import yaml
from dataclasses import dataclass
from typing import List, Optional, Tuple
from datetime import datetime

# 数据模型
@dataclass
class Account:
    id: int
    balance: float
    name: str
    created_at: str
    status: str

class AccountBook:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.accounts = self._load_accounts()
    
    def _load_accounts(self) -> List[Account]:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return [Account(**account) for account in data['accounts']]
    
    def _save_accounts(self):
        data = {'accounts': [
            {
                'id': acc.id,
                'balance': acc.balance,
                'name': acc.name,
                'created_at': acc.created_at,
                'status': acc.status
            } for acc in self.accounts
        ]}
        with open(self.file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True)
    
    def find_account(self, account_id: int) -> Optional[Account]:
        print("📚 账本：正在查找账号...")
        account = next((acc for acc in self.accounts if acc.id == account_id), None)
        if account:
            print(f"📚 账本：找到账号，余额为{account.balance}元")
        else:
            print("📚 账本：未找到该账号")
        return account
    
    def modify_balance(self, account_id: int, amount: float) -> Tuple[bool, str]:
        account = self.find_account(account_id)
        if not account:
            return False, "账号不存在"
        
        new_balance = account.balance + amount
        if new_balance < 0:
            return False, "余额不足"
        
        account.balance = new_balance
        self._save_accounts()
        print(f"📚 账本：余额已更新为{new_balance}元")
        return True, f"操作成功，当前余额为{new_balance}元"

class Accountant:
    def __init__(self, account_book: AccountBook):
        self.account_book = account_book
    
    def query_balance(self, account_id: int) -> str:
        print(f"👨‍💼 记账：收到查询请求，正在查询账号{account_id}...")
        account = self.account_book.find_account(account_id)
        result = f"编号为{account_id}的账号有{account.balance}元" if account else f"未找到编号为{account_id}的账号"
        print(f"👨‍💼 记账 -> 财务：{result}")
        return result
    
    def process_transaction(self, account_id: int, amount: float) -> str:
        print(f"👨‍💼 记账：收到交易请求，账号{account_id}，金额{amount}元")
        success, message = self.account_book.modify_balance(account_id, amount)
        result = f"交易{'成功' if success else '失败'}：{message}"
        print(f"👨‍💼 记账 -> 财务：{result}")
        return result

class FinanceStaff:
    def __init__(self, accountant: Accountant):
        self.accountant = accountant
    
    def query_balance(self, account_id: int) -> str:
        print(f"👨‍🏫 财务 -> 记账：帮我查一下编号为{account_id}的账号有多少余额")
        result = self.accountant.query_balance(account_id)
        print(f"👨‍🏫 财务 -> 前台：{result}")
        return result
    
    def handle_deposit(self, account_id: int, amount: float) -> str:
        print(f"👨‍🏫 财务 -> 记账：处理存款，账号{account_id}，金额{amount}元")
        result = self.accountant.process_transaction(account_id, amount)
        print(f"👨‍🏫 财务 -> 前台：{result}")
        return result
    
    def handle_withdrawal(self, account_id: int, amount: float) -> str:
        print(f"👨‍🏫 财务 -> 记账：处理取款，账号{account_id}，金额{amount}元")
        result = self.accountant.process_transaction(account_id, -amount)
        print(f"👨‍🏫 财务 -> 前台：{result}")
        return result

class FrontDesk:
    def __init__(self, finance_staff: FinanceStaff):
        self.finance_staff = finance_staff
    
    def handle_query_balance(self, account_id: int) -> str:
        print(f"👨‍💻 前台 -> 财务：帮我查一下编号为{account_id}的账号有多少余额")
        result = self.finance_staff.query_balance(account_id)
        print(f"👨‍💻 前台 -> 客户：{result}")
        return result
    
    def handle_deposit(self, account_id: int, amount: float) -> str:
        print(f"👨‍💻 前台 -> 财务：处理存款业务，账号{account_id}，金额{amount}元")
        result = self.finance_staff.handle_deposit(account_id, amount)
        print(f"👨‍💻 前台 -> 客户：{result}")
        return result
    
    def handle_withdrawal(self, account_id: int, amount: float) -> str:
        print(f"👨‍💻 前台 -> 财务：处理取款业务，账号{account_id}，金额{amount}元")
        result = self.finance_staff.handle_withdrawal(account_id, amount)
        print(f"👨‍💻 前台 -> 客户：{result}")
        return result
    
    def start_interaction(self):
        while True:
            print("\n👨‍💻 前台：你好，我是钱庄前台人员，请输入数字以选择你要办理的业务：")
            print("1. 查询余额")
            print("2. 存款")
            print("3. 取款")
            print("0. 退出")
            
            choice = input("👤 客户：").strip()
            
            if choice == "0":
                print("👨‍💻 前台：感谢使用，再见！")
                break
            
            try:
                if choice in ["1", "2", "3"]:
                    print("👨‍💻 前台：请输入账本编号：")
                    account_id = int(input("👤 客户：").strip())
                    
                    if choice in ["2", "3"]:
                        print("👨‍💻 前台：请输入金额：")
                        amount = float(input("👤 客户：").strip())
                        if amount <= 0:
                            print("❌ 金额必须大于0！")
                            continue
                    
                    print(f"\n=== 开始处理请求 ===")
                    if choice == "1":
                        result = self.handle_query_balance(account_id)
                    elif choice == "2":
                        result = self.handle_deposit(account_id, amount)
                    else:  # choice == "3"
                        result = self.handle_withdrawal(account_id, amount)
                    print(f"=== 请求处理完成 ===\n")
                else:
                    print("❌ 无效的选择，请重试！")
            except ValueError:
                print("❌ 输入格式错误，请重试！")

def main():
    print("🏦 === 钱庄系统启动 ===")
    # 初始化系统组件
    account_book = AccountBook('accounts.yaml')
    accountant = Accountant(account_book)
    finance_staff = FinanceStaff(accountant)
    front_desk = FrontDesk(finance_staff)
    
    # 启动交互
    front_desk.start_interaction()
    print("🏦 === 钱庄系统关闭 ===")

if __name__ == "__main__":
    main()
