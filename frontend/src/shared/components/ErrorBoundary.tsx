import type { PropsWithChildren, ReactNode } from 'react';
import { Component } from 'react';

import { ErrorState } from './ErrorState';

type ErrorBoundaryState = {
  hasError: boolean;
};

export class ErrorBoundary extends Component<
  PropsWithChildren,
  ErrorBoundaryState
> {
  state: ErrorBoundaryState = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  override render(): ReactNode {
    if (this.state.hasError) {
      return (
        <div className="mx-auto max-w-3xl px-4 py-16">
          <ErrorState
            title="Unexpected frontend error"
            message="The page crashed unexpectedly. Refreshing the page usually clears transient issues."
          />
        </div>
      );
    }

    return this.props.children;
  }
}
