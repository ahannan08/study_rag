import { Link, Navigate } from "react-router-dom";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { useAuth } from "@/context/AuthContext";
import { useState } from "react";

export function LoginPage() {
  const { login, user } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  if (user) return <Navigate to="/" replace />;

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await login(email, password);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-ink-950 via-ink-800 to-accent/80 p-4">
      <Card className="w-full max-w-md border-0 shadow-2xl">
        <h1 className="font-display text-2xl font-bold text-ink-950">Welcome back</h1>
        <p className="mt-1 text-sm text-ink-500">Sign in to your study library</p>
        <form className="mt-6 space-y-4" onSubmit={(e) => void submit(e)}>
          <div>
            <label className="mb-1 block text-sm font-medium text-ink-700">Email</label>
            <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required autoComplete="email" />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-ink-700">Password</label>
            <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required autoComplete="current-password" />
          </div>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <Button type="submit" className="w-full" loading={loading}>
            Sign in
          </Button>
        </form>
        <p className="mt-4 text-center text-sm text-ink-500">
          No account?{" "}
          <Link to="/register" className="font-semibold text-accent hover:underline">
            Register
          </Link>
        </p>
      </Card>
    </div>
  );
}
