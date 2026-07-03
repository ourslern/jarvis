import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

export function LiveLineChart({ title, data, dataKey, suffix = "%" }: any) {
  return (
    <div className="card">
      <h2>{title}</h2>
      <div className="chart-wrap">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid stroke="rgba(255,255,255,.08)" />
            <XAxis dataKey="time" hide />
            <YAxis stroke="#8f9bb3" width={40} />
            <Tooltip
              contentStyle={{
                background: "#0b1020",
                border: "1px solid rgba(255,255,255,.14)",
                borderRadius: "12px",
                color: "#e8eefc",
              }}
              formatter={(value: any) => [`${Number(value).toFixed(1)}${suffix}`, title]}
            />
            <Line
              type="monotone"
              dataKey={dataKey}
              stroke="#59f3ff"
              strokeWidth={3}
              dot={false}
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
