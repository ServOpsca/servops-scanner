import { useNavigate } from "react-router-dom";

const STRIPE_LINKS = {
  fix:        "https://buy.stripe.com/4gMbJ1aJ44Hh1Jz3M34wM03",
  monitoring: "https://buy.stripe.com/7sYfZh6sOehRfAp2HZ4wM01",
  msp:        "https://buy.stripe.com/8x214n2cyehR2ND6Yf4wM02",
};

const plans = [
  {
    name:     "Free scan",
    desc:     "See exactly where your IT stands.",
    price:    "$0",
    per:      "/ scan",
    featured: false,
    href:     "/",
    cta:      "Run a free scan →",
    features: [
      "5-check domain scan",
      "Plain-English PDF report",
      "Risk score out of 100",
      "Emailed to your inbox",
    ],
  },
  {
    name:     "Fix it for me",
    desc:     "We resolve every issue within 48 hours.",
    price:    "$200",
    per:      "/ one-time",
    featured: true,
    href:     STRIPE_LINKS.fix,
    cta:      "Get started →",
    external: true,
    features: [
      "Everything in Free",
      "48-hr issue remediation",
      "Re-scan to confirm fixes",
      "30-day email support",
      "Written fix documentation",
    ],
  },
  {
    name:     "Stay protected",
    desc:     "Monthly monitoring so issues are caught early.",
    price:    "$97",
    per:      "/ month",
    featured: false,
    href:     STRIPE_LINKS.monitoring,
    cta:      "Start monitoring →",
    external: true,
    features: [
      "Everything in Fix it for me",
      "Monthly automated scan",
      "Email alert on new issues",
      "Quarterly health summary",
      "Direct ServOps Slack line",
    ],
  },
];

const mspPlan = {
  name:     "MSP White-Label",
  desc:     "Offer this scanner under your own brand to all your clients.",
  price:    "$149",
  per:      "/ month",
  href:     STRIPE_LINKS.msp,
  cta:      "Get MSP access →",
  external: true,
  features: [
    "Your logo and colours",
    "Custom subdomain (scan.yourmsp.com)",
    "Up to 25 client scans/mo",
    "Your CTA in every report",
    "Scan dashboard",
    "Priority support",
  ],
};

