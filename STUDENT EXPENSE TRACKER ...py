import datetime
import json
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

# Simple data models
class Category(Enum):
    TUITION = "Tuition"
    BOOKS = "Books"
    RENT = "Rent"
    FOOD = "Food"
    TRANSPORT = "Transport"
    FUN = "Fun"
    OTHER = "Other"

@dataclass
class Transaction:
    amount: float
    category: Category
    description: str
    date: str = None
    
    def __post_init__(self):
        if not self.date:
            self.date = datetime.datetime.now().strftime("%Y-%m-%d")

# Main finance manager - keeping it simple!
class StudentFinanceManager:
    def __init__(self, data_file='student_finance.json'):
        self.data_file = data_file
        self.transactions: List[Transaction] = []
        self.monthly_budget = 0
        self.load_data()
    
    def save_data(self):
        """Save all data to file"""
        data = {
            'transactions': [
                {
                    'amount': t.amount,
                    'category': t.category.value,
                    'description': t.description,
                    'date': t.date
                } for t in self.transactions
            ],
            'monthly_budget': self.monthly_budget
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self):
        """Load data from file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.transactions = [
                    Transaction(
                        amount=t['amount'],
                        category=Category(t['category']),
                        description=t['description'],
                        date=t['date']
                    ) for t in data.get('transactions', [])
                ]
                self.monthly_budget = data.get('monthly_budget', 0)
        except FileNotFoundError:
            self.transactions = []
    
    def add_spending(self, amount: float, category: Category, description: str = "") -> str:
        """Add new spending with validation"""
        if amount <= 0:
            return "❌ Amount should be positive!"
        
        if amount > 100000:
            return "❌ That's too much money for one transaction!"
        
        transaction = Transaction(amount, category, description)
        self.transactions.append(transaction)
        self.save_data()
        
        return f"✅ Added ₹{amount} for {category.value} - {description}"
    
    def get_spending_summary(self) -> Dict:
        """Get simple spending overview"""
        total_spent = sum(t.amount for t in self.transactions)
        
        # Spending by category
        category_totals = {}
        for t in self.transactions:
            category_totals[t.category.value] = category_totals.get(t.category.value, 0) + t.amount
        
        # Monthly prediction (simple average of last 3 months)
        monthly_data = {}
        for t in self.transactions:
            month = t.date[:7]  # YYYY-MM
            monthly_data[month] = monthly_data.get(month, 0) + t.amount
        
        avg_monthly = sum(monthly_data.values()) / len(monthly_data) if monthly_data else 0
        
        return {
            'total_spent': total_spent,
            'transaction_count': len(self.transactions),
            'by_category': category_totals,
            'avg_monthly': avg_monthly,
            'budget_remaining': self.monthly_budget - total_spent if self.monthly_budget else 0
        }
    
    def show_spending_breakdown(self):
        """Show where money is going"""
        summary = self.get_spending_summary()
        
        print("\n📊 YOUR SPENDING BREAKDOWN")
        print("=" * 40)
        print(f"Total spent: ₹{summary['total_spent']:.2f}")
        print(f"Transactions: {summary['transaction_count']}")
        
        if summary['by_category']:
            print("\nWhere your money went:")
            for category, amount in summary['by_category'].items():
                percentage = (amount / summary['total_spent']) * 100
                print(f"  {category}: ₹{amount:.2f} ({percentage:.1f}%)")
        
        if self.monthly_budget:
            remaining = summary['budget_remaining']
            status = "✅ Under budget" if remaining >= 0 else "❌ Over budget"
            print(f"\nBudget: ₹{abs(remaining):.2f} {status}")
        
        if summary['avg_monthly'] > 0:
            print(f"Monthly average: ₹{summary['avg_monthly']:.2f}")

# Simple menu-driven app
def run_finance_app():
    manager = StudentFinanceManager()
    
    print("💰 STUDENT FINANCE HELPER")
    print("=" * 30)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. ➕ Add spending")
        print("2. 📊 View spending summary")
        print("3. 🎯 Set monthly budget")
        print("4. 📝 View recent transactions")
        print("5. 🚪 Exit")
        
        choice = input("\nChoose (1-5): ").strip()
        
        if choice == '1':
            print("\nAdd New Spending")
            print("Categories: " + " | ".join(f"{i+1}.{cat.value}" for i, cat in enumerate(Category)))
            
            try:
                cat_choice = int(input("Category (1-7): ")) - 1
                if 0 <= cat_choice < len(list(Category)):
                    amount = float(input("Amount ₹: "))
                    desc = input("What was this for? ")
                    
                    category = list(Category)[cat_choice]
                    result = manager.add_spending(amount, category, desc)
                    print(result)
                else:
                    print("❌ Please choose 1-7")
            except ValueError:
                print("❌ Please enter valid numbers")
        
        elif choice == '2':
            manager.show_spending_breakdown()
        
        elif choice == '3':
            try:
                budget = float(input("\nEnter your monthly budget ₹: "))
                manager.monthly_budget = budget
                manager.save_data()
                print(f"✅ Monthly budget set to ₹{budget}")
            except ValueError:
                print("❌ Please enter a valid amount")
        
        elif choice == '4':
            transactions = manager.transactions[-10:]  # Last 10 transactions
            if not transactions:
                print("\nNo transactions yet. Start adding your spending!")
            else:
                print(f"\nLast {len(transactions)} transactions:")
                for t in transactions:
                    print(f"  ₹{t.amount:.2f} | {t.category.value:10} | {t.description} | {t.date}")
        
        elif choice == '5':
            print("\n👋 Goodbye! Keep tracking your money!")
            break
        
        else:
            print("❌ Please choose 1-5")

if __name__ == "__main__":
    run_finance_app()
