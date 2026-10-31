import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export async function registrarIncidente(dados) {
  try {
    const resposta = await axios.post(
      "http://127.0.0.1:8000/incidente",
      dados
    );

    return resposta.data;

  } catch (erro) {
    throw erro;
  }
}

export async function finalizarIncidente(dados) {
  try {
    const resposta = await axios.post(
      "http://127.0.0.1:8000/finalizar-incidente",
      dados
    );

    return resposta.data;

  } catch (erro) {
    throw erro;
  }
}