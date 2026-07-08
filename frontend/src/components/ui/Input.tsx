import { forwardRef } from 'react';
import { cn } from '@/lib/utils';

/**
 * Input component with proper focus states and accessibility
 * @param {React.InputHTMLAttributes<HTMLInputElement>} props - Standard input props
 * @param {string} [props.className] - Additional CSS classes
 * @param {string} [props.type] - Input type (text, password, email, etc.)
 * @param {boolean} [props.disabled] - Whether the input is disabled
 * @param {string} [props.placeholder] - Placeholder text
 * @param {string} [props.value] - Input value
 * @param {function} [props.onChange] - Change handler
 * @param {function} [props.onBlur] - Blur handler
 * @param {function} [props.onFocus] - Focus handler
 * @returns {JSX.Element} Input component
 */
const Input = forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, type = 'text', ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          'flex h-10 w-full rounded-md border border-brand-muted bg-transparent px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-brand-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-primary focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
          className
        )}
        ref={ref}
        {...props}
        aria-invalid={props['aria-invalid'] || undefined}
        aria-describedby={props['aria-describedby'] || undefined}
      />
    );
  }
);
Input.displayName = 'Input';

export { Input };