export default function Pricing() {
  const navigate = useNavigate();

  return (
    <div style={styles.page}>
      <nav style={styles.nav}>
        <div style={styles.logo} onClick={() => navigate("/")}>
          <div style={styles.dot} />
          <span style={styles.brand}>ServOps</span>
        </div>
        <button
          style={styles.scanBtn}
          onClick={() => navigate("/")}
        >
          Free scan →
        </button>
      </nav>

      <div style={styles.content}>
        <p style={styles.eyebrow}>SIMPLE PRICING</p>
        <h1 style={styles.h1}>Start free. Pay only when you need us.</h1>
        <p style={styles.sub}>
          The scan is always free. Pay only if you want us to fix issues
          or monitor your business monthly.
        </p>

        {/* SMB PLANS */}
        <div style={styles.grid}>
          {plans.map((p) => (
            <div key={p.name} style={{
              ...styles.card,
              border: p.featured
                ? "2px solid #185FA5"
                : "0.5px solid rgba(255,255,255,0.1)",
            }}>
              {p.featured && (
                <div style={styles.popularBadge}>Most popular</div>
              )}
              <p style={styles.planName}>{p.name}</p>
              <p style={styles.planDesc}>{p.desc}</p>
              <p style={styles.price}>
                {p.price}
                <span style={styles.per}> {p.per}</span>
              </p>
              <div style={styles.divider} />
              <ul style={styles.featureList}>
                {p.features.map((f) => (
                  <li key={f} style={styles.feature}>
                    <div style={styles.check} />
                    {f}
                  </li>
                ))}
              </ul>
              <a
                href={p.href}
                target={p.external ? "_blank" : undefined}
                rel={p.external ? "noreferrer" : undefined}
                onClick={!p.external ? (e) => { e.preventDefault(); navigate(p.href); } : undefined}
                style={{
                  ...styles.planBtn,
                  background: p.featured ? "#185FA5" : "transparent",
                  color: p.featured ? "#fff" : "#7BA4C8",
                  border: p.featured
                    ? "none"
                    : "0.5px solid rgba(255,255,255,0.15)",
                }}
              >
                {p.cta}
              </a>
            </div>
          ))}
        </div>

        {/* MSP PLAN */}
        <div style={styles.mspSection}>
          <p style={styles.mspLabel}>FOR MSPs & IT PROVIDERS</p>
          <div style={styles.mspCard}>
            <div style={styles.mspLeft}>
              <p style={styles.planName}>{mspPlan.name}</p>
              <p style={styles.planDesc}>{mspPlan.desc}</p>
              <p style={styles.price}>
                {mspPlan.price}
                <span style={styles.per}> {mspPlan.per}</span>
              </p>
            </div>
            <div style={styles.mspRight}>
              <ul style={styles.featureList}>
                {mspPlan.features.map((f) => (
                  <li key={f} style={styles.feature}>
                    <div style={styles.check} />
                    {f}
                  </li>
                ))}
              </ul>
              <a
                href={mspPlan.href}
                target="_blank"
                rel="noreferrer"
                style={{ ...styles.planBtn, background: "#185FA5", color: "#fff", border: "none" }}
              >
                {mspPlan.cta}
              </a>
            </div>
          </div>
        </div>

        {/* FAQ */}
        <div style={styles.faq}>
          <p style={styles.sectionLabel}>COMMON QUESTIONS</p>
          {faqs.map((f) => (
            <div key={f.q} style={styles.faqItem}>
              <p style={styles.faqQ}>{f.q}</p>
              <p style={styles.faqA}>{f.a}</p>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}

const faqs = [
  {
    q: "Is the free scan really free?",
    a: "Yes — completely free, forever. No credit card, no signup required. Just enter your domain.",
  },
  {
    q: "What does 'Fix it for me' include?",
    a: "We resolve every critical and warning issue found in your scan within 48 hours. You get a written summary of what was fixed and a re-scan to confirm everything is clean.",
  },
  {
    q: "What happens after I pay?",
    a: "You'll receive a confirmation email from ServOps within 1 hour. We'll schedule a short call to review your report and begin remediation work.",
  },
  {
    q: "Can I cancel the monthly plan?",
    a: "Yes — cancel any time, no questions asked. No contracts, no minimum commitment.",
  },
  {
    q: "I'm an MSP. Can I offer this to my clients?",
    a: "Yes — the MSP White-Label plan lets you brand the tool as your own and offer it to all your clients. Your logo, your domain, your CTA in every report.",
  },
];

const styles = {
  page: {
    background: "#0A1628",
    minHeight: "100vh",
    fontFamily: "system-ui, -apple-system, sans-serif",
    color: "#fff",
  },
  nav: {
    display: "flex", justifyContent: "space-between",
    alignItems: "center", padding: "16px 32px",
    borderBottom: "0.5px solid rgba(255,255,255,0.08)",
  },
  logo: {
    display: "flex", alignItems: "center",
    gap: 8, cursor: "pointer",
  },
  dot: { width: 8, height: 8, borderRadius: "50%", background: "#378ADD" },
  brand: { fontSize: 15, fontWeight: 500 },
  scanBtn: {
    background: "#185FA5", color: "#fff", border: "none",
    borderRadius: 8, padding: "8px 16px",
    fontSize: 13, cursor: "pointer",
  },
  content: {
    maxWidth: 900, margin: "0 auto",
    padding: "48px 24px",
  },
  eyebrow: {
    textAlign: "center", fontSize: 11, color: "#4A6A8A",
    letterSpacing: "2px", margin: "0 0 12px",
  },
  h1: {
    textAlign: "center", fontSize: 28, fontWeight: 500,
    margin: "0 0 14px", lineHeight: 1.3,
  },
  sub: {
    textAlign: "center", fontSize: 14, color: "#7BA4C8",
    lineHeight: 1.7, margin: "0 0 40px",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
    gap: 16, marginBottom: 32,
  },
  card: {
    background: "rgba(255,255,255,0.04)",
    borderRadius: 12, padding: "24px",
    display: "flex", flexDirection: "column",
    position: "relative",
  },
  popularBadge: {
    position: "absolute", top: -12, left: "50%",
    transform: "translateX(-50%)",
    background: "#185FA5", color: "#fff",
    fontSize: 11, fontWeight: 500,
    padding: "3px 14px", borderRadius: 20,
    whiteSpace: "nowrap",
  },
  planName: {
    fontSize: 16, fontWeight: 500, margin: "0 0 6px", color: "#fff",
  },
  planDesc: {
    fontSize: 12, color: "#7BA4C8", margin: "0 0 16px", lineHeight: 1.5,
  },
  price: { fontSize: 28, fontWeight: 500, color: "#fff", margin: "0 0 4px" },
  per: { fontSize: 13, fontWeight: 400, color: "#4A6A8A" },
  divider: {
    borderTop: "0.5px solid rgba(255,255,255,0.08)", margin: "16px 0",
  },
  featureList: {
    listStyle: "none", padding: 0, margin: "0 0 20px",
    display: "flex", flexDirection: "column", gap: 8, flex: 1,
  },
  feature: {
    display: "flex", alignItems: "center",
    gap: 10, fontSize: 13, color: "#CBD5E0",
  },
  check: {
    width: 16, height: 16, borderRadius: "50%",
    background: "rgba(29,158,117,0.2)",
    border: "0.5px solid #1D9E75", flexShrink: 0,
  },
  planBtn: {
    display: "block", textAlign: "center",
    padding: "11px", borderRadius: 8,
    fontSize: 13, fontWeight: 500,
    textDecoration: "none", marginTop: "auto",
    cursor: "pointer",
  },
  mspSection: { marginBottom: 40 },
  mspLabel: {
    fontSize: 11, color: "#4A6A8A",
    letterSpacing: "2px", margin: "0 0 16px",
  },
  mspCard: {
    background: "rgba(255,255,255,0.04)",
    border: "0.5px solid rgba(55,138,221,0.3)",
    borderRadius: 12, padding: "24px",
    display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24,
  },
  mspLeft: {},
  mspRight: { display: "flex", flexDirection: "column" },
  faq: { borderTop: "0.5px solid rgba(255,255,255,0.08)", paddingTop: 32 },
  sectionLabel: {
    fontSize: 11, color: "#4A6A8A",
    letterSpacing: "2px", margin: "0 0 20px",
  },
  faqItem: {
    borderBottom: "0.5px solid rgba(255,255,255,0.06)",
    paddingBottom: 16, marginBottom: 16,
  },
  faqQ: { fontSize: 14, fontWeight: 500, color: "#fff", margin: "0 0 6px" },
  faqA: { fontSize: 13, color: "#7BA4C8", lineHeight: 1.6, margin: 0 },
};
