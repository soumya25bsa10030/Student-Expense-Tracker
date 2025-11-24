# Student-Expense-Tracker
Overview of the Project
The Student Expense Tracker is a Python-based application that helps students take control of their finances. It provides intelligent expense tracking, budget management, and predictive analytics to transform financial stress into confident money management through an intuitive console interface.

## *OBJECTIVES  
● To focus on wise and conscious expenditure 
● To categorize the expenditure under different domains like food expenses , rent etc .
● Easy mangement of budget 
● Identifying over expenditure to manage it

## Features
1. Expense Tracking: Record and categorize daily spending
2. Budget Management: Set and monitor monthly limits
3. Bill Reminders: Schedule and track payment deadlines
6.Data Persistence: Automatic save/load functionality
7.CRUD Operations: Full Create, Read, Update, Delete capabilities


## **Functional Requirements**
- **Expense Tracking**: Record daily spending with categories like food, transport, books
- **Budget Management**: Set monthly spending limits and track progress
- **Bill Reminders**: Schedule payments and get due date alerts
- **Data Safety**: Automatic saving and backup of all financial records
- **Easy Editing**: Update or delete transactions and bills as needed

## **Non-functional Requirements**
- **Performance**: Fast response even with years of transaction history
- **Reliability**: 99% uptime with no data loss
- **Security**: Protection against invalid inputs and data corruption
- **Usability**: Simple menu system anyone can use without training
- **Compatibility**: Works on Windows, Mac, and Linux systems
- **Maintainability**: Clean code that's easy to update and extend

## **System Architecture Diagram**
```
User Input → [Console Interface] → [Business Logic] → [Data Storage]
                ↑                    ↑                  ↑
          Menu System        Finance Rules       JSON File Database
          Display Results    Calculations        Backup System
```

## **Process Flow Diagram**
1. **Start** → Login with password
2. **Main Menu** → Choose action (add expense, view report, etc.)
3. **Process** → System calculates and validates
4. **Results** → Show updated information
5. **Loop** → Return to main menu until exit

## **UML Diagrams**

### **Use Case Diagram**
- **Actor**: Student User
- **Actions**: 
  - Record expenses
  - View spending reports  
  - Set budget limits
  - Schedule bill payments
  - Get spending predictions
  - Manage transaction history

### **Class Diagram**
```
FinanceManager (Controller)
├── FinanceService (Business Logic)
│   ├── TransactionManager
│   ├── BudgetCalculator
│   └── PredictionEngine
├── DataRepository (Storage)
└── Validator (Input Checker)
```

### **Sequence Diagram**
```
User → Controller: Choose "Add Expense"
Controller → Service: Validate inputs
Service → Repository: Save transaction
Repository → File: Write to JSON
File → Repository: Confirm save
Repository → Service: Return success
Service → Controller: Show confirmation
Controller → User: Display result
```

### **ER Diagram Concept**
```
STUDENT_USER ────◄ TRANSACTIONS
     │               ├─ Amount
     │               ├─ Category  
     │               ├─ Date
     │               └─ Description
     │
     └───────◄ BILLS
             ├─ Title
             ├─ Due Date
             ├─ Amount
             └─ Status
```


**Transactions Table:**
- ID (unique identifier)
- Amount (spending value)
- Category (food, transport, etc.)
- Date (when spent)
- Description (optional notes)

**Bills Table:**
- ID (unique identifier) 
- Title (bill name)
- DueDate (payment deadline)
- Amount (how much to pay)
- Status (pending/paid)

**System Settings:**
- MonthlyBudget (spending limit)
- UserPreferences (display options)


### **Dataset Description**
- **Source**: User's own transaction history
- **Features**: Amount, category, date, spending patterns
- **Size**: Grows with usage (5+ transactions needed for predictions)
- **Quality**: Real-world student spending data

### **Why I choose this model**
- **Simple Average**: Easy to understand, works with little data
- **Linear Regression**: Spots trends in growing/shrinking expenses
- **Choice Reason**: Students need simple, explainable predictions rather than complex black-box models

### **Evaluation Methodology**
- **Accuracy Check**: Compare predictions against actual future spending
- **Confidence Scores**: Show how reliable predictions are based on data quantity
- **User Feedback**: Students can report if predictions helped their budgeting
- **Performance Testing**: Ensure fast predictions even with large transaction history

## Technologies/Tools Used
1. Programming Language: Python 3.8+
2. Architecture Patterns: MVC, Repository, Strategy
3. Data Storage: JSON file-based persistence
4. Libraries: datetime, json, logging, collections, unittest


## Prerequisites
1. Python 3.8 or higher installed
2. Basic terminal/command prompt knowledge

## Installation Steps
1.Download the Code
2.Verify Python Installation
3.Run the Application


## Instructions for Testing
1. Run All Tests
2. Manual Testing Steps
3. Expense Management
4. Add transactions with different categories
5. Update existing transactions
6. Delete transactions and verify removal
7. Budget Features
8. Set monthly budget
9. Add expenses and check budget usage
10.View spending reports
11. Prediction System
12. Add multiple transactions across different dates
13. Generate spending predictions
14. Test different prediction algorithms
15. Data Persistence
16. Add data and restart application
17. Verify data reloads correctly
18. Check backup file creation
19. Error Handling



