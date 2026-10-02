import { BookOpen, Layers, LogOut, MessageSquare, Sparkles } from "lucide-react";
import { NavLink } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { cn } from "@/lib/cn";
import { Button } from "@/components/ui/Button";

const links = [
  { to: "/app", label: "Library", icon: BookOpen },
  { to: "/app/review", label: "Review", icon: Layers },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-br from-ink-50 via-white to-accent-muted/30">
      <header className="sticky top-0 z-40 border-b border-ink-100/80 bg-white/70 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-accent text-white shadow-glow">
              <Sparkles className="h-5 w-5" />
            </div>
            <div>
              <p className="font-display text-lg font-bold leading-tight text-ink-950">Study RAG</p>
              <p className="text-xs text-ink-500">Grounded in your documents</p>
            </div>
          </div>
          <nav className="hidden items-center gap-1 sm:flex">
            {links.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                end={to === "/app"}
                className={({ isActive }) =>
                  cn(
                    "flex items-center gap-2 rounded-xl px-3 py-2 text-sm font-medium transition",
                    isActive ? "bg-ink-950 text-white" : "text-ink-600 hover:bg-ink-100",
                  )
                }
              >
                <Icon className="h-4 w-4" />
                {label}
              </NavLink>
            ))}
          </nav>
          <div className="flex items-center gap-3">
            <span className="hidden max-w-[140px] truncate text-sm text-ink-500 sm:inline">{user?.email}</span>
            <Button variant="ghost" onClick={logout} aria-label="Log out">
              <LogOut className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6">{children}</main>
      <nav className="fixed bottom-0 left-0 right-0 flex border-t border-ink-100 bg-white/95 p-2 sm:hidden">
        {links.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === "/app"}
            className={({ isActive }) =>
              cn(
                "flex flex-1 flex-col items-center gap-1 rounded-lg py-2 text-xs font-medium",
                isActive ? "text-accent" : "text-ink-500",
              )
            }
          >
            <Icon className="h-5 w-5" />
            {label}
          </NavLink>
        ))}
        <NavLink to="/app" className="flex flex-1 flex-col items-center gap-1 rounded-lg py-2 text-xs text-ink-500">
          <MessageSquare className="h-5 w-5" />
          Chat
        </NavLink>
      </nav>
    </div>
  );
}
