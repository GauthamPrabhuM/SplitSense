import { Github, Heart } from 'lucide-react';
import { BuyMeCoffee } from '@/components/buy-me-coffee';

export function Footer() {
  return (
    <footer className="border-t bg-muted/30">
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
          {/* Left */}
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span>Built with</span>
            <Heart className="h-4 w-4 text-destructive" fill="currentColor" />
            <span>for better expense tracking</span>
          </div>

          {/* Center */}
          <BuyMeCoffee variant="footer" />

          {/* Right */}
          <div className="flex items-center gap-4">
            <a
              href="https://github.com/GauthamPrabhuM/SplitSense"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              <Github className="h-4 w-4" />
              <span>GitHub</span>
            </a>
            <span className="text-sm text-muted-foreground">
              © {new Date().getFullYear()} SplitSense
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}
