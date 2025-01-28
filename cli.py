import argparse
from database import init_db, add_expense, get_expenses
from analytics import calculate_total, category_breakdown

def main():
    parser = argparse.ArgumentParser(description='Local Expense Tracker')
    subparsers = parser.add_subparsers(dest='command')

    # Add expense command
    add_parser = subparsers.add_parser('add', help='Add a new expense')
    add_parser.add_argument('--date', required=True, help='Date of the expense (YYYY-MM-DD)')
    add_parser.add_argument('--category', required=True, help='Category of the expense')
    add_parser.add_argument('--amount', required=True, type=float, help='Amount spent')
    add_parser.add_argument('--description', help='Short description')

    # View expenses command
    view_parser = subparsers.add_parser('view', help='View all expenses')

    # Analytics command
    stats_parser = subparsers.add_parser('stats', help='View expense statistics')

    args = parser.parse_args()
    init_db()

    if args.command == 'add':
        add_expense(args.date, args.category, args.amount, args.description or '')
        print('Expense added successfully!')
    elif args.command == 'view':
        expenses = get_expenses()
        for expense in expenses:
            print(expense)
    elif args.command == 'stats':
        expenses = get_expenses()
        print('Total Expenses:', calculate_total(expenses))
        print('Category Breakdown:', category_breakdown(expenses))
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
