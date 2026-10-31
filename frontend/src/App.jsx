import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import RegistrarIncidente from "./pages/RegistrarIncidente";
import FinalizarIncidente from "./pages/FinalizarIncidente";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />

        <Route
          path="/registrar"
          element={<RegistrarIncidente />}
        />

        <Route
          path="/finalizar"
          element={<FinalizarIncidente />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;