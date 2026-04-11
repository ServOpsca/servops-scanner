import { BrowserRouter, Routes, Route } from "react-router-dom";
import Landing from "./pages/Landing";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/scan" element={<div style={{color:"#fff",padding:40}}>Scan page — coming soon</div>} />
        <Route path="/results" element={<div style={{color:"#fff",padding:40}}>Results page — coming soon</div>} />
      </Routes>
    </BrowserRouter>
  );
}