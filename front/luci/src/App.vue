<template>
  <div class="d-flex align-items-center justify-content-center min-vh-100 bg-page">
    <div class="card shadow w-100" style="max-width: 500px">
      <div class="card-body p-5">
        <h1 class="text-center mb-4">Consultar Associado</h1>

        <!-- Tela de login -->
        <template v-if="!token">
          <div class="d-flex justify-content-start">
            <h5>Logue com sua agência</h5>
          </div>
          <form @submit.prevent="login">
            <div class="mb-3">
              <input
                v-model="agencia"
                type="text"
                class="form-control"
                placeholder="Agência"
              />
            </div>
            <div class="mb-4">
              <input
                v-model="senha"
                type="password"
                class="form-control"
                placeholder="Senha"
              />
            </div>
            <button
              type="submit"
              class="btn btn-outline-success w-100 p-2"
              :disabled="logando"
            >
              <p v-if="!logando" class="m-1">Entrar</p>
              <p v-else class="m-1">Entrando...</p>
            </button>
            <div class="d-flex justify-content-start">
              <p v-if="loginError" class="text-danger m-2 error">
                <span>{{ loginError }}</span>
              </p>
            </div>
          </form>
        </template>

        <!-- Tela de consulta -->
        <template v-else>
          <form @submit.prevent="consultar">
            <div class="mb-3">
              <input
                v-model="cpf"
                type="text"
                class="form-control"
                placeholder="Digite o CPF"
              />
            </div>
            <button type="submit" class="btn btn-success w-100" :disabled="consultando">
              <p v-if="!consultando">Consultar</p>
              <p v-else="!consultando">Gerando consulta...</p>
            </button>
            <div class="d-flex justify-content-start">
              <p v-if="consultaError" class="text-danger m-2 error">
                {{ consultaError }}
              </p>
            </div>
          </form>
          <button @click="logout" class="btn btn-outline-success w-100 mt-3">
            <p>Sair</p>
          </button>

          <hr class="m-5" />

          <!-- Sugestões de abordagem -->
          <h2 class="text-center mb-3">Sugestões de Abordagem</h2>
          <div class="mt-3">
            <div
              class="card shadow-sm border mb-4"
              v-for="registro in registros"
              :key="registro.nome"
            >
              <div class="card-body">
                <div class="d-flex justify-content-center">
                  <h4 class="card-title">{{ registro.nome }}</h4>
                </div>
                <div v-if="!registro.ia">
                  <div class="mt-3" v-if="registro.colaboradores">
                    <h6 class="fw-bold">🧑‍💼 Ordem dos Colaboradores:</h6>
                    <ol class="list-group list-group-numbered mb-3">
                      <li
                        v-for="(colab, index) in registro.colaboradores"
                        :key="index"
                        class="list-group-item"
                      >
                        {{ colab }}
                      </li>
                    </ol>
                  </div>
                  <div class="mb-3" v-if="registro.limite_credito">
                    <h5 class="fw-bold text-success">🤑 Crédito pré-aprovado:</h5>
                    <div class="d-flex justify-content-center">
                      <p class="h5 text-success">
                        {{
                          new Intl.NumberFormat("pt-BR", {
                            style: "currency",
                            currency: "BRL",
                          }).format(registro.limite_credito)
                        }}
                      </p>
                    </div>
                  </div>
                  <div class="mb-3" v-if="registro.propor">
                    <h6 class="fw-bold text-success">🟢 Assuntos para Propor:</h6>
                    <div>
                      <span
                        v-for="(item, index) in registro.propor"
                        :key="index"
                        class="badge bg-success d-block py-2 mb-2 text-wrap"
                      >
                        {{ item }}
                      </span>
                    </div>
                  </div>

                  <div v-if="registro.evitar">
                    <h6 class="fw-bold text-danger">🟠 Assuntos a Evitar:</h6>
                    <div>
                      <span
                        v-for="(item, index) in registro.evitar"
                        :key="index"
                        class="badge bg-danger d-block py-2 mb-2 text-wrap"
                      >
                        {{ item }}
                      </span>
                    </div>
                  </div>
                </div>
                <div v-else>
                  <p class="card-title">
                    Infelizmente ia gerou fora do modelo proposto. Mas ainda podes ver sua
                    resposta:
                  </p>
                  <div>
                    <span>
                      {{ registro.ia }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
      </div>
      <div class="footer">
        <p>&copy;2025 - Lucas H. Cipriano</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import axios from "axios";

type registro = {
  nome: string;
  limite_credito: number;
  ia?: string;
  colaboradores: string[];
  propor: string[];
  evitar: string[];
};

const agencia = ref<string>("");
const senha = ref<string>("");
const loginError = ref<string>("");
const consultaError = ref<string>("");
const logando = ref<boolean>(false);
const consultando = ref<boolean>(false);
const token = ref<string | null>(null);

const cpf = ref<string>("");
const registros = ref<registro[]>([]);

const api = axios.create({
  baseURL: import.meta.env.VITE_API,
});

let intervaloId: number | null = null;

onMounted(() => {
  const storedToken = localStorage.getItem("token");
  if (storedToken) token.value = storedToken;

  buscarRegistros();
  intervaloId = window.setInterval(buscarRegistros, 5000);
});

onUnmounted(() => {
  if (intervaloId) clearInterval(intervaloId);
});

async function login(): Promise<void> {
  if (!agencia.value || !senha.value) {
    loginError.value = "Agência e/ou senha não informados";
    return;
  }

  logando.value = true;
  try {
    const { data } = await api.post("/get_token/", {
      agencia: agencia.value,
      senha: senha.value,
    });
    token.value = data.token as string;
    localStorage.setItem("token", token.value);
    loginError.value = "";
  } catch (error: any) {
    loginError.value = error.response?.data?.detail || error.message;
  } finally {
    logando.value = false;
    agencia.value = "";
    senha.value = "";
  }
}

function logout(): void {
  token.value = null;
  localStorage.removeItem("token");
  cpf.value = "";
}

async function consultar(): Promise<void> {
  if (!token.value) return;
  consultando.value = true;

  try {
    await api.post(
      "/consulta/",
      {
        associado: cpf.value,
      },
      {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      }
    );
    cpf.value = "";
    consultaError.value = "";
  } catch (error: any) {
    if (error.status === 401) logout();
    consultaError.value = error.response?.data?.detail || error.message;
  } finally {
    consultando.value = false;
  }
}

async function buscarRegistros(): Promise<void> {
  if (!token.value) return;

  try {
    const { data } = await api.get("/consulta/", {
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });
    registros.value = data;
  } catch (error: any) {
    if (error.status === 401) logout();
    console.error(error.response?.data?.detail || error.message);
  }
}
</script>

<style>
.bg-page {
  background-color: #3fa110;
}

/* Aplica imagem de fundo apenas em telas web */
@media screen and (min-width: 768px) {
  .bg-page {
    background-image: url("/media_produtos_filer_public_thumbnails_filer_public_2024_06_28_banner-seja-associado-sicredi-ana-castela.png__1920x860_subsampling-2.webp");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
  }
}

input {
  border-top: 0 !important;
  border-left: 0 !important;
  border-right: 0 !important;
  border-radius: 0 !important;
  border-color: #146e37 !important;
}

input:focus {
  border-top: 0 !important;
  border-left: 0 !important;
  border-right: 0 !important;
  border-radius: 0 !important;
  border-bottom: 2px solid #146e37 !important;
  box-shadow: none !important;
}

h1 {
  font-style: normal !important;
  font-weight: 400 !important;
  font-family: "Exo 2";
  font-size: 30px !important;
  color: #323c32 !important;
  line-height: 120% !important;
  letter-spacing: -0.4px !important;
}

h2,
h3,
h4,
h5,
h6 {
  font-style: normal !important;
  font-weight: 400 !important;
  font-family: "Exo 2", sans-serif;
  color: #323c32 !important;
  line-height: 120% !important;
  letter-spacing: -0.4px !important;
}

p {
  font-family: "Nunito", sans-serif;
  font-weight: 700;
  margin: 0;
  padding: 0;
}

.error {
  font-weight: 400;
  color: #aa003c !important;
}

span {
  font-family: "Open Sans", sans-serif;
  font-weight: 300;
}

.footer {
  color: #00000062;
  text-align: center;
  justify-content: center;
  margin: 10px 0px;
  padding: 10px;
}
</style>
