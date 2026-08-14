import React from 'react';
import { Calendar, DollarSign, FileText, MapPin, CreditCard, CheckCircle2, Clock, XCircle } from 'lucide-react';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';

interface Expense {
  expense_id: string;
  trip_name?: string;
  date: string;
  category: string;
  merchant: string;
  amount: number;
  currency: string;
  payment_method: string;
  gst_amount?: number;
  notes?: string;
  status: string;
  policy_compliance: string;
  created_at: string;
}

interface ShowExpensesProps {
  expenses: Expense[];
  statistics?: {
    total_amount: number;
    pending_count: number;
    approved_count: number;
    average_amount: number;
  };
}

export function ShowExpenses({ expenses, statistics }: ShowExpensesProps) {
  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'approved':
        return (
          <Badge variant="success" className="flex items-center gap-1">
            <CheckCircle2 size={14} />
            Approved
          </Badge>
        );
      case 'rejected':
        return (
          <Badge variant="error" className="flex items-center gap-1">
            <XCircle size={14} />
            Rejected
          </Badge>
        );
      default:
        return (
          <Badge variant="warning" className="flex items-center gap-1">
            <Clock size={14} />
            Pending
          </Badge>
        );
    }
  };

  const getComplianceBadge = (compliance: string) => {
    switch (compliance) {
      case 'compliant':
        return <Badge variant="success">Compliant</Badge>;
      case 'non-compliant':
        return <Badge variant="error">Non-Compliant</Badge>;
      default:
        return <Badge variant="secondary">Under Review</Badge>;
    }
  };

  const getCategoryIcon = (category: string) => {
    const icons: Record<string, string> = {
      'Flight': '✈️',
      'Hotel': '🏨',
      'Food & Dining': '🍽️',
      'Transportation': '🚗',
      'Fuel': '⛽',
      'Entertainment': '🎬',
      'Office Supplies': '📎',
      'Client Meeting': '🤝',
      'Conference': '🎤',
      'Other': '📄'
    };
    return icons[category] || '📄';
  };

  if (expenses.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-400 mb-4">
          <FileText size={64} className="mx-auto" />
        </div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">No Expenses Found</h3>
        <p className="text-gray-600">Create your first expense to get started!</p>
      </div>
    );
  }

  return (
    <div>
      {/* Statistics Cards */}
      {statistics && (
        <div className="grid grid-cols-4 gap-4 mb-6">
          <Card className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Total Amount</p>
                <p className="text-2xl font-bold text-gray-900">
                  ₹{statistics.total_amount.toLocaleString()}
                </p>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <DollarSign size={24} className="text-blue-600" />
              </div>
            </div>
          </Card>

          <Card className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Pending</p>
                <p className="text-2xl font-bold text-yellow-600">{statistics.pending_count}</p>
              </div>
              <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                <Clock size={24} className="text-yellow-600" />
              </div>
            </div>
          </Card>

          <Card className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Approved</p>
                <p className="text-2xl font-bold text-green-600">{statistics.approved_count}</p>
              </div>
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <CheckCircle2 size={24} className="text-green-600" />
              </div>
            </div>
          </Card>

          <Card className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Average</p>
                <p className="text-2xl font-bold text-gray-900">
                  ₹{Math.round(statistics.average_amount).toLocaleString()}
                </p>
              </div>
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <FileText size={24} className="text-purple-600" />
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* Expense List */}
      <div className="space-y-4">
        {expenses.map((expense) => (
          <Card key={expense.expense_id} className="p-5 hover:shadow-lg transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-start gap-3">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center text-2xl">
                  {getCategoryIcon(expense.category)}
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="text-lg font-bold text-gray-900">{expense.merchant}</h3>
                    <Badge variant="info" className="text-xs">
                      {expense.expense_id}
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-600">{expense.category}</p>
                  {expense.trip_name && (
                    <div className="flex items-center gap-1 mt-1">
                      <MapPin size={14} className="text-gray-500" />
                      <span className="text-xs text-gray-600">{expense.trip_name}</span>
                    </div>
                  )}
                </div>
              </div>

              <div className="text-right">
                <div className="text-2xl font-bold text-gray-900 mb-1">
                  {expense.currency} {expense.amount.toLocaleString()}
                </div>
                {expense.gst_amount && (
                  <p className="text-xs text-gray-600">GST: ₹{expense.gst_amount}</p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-4 gap-4 mb-4">
              <div className="flex items-center gap-2">
                <Calendar size={16} className="text-gray-500" />
                <div>
                  <p className="text-xs text-gray-600">Date</p>
                  <p className="text-sm font-medium text-gray-900">
                    {new Date(expense.date).toLocaleDateString()}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <CreditCard size={16} className="text-gray-500" />
                <div>
                  <p className="text-xs text-gray-600">Payment</p>
                  <p className="text-sm font-medium text-gray-900">
                    {expense.payment_method.split(' ')[0]}
                  </p>
                </div>
              </div>

              <div>
                <p className="text-xs text-gray-600 mb-1">Status</p>
                {getStatusBadge(expense.status)}
              </div>

              <div>
                <p className="text-xs text-gray-600 mb-1">Compliance</p>
                {getComplianceBadge(expense.policy_compliance)}
              </div>
            </div>

            {expense.notes && (
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-xs text-gray-600 mb-1">Notes:</p>
                <p className="text-sm text-gray-700">{expense.notes}</p>
              </div>
            )}
          </Card>
        ))}
      </div>
    </div>
  );
}
