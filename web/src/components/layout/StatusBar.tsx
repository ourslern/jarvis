export function StatusBar({ live, connected }: any) {
  const sys = live?.system;
  const gpu = live?.gpu;
  const docker = live?.docker;

  return (
    <div className="status-bar">
      <span>{connected ? "🟢 Jarvis Live" : "🔴 Jarvis Offline"}</span>
      <span>CPU {sys?.cpu_percent ?? 0}%</span>
      <span>RAM {sys?.ram_percent ?? 0}%</span>
      <span>GPU {gpu?.util_percent ?? 0}%</span>
      <span>VRAM {gpu?.memory_used_mb ?? 0} MB</span>
      <span>Docker {docker?.running ?? 0}/{docker?.total ?? 0}</span>
    </div>
  );
}
