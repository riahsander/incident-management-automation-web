import { registrarIncidente } from "../services/api.js";
import { useState } from "react";
import "../styles/forms.css"
import { useNavigate } from "react-router-dom";

const parceiros = [
  "AGIBANK",
  "AILOS",
  "ALETHA",
  "BANCO DA AMAZONIA",
  "BANCO TOPAZIO ATM",
  "BANCOAGIBANK",
  "BANESE",
  "BANESTES",
  "BANPARA",
  "BANRISUL",
  "BNB",
  "BANRISUL CORBAN",
  "CIRRUS",
  "CREFISA",
  "EDENRED",
  "PLUS",
  "SICOOB",
  "SICREDI",
  "UNICRED",
  "EMBRATEC",
];

export default function RegistrarIncidenteForm() {
  const [parceiro, setParceiro] = useState("");
  const [horarioInicio, setHorarioInicio] = useState("");
  const [tipoIndisponibilidade, setTipoIndisponibilidade] = useState("");
  const [tipoTransacao, setTipoTransacao] = useState("");
  const [autorizador, setAutorizador] = useState("");
  const [status, setStatus] = useState("");

  const [carregando, setCarregando] = useState(false);

  const navigate = useNavigate();


  async function registrarIncidenteForm() {

    if (carregando) {
      return;
    }


    if (
      !parceiro ||
      !tipoTransacao ||
      !autorizador ||
      !status ||
      !tipoIndisponibilidade ||
      !horarioInicio
    ) {
      alert("Preencha todos os campos.");
      return;
    }

    const confirmar = window.confirm(
      "Deseja realmente registrar este incidente?"
    );

    if (!confirmar) {
      return;
    }

    setCarregando(true);

    try {

      const resposta = await registrarIncidente({
        parceiro,
        tipo_transacao: tipoTransacao,
        autorizador,
        status,
        indisponibilidade: tipoIndisponibilidade,
        hora_inicio: horarioInicio,
      });

      if (resposta.success) {
        alert(`${resposta.message}\n\nChamado: ${resposta.chamado}`);

        setParceiro("");
        setHorarioInicio("");
        setTipoIndisponibilidade("");
        setTipoTransacao("");
        setAutorizador("");
        setStatus("");

        navigate("/");
      } else {
        alert(resposta.message);
      }

    } catch (erro) {
      console.error(erro);
      const mensagem = erro?.response?.data?.detail ?? "Erro inesperado ao registrar incidente."
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
        <h2 className="form-title">Registro de Incidente</h2>

        <div className="form-group">
          <label>Parceiro</label>

          <select
            value={parceiro}
            onChange={(e) => setParceiro(e.target.value)}
          >
            <option value="">Selecione</option>

            {parceiros.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </div>


        <div className="form-group">
          <label>Horário de início</label>

          <input
            type="time"
            value={horarioInicio}
            onChange={(e) => setHorarioInicio(e.target.value)}
          />
        </div>


        <div className="form-group">
          <label>Tipo de indisponibilidade</label>

          <select
            value={tipoIndisponibilidade}
            onChange={(e) => setTipoIndisponibilidade(e.target.value)}
          >
            <option value="">Selecione</option>
            <option value="Total">Total</option>
            <option value="Parcial">Parcial</option>
          </select>
        </div>


        <div className="form-group">
          <label>Tipo de Transação</label>

          <select
            value={tipoTransacao}
            onChange={(e) => setTipoTransacao(e.target.value)}
          >
            <option value="">Selecione</option>
            <option value="SAQUE">SAQUE</option>
            <option value="DEPOSITO">DEPOSITO</option>
            <option value="SALDO">SALDO</option>
            <option value="AMBOS">AMBOS</option>
          </select>
        </div>


        <div className="form-group">
          <label>Erro no Autorizador</label>

          <select
            value={autorizador}
            onChange={(e) => setAutorizador(e.target.value)}
          >
            <option value="">Selecione</option>
            <option value="Sim">Sim</option>
            <option value="Não">Não</option>
          </select>
        </div>


        <div className="form-group">
          <label>Status das Transações</label>

          <select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
          >
            <option value="">Selecione</option>
            <option value="Negadas">Negadas</option>
            <option value="Pendentes">Pendentes</option>
            <option value="Desfeitas">Desfeitas</option>
            <option value="Erro">Erro</option>
            <option value="Negadas e Pendentes">
              Negadas e Pendentes
            </option>
            <option value="Desfeitas e Pendentes">
              Desfeitas e Pendentes
            </option>
          </select>
        </div>


        <button
          className="primary-button"
          onClick={registrarIncidenteForm}
          disabled={carregando}
        >
          {carregando
            ? "Processando..."
            : "Registrar Incidente"}
        </button>
      </div>
    </div>
  );
}