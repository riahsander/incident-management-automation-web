import { useNavigate } from "react-router-dom";
import "../styles/forms.css"

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <div className="home-card">
        <div className="home-logo">
          <h1>Automação de Incidentes</h1>
          <p>Registro e Finalização de Incidentes Transacionais</p>
        </div>

        <div className="home-actions">
          <button
            className="home-button"
            onClick={() => navigate("/registrar")}
          >
             Registrar Incidente
          </button>

          <button
            className="home-button secondary"
            onClick={() => navigate("/finalizar")}
          >
             Finalizar Incidente
          </button>
        </div>
      </div>
    </div>
  );
}