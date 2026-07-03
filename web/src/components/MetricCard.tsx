import { motion } from "framer-motion";

export function MetricCard({ title, value, subtitle, icon }: any) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.03 }}
      transition={{ duration: 0.25 }}
      className="card metric-card"
    >
      <div className="metric-header">
        <span>{icon}</span>
        <span>{title}</span>
      </div>
      <div className="metric-value">{value}</div>
      <div className="metric-subtitle">{subtitle}</div>
    </motion.div>
  );
}
