<template>
    <empty-layout>
        <div class="verification-container">
            <div class="card" v-if="!verificando && !temAcesso">
                <div class="card-header">
                    <h1 class="title is-3">Verificação de Acesso</h1>
                </div>
                <div class="card-content">
                    <div v-if="!emailUsuario">
                        <div class="field">
                            <label class="label">Email</label>
                            <div class="control">
                                <input class="input" type="email" v-model="emailManual" placeholder="Digite seu email"
                                    @keyup.enter="verificarAcesso" />
                            </div>
                        </div>
                        <button class="button is-primary is-fullwidth" @click="verificarAcesso"
                            :disabled="!emailManual">
                            Verificar Acesso
                        </button>
                    </div>
                    <div v-else>
                        <div class="notification is-info">
                            <p>Olá! Identificamos você como: <strong>{{ emailUsuario }}</strong></p>
                            <p v-if="idColaborador" class="is-size-7">ID do colaborador:
                                <code>{{ idColaborador }}</code>
                            </p>
                        </div>

                        <div class="notification is-primary">
                            <p>Posto de trabalho: <strong>{{ nomePosto }}</strong></p>
                        </div>

                        <div class="notification is-warning" v-if="mensagemErro">
                            <p>{{ mensagemErro }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="verificando" class="card">
                <div class="card-content has-text-centered">
                    <span class="icon is-large">
                        <i class="fas fa-spinner fa-pulse"></i>
                    </span>
                    <p>Verificando acesso...</p>
                </div>
            </div>

            <!-- Modal de acesso negado -->
            <div class="modal" :class="{ 'is-active': mostrarResultado && !temAcesso }">
                <div class="modal-background" @click="fecharModal"></div>
                <div class="modal-content">
                    <div class="box">
                        <h2 class="title is-4">Acesso Negado</h2>
                        <p>{{ mensagemResultado }}</p>
                        <div class="buttons is-centered mt-4">
                            <button class="button" @click="fecharModal">Fechar</button>
                        </div>
                    </div>
                </div>
                <button class="modal-close is-large" @click="fecharModal"></button>
            </div>
        </div>
    </empty-layout>
</template>

<script>
import firebase from "firebase";

export default {
    data() {
        return {
            emailManual: "",
            verificando: false,
            mostrarResultado: false,
            temAcesso: false,
            mensagemResultado: "",
            mensagemErro: "",
            colaboradorEncontrado: null,
            nomePosto: "Carregando...",
            idPosto: null,
            idColaborador: null,
            selectedFicha: null,
            fichas: [],
            postoSelecionado: null,
        };
    },
    created() {
        var thisVM = this;
        thisVM.idPosto = thisVM.$route.params.idPosto;
        thisVM.carregarDetalhesPosto();
    },
    mounted() {
        // Após carregar os detalhes do posto, verificamos se o usuário já está autenticado
        var thisVM = this;
        thisVM.$nextTick(() => {
            // Verificamos se já temos um usuário logado
            if (thisVM.emailUsuario) {
                // Iniciamos a verificação automaticamente
                thisVM.getProntuarios();
                thisVM.verificarAcesso();
            }
        });
    },
    computed: {
        emailUsuario() {
            var thisVM = this;
            return thisVM.$store.state.currentUser ? thisVM.$store.state.currentUser.email : null;
        },
        emailUsuarioValido() {
            var thisVM = this;
            return thisVM.emailUsuario || thisVM.emailManual;
        },
    },
    methods: {
        carregarDetalhesPosto() {
            var thisVM = this;
            const time = thisVM.$route.params.time;

            firebase.database().ref(`${time}/postosTrabalho/${thisVM.idPosto}`)
                .once("value")
                .then(snapshot => {
                    const posto = snapshot.val();
                    if (posto) {
                        thisVM.nomePosto = posto.nome;
                    } else {
                        thisVM.nomePosto = "Posto não encontrado";
                        thisVM.mensagemErro = "Posto de trabalho não encontrado no sistema.";
                    }
                })
                .catch(() => {
                    thisVM.nomePosto = "Erro ao carregar posto";
                    thisVM.mensagemErro = "Erro ao carregar informações do posto de trabalho.";
                });
        },

        verificarAcesso() {
            var thisVM = this;
            if (!thisVM.emailUsuarioValido) {
                return;
            }

            thisVM.verificando = true;
            const time = thisVM.$route.params.time;
            const emailParaVerificar = thisVM.emailUsuario || thisVM.emailManual;

            firebase.database().ref(`${time}/Colaboradores/`)
                .orderByChild("email")
                .equalTo(emailParaVerificar)
                .once("value")
                .then(snapshot => {
                    thisVM.verificando = false;

                    snapshot.forEach(childSnapshot => {
                        thisVM.idColaborador = childSnapshot.key;
                    });

                    if (!thisVM.idColaborador) {
                        thisVM.temAcesso = false;
                        thisVM.mensagemResultado = "Colaborador não encontrado.";
                        thisVM.mostrarResultado = true;
                        return;
                    }

                    const colaborador = snapshot.val()[thisVM.idColaborador];

                    if (!colaborador.ativo) {
                        thisVM.temAcesso = false;
                        thisVM.mensagemResultado = "Colaborador inativo no sistema.";
                        thisVM.mostrarResultado = true;
                        return;
                    }

                    if (colaborador.idPosto === thisVM.idPosto) {
                        thisVM.temAcesso = true;
                        thisVM.mensagemResultado = `Bem-vindo(a), ${colaborador.nome}! Você tem permissão para registrar ponto neste local.`;

                        // Se não temos as fichas ainda, carregamos elas primeiro
                        if (thisVM.fichas.length === 0) {
                            thisVM.getProntuarios(() => {
                                // Callback para executar após carregar as fichas
                                thisVM.redirecionarParaPonto();
                            });
                        } else {
                            // Se já temos as fichas, redirecionamos diretamente
                            thisVM.redirecionarParaPonto();
                        }
                    } else {
                        thisVM.temAcesso = false;
                        thisVM.mensagemResultado = "Você não tem permissão para registrar ponto neste posto de trabalho.";
                        thisVM.mostrarResultado = true;
                    }
                })
                .catch(() => {
                    thisVM.verificando = false;
                    thisVM.temAcesso = false;
                    thisVM.mensagemResultado = "Erro ao verificar acesso. Por favor, tente novamente.";
                    thisVM.mostrarResultado = true;
                });
        },

        fecharModal() {
            var thisVM = this;
            thisVM.mostrarResultado = false;
            if (thisVM.temAcesso) {
                thisVM.emailManual = "";
            }
        },

        getProntuarios(callback) {
            var thisVM = this;
            thisVM.$store.commit("startLoading");
            var fichas = firebase
                .database()
                .ref(thisVM.$route.params.time + "/pastasOperacao")
                .orderByChild("ativa");

            fichas.once("value", function (snapshot) {
                thisVM.fichas.splice(0, thisVM.fichas.length);
                snapshot.forEach(function (childSnapshot) {
                    var childData = childSnapshot.val();
                    if (
                        childSnapshot.key != "_count" &&
                        childData.ativa != null &&
                        childData.ativa == true
                    ) {
                        var ficha = childData;
                        ficha.id = childSnapshot.key;
                        thisVM.fichas.unshift(ficha);
                        thisVM.selectedFicha = ficha;
                    }
                });
                thisVM.$store.commit("stopLoading");

                // Executamos o callback se ele existir
                if (callback && typeof callback === 'function') {
                    callback();
                }
            });
        },

        redirecionarParaPonto() {
            var thisVM = this;
            if (thisVM.temAcesso && thisVM.idColaborador && thisVM.selectedFicha) {
                thisVM.$router.push({
                    name: 'ControlePonto',
                    params: {
                        time: thisVM.$route.params.time,
                        idProntuario: thisVM.selectedFicha ? thisVM.selectedFicha.id : null,
                        idColaborador: thisVM.idColaborador,
                        idPosto: this.idPosto
                    }, 
                });
            }
        }
    }
}
</script>

<style>
.verification-container {
    max-width: 500px;
    margin: 2rem auto;
    padding: 1rem;
}

.card {
    box-shadow: 0 0.5em 1em -0.125em rgba(10, 10, 10, 0.1), 0 0 0 1px rgba(10, 10, 10, 0.02);
    border-radius: 0.25rem;
}

.card-header {
    background-color: #f5f5f5;
    padding: 1.5rem;
    border-radius: 0.25rem 0.25rem 0 0;
}

.card-content {
    padding: 1.5rem;
}

.mt-4 {
    margin-top: 1.5rem;
}
</style>