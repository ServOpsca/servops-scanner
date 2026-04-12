import { useLocation, useNavigate } from "react-router-dom";

const STATUS_COLORS = {
  pass: { bg: "#0F3D2E", border: "#1D9E75", text: "#4ADE80", badge: "#052E1A" },
  warn: { bg: "#3D2E0F", border: "#EF9F27", text: "#FCD34D", badge: "#2E1F05" },
  fail: { bg: "#3D0F0F", border: "#E24B4A", text: "#FCA5A5", badge: "#2E0505" },
};

const STATUS_LABELS = {
  pass: "Passing",
  warn: "Warning",
  fail: "Critical",
};

const SCORE_COLORS = {
  pass: "#1D9E75",
  warn: "#EF9F27",
  fail: "#E24B4A",
};

export default function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const { result, domain } = location.state || {};

  if (!result) {
    return (
      <div style={styles.page}>
        <div style={styles.center}>
          <p style={{ color: "#7BA4C8" }}>No scan data found.</p>
          <button style={styles.backBtn} onClick={() => navigate("/")}>
            Run a new scan
          </button>
        </div>
      </div>
    );
  }

  const { score, results } = result;
  const scoreColor = SCORE_COLORS[score.status];

  return (
    <div style={styles.page}>

      {/* NAV */}
      <nav style={styles.nav}>
        <div style={styles.logoRow}>
          <div style={styles.logoDot} />
          <span style={styles.logoText}>ServOps</span>
        </div>
        <button style={styles.newScanBtn} onClick={() => navigate("/")}>
          Scan another domain
        </button>
      </nav>

      <div style={styles.content}>

        {/* SCORE HEADER */}
        <div style={styles.scoreHeader}>
          <div>
            <p style={styles.scanLabel}>IT health report for</p>
            <h1 style={styles.domainTitle}>{domain}</h1>
          </div>
          <div style={styles.scoreCircle}>
            <span style={{ ...styles.scoreNum, color: scoreColor }}>
              {score.total_score}
            </span>
            <span style={styles.scoreMax}>/100</span>
            <span style={{ ...styles.scoreLabel, color: scoreColor }}>
              {score.label}
            </span>
          </div>
        </div>

        {/* SUMMARY TILES */}
        <div style={styles.tilesRow}>
          <div style={{ ...styles.tile, borderColor: "#E24B4A" }}>
            <span style={{ ...styles.tileNum, color: "#E24B4A" }}>
              {score.critical}
            </span>
            <span style={styles.tileLabel}>Critical</span>
          </div>
          <div style={{ ...styles.tile, borderColor: "#EF9F27" }}>
            <span style={{ ...styles.tileNum, color: "#EF9F27" }}>
              {score.warnings}
            </span>
            <span style={styles.tileLabel}>Warnings</span>
          </div>
          <div style={{ ...styles.tile, borderColor: "#1D9E75" }}>
            <span style={{ ...styles.tileNum, color: "#1D9E75" }}>
              {score.passing}
            </span>
            <span style={styles.tileLabel}>Passing</span>
          </div>
        </div>

        {/* PLAIN ENGLISH SUMMARY */}
        <div style={styles.summaryBox}>
          <p style={styles.summaryTitle}>What this means for your business</p>
          <p style={styles.summaryText}>
            Your IT health score is{" "}
            <span style={{ color: scoreColor, fontWeight: 500 }}>
              {score.total_score} out of 100
            </span>
            .{" "}
            {score.status === "fail" &&
              "Your business has several security gaps that need immediate attention."}
            {score.status === "warn" &&
              "Your business has some security gaps that should be addressed soon."}
            {score.status === "pass" &&
              "Your business has a healthy IT posture. Keep it up."}
            {score.critical > 0 &&
              ` ${score.critical} critical issue${score.critical > 1 ? "s" : ""} require immediate action.`}
          </p>
        </div>

        {/* FINDINGS */}
        <div style={styles.section}>
          <p style={styles.sectionLabel}>DETAILED FINDINGS</p>
          <div style={styles.findingsList}>
            {results.map((r) => {
              const c = STATUS_COLORS[r.status];
              return (
                <div key={r.check} style={{
                  ...styles.findingCard,
                  background: c.bg,
                  borderColor: c.border,
                }}>
                  <div style={styles.findingHeader}>
                    <span style={{
                      ...styles.findingBadge,
                      background: c.badge,
                      color: c.text,
                      border: `0.5px solid ${c.border}`,
                    }}>
                      {STATUS_LABELS[r.status]}
                    </span>
                    <span style={styles.findingTitle}>{r.label}</span>
                    <span style={{ ...styles.findingScore, color: c.text }}>
                      {r.score}/100
                    </span>
                  </div>
                  <p style={styles.findingText}>{r.plain_english}</p>
                </div>
              );
            })}
          </div>
        </div>

        {/* SCORE BARS */}
        <div style={styles.section}>
          <p style={styles.sectionLabel}>SCORE BREAKDOWN</p>
          <div style={styles.barsList}>
            {results.map((r) => {
              const c = STATUS_COLORS[r.status];
              return (
                <div key={r.check} style={styles.barRow}>
                  <span style={styles.barLabel}>{r.label}</span>
                  <div style={styles.barBg}>
                    <div style={{
                      ...styles.barFill,
                      width: `${r.score}%`,
                      background: c.border,
                    }} />
                  </div>
                  <span style={{ ...styles.barPct, color: c.text }}>
                    {r.score}%
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* CTA */}
        <div style={styles.ctaBox}>
          <p style={styles.ctaEyebrow}>Your next step</p>
          <h2 style={styles.ctaTitle}>Want us to fix these issues for you?</h2>
          <p style={styles.ctaText}>
            ServOps can resolve all critical and warning issues within 48 hours.
            Book a free 15-minute call — no obligation, no technical jargon.
          </p>
          <a
            href="mailto:servopsca@gmail.com?subject=IT Health Report — Fix Request"
            style={styles.ctaBtn}
          >
            Book a free call with ServOps →
          </a>
          <p style={styles.ctaFooter}>
            ServOps · Windsor, Ontario · servopsca.com · +1 (519) 992-8997
          </p>
        </div>

        {/* NEW SCAN */}
        <div style={styles.newScanRow}>
          <button style={styles.newScanLink} onClick={() => navigate("/")}>
            ← Scan another domain
          </button>
        </div>

      </div>
    </div>
  );
}

const styles = {
  page: {
    background: "#0A1628",
    minHeight: "100vh",
    fontFamily: "system-ui, -apple-system, sans-serif",
    color: "#fff",
  },
  center: {
    display: "flex", flexDirection: "column",
    alignItems: "center", justifyContent: "center",
    minHeight: "100vh", gap: 16,
  },
  nav: {
    display: "flex", justifyContent: "space-between",
    alignItems: "center", padding: "16px 24px",
    borderBottom: "0.5px solid rgba(255,255,255,0.08)",
  },
  logoRow: { display: "flex", alignItems: "center", gap: 8 },
  logoDot: { width: 8, height: 8, borderRadius: "50%", background: "#378ADD" },
  logoText: { fontSize: 14, fontWeight: 500, color: "#fff" },
  newScanBtn: {
    background: "transparent",
    border: "0.5px solid rgba(255,255,255,0.15)",
    color: "#7BA4C8", fontSize: 12,
    padding: "6px 14px", borderRadius: 6, cursor: "pointer",
  },
  content: { maxWidth: 600, margin: "0 auto", padding: "32px 24px" },
  scoreHeader: {
    display: "flex", justifyContent: "space-between",
    alignItems: "flex-start", marginBottom: 24,
    background: "#0F2744", borderRadius: 12,
    padding: "24px",
  },
  scanLabel: { fontSize: 12, color: "#7BA4C8", margin: "0 0 4px" },
  domainTitle: { fontSize: 20, fontWeight: 500, color: "#fff", margin: 0 },
  scoreCircle: {
    display: "flex", flexDirection: "column",
    alignItems: "center", gap: 2,
  },
  scoreNum: { fontSize: 36, fontWeight: 500, lineHeight: 1 },
  scoreMax: { fontSize: 12, color: "#4A6A8A" },
  scoreLabel: { fontSize: 11, fontWeight: 500, letterSpacing: "1px" },
  tilesRow: {
    display: "grid", gridTemplateColumns: "1fr 1fr 1fr",
    gap: 10, marginBottom: 20,
  },
  tile: {
    background: "rgba(255,255,255,0.03)",
    border: "0.5px solid",
    borderRadius: 10, padding: "14px",
    display: "flex", flexDirection: "column",
    alignItems: "center", gap: 4,
  },
  tileNum: { fontSize: 24, fontWeight: 500 },
  tileLabel: { fontSize: 11, color: "#4A6A8A" },
  summaryBox: {
    background: "rgba(255,255,255,0.03)",
    border: "0.5px solid rgba(255,255,255,0.08)",
    borderRadius: 10, padding: "16px 18px", marginBottom: 24,
  },
  summaryTitle: {
    fontSize: 11, color: "#4A6A8A",
    letterSpacing: "1.5px", margin: "0 0 8px",
  },
  summaryText: { fontSize: 13, color: "#CBD5E0", lineHeight: 1.7, margin: 0 },
  section: { marginBottom: 24 },
  sectionLabel: {
    fontSize: 11, color: "#4A6A8A",
    letterSpacing: "2px", margin: "0 0 12px",
  },
  findingsList: { display: "flex", flexDirection: "column", gap: 10 },
  findingCard: {
    border: "0.5px solid",
    borderRadius: 10, padding: "14px 16px",
  },
  findingHeader: {
    display: "flex", alignItems: "center",
    gap: 10, marginBottom: 8, flexWrap: "wrap",
  },
  findingBadge: {
    fontSize: 10, fontWeight: 500,
    padding: "3px 10px", borderRadius: 20,
    letterSpacing: "0.5px",
  },
  findingTitle: { fontSize: 13, fontWeight: 500, color: "#fff", flex: 1 },
  findingScore: { fontSize: 12, fontWeight: 500 },
  findingText: { fontSize: 12, color: "#CBD5E0", lineHeight: 1.6, margin: 0 },
  barsList: { display: "flex", flexDirection: "column", gap: 10 },
  barRow: { display: "flex", alignItems: "center", gap: 10 },
  barLabel: { fontSize: 12, color: "#7BA4C8", width: 130, flexShrink: 0 },
  barBg: {
    flex: 1, height: 6, borderRadius: 4,
    background: "rgba(255,255,255,0.08)", overflow: "hidden",
  },
  barFill: { height: "100%", borderRadius: 4, transition: "width 1s ease" },
  barPct: { fontSize: 11, fontWeight: 500, width: 36, textAlign: "right" },
  ctaBox: {
    background: "#0F2744", borderRadius: 12,
    padding: "28px 24px", textAlign: "center",
    marginBottom: 20,
  },
  ctaEyebrow: { fontSize: 12, color: "#7BA4C8", margin: "0 0 6px" },
  ctaTitle: { fontSize: 18, fontWeight: 500, color: "#fff", margin: "0 0 10px" },
  ctaText: {
    fontSize: 13, color: "#7BA4C8",
    lineHeight: 1.7, margin: "0 0 20px",
  },
  ctaBtn: {
    display: "inline-block",
    background: "#185FA5", color: "#fff",
    textDecoration: "none", borderRadius: 8,
    padding: "12px 24px", fontSize: 14, fontWeight: 500,
  },
  ctaFooter: { fontSize: 11, color: "#4A6A8A", margin: "16px 0 0" },
  newScanRow: { textAlign: "center" },
  newScanLink: {
    background: "transparent", border: "none",
    color: "#4A6A8A", fontSize: 13, cursor: "pointer",
  },
  backBtn: {
    background: "#185FA5", color: "#fff",
    border: "none", borderRadius: 8,
    padding: "10px 24px", fontSize: 13, cursor: "pointer",
  },
};
