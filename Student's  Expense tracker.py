"""
Student Finance Manager - Production Ready
Architecture: MVC with Repository & Strategy Patterns
"""

import datetime
import json
import logging
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Tuple
from collections import defaultdict
from enum import Enum
from dataclasses import dataclass

# =============================================================================
# DATA MODELS
# =============================================================================

class Category(Enum):
    TUITION = (1, "Tuition")
    BOOKS = (2, "Books") 
    RENT = (3, "Rent")
    GROCERIES = (4, "Groceries")
    TRANSPORT = (5, "Transport")
    ENTERTAINMENT = (6, "Entertainment")
    MISC = (7, "Miscellaneous")
    
    def __init__(self, id, description):
        self.id = id
        self.description = description

@dataclass
class Transaction:
    id: int
    amount: float
    category: Category
    description: str
    date: str
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category.name,
            'description': self.description,
            'date': self.date
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            amount=data['amount'],
            category=Category[data['category']],
            description=data['description'],
            date=data['date']
        )

# =============================================================================
# STRATEGY PATTERN - PREDICTION ALGORITHMS
# =============================================================================

class PredictionStrategy(ABC):
    @abstractmethod
    def predict(self, transactions: List[Transaction]) -> Dict:
        pass

class SimpleAverageStrategy(PredictionStrategy):
    def predict(self, transactions: List[Transaction]) -> Dict:
        if len(transactions) < 5:
            return {"error": "Need at least 5 transactions"}
        
        monthly_totals = defaultdict(float)
        for t in transactions:
            month = t.date[:7]  # YYYY-MM
            monthly_totals[month] += t.amount
        
        if not monthly_totals:
            return {"predicted": 0.0, "confidence": 0.0}
        
        avg = sum(monthly_totals.values()) / len(monthly_totals)
        confidence = min(0.9, len(transactions) / 50.0)
        
        return {
            "predicted": avg,
            "confidence": confidence,
            "algorithm": "simple_average"
        }

# =============================================================================
# REPOSITORY PATTERN - DATA PERSISTENCE
# =============================================================================

class Repository:
    def __init__(self, data_file='finance_data.json'):
        self.data_file = data_file
    
    def save_all(self, transactions: List[Transaction], bills: List) -> bool:
        try:
            data = {
                'transactions': [t.to_dict() for t in transactions],
                'bills': bills,
                'last_updated': datetime.datetime.now().isoformat()
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logging.error(f"Save failed: {e}")
            return False
    
    def load_all(self) -> Tuple[List[Transaction], List]:
        try:
            if not os.path.exists(self.data_file):
                return [], []
            
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            transactions = [Transaction.from_dict(t) for t in data.get('transactions', [])]
            bills = data.get('bills', [])
            return transactions, bills
        except Exception as e:
            logging.error(f"Load failed: {e}")
            return [], []

# =============================================================================
# VALIDATION SERVICE
# =============================================================================

class Validator:
    @staticmethod
    def validate_amount(amount: float) -> Tuple[bool, str]:
        if amount <= 0:
            return False, "Amount must be positive"
        if amount > 1000000:
            return False, "Amount too large"
        return True, "Valid"
    
    @staticmethod
    def validate_date(date_str: str) -> Tuple[bool, str]:
        try:
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return True, "Valid"
        except ValueError:
            return False, "Use YYYY-MM-DD format"
    
    @staticmethod
    def validate_category(category_id: int) -> Tuple[bool, str]:
        valid_ids = [c.id for c in Category]
        return (category_id in valid_ids, f"Category must be 1-{len(valid_ids)}")

# =============================================================================
# CORE BUSINESS LOGIC
# =============================================================================

class FinanceService:
    def __init__(self):
        self.repository = Repository()
        self.transactions: List[Transaction] = []
        self.bills: List = []
        self.monthly_limit = 0
        self.next_id = 1
        self.prediction_strategy = SimpleAverageStrategy()
        self._load_data()
    
    def _load_data(self):
        self.transactions, self.bills = self.repository.load_all()
        if self.transactions:
            self.next_id = max(t.id for t in self.transactions) + 1
    
    def create_transaction(self, amount: float, category_id: int, description: str = "") -> Tuple[bool, str]:
        # Validate inputs
        is_valid, msg = Validator.validate_amount(amount)
        if not is_valid:
            return False, msg
        
        is_valid, msg = Validator.validate_category(category_id)
        if not is_valid:
            return False, msg
        
        # Find category
        category = next((c for c in Category if c.id == category_id), None)
        if not category:
            return False, "Invalid category"
        
        # Create and save
        transaction = Transaction(
            id=self.next_id,
            amount=amount,
            category=category,
            description=description,
            date=datetime.datetime.now().strftime("%Y-%m-%d")
        )
        
        self.transactions.append(transaction)
        self.next_id += 1
        
        if self.repository.save_all(self.transactions, self.bills):
            return True, f"✅ Recorded ₹{amount} for {category.description}"
        else:
            self.transactions.pop()  # Rollback
            self.next_id -= 1
            return False, "❌ Save failed"
    
    def get_spending_report(self) -> Dict:
        total = sum(t.amount for t in self.transactions)
        
        # Category breakdown
        by_category = defaultdict(float)
        for t in self.transactions:
            by_category[t.category.description] += t.amount
        
        # Prediction
        prediction = self.prediction_strategy.predict(self.transactions)
        
        return {
            'total_transactions': len(self.transactions),
            'total_spent': total,
            'by_category': dict(by_category),
            'prediction': prediction,
            'budget_status': {
                'limit': self.monthly_limit,
                'remaining': self.monthly_limit - total,
                'usage_pct': (total / self.monthly_limit * 100) if self.monthly_limit else 0
            }
        }
    
    def classify_spending(self) -> Dict[str, float]:
        totals = defaultdict(float)
        for t in self.transactions:
            totals[t.category.description] += t.amount
        return dict(totals)
    
    def predict_spending(self) -> Dict:
        return self.prediction_strategy.predict(self.transactions)

# =============================================================================
# PRESENTATION LAYER
# =============================================================================

class FinanceManagerApp:
    def __init__(self):
        self.service = FinanceService()
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def run(self):
        """Main application loop"""
        print("💰 STUDENT FINANCE MANAGER")
        print("=" * 40)
        
        while True:
            self.show_menu()
            choice = input("\nChoose option (1-8): ").strip()
            
            if choice == '1':
                self.record_transaction()
            elif choice == '2':
                self.view_transactions()
            elif choice == '3':
                self.show_report()
            elif choice == '4':
                self.show_classification()
            elif choice == '5':
                self.show_prediction()
            elif choice == '6':
                self.set_budget()
            elif choice == '7':
                self.system_info()
            elif choice == '8':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice")
    
    def show_menu(self):
        menu = [
            "1. 💰 Record Transaction",
            "2. 📋 View Transactions", 
            "3. 📊 Financial Report",
            "4. 🎯 Spending Classification",
            "5. 🔮 Spending Prediction",
            "6. 💸 Set Budget",
            "7. ℹ️  System Info",
            "8. 🚪 Exit"
        ]
        print("\n" + "\n".join(menu))
    
    def record_transaction(self):
        print("\n➕ RECORD TRANSACTION")
        print("Categories: " + " | ".join(f"{c.id}.{c.description}" for c in Category))
        
        try:
            cat_id = int(input("Category ID: "))
            amount = float(input("Amount ₹: "))
            desc = input("Description: ")
            
            success, message = self.service.create_transaction(amount, cat_id, desc)
            print(message)
        except ValueError:
            print("❌ Invalid input")
    
    def view_transactions(self):
        transactions = self.service.transactions
        if not transactions:
            print("📭 No transactions found")
            return
        
        print(f"\n📋 TRANSACTIONS ({len(transactions)} total)")
        print("-" * 50)
        for t in transactions[-10:]:  # Show last 10
            print(f"#{t.id} | {t.date} | {t.category.description:12} | ₹{t.amount:8.2f} | {t.description}")
    
    def show_report(self):
        report = self.service.get_spending_report()
        
        print("\n📊 FINANCIAL REPORT")
        print("=" * 40)
        print(f"Total Transactions: {report['total_transactions']}")
        print(f"Total Spent: ₹{report['total_spent']:.2f}")
        
        if report['by_category']:
            print("\n📈 BY CATEGORY:")
            for category, amount in report['by_category'].items():
                pct = (amount / report['total_spent'] * 100) if report['total_spent'] > 0 else 0
                print(f"  {category:15} ₹{amount:8.2f} ({pct:5.1f}%)")
        
        if 'predicted' in report['prediction']:
            pred = report['prediction']
            print(f"\n🔮 Prediction: ₹{pred['predicted']:.2f} ({(pred.get('confidence', 0)*100):.1f}% confidence)")
    
    def show_classification(self):
        classification = self.service.classify_spending()
        if not classification:
            print("📊 No spending data")
            return
        
        print("\n🎯 SPENDING CLASSIFICATION")
        print("=" * 40)
        total = sum(classification.values())
        
        for category, amount in sorted(classification.items(), key=lambda x: x[1], reverse=True):
            pct = (amount / total * 100) if total > 0 else 0
            bar = "█" * int(pct / 5)
            print(f"{category:15} ₹{amount:8.2f} ({pct:5.1f}%) {bar}")
    
    def show_prediction(self):
        prediction = self.service.predict_spending()
        
        print("\n🔮 SPENDING PREDICTION")
        print("=" * 40)
        
        if 'error' in prediction:
            print(f"❌ {prediction['error']}")
        else:
            print(f"Algorithm: {prediction.get('algorithm', 'N/A')}")
            print(f"Predicted: ₹{prediction.get('predicted', 0):.2f}")
            print(f"Confidence: {(prediction.get('confidence', 0)*100):.1f}%")
            
            if self.service.monthly_limit > 0:
                remaining = self.service.monthly_limit - prediction.get('predicted', 0)
                status = "UNDER ✅" if remaining >= 0 else "OVER ❌"
                print(f"Budget: ₹{abs(remaining):.2f} {status}")
    
    def set_budget(self):
        try:
            budget = float(input("\nEnter monthly budget ₹: "))
            if budget < 0:
                print("❌ Budget cannot be negative")
                return
            self.service.monthly_limit = budget
            print(f"✅ Budget set to ₹{budget}")
        except ValueError:
            print("❌ Invalid amount")
    
    def system_info(self):
        print("\n💾 SYSTEM INFORMATION")
        print("=" * 30)
        print(f"Transactions: {len(self.service.transactions)}")
        print(f"Budget: ₹{self.service.monthly_limit}")
        print(f"Data File: {self.service.repository.data_file}")
        print("Architecture: MVC + Repository Pattern")

# =============================================================================
# TEST SUITE
# =============================================================================

import unittest

class TestFinanceManager(unittest.TestCase):
    def setUp(self):
        self.service = FinanceService()
        self.validator = Validator()
    
    def test_amount_validation(self):
        self.assertTrue(self.validator.validate_amount(100)[0])
        self.assertFalse(self.validator.validate_amount(-50)[0])
    
    def test_transaction_creation(self):
        success, msg = self.service.create_transaction(100, 1, "Test")
        self.assertTrue(success)
    
    def test_spending_classification(self):
        # Add test data
        self.service.create_transaction(100, 1, "Test1")
        self.service.create_transaction(200, 2, "Test2")
        classification = self.service.classify_spending()
        self.assertIn("Tuition", classification)

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("🧪 Running tests...")
        unittest.main(argv=[''], exit=False)
    else:
        app = FinanceManagerApp()
        app.run()
