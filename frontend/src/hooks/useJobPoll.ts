import { useEffect, useRef, useState } from "react";
import { jobsApi } from "@/api";
import type { Job } from "@/types/api";

export function useJobPoll(jobId: string | null, onComplete?: () => void) {
  const [job, setJob] = useState<Job | null>(null);
  const [error, setError] = useState<string | null>(null);
  const doneRef = useRef(false);

  useEffect(() => {
    if (!jobId) {
      setJob(null);
      return;
    }
    doneRef.current = false;
    let cancelled = false;
    const tick = async () => {
      try {
        const j = await jobsApi.get(jobId);
        if (cancelled) return;
        setJob(j);
        if (j.status === "completed" || j.status === "failed") {
          if (!doneRef.current) {
            doneRef.current = true;
            onComplete?.();
          }
          return;
        }
        window.setTimeout(tick, 1500);
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : "Job poll failed");
      }
    };
    void tick();
    return () => {
      cancelled = true;
    };
  }, [jobId, onComplete]);

  return { job, error };
}
