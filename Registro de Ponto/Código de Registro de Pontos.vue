<template>
    <empty-layout>
        <!-- Painel de Depuração do Modo de Desenvolvimento -->
        <div v-if="!isProduction" style="background-color: red; color: #fff" class="row">
            <div>Aparece somente em modo de desenvolvimento PARA TESTAR O POSISIONAMENTO</div><br />
            <div v-if="this.checkinInfo.localizacao !== null">
                localizacao atual:
                {{ this.checkinInfo.localizacao.latitude }}
                {{ this.checkinInfo.localizacao.longitude }}
            </div>
            <div class="columns">
                <div class="column is-6">
                    Latitude:
                    <b-input id="latitude" v-model="informacoesPonto.posicaoReferencia.latitude" />
                </div>
                <div class="column is-6">
                    Longitude:
                    <b-input id="longitude" v-model="informacoesPonto.posicaoReferencia.longitude" />
                </div>
            </div>
            <br />
            <br />
        </div>
        <br />
        <div class="row">
            <div class="columns">
                <div class="column is-12">
                    <div class="box">

                        <div>
                            <h1 class="title is-2" style="color:#00CCB3">Registro de ponto </h1>
                            <h2 class="subtitle is-4" style="color:#00CCB3">👤 Pessoa:
                                {{ informacoesPonto.nomeColaborador }} <br /> <span
                                    v-if="informacoesPonto.posicaoReferencia.longitude"> 🚩 </span> Local: {{
                                        informacoesPonto.nomePosto }}
                            </h2>

                        </div>
                        <b-message v-if="verificacaoConcluida && !dadosValidos" title="Falha no carregamento"
                            type="is-danger" has-icon>
                            <p>Não foi possível carregar todas as informações necessárias.</p>
                            <p><strong>Por favor, escaneie o QR code novamente.</strong></p>
                            <br>
                            <b-button type="is-primary" @click="recarregarDados">
                                🔄 Tentar Recarregar
                            </b-button>
                        </b-message>
                        <br />
                        <b-message :title="diagnosticoPonto.titulo" :type="diagnosticoPonto.tipoDiagnostico" has-icon
                            :closable="false" v-if="diagnosticoPonto.mensagem">
                            {{ diagnosticoPonto.mensagem }}
                        </b-message>
                        <br />

                        <div class="container">
                            <!-- Botão para abrir a câmera -->
                            <b-button v-if="!checkinInfo.foto" @click="abrirCamera">
                                📷 Tirar Foto 📷
                            </b-button>
                        </div>

                        <!-- Exibe a câmera -->
                        <div v-if="mostrarCamera">
                            <video ref="video" autoplay
                                style="width: 20%; height: auto; border: 2px solid black; margin-bottom: 10px;"></video>
                            <b-button @click="tirarFoto">Capturar Foto</b-button>
                        </div>

                        <!-- Exibe a foto capturada -->
                        <div v-if="this.checkinInfo.foto">
                            <h3>Foto Capturada:</h3>
                            <img :src="this.checkinInfo.foto" alt="Foto capturada"
                                style="width: 20%; height: auto; border: 2px solid black; margin-top: 10px;" />
                            <!-- Botão para excluir a foto foi removido como solicitado -->
                        </div>
                        <div v-if="checkinInfo.foto">
                            <img :src="checkinInfo.foto" alt="Foto capturada"
                                style="max-width: 100%; margin-bottom: 10px;">
                            <b-button type="is-danger" size="is-small" icon-left="trash" @click="removerFoto"
                                v-if="!pontoRegistrado">
                                Remover Foto
                            </b-button>
                        </div>

                        <canvas ref="canvas" style="display: none;"></canvas>


                        <div class="container">
                            <!-- Botão de registro de ponto - desabilitado se não houver foto ou se já foi registrado -->

                            <b-button :disabled="!permiteFazerRegistro" style="background-color: #00CCB3; color:#fff"
                                class="is-large" @click="registrarPonto()">

                                Registrar ponto
                            </b-button>
                            <br />
                        </div>

                        <br />
                        <b-button v-if="this.pontoRecusado && motivoRecusa === 'horario'"
                            @click="justificativaAtivador">
                            Justificar 📋
                        </b-button>

                        <div v-if="this.justificativaExigida">
                            <input v-model="checkinInfo.justificativa" />
                        </div>
                        <div class="container">
                            <div class="is-large" style="color:#00CCB3; font-size: 18px;"
                                v-if="this.pontoRecusado !== null && !this.pontoRecusado">
                                Ponto registrado com sucesso às {{ this.checkinInfo.dataHora.getHours() }}:{{
                                    this.checkinInfo.dataHora.getMinutes() }}!
                            </div>
                            <div class="is-large" style="color:#00CCB3; font-size: 18px;" v-if="this.pontoRecusado">
                                Ponto não registrado
                            </div>
                        </div>

                        <div>


                            <div v-if="checkinsFeitos.length > 0">
                                <h3>Registros de Hoje:</h3>
                                <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
                                    <thead>
                                        <tr>
                                            <th>#</th>
                                            <th>Horário</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(checkin, index) in checkinsFeitos" :key="index">
                                            <td>{{ index + 1 }}</td>
                                            <td>{{ new Date(checkin).toLocaleTimeString() }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <div v-else>
                                <p>Não há registros de ponto hoje.</p>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </empty-layout>
</template>

<style>
.container {
    display: flex;
    justify-content: center;
    align-items: center;
}

.red {
    background-color: red;
}

.green {
    background-color: green;
}
</style>

<script>
import firebase from "firebase";

export default {
    name: "ControlePonto",

    data() {
        return {
            tentativasRecarregamento: 0,

            idPosto: null,
            semprePermitir: false, //esta variável é para permitir o registro de ponto independente do horário e localização - ajuda no debug
            intervaloEntreCheckins: 15, // em minutos, define o intervalo mínimo entre check-ins
            idColaborador: "",
            idProntuario: null,

            postoTrabalhoId: null,


            motivoRecusa: null, // Pode ser "horario", "localizacao", etc.

            isProduction: process.env.NODE_ENV === "production",
            distancia: null,
            permissao: null,
            pontoRecusado: null,
            //numero da pessoa responsavel por receber a justificativa
            whatsappNumeroJustificativa: 5511983250915,
            naoPontual: null,
            mostrarCamera: false, // Controla a exibição da câmera
            fotoCapturada: null,  // Armazena a foto tirada
            justificativaExigindo: false,
            //o objeto abaixo possui as informações da localização do colaborador
            informacoesPonto: null,
            //este será o objeto que será gravado no banco de dados
            checkinInfo: {
                dataHora: null,
                localizacao: null,
                foto: null,
                justificativa: null,
                informacoesPonto: null,
            },
            verificacaoConcluida: false, // determina se todas as verificações prévias foram feitas
            checkinsFeitos: [],
            pontoRegistrado: false,
        }
    },

    computed: {
        dadosValidos() {
            return this.informacoesPonto.nomeColaborador &&
                this.informacoesPonto.nomeColaborador.trim() !== '' &&
                this.informacoesPonto.nomePosto &&
                this.informacoesPonto.nomePosto.trim() !== '' &&
                this.idPosto !== null &&
                this.verificacaoConcluida;
        },
        justificativaExigida() {
            return this.justificativaExigindo;
        },
        diagnosticoPonto() {
            if (!this.estaDentroDoHorario) {

                const horariosPermitidos = [
                    `Entrada: ${this.formatarHorario(this.informacoesPonto.horarioInicio)}`,
                    `Início do almoço: ${this.formatarHorario(this.informacoesPonto.horarioAlmocoInicio)}`,
                    `Fim do almoço: ${this.formatarHorario(this.informacoesPonto.horarioAlmocoFim)}`,
                    `Saída: ${this.formatarHorario(this.informacoesPonto.horarioFim)}`
                ].join(", ");


                const horaAtual = this.formatarHorario(this.checkinInfo.dataHora);
                return {
                    titulo: "Fora do horário",
                    tipoDiagnostico: "is-danger",
                    mensagem: `Fora do horário permitido para registro de ponto. Horários permitidos: ${horariosPermitidos}. Hora atual: ${horaAtual}. Margem de tolerância: ${this.informacoesPonto.margemMinutos} minutos.`
                };

            }
            if (!this.estaNoRaioDoPosto) {
                if (this.distanciaColaboradorAoPosto == null) {
                    return {
                        titulo: "Localização não disponível",
                        tipoDiagnostico: "is-warning",
                        mensagem: "Não foi possível determinar a sua localização. Verifique as permissões de localização."
                    };
                }
                return {
                    titulo: "Fora do local",
                    tipoDiagnostico: "is-danger",
                    mensagem: `Fora do local permitido para registro de ponto. Você está a ${this.distanciaColaboradorAoPosto.toFixed(2)} metros do local de trabalho.`
                };
            }

            if (this.minutosDesdeUltimoRegistro < this.intervaloEntreCheckins) {
                return {
                    titulo: "Intervalo entre Registros",
                    tipoDiagnostico: "is-warning",
                    mensagem: `Intervalo mínimo de ${this.intervaloEntreCheckins} minutos entre registros de ponto não respeitado. Você deve esperar mais ${(this.intervaloEntreCheckins - this.minutosDesdeUltimoRegistro).toFixed(0)} minutos.`
                };
            }

            return { titulo: null, tipoDiagnostico: null, mensagem: null };
        },

        minutosDesdeUltimoRegistro() {

            if (this.checkinsFeitos.length === 0) {
                return this.intervaloEntreCheckins;
            }

            const ultimoCheckin = this.checkinsFeitos[this.checkinsFeitos.length - 1];
            const ultimoHorario = new Date(ultimoCheckin);
            const agora = new Date();
            const diffMinutos = (agora - ultimoHorario) / (1000 * 60); // diferença em minutos



            return diffMinutos; // retorna a diferença em minutos
        },
        permiteFazerRegistro() {

            if (!this.dadosValidos) {
                return false;
            }

            if (!this.estaDentroDoHorario || !this.estaNoRaioDoPosto) {
                return false; // Se não estiver dentro do horário ou fora do raio , não permite registro
            }



            // Se não houver foto e a foto for exigida, desabilite o botão
            if (this.informacoesPonto.fotoExigida && !this.checkinInfo.foto) {
                return false;
            }
            if (this.minutosDesdeUltimoRegistro < this.intervaloEntreCheckins) {
                // Se a diferença for menor que o intervalo, desabilita o botão
                return false; // desabilita o botão
            }


            if (!this.informacoesPonto) return false;
            return true;
        }
        ,
        estaNoRaioDoPosto() {
            if (!this.checkinInfo.localizacao) return false; // Verifica se a localização foi capturada 

            if (this.distanciaColaboradorAoPosto == null) return false; // Verifica se a distância foi calculada

            // Verifica se a distância está dentro da margem permitida
            return this.distanciaColaboradorAoPosto <= this.informacoesPonto.margemDistancia;
        },
        distanciaColaboradorAoPosto() {
            if (!this.checkinInfo.localizacao) return null; // Verifica se a localização foi capturada

            const { latitude, longitude } = this.checkinInfo.localizacao;
            const { latitude: latPosto, longitude: lonPosto } = this.informacoesPonto.posicaoReferencia;

            // Calcula a distância entre o ponto de trabalho e a localização atual
            return this.calcularDistanciaMetros(latPosto, lonPosto, latitude, longitude);
        }

        ,
        estaDentroDoHorario() {
            var thisVM = this;


            const margemMinutos = thisVM.informacoesPonto.margemMinutos;

            // Data e hora atual do check-in
            const agora = new Date(thisVM.checkinInfo.dataHora);

            // Lista dos quatro horários esperados definidos no prontuário
            const horarios = [
                thisVM.informacoesPonto.horarioInicio,         // Entrada
                thisVM.informacoesPonto.horarioAlmocoInicio,   // Início do almoço
                thisVM.informacoesPonto.horarioAlmocoFim,      // Fim do almoço
                thisVM.informacoesPonto.horarioFim             // Saída
            ];

            // Verifica se o horário atual está dentro da margem de qualquer um dos horários esperados
            return horarios.some(horarioOriginal => {
                if (!horarioOriginal) return false; // Pula se não estiver definido

                // Converte o horário base (ex: 08:00) para uma data completa com o dia de hoje
                const horarioBase = new Date(horarioOriginal);
                const hoje = new Date(); // Garante que usamos a data de hoje

                const horarioEsperado = new Date(
                    hoje.getFullYear(),
                    hoje.getMonth(),
                    hoje.getDate(),
                    horarioBase.getHours(),
                    horarioBase.getMinutes(),
                    0,  // segundos
                    0   // milissegundos
                );

                // Calcula o intervalo permitido com base na margem de tolerância
                const inicioPermitido = new Date(horarioEsperado.getTime() - margemMinutos * 60000);
                const fimPermitido = new Date(horarioEsperado.getTime() + margemMinutos * 60000);
                // debugger;
                // Retorna true se o horário atual estiver dentro da faixa permitida
                return agora >= inicioPermitido && agora <= fimPermitido;
            });
        }
    },
    methods: {
        recarregarDados() {
            this.verificacaoConcluida = false;
            this.tentativasRecarregamento = (this.tentativasRecarregamento || 0) + 1;

            if (this.tentativasRecarregamento > 3) {
                this.$buefy.dialog.alert({
                    title: 'Erro Persistente',
                    message: 'Não foi possível carregar os dados após várias tentativas. Por favor, escaneie o QR code novamente.',
                    type: 'is-danger'
                });
                return;
            }

            this.carregarInformacoesPonto();
        },

        mostrarErroRecarregamento() {
            this.verificacaoConcluida = true;
            this.$store.commit("stopLoading");

            this.$buefy.dialog.confirm({
                title: 'Erro no Carregamento',
                message: 'Não foi possível carregar as informações. Deseja tentar novamente ou escanear o QR code?',
                confirmText: 'Tentar Novamente',
                cancelText: 'Escanear QR Code',
                type: 'is-danger',
                onConfirm: () => this.recarregarDados()
            });
        },

        removerFoto() {
            this.checkinInfo.foto = null;
        },
        formatarHorario(horario) {
            if (!horario) return "";
            const date = new Date(horario);
            const horas = date.getHours().toString().padStart(2, "0");
            const minutos = date.getMinutes().toString().padStart(2, "0");
            return `${horas}:${minutos}`;
        },


        abrirCamera() {
            this.mostrarCamera = true;

            navigator.mediaDevices.getUserMedia({ video: true })
                .then((stream) => {
                    this.$nextTick(() => {
                        const video = this.$refs.video;
                        if (video) {
                            video.srcObject = stream;
                        }
                    });
                })
                .catch(error => {
                    alert("Erro ao acessar a câmera:", error);
                    alert("Não foi possível acessar a câmera. Verifique suas permissões.");
                    this.mostrarCamera = false;
                });
        },

        tirarFoto() {
            const video = this.$refs.video;
            const canvas = this.$refs.canvas;


            const MAX_DIMENSION = 640; // ajustar se necessario
            // calcula as dimensões do video
            let newWidth, newHeight;
            if (video.videoWidth > video.videoHeight) {

                newWidth = MAX_DIMENSION;
                newHeight = Math.floor(video.videoHeight * (MAX_DIMENSION / video.videoWidth));
            } else {
                // 
                newHeight = MAX_DIMENSION;
                newWidth = Math.floor(video.videoWidth * (MAX_DIMENSION / video.videoHeight));
            }

            canvas.width = newWidth;
            canvas.height = newHeight;

            const context = canvas.getContext("2d");

            context.drawImage(video, 0, 0, newWidth, newHeight);
            this.checkinInfo.foto = canvas.toDataURL("image/jpeg", 0.5);

            video.srcObject.getTracks().forEach(track => track.stop());
            this.mostrarCamera = false;

        },

        //metodo para calcular distancia da posicao capitada com relação ao ponto de referencia
        calcularDistanciaMetros(lat1, lon1, lat2, lon2) {
            const R = 6371; // raio da Terra em KM
            const dLat = (lat2 - lat1) * (Math.PI / 180);
            const dLon = (lon2 - lon1) * (Math.PI / 180);
            const a =
                Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(lat1 * (Math.PI / 180)) * Math.cos(lat2 * (Math.PI / 180)) *
                Math.sin(dLon / 2) * Math.sin(dLon / 2);
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
            return R * c * 1000; // retorna a distância em metros
        },
        carregarDetalhesPosto() {
            var thisVM = this;

            if (!thisVM.idPosto) {
                thisVM.mostrarErroRecarregamento();
                return;
            }

            const time = thisVM.$route.params.time;

            firebase.database().ref(`${time}/postosTrabalho/${thisVM.idPosto}`)
                .once("value")
                .then(snapshot => {
                    const posto = snapshot.val();

                    if (!posto) {
                        throw new Error("Posto de trabalho não encontrado");
                    }

                    thisVM.informacoesPonto.nomePosto = posto.nome;
                    thisVM.informacoesPonto.posicaoReferencia.longitude = posto.localizacao.longitude;
                    thisVM.informacoesPonto.posicaoReferencia.latitude = posto.localizacao.latitude;
                    thisVM.informacoesPonto.margemDistancia = posto.margemDistancia || 100;

                    thisVM.verificacaoConcluida = true;
                })
                .catch((error) => {
                    alert("Erro ao carregar posto:", error);
                    thisVM.mostrarErroRecarregamento();
                });
        },

        registrarPonto() {
            var thisVM = this;
            var fbPath = `${thisVM.$route.params.time}/resultadosOperacao/prontuarios/${thisVM.idProntuario}/${thisVM.idColaborador}/registrosPontos`;
            // Verificação explícita: impedir o registro sem foto
            if (!this.checkinInfo.foto && this.informacoesPonto.fotoExigida) {
                alert("É necessário tirar uma foto para registrar o ponto.");
                return;
            }

            this.getLocalizacao()

                .then(() => {
                    thisVM.getDataHora();

                    if (!thisVM.checkinInfo.localizacao) {
                        alert("Erro ao obter localização. Verifique as permissões.");
                        return;
                    }



                    if (this.estaDentroDoHorario && this.distancia <= this.informacoesPonto.margemDistancia) {


                        firebase.database().ref(fbPath).once('value')
                            .then(snapshot => {
                                const dados = snapshot.val();
                                const agora = new Date();

                                if (dados) {
                                    const registrosHoje = Object.values(dados)
                                        .filter(reg => reg.dataHora.startsWith(agora.toISOString().split('T')[0]))
                                        .sort((a, b) => new Date(b.dataHora) - new Date(a.dataHora));

                                    if (registrosHoje.length > 0) {
                                        const ultimoRegistro = new Date(registrosHoje[0].dataHora);
                                        const minutosDesdeUltimo = (agora - ultimoRegistro) / (1000 * 60);

                                        if (minutosDesdeUltimo < 15) {
                                            alert("⚠️ Já existe um registro recente. Aguarde pelo menos 15 minutos.");
                                            this.$store.commit("stopLoading");
                                            return;
                                        }
                                    }
                                }

                                // 🔽 Salvar ponto normalmente
                                var dadosParaSalvar = {
                                    dataHora: agora.toISOString(),
                                    localizacao: this.checkinInfo.localizacao,
                                    postoTrabalhoId: this.idPosto
                                };

                                if (this.checkinInfo.foto) {
                                    dadosParaSalvar.foto = this.checkinInfo.foto;
                                }
                                if (this.checkinInfo.justificativa) {
                                    dadosParaSalvar.justificativa = this.checkinInfo.justificativa;
                                }

                                var idPonto = firebase.database().ref(fbPath).push().key;
                                firebase.database().ref(`${fbPath}/${idPonto}`).set(dadosParaSalvar)
                                    .then(() => {
                                        this.pontoRegistrado = true;
                                        this.$store.commit("stopLoading");
                                        alert("✅ Ponto registrado com sucesso!");

                                        this.atualizarListaCheckinsEmTempoReal();
                                    })
                                    .catch(error => {
                                        alert("Erro ao salvar no Firebase: " + error.message);
                                        alert("Erro ao salvar o registro. Tente novamente.");
                                    });
                            })
                            .catch(error => {
                                alert("Erro ao verificar registros anteriores: " + error.message);
                                this.$store.commit("stopLoading");
                            });
                    }
                })
                .catch((error) => {
                    alert("Erro ao obter localização: " + error.message);
                    thisVM.$store.commit("stopLoading");
                });
        },
        atualizarListaCheckinsEmTempoReal() {
            if (this.idProntuario && this.idColaborador) {
                const fbPath = `${this.$route.params.time}/resultadosOperacao/prontuarios/${this.idProntuario}/${this.idColaborador}/registrosPontos`;

                firebase.database().ref(fbPath).once('value')
                    .then(snapshot => {
                        const dados = snapshot.val();
                        if (dados) {
                            // Extrair os check-ins feitos hoje
                            const hoje = new Date().toISOString().split('T')[0];
                            const checkinsHoje = Object.values(dados)
                                .filter(checkin => checkin.dataHora.startsWith(hoje))
                                .map(checkin => checkin.dataHora)
                                .sort((a, b) => new Date(a) - new Date(b)); // Ordenar por horário crescente

                            // Atualizar a lista reativa
                            this.checkinsFeitos = checkinsHoje;
                        }
                    })
                    .catch(error => {
                        alert("Erro ao atualizar check-ins:", error);
                    });
            }
        },

        getLocalizacao() {
            return new Promise((resolve, reject) => {
                if ("geolocation" in navigator) {
                    navigator.geolocation.getCurrentPosition(
                        (position) => {
                            this.checkinInfo.localizacao = {
                                latitude: position.coords.latitude,
                                longitude: position.coords.longitude
                            };
                            resolve();
                        },
                        (error) => {
                            this.checkinInfo.localizacao = null;
                            reject(error);
                        }
                    );
                } else {
                    alert("Geolocalização não suportada pelo navegador.");
                    reject(new Error("Geolocalização não suportada."));
                }
            });
        },

        getDataHora() {
            this.checkinInfo.dataHora = new Date(); // armazna como um objeto Date
        },

        justificativaAtivador() {
            this.justificativaExigindo = true;
        },


        carregarInformacoesPonto() {
            var thisVM = this;

            // // Adicionar timeout de 10 segundos
            // const timeout = setTimeout(() => {
            //     if (!thisVM.verificacaoConcluida) {
            //         thisVM.$buefy.toast.open({
            //             message: 'Tempo limite excedido. Recarregando...',
            //             type: 'is-warning'
            //         });
            //         thisVM.recarregarDados();
            //     }
            // }, 10000);

            thisVM.$store.commit("startLoading");

            firebase.database().ref(`${this.$route.params.time}/Colaboradores/${this.idColaborador}`)
                .once("value")
                .then(snapshot => {
                    // clearTimeout(timeout);

                    const colaborador = snapshot.val();

                    if (!colaborador) {
                        throw new Error("Colaborador não encontrado no banco de dados");
                    }

                    if (colaborador.idPosto == null) {
                        throw new Error("Colaborador não possui posto de trabalho definido.");
                    }
                    thisVM.idPosto = colaborador.idPosto;
                    /**
                     * Configura as informações do ponto do colaborador com base nos dados fornecidos.
                     * 
                     * @property {Object} informacoesPonto - Objeto que armazena as informações do ponto.
                     * @property {string} informacoesPonto.nomeColaborador - Nome do colaborador.
                     * @property {Date} informacoesPonto.horarioInicio - Horário de início do expediente. 
                     *                                                   Usa o horário de entrada do colaborador ou o padrão (08:00) se não fornecido.
                     * @property {Date} informacoesPonto.horarioFim - Horário de término do expediente. 
                     *                                                Usa o horário de saída do colaborador ou o padrão (17:00) se não fornecido.
                     * @property {Date} informacoesPonto.horarioAlmocoInicio - Horário de início do almoço. 
                     *                                                         Usa o horário de início do almoço do colaborador ou o padrão (12:00) se não fornecido.
                     * @property {Date} informacoesPonto.horarioAlmocoFim - Horário de término do almoço. 
                     *                                                      Usa o horário de término do almoço do colaborador ou o padrão (13:00) se não fornecido.
                     * @property {number} informacoesPonto.margemMinutos - Margem de minutos permitida para atrasos. 
                     *                                                     Usa o valor do colaborador ou o padrão (10 minutos) se não fornecido.
                     * @property {boolean} informacoesPonto.fotoExigida - Indica se a foto é exigida para o ponto. 
                     *                                                    Usa o valor do colaborador ou o padrão (true) se não fornecido.
                     * 
                     * @param {Object} colaborador - Objeto contendo os dados do colaborador.
                     * @param {string} colaborador.nome - Nome do colaborador.
                     * @param {Date} [colaborador.horarioEntrada] - Horário de entrada do colaborador.
                     * @param {Date} [colaborador.horarioSaida] - Horário de saída do colaborador.
                     * @param {Date} [colaborador.horarioAlmocoInicio] - Horário de início do almoço do colaborador.
                     * @param {Date} [colaborador.horarioAlmocoFim] - Horário de término do almoço do colaborador.
                     * @param {number} [colaborador.margemMinutos] - Margem de minutos permitida para atrasos do colaborador.
                     * @param {boolean} [colaborador.fotoExigida] - Indica se a foto é exigida para o ponto do colaborador.
                     */
                    thisVM.informacoesPonto = {
                        nomeColaborador: colaborador.nome,
                        horarioInicio: colaborador.horarioEntrada ? colaborador.horarioEntrada : new Date(new Date().setHours(8, 0, 0, 0)),
                        horarioFim: colaborador.horarioSaida ? colaborador.horarioSaida : new Date(new Date().setHours(17, 0, 0, 0)),
                        horarioAlmocoInicio: colaborador.horarioAlmocoInicio ? colaborador.horarioAlmocoInicio : new Date(new Date().setHours(12, 0, 0, 0)),
                        horarioAlmocoFim: colaborador.horarioAlmocoFim ? colaborador.horarioAlmocoFim : new Date(new Date().setHours(13, 0, 0, 0)),

                        margemMinutos: colaborador.margemHorarioMinutos ? colaborador.margemHorarioMinutos : 10, // margem de minutos para considerar atraso ou que a pessoa pode fazer checkin antes do expediente começar,
                        fotoExigida: colaborador.fotoExigida ? colaborador.fotoExigida : true, // se a foto é exigida no checkin
                        nomePosto: colaborador.nomePosto, // nome do posto de trabalho
                        dentroMargem: false, // afirma se o horario de entrada esta dentro da margem ou não
                        posicaoReferencia: { latitude: 0, longitude: 0 }, // coordenadas do posto de trbalho do colaborador

                        margemDistancia: 0, // margem de distancia em metros para considerar que o colaborador esta no local correto
                    }
                    // thisVM.informacoesPonto.nomeColaborador = colaborador.nome;
                    // thisVM.informacoesPonto.horarioInicio = colaborador.horarioEntrada ? colaborador.horarioEntrada : new Date(new Date().setHours(8, 0, 0, 0));
                    // thisVM.informacoesPonto.horarioFim = colaborador.horarioSaida ? colaborador.horarioSaida : new Date(new Date().setHours(17, 0, 0, 0));
                    // thisVM.informacoesPonto.horarioAlmocoInicio = colaborador.horarioAlmocoInicio ? colaborador.horarioAlmocoInicio : new Date(new Date().setHours(12, 0, 0, 0));
                    // thisVM.informacoesPonto.horarioAlmocoFim = colaborador.horarioAlmocoFim ? colaborador.horarioAlmocoFim : new Date(new Date().setHours(13, 0, 0, 0));
                    // thisVM.informacoesPonto.margemMinutos = colaborador.margemHorarioMinutos ? colaborador.margemHorarioMinutos : 10;
                    // thisVM.informacoesPonto.fotoExigida = colaborador.fotoExigida ? colaborador.fotoExigida : true;

                    thisVM.$store.commit("stopLoading");
                    thisVM.carregarDetalhesPosto();
                })
                .catch((err) => {
                    //  clearTimeout(timeout);
                    alert("Erro ao carregar colaborador:", err);
                    thisVM.mostrarErroRecarregamento();
                });
        }
    },

    mounted() {
        this.getDataHora();
        this.idProntuario = this.$route.params.idProntuario;
        this.idColaborador = this.$route.params.idColaborador;

        // Verificar se os parâmetros existem
        if (!this.idProntuario || !this.idColaborador) {
            this.$buefy.dialog.alert({
                title: 'Parâmetros Inválidos',
                message: 'Por favor, escaneie o QR code novamente.',
                type: 'is-danger'
            });
            return;
        }

        this.getLocalizacao();
        this.carregarInformacoesPonto();

        // // Verificação automática após 5 segundos
        // setTimeout(() => {
        //     if (!this.dadosValidos || !this.verificacaoConcluida) {
        //         this.$buefy.dialog.confirm({
        //             title: 'Carregamento Lento',
        //             message: 'Os dados estão demorando para carregar. Deseja aguardar mais ou escanear o QR code novamente?',
        //             confirmText: 'Aguardar',
        //             cancelText: 'Escanear QR Code',
        //             type: 'is-warning',
        //             onCancel: () => {
        //                 this.$buefy.dialog.alert({
        //                     message: 'Por favor, escaneie o QR code novamente.',
        //                     type: 'is-info'
        //                 });
        //             }
        //         });
        //     }
        // }, 5000);

        // Verifica se existem registros de ponto no Firebase
        if (this.idProntuario && this.idColaborador) {
            const fbPath = `${this.$route.params.time}/resultadosOperacao/prontuarios/${this.idProntuario}/${this.idColaborador}/registrosPontos`;

            firebase.database().ref(fbPath).once('value')
                .then(snapshot => {
                    const dados = snapshot.val();
                    if (dados) {
                        // Extrair os check-ins feitos hoje
                        const hoje = new Date().toISOString().split('T')[0];
                        const checkinsHoje = Object.values(dados)
                            .filter(checkin => checkin.dataHora.startsWith(hoje))
                            .map(checkin => checkin.dataHora);

                        this.checkinsFeitos = checkinsHoje;
                    }
                })
                .catch(error => {
                    alert("Erro ao carregar check-ins anteriores:", error);
                });
        }
    }
}
</script>
