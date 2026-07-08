import { forwardRef } from 'react';
import { cn } from '@/lib/utils';

/**
 * Textarea component with proper focus states and accessibility
 * @param {React.TextareaHTMLAttributes<HTMLTextAreaElement>} props - Standard textarea props
 * @param {string} [props.className] - Additional CSS classes
 * @param {boolean} [props.disabled] - Whether the textarea is disabled
 * @param {string} [props.placeholder] - Placeholder text
 * @param {string} [props.value] - Textarea value
 * @param {function} [props.onChange] - Change handler
 * @param {function} [props.onBlur] - Blur handler
 * @param {function} [props.onFocus] - Focus handler
 * @returns {JSX.Element} Textarea component
 */
const Textarea = forwardRef<HTMLTextAreaElement, React.TextareaHTMLAttributes<HTMLTextAreaElement>>(
  ({ className, ...props }, ref) => {
    return (
      <textarea
        className={cn(
          'flex min-h-[80px] w-full rounded-md border border-brand-muted bg-transparent px-3 py-2 text-sm ring-offset-background placeholder:text-brand-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-primary focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
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
Textarea.displayName = 'Textarea';

export { Textarea };