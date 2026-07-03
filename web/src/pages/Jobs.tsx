import { useEffect, useState } from "react";
import { Header } from "../components/layout/Header";
import { getJobs } from "../api/jarvis";

export function Jobs() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [error, setError] = useState("");

  async function refresh() {
    try {
      const data = await getJobs();
      setJobs(Array.isArray(data) ? data : []);
      setError("");
    } catch (err: any) {
      setError(err.message || String(err));
    }
  }

  useEffect(() => {
    refresh();
    const timer = setInterval(refresh, 2000);
    return () => clearInterval(timer);
  }, []);

  return (
    <>
      <Header title="Background Jobs" subtitle="Downloads, benchmarks, and long-running tasks" />

      {error && (
        <div className="card">
          <h3>Jobs error</h3>
          <p style={{ color: "#ff7777" }}>{error}</p>
        </div>
      )}

      {jobs.length === 0 && !error && (
        <div className="card">
          <h3>No jobs running</h3>
          <p>Everything is idle.</p>
        </div>
      )}

      <section className="grid">
        {jobs.map((job) => (
          <div className="card" key={job.id}>
            <h3>{job.name}</h3>
            <p>Status: {job.status}</p>
            <progress value={job.progress ?? 0} max={100} style={{ width: "100%" }} />
            <p>{job.message}</p>
            {job.error && <p style={{ color: "#ff7777" }}>{job.error}</p>}
          </div>
        ))}
      </section>
    </>
  );
}
