import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { runScan } from "../lib/api";

const CHECKS = [
  { key: "ssl",              label: "Checking SSL certificate",         icon: "🔒" },
  { key: "email_security",   label: "Checking email security (SPF/DKIM/DMARC)", icon: "📧" },
  { key: "open_ports",       label: "Scanning for open ports",          icon: "🚪" },
  { key: "security_headers", label: "Checking security headers",        icon: "🛡️" },
  { key: "dns_health",       label: "Checking DNS health & blacklists", icon: "🌐" },
];

export default function Scan() {
  const location  = useLocation();
  const navigate  = useNavigate();
  const { domain, email, name } = location.state || {};

  const [completedChecks, setCompletedChecks] = useState([]);
  const [activeCheck,     setActiveCheck]     = useState(0);
  const [error,           setError]           = useState("");

  useEffect(() => {
    // Redirect back if no form data
    if (!domain || !email) {
      navigate("/");
      return;
    }
    startScan();
  }, []);

  async function startScan() {
    // Animate checks ticking off while real scan runs in background
    const interval = setInterval(() => {
      setActiveCheck((prev) => {
        const next = prev + 1;
        setCompletedChecks((c) => [...c, prev]);
        if (next >= CHECKS.length) clearInterval(interval);
        return next;
      });
    }, 900);

    try {
      const result = await runScan({ domain, email, name });
      // Wait for animation to finish before navigating
      setTimeout(() => {
        clearInterval(interval);
        navigate("/results", { state: { result, domain, email, name } });
      }, CHECKS.length * 900 + 400);
    } catch (err) {
      clearInterval(interval);
      setError(err.message || "Something went wrong. Please try again.");
    }
  }

  if (error) {
    return (
      <div style={styles.page}>
        <div style={styles.card}>
          <div style={styles.errorIcon}>⚠️</div>
          <h2 style={styles.errorTitle}>Scan failed</h2>
          <p style={styles.errorMsg}>{error}</p>
          <button style={styles.retryBtn} onClick={() => navigate("/")}>
            Try again
          </button>
        </div>
      </div>
    );
  }

  const progress = Math.round((completedChecks.length / CHECKS.length) * 100);

  return (
    <div style={styles.page}>
      <div style={styles.card}>

        {/* Logo */}
        <div style={styles.logoRow}>
          <div style={styles.logoDot} />
          <span style={styles.logoText}>ServOps</span>
        </div>

        {/* Domain */}
        <p style={styles.scanning}>Scanning</p>
        <p style={styles.domain}>{domain}</p>

        {/* Progress bar */}
        <div style={styles.barBg}>
          <div style={{ ...styles.barFill, width: `${progress}%` }} />
        </div>
        <p style={styles.progressPct}>{progress}% complete</p>

        {/* Checks list */}
        <div style={styles.checksList}>
          {CHECKS.map((c, i) => {
            const done    = completedChecks.includes(i);
            const active  = activeCheck === i && !done;
            return (
              <div key={c.key} style={styles.checkRow}>
                <div style={{
                  ...styles.checkDot,
                  background: done
                    ? "#1D9E75"
                    : active ? "#378ADD" : "rgba(255,255,255,0.1)",
                  border: active
                    ? "2px solid #378ADD"
                    : done ? "2px solid #1D9E75" : "2px solid rgba(255,255,255,0.1)",
                }}>
                  {done && (
                    <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
                      <path d="M2 5l2.5 2.5L8 3" stroke="#fff" strokeWidth="1.5"
                        strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  )}
                  {active && <div style={styles.pulse} />}
                </div>
                <span style={{
                  ...styles.checkLabel,
                  color: done ? "#1D9E75" : active ? "#fff" : "#4A6A8A",
                }}>
                  {c.icon} {c.label}
                </span>
              </div>
            );
          })}
        </div>

        <p style={styles.note}>
          Do not close this tab. Your report will be emailed to {email}.
        </p>

      </div>
    </div>
  );
}

const styles = {
  page: {
    background: "#0A1628",
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: 24,
    fontFamily: "system-ui, -apple-system, sans-serif",
  },
  card: {
    background: "rgba(255,255,255,0.04)",
    border: "0.5px solid rgba(255,255,255,0.1)",
    borderRadius: 16,
    padding: "36px 32px",
    width: "100%",
    maxWidth: 480,
    textAlign: "center",
  },
  logoRow: {
    display: "flex", alignItems: "center",
    justifyContent: "center", gap: 8, marginBottom: 28,
  },
  logoDot: {
    width: 8, height: 8,
    borderRadius: "50%", background: "#378ADD",
  },
  logoText: { fontSize: 14, fontWeight: 500, color: "#fff" },
  scanning: { fontSize: 13, color: "#4A6A8A", margin: "0 0 4px" },
  domain: {
    fontSize: 20, fontWeight: 500,
    color: "#fff", margin: "0 0 24px",
  },
  barBg: {
    background: "rgba(255,255,255,0.08)",
    borderRadius: 4, height: 6,
    overflow: "hidden", marginBottom: 8,
  },
  barFill: {
    height: "100%", borderRadius: 4,
    background: "#378ADD",
    transition: "width 0.8s ease",
  },
  progressPct: {
    fontSize: 12, color: "#4A6A8A",
    margin: "0 0 28px",
  },
  checksList: {
    display: "flex", flexDirection: "column",
    gap: 12, textAlign: "left", marginBottom: 28,
  },
  checkRow: {
    display: "flex", alignItems: "center", gap: 12,
  },
  checkDot: {
    width: 22, height: 22, borderRadius: "50%",
    flexShrink: 0,
    display: "flex", alignItems: "center",
    justifyContent: "center",
    transition: "all 0.3s ease",
    position: "relative",
  },
  pulse: {
    width: 8, height: 8, borderRadius: "50%",
    background: "#378ADD",
    animation: "pulse 1s infinite",
  },
  checkLabel: {
    fontSize: 13, transition: "color 0.3s ease",
  },
  note: {
    fontSize: 11, color: "#4A6A8A",
    lineHeight: 1.6, margin: 0,
  },
  errorIcon: { fontSize: 32, marginBottom: 12 },
  errorTitle: { fontSize: 18, color: "#fff", margin: "0 0 8px" },
  errorMsg: { fontSize: 13, color: "#7BA4C8", margin: "0 0 20px" },
  retryBtn: {
    background: "#185FA5", color: "#fff",
    border: "none", borderRadius: 8,
    padding: "10px 24px", fontSize: 13,
    cursor: "pointer",
  },
};
