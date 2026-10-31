import { useState } from "react";
import { finalizarIncidente } from "../services/api.js";
import "../styles/forms.css"
import { useNavigate } from "react-router-dom";

export default function FinalizarIncidente() {
  const [horaFim, setHoraFim] = useState("");
  const [origem, setOrigem] = useState("");
  const [causa, setCausa] = useState("");
  const [chamado, setChamado] = useState("");
  const [escopo, setEscopo] = useState("");

  const [carregando, setCarregando] = useState(false);

  const navigate = useNavigate()

  async function finalizarIncidenteForm() {
    if (carregando) {
      return;
    }

    if (
      !horaFim ||
      !origem ||
      !causa.trim() ||
      !chamado.trim() ||
      !escopo
    ) {
      alert("Preencha todos os campos.");
      return;
    }

    const confirmar = window.confirm(
      "Deseja realmente finalizar este incidente?"
    );

    if (!confirmar) {
      return;
    }

    setCarregando(true)

    const dados = {
      hora_fim: horaFim,
      origem: origem,
      causa: causa,
      chamado: chamado,
      escopo: escopo,
    };

    try {
        const resposta = await finalizarIncidente(dados);


      if (resposta.success) {
        alert(`${resposta.message}\n\nChamado: ${resposta.chamado}`);

        setHoraFim("");
        setOrigem("");
        setCausa("");
        setChamado("");
        setEscopo("");

        navigate("/");
      } else {
        alert(resposta.message);
      }

    } catch (erro) {
      console.error(erro);
      const mensagem = erro?.response?.data?.detail || "Erro inesperado ao finalizar incidente."
      alert(mensagem);
    } finally {
      setCarregando(false);
    }
  }

  return (
    <div className="page-container">
      <div className="form-card">
        <div className="logo">
          <h1>S/NOC</h1>
          <p>Security Network Operations Center</p>
        </div>
        <h2 className="form-title">Encerramento de Incidente</h2>

        <div className="form-group">
          <label>Hora Fim</label>
          

          <input
            type="time"
            value={horaFim}
            onChange={(e) => setHoraFim(e.target.value)}
          />
        </div>


        <div className="form-group">
          <label>Origem</label>

          <select
            value={origem}
            onChange={(e) => setOrigem(e.target.value)}
          >
            <option value="">Selecione</option>
            <option value="EXTERNA">EXTERNA</option>
            <option value="INTERNA">INTERNA</option>
          </select>
        </div>


        <div className="form-group">
          <label>Causa / Resolução</label>

          <input
            value={causa}
            onChange={(e) => setCausa(e.target.value)}
          />
        </div>


        <div className="form-group">
          <label>Chamado</label>

          <input
            type="text"
            value={chamado}
            onChange={(e) => setChamado(e.target.value)}
          />
        </div>


        <div className="form-group">
          <label>Escopo</label>

          <select
            value={escopo}
            onChange={(e) => setEscopo(e.target.value)}
          >
            <option value="">Selecione</option>
            <option value="SAQUE">SAQUE</option>
            <option value="DEPOSITO">DEPOSITO</option>
            <option value="SALDO">SALDO</option>
            <option value="GERAL">GERAL</option>
          </select>
        </div>


        <button
        className="primary-button"
          onClick={finalizarIncidenteForm}
          disabled={carregando}
        >
          {carregando
            ? "Processando..."
            : "Finalizar Incidente"}
        </button>
      </div>
    </div>
  );
}