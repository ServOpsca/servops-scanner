import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Landing() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ domain: "", name: "", email: "" });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError("");
  };

  const handleSubmit = () => {
    if (!form.domain) return setError("Please enter your business domain.");
    if (!form.name) return setError("Please enter your name.");
    if (!form.email || !form.email.includes("@"))
      return setError("Please enter a valid email address.");

    // Pass form data to the Scan page
    navigate("/scan", { state: { ...form } });
  };

  return (
    <div style={styles.page}>

      {/* NAV */}
      <nav style={styles.nav}>
        <div style={styles.navLogo}>
          <div style={styles.navDot} />
          <span style={styles.navBrand}>ServOps</span>
        </div>
        <div style={styles.navLinks}>
          <a href="#how-it-works" style={styles.navLink}>How it works</a>
          <a href="#checks" style={styles.navLink}>What we check</a>
          <a href="mailto:servopsca@gmail.com" style={styles.navCta}>Contact</a>
        </div>
      </nav>

      {/* HERO */}
      <section style={styles.hero}>
        <div style={styles.pill}>FREE IT HEALTH CHECK — NO SIGNUP REQUIRED</div>

        <h1 style={styles.h1}>
          Is your business{" "}
          <span style={styles.h1Accent}>one cyber attack</span>{" "}
          away from shutting down?
        </h1>

        <p style={styles.sub}>
          Enter your domain below. In 60 seconds we'll scan your IT security,
          find the gaps, and send you a plain-English report — completely free,
          no technical knowledge needed.
        </p>

        {/* FORM */}
        <div style={styles.formBox}>
          <p style={styles.formLabel}>Enter your business domain to get started</p>

          <input
            style={styles.input}
            type="text"
            name="domain"
            placeholder="yourbusiness.com"
            value={form.domain}
            onChange={handleChange}
          />
          <input
            style={styles.input}
            type="text"
            name="name"
            placeholder="Your name"
            value={form.name}
            onChange={handleChange}
          />
          <input
            style={styles.input}
            type="email"
            name="email"
            placeholder="Your email — report sent here"
            value={form.email}
            onChange={handleChange}
          />

          {error && <p style={styles.error}>{error}</p>}

          <button style={styles.btn} onClick={handleSubmit}>
            Run my free IT health scan →
          </button>
        </div>

        {/* TRUST STRIP */}
        <div style={styles.trustRow}>
          {[
            "No software to install",
            "No credit card required",
            "Results in under 60 seconds",
            "We never access your files",
          ].map((t) => (
            <div key={t} style={styles.trustItem}>
              <div style={styles.trustDot} />
              <span>{t}</span>
            </div>
          ))}
        </div>
      </section>

      {/* WHAT WE CHECK */}
      <section id="checks" style={styles.section}>
        <p style={styles.sectionLabel}>WHAT WE CHECK</p>
        <div style={styles.checksGrid}>
          {checks.map((c) => (
            <div key={c.title} style={styles.checkCard}>
              <div style={styles.checkIcon}>{c.icon}</div>
              <p style={styles.checkTitle}>{c.title}</p>
              <p style={styles.checkDesc}>{c.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section id="how-it-works" style={styles.section}>
        <p style={styles.sectionLabel}>HOW IT WORKS</p>
        <div style={styles.stepsRow}>
          {steps.map((s) => (
            <div key={s.num} style={styles.stepItem}>
              <div style={styles.stepNum}>{s.num}</div>
              <p style={styles.stepTitle}>{s.title}</p>
              <p style={styles.stepDesc}>{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* TESTIMONIAL */}
      <section style={styles.section}>
        <p style={styles.sectionLabel}>TRUSTED BY LOCAL BUSINESSES</p>
        <div style={styles.testimonialCard}>
          <p style={styles.testimonialText}>
            "I had no idea our email domain was unprotected. The report showed
            exactly what was wrong in plain English. ServOps fixed everything
            within 48 hours."
          </p>
          <div style={styles.testimonialAuthor}>
            <div style={styles.avatar}>CN</div>
            <div>
              <p style={styles.authorName}>CND Nailart</p>
              <p style={styles.authorLocation}>Windsor, Ontario</p>
            </div>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer style={styles.footer}>
        <span style={styles.footerText}>
          ServOps · Windsor, Ontario · servopsca.com
        </span>
        <div style={styles.footerLinks}>
          <a href="/privacy" style={styles.footerLink}>Privacy policy</a>
          <a href="mailto:servopsca@gmail.com" style={styles.footerLink}>
            servopsca@gmail.com
          </a>
        </div>
      </footer>

    </div>
  );
}

// ─── DATA ────────────────────────────────────────────────────────────────────

const checks = [
  {
    title: "SSL certificate",
    desc: "Is your website secure and trusted by browsers?",
    icon: "🔒",
  },
  {
    title: "Email security",
    desc: "Can hackers send fake emails pretending to be you?",
    icon: "📧",
  },
  {
    title: "Open ports",
    desc: "Is your server accidentally exposed to attackers?",
    icon: "🚪",
  },
  {
    title: "Security headers",
    desc: "Does your website protect visitor data?",
    icon: "🛡️",
  },
  {
    title: "DNS health",
    desc: "Is your domain on a spam blacklist?",
    icon: "🌐",
  },
];

const steps = [
  {
    num: "1",
    title: "Enter your domain",
    desc: "Type your business website address. No login, no setup.",
  },
  {
    num: "2",
    title: "We scan in 60 seconds",
    desc: "Our tool checks 5 critical security areas automatically.",
  },
  {
    num: "3",
    title: "Get your free report",
    desc: "A plain-English PDF lands in your inbox — no jargon.",
  },
];

// ─── STYLES ──────────────────────────────────────────────────────────────────

const styles = {
  page: {
    background: "#0A1628",
    minHeight: "100vh",
    color: "#fff",
    fontFamily: "system-ui, -apple-system, sans-serif",
  },
  nav: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "16px 32px",
    borderBottom: "0.5px solid rgba(255,255,255,0.08)",
  },
  navLogo: { display: "flex", alignItems: "center", gap: 8 },
  navDot: {
    width: 8, height: 8, borderRadius: "50%", background: "#378ADD",
  },
  navBrand: { fontSize: 15, fontWeight: 500, color: "#fff" },
  navLinks: { display: "flex", alignItems: "center", gap: 20 },
  navLink: { fontSize: 13, color: "#7BA4C8", textDecoration: "none" },
  navCta: {
    fontSize: 12, color: "#85B7EB", textDecoration: "none",
    border: "0.5px solid rgba(55,138,221,0.3)",
    padding: "5px 14px", borderRadius: 6,
  },
  hero: {
    maxWidth: 600, margin: "0 auto",
    padding: "56px 24px 48px", textAlign: "center",
  },
  pill: {
    display: "inline-block",
    background: "rgba(55,138,221,0.15)",
    color: "#85B7EB",
    fontSize: 11, letterSpacing: "1.5px",
    padding: "4px 14px", borderRadius: 20,
    border: "0.5px solid rgba(55,138,221,0.3)",
    marginBottom: 20,
  },
  h1: {
    fontSize: 30, fontWeight: 500, lineHeight: 1.3,
    margin: "0 0 16px", color: "#fff",
  },
  h1Accent: { color: "#378ADD" },
  sub: {
    fontSize: 14, color: "#7BA4C8", lineHeight: 1.7,
    margin: "0 0 32px",
  },
  formBox: {
    background: "rgba(255,255,255,0.05)",
    border: "0.5px solid rgba(255,255,255,0.12)",
    borderRadius: 12, padding: 20,
    maxWidth: 420, margin: "0 auto 20px",
    textAlign: "left",
  },
  formLabel: { fontSize: 12, color: "#7BA4C8", margin: "0 0 10px" },
  input: {
    width: "100%", boxSizing: "border-box",
    background: "rgba(255,255,255,0.07)",
    border: "0.5px solid rgba(255,255,255,0.15)",
    borderRadius: 8, padding: "10px 14px",
    color: "#fff", fontSize: 13, marginBottom: 10,
    outline: "none",
  },
  error: { fontSize: 12, color: "#E24B4A", margin: "0 0 10px" },
  btn: {
    width: "100%", background: "#185FA5",
    color: "#fff", border: "none", borderRadius: 8,
    padding: 12, fontSize: 14, fontWeight: 500, cursor: "pointer",
  },
  trustRow: {
    display: "flex", justifyContent: "center",
    gap: 16, flexWrap: "wrap", marginTop: 16,
  },
  trustItem: {
    display: "flex", alignItems: "center",
    gap: 6, fontSize: 12, color: "#4A6A8A",
  },
  trustDot: {
    width: 6, height: 6, borderRadius: "50%", background: "#1D9E75",
  },
  section: {
    padding: "36px 24px",
    borderTop: "0.5px solid rgba(255,255,255,0.08)",
  },
  sectionLabel: {
    textAlign: "center", fontSize: 11,
    color: "#4A6A8A", letterSpacing: "2px", marginBottom: 20,
  },
  checksGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
    gap: 12, maxWidth: 640, margin: "0 auto",
  },
  checkCard: {
    background: "rgba(255,255,255,0.04)",
    border: "0.5px solid rgba(255,255,255,0.08)",
    borderRadius: 8, padding: 16,
  },
  checkIcon: { fontSize: 20, marginBottom: 10 },
  checkTitle: { fontSize: 13, fontWeight: 500, color: "#fff", margin: "0 0 4px" },
  checkDesc: { fontSize: 11, color: "#4A6A8A", lineHeight: 1.5, margin: 0 },
  stepsRow: {
    display: "grid", gridTemplateColumns: "repeat(3, 1fr)",
    gap: 12, maxWidth: 560, margin: "0 auto",
  },
  stepItem: { textAlign: "center", padding: "16px 12px" },
  stepNum: {
    width: 28, height: 28, borderRadius: "50%",
    background: "rgba(55,138,221,0.15)",
    border: "0.5px solid rgba(55,138,221,0.3)",
    color: "#85B7EB", fontSize: 12, fontWeight: 500,
    display: "flex", alignItems: "center", justifyContent: "center",
    margin: "0 auto 10px",
  },
  stepTitle: { fontSize: 13, fontWeight: 500, color: "#fff", margin: "0 0 4px" },
  stepDesc: { fontSize: 11, color: "#4A6A8A", lineHeight: 1.5, margin: 0 },
  testimonialCard: {
    background: "rgba(255,255,255,0.04)",
    border: "0.5px solid rgba(255,255,255,0.08)",
    borderRadius: 12, padding: "18px 20px",
    maxWidth: 420, margin: "0 auto",
  },
  testimonialText: {
    fontSize: 13, color: "#CBD5E0",
    lineHeight: 1.7, fontStyle: "italic", margin: "0 0 14px",
  },
  testimonialAuthor: { display: "flex", alignItems: "center", gap: 10 },
  avatar: {
    width: 32, height: 32, borderRadius: "50%",
    background: "rgba(55,138,221,0.2)",
    display: "flex", alignItems: "center", justifyContent: "center",
    fontSize: 12, fontWeight: 500, color: "#85B7EB",
  },
  authorName: { fontSize: 12, fontWeight: 500, color: "#fff", margin: 0 },
  authorLocation: { fontSize: 11, color: "#4A6A8A", margin: 0 },
  footer: {
    borderTop: "0.5px solid rgba(255,255,255,0.08)",
    padding: "20px 32px",
    display: "flex", justifyContent: "space-between",
    alignItems: "center", flexWrap: "wrap", gap: 8,
  },
  footerText: { fontSize: 11, color: "#4A6A8A" },
  footerLinks: { display: "flex", gap: 16 },
  footerLink: { fontSize: 11, color: "#4A6A8A", textDecoration: "none" },
};
