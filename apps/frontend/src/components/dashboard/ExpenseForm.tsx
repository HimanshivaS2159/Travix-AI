import React, { useState } from 'react';
import { X, Upload, CheckCircle2, ArrowLeft } from 'lucide-react';
import { apiService } from '../../services/api';
import { useOrchestratorContext } from '../../contexts/OrchestratorContext';

interface ExpenseFormProps {
  formData: any;
  onSubmit: (data: any) => void;
  onCancel: () => void;
}

export function ExpenseForm({ formData, onSubmit, onCancel }: ExpenseFormProps) {
  const { sendMessage } = useOrchestratorContext();
  const [expense, setExpense] = useState({
    expense_id: formData.expense_id || '',
    date: '',
    category: '',
    merchant: '',
    amount: '',
    currency: 'INR',
    payment_method: '',
    gst_amount: '',
    notes: '',
    associated_trip: 'None',
    receipt_url: ''
  });

  const [receiptFile, setReceiptFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitError(null);

    try {
      // Submit to backend
      const result = await apiService.saveExpense(expense);
      
      // Show success message
      if (result.success) {
        onSubmit(expense);
        // Trigger a refresh of the expense list
        await sendMessage('Show my expenses');
      } else {
        setSubmitError(result.message || 'Failed to save expense');
      }
    } catch (error) {
      console.error('Error saving expense:', error);
      setSubmitError(error instanceof Error ? error.message : 'Failed to save expense');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setReceiptFile(file);
      setExpense({ ...expense, receipt_url: file.name });
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      setReceiptFile(file);
      setExpense({ ...expense, receipt_url: file.name });
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  return (
    <div className="h-full overflow-y-auto" style={{ backgroundColor: '#F5F3EF' }}>
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 sticky top-0 z-10">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={onCancel}
              className="text-blue-600 hover:text-blue-700 flex items-center gap-2"
            >
              <ArrowLeft size={20} />
              <span className="text-sm">Back to Summary</span>
            </button>
            <span className="text-gray-300">•</span>
            <span className="text-sm text-gray-600">Form Mode</span>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={onCancel}
              className="flex items-center gap-2 px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors border border-gray-300"
            >
              <X size={18} />
              Cancel
            </button>
            <button
              onClick={() => console.log('Save & Add Another')}
              className="flex items-center gap-2 px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors border border-blue-600"
              disabled={isSubmitting}
            >
              💾 Save & Add Another
            </button>
            <button
              onClick={handleSubmit}
              className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg disabled:bg-gray-400 disabled:cursor-not-allowed"
              disabled={isSubmitting}
            >
              {isSubmitting ? '⏳ Saving...' : '💾 Save Expense'}
            </button>
          </div>
        </div>
        
        {submitError && (
          <div className="mx-6 mb-4 bg-red-50 border border-red-200 rounded-lg p-3">
            <p className="text-sm text-red-800">❌ {submitError}</p>
          </div>
        )}
        
        <div className="mt-3 px-6">
          <h1 className="text-2xl font-bold text-gray-900">Create Expense</h1>
          <p className="text-sm text-gray-600 mt-1">Business Trip • July 2026</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="p-6 max-w-7xl mx-auto">
        <div className="grid grid-cols-12 gap-6">
          {/* Left Column - Expense Core Details */}
          <div className="col-span-12 lg:col-span-6">
            <div className="bg-white rounded-lg p-6 mb-6">
              <div className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 bg-blue-600 rounded flex items-center justify-center">
                  <span className="text-white text-xs">📋</span>
                </div>
                <h3 className="text-base font-semibold text-gray-900">Expense Core Details</h3>
                <span className="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded ml-auto">
                  {formData.expense_id || 'EXP-2026-007'}
                </span>
              </div>

              <div className="space-y-4">
                {/* Expense ID */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Expense ID (Auto-generated)
                  </label>
                  <input
                    value={formData.expense_id || expense.expense_id}
                    disabled
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-600"
                  />
                </div>

                {/* Date */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    📅 Date <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="date"
                    value={expense.date}
                    onChange={(e) => setExpense({ ...expense, date: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                  <p className="text-xs text-gray-500 mt-1">Jul 18, 2026</p>
                </div>

                {/* Category */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Category <span className="text-red-500">*</span>
                  </label>
                  <select
                    value={expense.category}
                    onChange={(e) => setExpense({ ...expense, category: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  >
                    <option value="">✈️ Flight</option>
                    {formData.categories?.map((cat: string) => (
                      <option key={cat} value={cat}>{cat}</option>
                    ))}
                  </select>
                </div>

                {/* Merchant */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    💼 Merchant / Vendor Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    value={expense.merchant}
                    onChange={(e) => setExpense({ ...expense, merchant: e.target.value })}
                    placeholder="e.g. Marriott Executive Suites, Indigo, Uber..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>

                {/* Amount */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    💰 Amount <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={expense.amount}
                    onChange={(e) => setExpense({ ...expense, amount: e.target.value })}
                    placeholder="e.g. 10000"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>

                {/* Currency */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Currency <span className="text-red-500">*</span>
                  </label>
                  <select
                    value={expense.currency}
                    onChange={(e) => setExpense({ ...expense, currency: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  >
                    {formData.currencies?.map((curr: string) => (
                      <option key={curr} value={curr}>₹ {curr}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Corporate Audit & Policy and Receipt Upload */}
          <div className="col-span-12 lg:col-span-6">
            {/* Corporate Audit & Policy */}
            <div className="bg-white rounded-lg p-6 mb-6">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-8 h-8 bg-green-600 rounded flex items-center justify-center">
                  <span className="text-white text-xs">📊</span>
                </div>
                <h3 className="text-base font-semibold text-gray-900">Corporate Audit & Policy</h3>
              </div>
              <p className="text-xs text-gray-600 mb-4">Policy Compliance Checklist</p>

              <div className="space-y-4">
                {/* Associated Trip */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    🗺️ Associated Trip
                  </label>
                  <select
                    value={expense.associated_trip}
                    onChange={(e) => setExpense({ ...expense, associated_trip: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="None">Business Trip • July 2026</option>
                    {formData.trips?.map((trip: any) => (
                      <option key={trip.id} value={trip.name}>{trip.name}</option>
                    ))}
                  </select>
                </div>

                {/* Payment Method */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Payment Method <span className="text-red-500">*</span>
                  </label>
                  <select
                    value={expense.payment_method}
                    onChange={(e) => setExpense({ ...expense, payment_method: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  >
                    <option value="">💳 Corporate Card (Ending 4090)</option>
                    {formData.payment_methods?.map((method: string) => (
                      <option key={method} value={method}>{method}</option>
                    ))}
                  </select>
                </div>

                {/* GST Amount */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    GST / Tax Amount (₹)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={expense.gst_amount}
                    onChange={(e) => setExpense({ ...expense, gst_amount: e.target.value })}
                    placeholder="Auto-calculated from bill"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                {/* Notes */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    📝 Notes / Business Purpose
                  </label>
                  <textarea
                    value={expense.notes}
                    onChange={(e) => setExpense({ ...expense, notes: e.target.value })}
                    placeholder="Specify client meeting details, purpose of trip, or exchange rate..."
                    rows={4}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  />
                </div>
              </div>
            </div>

            {/* Receipt & Invoice Upload */}
            <div className="bg-white rounded-lg p-6">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-8 h-8 bg-purple-600 rounded flex items-center justify-center">
                  <span className="text-white text-xs">📎</span>
                </div>
                <h3 className="text-base font-semibold text-gray-900">Receipt & Invoice Upload</h3>
                <span className="text-xs bg-cyan-100 text-cyan-700 px-3 py-1 rounded ml-auto">
                  🤖 OCR Ready
                </span>
              </div>
              <p className="text-xs text-gray-600 mb-4">
                Upload JPG, PNG or PDF receipts for automated line-item OCR parsing
              </p>

              <div
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                  isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-gray-50'
                }`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
              >
                {receiptFile ? (
                  <div className="flex flex-col items-center gap-3">
                    <CheckCircle2 size={48} className="text-green-600" />
                    <p className="font-medium text-gray-900">{receiptFile.name}</p>
                    <p className="text-sm text-gray-600">Receipt uploaded successfully</p>
                    <button
                      type="button"
                      onClick={() => {
                        setReceiptFile(null);
                        setExpense({ ...expense, receipt_url: '' });
                      }}
                      className="text-sm text-blue-600 hover:text-blue-700"
                    >
                      Remove file
                    </button>
                  </div>
                ) : (
                  <div className="flex flex-col items-center gap-3">
                    <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center">
                      <Upload size={32} className="text-blue-600" />
                    </div>
                    <p className="font-medium text-gray-700">Drag & drop receipt here, or browse file</p>
                    <p className="text-xs text-gray-500">
                      Receipt Agent will scan receipt and line items. MX intricates auto-filled.
                    </p>
                    <label htmlFor="receipt-upload">
                      <button
                        type="button"
                        onClick={() => document.getElementById('receipt-upload')?.click()}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg text-sm font-medium"
                      >
                        Select Receipt File
                      </button>
                    </label>
                    <input
                      id="receipt-upload"
                      type="file"
                      accept=".jpg,.jpeg,.png,.pdf"
                      onChange={handleFileChange}
                      className="hidden"
                    />
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
}
