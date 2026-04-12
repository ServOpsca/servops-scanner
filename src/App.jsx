import { BrowserRouter, Routes, Route } from "react-router-dom";
import Landing from "./pages/Landing";
import Scan    from "./pages/Scan";
import Results from "./pages/Results";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/"       element={<Landing />} />
        <Route path="/scan"   element={<Scan />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </BrowserRouter>
  );
}