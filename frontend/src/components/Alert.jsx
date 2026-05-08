import React, { useEffect } from 'react';
import '../styles/components.css';

const Alert = ({ type = 'info', message, onClose, autoClose = true }) => {
  useEffect(() => {
    if (autoClose) {
      const timer = setTimeout(onClose, 3000);
      return () => clearTimeout(timer);
    }
  }, [autoClose, onClose]);

  return (
    <div className={`alert alert-${type}`}>
      <div className="alert-message">{message}</div>
      <button
        type="button"
        className="alert-close"
        onClick={onClose}
      >
        ✕
      </button>
    </div>
  );
};

export default Alert;
