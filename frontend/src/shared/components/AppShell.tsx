import { type PropsWithChildren } from 'react';

import { Header } from './Header';

export function AppShell({ children }: PropsWithChildren) {
  return (
    <div className="min-h-screen">
      <div className="mx-auto flex min-h-screen max-w-7xl flex-col px-4 pb-10 pt-6 sm:px-6 lg:px-8">
        <Header />
        <main className="fade-in flex-1">{children}</main>
      </div>
    </div>
  );
}
