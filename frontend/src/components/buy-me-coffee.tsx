'use client';

import { motion } from 'framer-motion';
import { Coffee, Sparkles } from 'lucide-react';
import { Button } from './ui/button';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from './ui/tooltip';

const BUY_ME_A_COFFEE_URL = 'https://buymeacoffee.com/gauthamprabhum';

interface BuyMeCoffeeProps {
  variant?: 'header' | 'footer' | 'floating';
}

export function BuyMeCoffee({ variant = 'header' }: BuyMeCoffeeProps) {
  if (variant === 'floating') {
    return (
      <motion.a
        href={BUY_ME_A_COFFEE_URL}
        target="_blank"
        rel="noopener noreferrer"
        className="fixed bottom-6 right-6 z-50 flex items-center gap-2 rounded-full bg-[#FFDD00] px-4 py-3 text-sm font-semibold text-black shadow-lg transition-all hover:scale-105 hover:shadow-xl focus-ring"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1, duration: 0.4 }}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.98 }}
      >
        <Coffee className="h-5 w-5" />
        <span className="hidden sm:inline">Buy me a coffee</span>
      </motion.a>
    );
  }

  if (variant === 'footer') {
    return (
      <a
        href={BUY_ME_A_COFFEE_URL}
        target="_blank"
        rel="noopener noreferrer"
        className="group inline-flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
      >
        <Coffee className="h-4 w-4 transition-transform group-hover:scale-110" />
        <span>Support this project</span>
      </a>
    );
  }

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <motion.a
            href={BUY_ME_A_COFFEE_URL}
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Button
              variant="outline"
              size="sm"
              className="gap-2 border-[#FFDD00]/30 bg-[#FFDD00]/10 text-foreground hover:border-[#FFDD00] hover:bg-[#FFDD00] hover:text-black"
            >
              <Coffee className="h-4 w-4" />
              <span className="hidden sm:inline">Buy me a coffee</span>
            </Button>
          </motion.a>
        </TooltipTrigger>
        <TooltipContent>
          <p className="flex items-center gap-1.5">
            <Sparkles className="h-3 w-3" />
            Support the development
          </p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
