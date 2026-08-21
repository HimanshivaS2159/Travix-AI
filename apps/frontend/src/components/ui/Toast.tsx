import React, { useEffect, useState } from 'react';
import { CheckCircle, XCircle, AlertCircle, X } from 'lucide-react';

export type ToastType = 'success' | 'error' | 'info';

interface ToastProps {
  message: string;
  type: ToastType;
  duration?: number;
  onClose: () => void;
}

export function Toast({ message, type, duration = 3000, onClose }: ToastProps) {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false);
      setTimeout(onClose, 300); // Wait for fade out animation
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  const icons = {
    success: <CheckCircle className="w-5 h-5 text-green-600" />,
    error: <XCircle className="w-5 h-5 text-red-600" />,
    info: <AlertCircle className="w-5 h-5 text-blue-600" />,
  };

  const styles = {
    success: 'bg-green-50 border-green-200 text-green-800',
    error: 'bg-red-50 border-red-200 text-red-800',
    info: 'bg-blue-50 border-blue-200 text-blue-800',
  };

  return (
    <div
      className={`fixed top-4 right-4 z-50 min-w-[300px] max-w-[500px] border rounded-lg shadow-lg p-4 transition-all duration-300 ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2'
      } ${styles[type]}`}
    >
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 mt-0.5">{icons[type]}</div>
        <p className="flex-1 text-sm font-medium">{message}</p>
        <button
          onClick={() => {
            setIsVisible(false);
            setTimeout(onClose, 300);
          }}
          className="flex-shrink-0 hover:opacity-70 transition-opacity"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}

// Toast Manager Component
interface ToastMessage {
  id: string;
  message: string;
  type: ToastType;
}

export function ToastContainer() {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  // Expose showToast globally
  useEffect(() => {
    (window as any).showToast = (message: string, type: ToastType = 'info') => {
      const id = Math.random().toString(36).substr(2, 9);
      setToasts((prev) => [...prev, { id, message, type }]);
    };

    return () => {
      delete (window as any).showToast;
    };
  }, []);

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  };

  return (
    <>
      {toasts.map((toast, index) => (
        <div key={toast.id} style={{ top: `${16 + index * 80}px` }} className="fixed right-4 z-50">
          <Toast message={toast.message} type={toast.type} onClose={() => removeToast(toast.id)} />
        </div>
      ))}
    </>
  );
}

// Helper function to show toast
export const showToast = (message: string, type: ToastType = 'info') => {
  if ((window as any).showToast) {
    (window as any).showToast(message, type);
  }
};
