import { cn } from "@/lib/cn";
import type { ReactNode } from "react";

export function Card({ className, children }: { className?: string; children: ReactNode }) {
  return (
    <div className={cn("rounded-2xl border border-ink-100 bg-white/90 p-6 shadow-card backdrop-blur-sm", className)}>
      {children}
    </div>
  );
}
