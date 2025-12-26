'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import {
  Wallet,
  Github,
  Menu,
  X,
} from 'lucide-react';
import { useState } from 'react';
import { Button } from '../ui/button';
import { BuyMeCoffee } from '../buy-me-coffee';
import { cn } from '../../lib/utils';

export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 w-full border-b bg-background/80 backdrop-blur-lg">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2.5">
          <motion.div
            className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-primary to-purple-600"
            whileHover={{ scale: 1.05, rotate: 5 }}
            whileTap={{ scale: 0.95 }}
          >
            <Wallet className="h-5 w-5 text-white" />
          </motion.div>
          <div className="flex flex-col">
            <span className="text-lg font-bold tracking-tight text-gradient">
              SplitSense
            </span>
            <span className="hidden text-2xs text-muted-foreground sm:block">
              Splitwise Analytics
            </span>
          </div>
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden items-center gap-1 md:flex">
          <NavLink href="/">Dashboard</NavLink>
          <NavLink href="/groups">Groups</NavLink>
          <NavLink href="/friends">Friends</NavLink>
          <NavLink href="/insights">Insights</NavLink>
        </nav>

        {/* Actions */}
        <div className="flex items-center gap-3">
          <BuyMeCoffee variant="header" />
          
          <a
            href="https://github.com/GauthamPrabhuM/SplitSense"
            target="_blank"
            rel="noopener noreferrer"
            className="hidden text-muted-foreground transition-colors hover:text-foreground md:block"
          >
            <Github className="h-5 w-5" />
          </a>

          {/* Mobile menu button */}
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? (
              <X className="h-5 w-5" />
            ) : (
              <Menu className="h-5 w-5" />
            )}
          </Button>
        </div>
      </div>

      {/* Mobile menu */}
      <motion.div
        initial={false}
        animate={{
          height: mobileMenuOpen ? 'auto' : 0,
          opacity: mobileMenuOpen ? 1 : 0,
        }}
        className="overflow-hidden border-t md:hidden"
      >
        <nav className="flex flex-col gap-1 p-4">
          <MobileNavLink href="/" onClick={() => setMobileMenuOpen(false)}>
            Dashboard
          </MobileNavLink>
          <MobileNavLink href="/groups" onClick={() => setMobileMenuOpen(false)}>
            Groups
          </MobileNavLink>
          <MobileNavLink href="/friends" onClick={() => setMobileMenuOpen(false)}>
            Friends
          </MobileNavLink>
          <MobileNavLink href="/insights" onClick={() => setMobileMenuOpen(false)}>
            Insights
          </MobileNavLink>
        </nav>
      </motion.div>
    </header>
  );
}

function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <Link
      href={href}
      className={cn(
        'rounded-md px-3 py-2 text-sm font-medium text-muted-foreground transition-colors',
        'hover:bg-accent hover:text-foreground',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring'
      )}
    >
      {children}
    </Link>
  );
}

function MobileNavLink({
  href,
  onClick,
  children,
}: {
  href: string;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <Link
      href={href}
      onClick={onClick}
      className="rounded-md px-4 py-3 text-sm font-medium text-foreground transition-colors hover:bg-accent"
    >
      {children}
    </Link>
  );
}
