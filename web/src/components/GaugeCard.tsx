import { motion } from "framer-motion";

export function GaugeCard({ title, value, subtitle, detail }: any) {
  const v = Math.max(0, Math.min(100, Number(value || 0)));

  return (
    <motion.div
      className="gauge-card"
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.03 }}
    >
      <div className="gauge-title">{title}</div>

      <div className="gauge-ring" style={{ "--value": `${v}%` } as any}>
        <div className="gauge-inner">
          <div className="gauge-value">{v.toFixed(0)}%</div>
          <div className="gauge-subtitle">{subtitle}</div>
        </div>
      </div>

      <div className="gauge-detail">{detail}</div>
    </motion.div>
  );
}
