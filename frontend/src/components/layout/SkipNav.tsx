export function SkipNav() {
  return (
    <a
      href="#main-content"
      className="sr-only focus:not-sr-only focus:fixed focus:top-0 focus:left-0 focus:z-40 focus:w-auto focus:h-auto focus:p-4 focus:bg-brand-primary focus:text-white focus:rounded-md transition-all duration-200"
      data-testid="skip-nav-link"
    >
      Skip to main content
    </a>
  );
}
