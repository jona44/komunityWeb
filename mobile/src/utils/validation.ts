/**
 * Utility functions for input validation in the Komunity app.
 */

export const validatePhone = (phone: string): string | null => {
    if (!phone) return null; // Optional field
    const phoneRegex = /^\+?[1-9]\d{1,14}$/;
    if (!phoneRegex.test(phone.replace(/\s/g, ''))) {
        return 'Please enter a valid phone number (e.g., +1234567890).';
    }
    return null;
};

export const validateAmount = (amount: string, min = 0, max?: number): string | null => {
    if (!amount) return 'Amount is required.';
    const num = parseFloat(amount);
    if (isNaN(num)) return 'Please enter a valid number.';
    if (num <= min) return `Amount must be greater than ${min}.`;
    if (max !== undefined && num > max) return `Amount cannot exceed ${max}.`;
    return null;
};

export const validateEmail = (email: string): string | null => {
    if (!email) return 'Email is required.';
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        return 'Please enter a valid email address.';
    }
    return null;
};

export const validateName = (name: string, fieldName = 'Name'): string | null => {
    if (!name || !name.trim()) return `${fieldName} is required.`;
    if (name.trim().length < 2) return `${fieldName} must be at least 2 characters.`;
    return null;
};

export const validatePassword = (password: string): string | null => {
    if (!password) return 'Password is required.';
    if (password.length < 8) return 'Password must be at least 8 characters.';
    return null;
};

export const validateDateOfBirth = (dob: Date | null): string | null => {
    if (!dob) return null; // Optional
    const today = new Date();
    const age = today.getFullYear() - dob.getFullYear();
    const m = today.getMonth() - dob.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) {
        // age--;
    }
    if (dob > today) return 'Date of birth cannot be in the future.';
    return null;
};
