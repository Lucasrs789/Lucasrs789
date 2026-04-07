<template>
    <layout-default>
        <div class="box">
            <h1 class="title is-4 mb-5">Cadastrar Postos de Trabalho</h1>

            <div class="columns is-variable is-6">
                <!-- Formulário de Cadastro -->
                <div class="column is-6">
                    <div class="box">
                        <div class="field">
                            <label class="label">Nome do Posto</label>
                            <div class="control">
                                <input class="input" v-model="novoPosto.nome" type="text" placeholder="Nome do posto"
                                    required />
                            </div>
                        </div>

                        <div class="field">
                            <label class="label">Latitude</label>
                            <div class="control">
                                <input class="input" v-model="novoPosto.latitude" type="number" placeholder="Latitude"
                                    required />
                            </div>
                        </div>

                        <div class="field">
                            <label class="label">Longitude</label>
                            <div class="control">
                                <input class="input" v-model="novoPosto.longitude" type="number" placeholder="Longitude"
                                    required />
                            </div>
                        </div>

                        <!-- Novo campo para Margem de Distância -->
                        <div class="field">
                            <label class="label">Margem de Distância (metros)</label>
                            <div class="control has-icons-right">
                                <input class="input" v-model="novoPosto.margemDistancia" type="number" min="1" step="1"
                                    placeholder="Distância em metros" required />
                                <span class="icon is-small is-right">
                                    <i class="fas fa-ruler-horizontal"></i>
                                </span>
                            </div>
                            <p class="help">Defina a margem de distância permitida para registro de ponto neste local
                                (em metros)</p>
                        </div>

                        <!-- Botão para abrir o mapa -->
                        <div class="field">
                            <div class="control">
                                <button class="button is-info" @click="abrirMapaSelecao">
                                    <span class="icon">
                                        <i class="fas fa-map-marker-alt"></i>
                                    </span>
                                    <span>Selecionar no mapa</span>
                                </button>
                            </div>
                        </div>
                        <div class="field">
                            <label class="label">Responsável</label>
                            <div class="control">
                                <input class="input" v-model="novoPosto.responsavel" type="text"
                                    placeholder="Responsável" required />
                            </div>
                        </div>

                        <div class="field is-grouped is-justify-content-flex-end">
                            <div class="control">
                                <button class="button is-success" @click="salvarPosto()">Gravar</button>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Coluna Direita: Mapa -->
                <div class="column is-6">
                    <div class="box">
                        <h2 class="title is-5">Mapa dos Postos</h2>
                        <div id="mapa-postos" style="height: 500px;"></div>
                    </div>
                </div>
            </div>

        </div>


        <!-- Lista de Postos -->
        <div class="column is-6">
            <div class="box">
                <h2 class="title is-5">Postos Cadastrados</h2>
                <table class="table is-fullwidth is-striped">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Raio</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="posto in postosSalvos" :key="posto.id">
                            <td>{{ posto.nome }}</td>
                            <td>{{ posto.margemDistancia || '100' }} m</td>
                            <td>
                                <button class="button is-info is-small" @click="verDetalhesPosto(posto)">
                                    Detalhes
                                </button>
                                &nbsp;
                                <b-button class="button is-success is-small" @click="editarPosto(posto)">
                                    Editar
                                </b-button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>


        <!-- Modal de Detalhes -->
        <b-modal :active.sync="isModalActive" has-modal-card>
            <div class="modal-card" style="width: auto">
                <header class="modal-card-head">
                    <p class="modal-card-title">Detalhes do Posto: {{ postoSelecionado ? postoSelecionado.nome : ''
                    }}</p>

                    <button class="delete" aria-label="close" @click="isModalActive = false"></button>
                </header>
                <section class="modal-card-body">
                    <div v-if="postoSelecionado">
                        <div class="field is-horizontal">
                            <div class="field-label is-normal">
                                <label class="label">Nome:</label>
                            </div>
                            <div class="field-body">
                                <div class="field">
                                    <p class="control">{{ postoSelecionado.nome }}</p>
                                </div>
                            </div>
                        </div>

                        <div class="field is-horizontal">
                            <div class="field-label is-normal">
                                <label class="label">Responsável:</label>
                            </div>
                            <div class="field-body">
                                <div class="field">
                                    <p class="control">{{ postoSelecionado.responsavel }}</p>
                                </div>
                            </div>
                        </div>

                        <!-- Exibir margem de distância -->
                        <div class="field is-horizontal">
                            <div class="field-label is-normal">
                                <label class="label">Margem:</label>
                            </div>
                            <div class="field-body">
                                <div class="field">
                                    <p class="control">
                                        <span class="tag is-info is-medium">
                                            <i class="fas fa-ruler-horizontal mr-2"></i>
                                            {{ postoSelecionado.margemDistancia || '100' }} metros
                                        </span>
                                    </p>
                                </div>
                            </div>
                        </div>

                        <div class="field is-horizontal">
                            <div class="field-label is-normal">
                                <label class="label">QR Code:</label>
                            </div>
                            <div class="field-body">
                                <div class="field is-grouped">
                                    <figure class="image is-128x128">
                                        <img v-if="qrCodeData" :src="qrCodeData" alt="QR Code">
                                    </figure>
                                    <p class="control ml-3">
                                        <button @click="gerarPDFQRCode" class="button is-primary"
                                            :disabled="!postoSelecionado || !qrCodeData">
                                            Gerar PDF
                                        </button>
                                    </p>

                                </div>
                            </div>
                        </div>
                        <div class="field is-horizontal">
                            <div class="field-label is-normal">
                                <label class="label">Link para registro do ponto:</label>
                            </div>
                            <div class="field-body">
                                <div class="field is-grouped">


                                    {{
                                        `${baseUrl}/#/${$route.params.time}/ControlePonto/${postoSelecionado.id}`
                                    }}

                                </div>
                            </div>
                        </div>
                        <hr>

                        <h4 class="title is-5 mb-3">Colaboradores neste Posto</h4>
                        <div v-if="colaboradoresDoPosto.length > 0">
                            <table class="table is-fullwidth is-striped">
                                <thead>
                                    <tr>
                                        <th>Registro</th>
                                        <th>Nome</th>
                                        <th>Função</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="colab in colaboradoresDoPosto" :key="colab.id">
                                        <td>{{ colab.codigo }}</td>
                                        <td>{{ colab.nome }}</td>
                                        <td>{{ colab.Funcao }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div v-else class="notification is-light">
                            Nenhum colaborador designado para este posto.
                        </div>
                    </div>
                </section>
                <footer class="modal-card-foot">
                    <button class="button" @click="isModalActive = false">Fechar</button>
                </footer>
            </div>
        </b-modal>
        <!-- Modal de Edição -->
        <b-modal :active.sync="isModalEdicaoActive" has-modal-card>
            <div class="modal-card" style="width: auto">
                <header class="modal-card-head">
                    <p class="modal-card-title">Editar Posto: {{ form.nome }}</p>
                    <button class="delete" aria-label="close" @click="isModalEdicaoActive = false"></button>
                </header>
                <section class="modal-card-body">
                    <!-- Formulário de Edição (igual ao de cadastro) -->
                    <div class="field">
                        <label class="label">Nome do Posto</label>
                        <div class="control">
                            <input class="input" v-model="form.nome" type="text" placeholder="Nome do posto" required />
                        </div>
                    </div>

                    <div class="field">
                        <label class="label">Latitude</label>
                        <div class="control">
                            <input class="input" v-model="form.localizacao.latitude" type="number"
                                placeholder="Latitude" required />
                        </div>
                    </div>

                    <div class="field">
                        <label class="label">Longitude</label>
                        <div class="control">
                            <input class="input" v-model="form.localizacao.longitude" type="number"
                                placeholder="Longitude" required />
                        </div>
                    </div>

                    <!-- Novo campo de margem de distância na edição -->
                    <div class="field">
                        <label class="label">Margem de Distância (metros)</label>
                        <div class="control has-icons-right">
                            <input class="input" v-model="form.margemDistancia" type="number" min="1" step="1"
                                placeholder="Distância em metros" required />
                            <span class="icon is-small is-right">
                                <i class="fas fa-ruler-horizontal"></i>
                            </span>
                        </div>
                        <p class="help">Define o raio de distância permitido para registro (em metros)</p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-info" @click="abrirMapaSelecaoParaEdicao">
                                <span class="icon">
                                    <i class="fas fa-map-marker-alt"></i>
                                </span>
                                <span>Selecionar no mapa</span>
                            </button>
                        </div>
                    </div>

                    <div class="field">
                        <label class="label">Responsável</label>
                        <div class="control">
                            <input class="input" v-model="form.responsavel" type="text" placeholder="Responsável"
                                required />
                        </div>
                    </div>
                </section>
                <footer class="modal-card-foot">
                    <button class="button is-success" @click="salvarEdicao">Salvar</button>
                    <button class="button" @click="isModalEdicaoActive = false">Cancelar</button>
                </footer>
            </div>
        </b-modal>
        <!-- Modal do Mapa -->
        <b-modal :active.sync="isMapModalActive" has-modal-card>

            <div class="modal-card" style="width: 80%; max-width: 800px;">
                <header class="modal-card-head">
                    <p class="modal-card-title">Selecione a localização</p>
                    <button class="delete" aria-label="close" @click="isMapModalActive = false"></button>
                </header>

                <section class="modal-card-body">
                    <div class="field has-addons mb-3">
                        <!-- Campo de busca de endereço no modal de mapa -->
                        <b-field label="Buscar endereço ou CEP">&nbsp;
                            <b-input v-model="cepBusca" placeholder="Exemplo: Av. Francisco Ferreira Lopes, 4412"
                                @keyup.enter="buscarEndereco"></b-input>
                            <b-button type="is-primary" @click="buscarEndereco">Buscar</b-button>
                        </b-field>
                    </div>
                    Exemplo: Av. Francisco Ferreira Lopes, 4412

                    <!-- Mensagem de feedback -->
                    <div class="notification is-light"
                        :class="{ 'is-info': mensagemCep && !mensagemCep.includes('Erro'), 'is-danger': mensagemCep && mensagemCep.includes('Erro') }"
                        v-if="mensagemCep">
                        {{ mensagemCep }}
                    </div>
                    <div class="notification is-info is-light">
                        Clique no mapa para selecionar a localização do posto de trabalho.
                    </div>
                    <div id="mapa-selecao" style="height: 400px; width: 100%;"></div>
                    <div class="mt-3" v-if="coordenadasSelecionadas">
                        <p><strong>Latitude:</strong> {{ coordenadasSelecionadas.lat }}</p>
                        <p><strong>Longitude:</strong> {{ coordenadasSelecionadas.lng }}</p>
                    </div>
                </section>
                <footer class="modal-card-foot">
                    <button class="button is-primary" @click="confirmarLocalizacao"
                        :disabled="!coordenadasSelecionadas">Confirmar</button>
                    <button class="button" @click="isMapModalActive = false">Cancelar</button>
                </footer>

            </div>
        </b-modal>


    </layout-default>
</template>

<style>
/* Garante que os modais fiquem acima do mapa */
.modal-card,
.modal {
    z-index: 1000 !important;
}

#mapa-postos {
    width: 100%;
    height: 500px;
    border-radius: 4px;
}

.leaflet-popup-content {
    min-width: 200px;
}

.leaflet-popup-content button {
    margin-top: 8px;
    width: 100%;
}

.leaflet-text-path {
    font-size: 12px;
    font-weight: bold;
    fill: #333;
    stroke: white;
    stroke-width: 2px;
    paint-order: stroke;
    text-anchor: middle;
}
</style>

<script>
import QRCode from "qrcode";
import firebase from "firebase";
import jsPDF from "jspdf"; // Biblioteca para geração de PDF
import L from "leaflet";


export default {
    name: 'PostosTrabalho',
    data() {
        return {
            baseUrl: window.location.origin,
            postosSalvos: [],
            novoPosto: {
                nome: "",
                localizacao: {
                    latitude: "",
                    longitude: ""
                },
                responsavel: "",
            },
            isModalEdicaoActive: false,
            modoMapaParaEdicao: false,
            form: {
                id: null,
                nome: "",
                localizacao: {
                    latitude: "",
                    longitude: ""
                },
                responsavel: "",
                margemDistancia: 100
            },

            margemDistancia: 100,

            postoSelecionado: null,
            qrCodeData: null,
            isModalActive: false,
            colaboradoresDoPosto: [],

            isMapModalActive: false,
            mapaInstance: null,
            marcador: null,
            coordenadasSelecionadas: null,
            cepBusca: "",
            mensagemCep: "",
            carregandoCep: false,

            editandoId: null,

        }
    },

    methods: {
        // Método para buscar endereço ou CEP usando a API Nominatim
        async buscarEndereco() {
            var thisVM = this;

            // Se não digitou nada, sai
            if (!thisVM.cepBusca || thisVM.cepBusca.length < 3) {
                thisVM.$buefy.toast.open({
                    message: 'Digite um endereço ou CEP válido',
                    type: 'is-warning'
                });
                return;
            }

            // Monta a URL da API de geocodificação
            const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(thisVM.cepBusca)}`;

            try {
                // Faz a requisição para obter as coordenadas
                const response = await fetch(url, {
                    headers: {
                        'Accept-Language': 'pt-BR' // Retorna nomes em português se possível
                    }
                });
                const data = await response.json();

                // Se não encontrar resultado, avisa
                if (!data || data.length === 0) {
                    thisVM.$buefy.toast.open({
                        message: 'Endereço não encontrado',
                        type: 'is-danger'
                    });
                    return;
                }

                // Pega o primeiro resultado (o mais relevante)
                const resultado = data[0];
                const lat = parseFloat(resultado.lat);
                const lng = parseFloat(resultado.lon);

                // Atualiza o mapa e o marcador
                if (thisVM.mapaInstance) {
                    thisVM.mapaInstance.setView([lat, lng], 17); // Centraliza o mapa no local
                    thisVM.adicionarMarcador({ lat, lng }); // Adiciona marcador
                    thisVM.coordenadasSelecionadas = { lat, lng }; // Salva coordenadas
                }

                // Mostra um aviso com o endereço encontrado
                thisVM.$buefy.toast.open({
                    message: 'Endereço encontrado e centralizado no mapa',
                    type: 'is-success'
                });

            } catch (error) {
                // Mostra erro caso a API falhe
                thisVM.$buefy.toast.open({
                    message: 'Erro ao buscar o endereço',
                    type: 'is-danger'
                });
            }
        },
        adicionarMarcadoresPostosExistentes() {
            var thisVM = this;

            // Remove marcadores existentes se houver
            if (thisVM.marcadoresPostos) {
                thisVM.marcadoresPostos.forEach(marker => {
                    thisVM.mapaInstance.removeLayer(marker);
                });
            }

            thisVM.marcadoresPostos = [];

            // Adiciona um marcador para cada posto
            thisVM.postosSalvos.forEach(posto => {
                if (posto.localizacao && posto.localizacao.latitude && posto.localizacao.longitude) {
                    const lat = parseFloat(posto.localizacao.latitude);
                    const lng = parseFloat(posto.localizacao.longitude);

                    // Cria um marcador diferente (azul) para os postos existentes
                    const marcador = L.marker([lat, lng], {
                        icon: L.icon({
                            iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
                            iconSize: [25, 41],
                            iconAnchor: [12, 41],
                            popupAnchor: [1, -34],
                            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
                            shadowSize: [41, 41]
                        })
                    }).addTo(thisVM.mapaInstance);

                    // Adiciona popup com informações do posto
                    marcador.bindPopup(`
                <strong>${posto.nome}</strong><br>
                Lat: ${lat.toFixed(6)}<br>
                Lng: ${lng.toFixed(6)}<br>
                ${posto.responsavel ? 'Resp: ' + posto.responsavel : ''}
            `);

                    thisVM.marcadoresPostos.push(marcador);
                }
            });
        },
        // Método para permitir apenas números no campo de CEP
        permitirApenasNumeros(event) {
            const charCode = (event.which) ? event.which : event.keyCode;
            if (charCode > 31 && (charCode < 48 || charCode > 57)) {
                event.preventDefault();
                return false;
            }
            return true;
        },
        // Método aprimorado para buscar CEP com precisão a nível de rua
        async buscarCep() {
            var thisVM = this;

            // Validação do CEP
            if (!thisVM.cepBusca || thisVM.cepBusca.length < 8) {
                thisVM.mensagemCep = "Digite um CEP válido com 8 dígitos";
                return;
            }

            thisVM.mensagemCep = "Buscando CEP...";
            thisVM.carregandoCep = true;
            thisVM.$store.commit("startLoading");

            try {
                // Usando o serviço ViaCEP
                const response = await fetch(`https://viacep.com.br/ws/${thisVM.cepBusca}/json/`);
                const endereco = await response.json();

                if (endereco.erro) {
                    thisVM.mensagemCep = "CEP não encontrado";
                    thisVM.$store.commit("stopLoading");
                    thisVM.carregandoCep = false;
                    return;
                }

                // Verifica se temos informações suficientes para buscar a rua
                if (!endereco.logradouro) {
                    thisVM.mensagemCep = "CEP encontrado, mas sem informações de rua. Tente selecionar no mapa.";
                    await thisVM.geocodificarCidadeEstado(endereco);
                    return;
                }

                // Formatação de endereço otimizada para melhor resultado de geocodificação
                const rua = endereco.logradouro.replace(/[^\w\s]/gi, ' '); // Remove caracteres especiais
                const bairro = endereco.bairro ? endereco.bairro : '';

                // Formatos de endereço que tentaremos, do mais específico ao menos específico
                const formatos = [
                    // Formato 1: Rua completa com número aproximado no meio da rua (para melhor precisão)
                    `${rua}, 100, ${bairro}, ${endereco.localidade}, ${endereco.uf}, Brasil`,
                    // Formato 2: Rua sem número
                    `${rua}, ${bairro}, ${endereco.localidade}, ${endereco.uf}, Brasil`,
                    // Formato 3: Apenas rua e cidade
                    `${rua}, ${endereco.localidade}, ${endereco.uf}, Brasil`,
                    // Formato 4: Último recurso - cidade e estado
                    `${endereco.localidade}, ${endereco.uf}, Brasil`
                ];

                let coordenadas = null;
                for (const formato of formatos) {
                    // Tenta cada formato até obter sucesso
                    coordenadas = await thisVM.obterCoordenadas(formato);
                    if (coordenadas) break;
                }

                if (coordenadas) {
                    // Centraliza o mapa na nova localização com zoom apropriado
                    // Zoom 17 para rua, 13 para cidade
                    const zoomLevel = formatos.indexOf(formatos.find(f => f === coordenadas.formatoUsado)) <= 2 ? 17 : 13;
                    thisVM.mapaInstance.setView([coordenadas.lat, coordenadas.lng], zoomLevel);

                    // Adiciona o marcador
                    thisVM.adicionarMarcador(coordenadas);

                    // Atualiza as coordenadas selecionadas
                    thisVM.coordenadasSelecionadas = coordenadas;

                    // Atualiza a mensagem com o endereço encontrado
                    thisVM.mensagemCep = formatos.indexOf(coordenadas.formatoUsado) <= 2 ?
                        `Endereço encontrado: ${endereco.logradouro}, ${endereco.bairro}, ${endereco.localidade}` :
                        `Localização aproximada: ${endereco.localidade}, ${endereco.uf}. Ajuste o marcador se necessário.`;

                    // Se estiver no modo de edição, atualiza o form, senão atualiza o novoPosto
                    if (thisVM.modoMapaParaEdicao) {
                        thisVM.form.localizacao.latitude = coordenadas.lat.toFixed(6);
                        thisVM.form.localizacao.longitude = coordenadas.lng.toFixed(6);
                    } else {
                        thisVM.novoPosto.latitude = coordenadas.lat.toFixed(6);
                        thisVM.novoPosto.longitude = coordenadas.lng.toFixed(6);
                    }
                } else {
                    thisVM.mensagemCep = "Não foi possível obter as coordenadas precisas. Tente selecionar no mapa.";
                    // Tenta pelo menos posicionar na cidade
                    await thisVM.geocodificarCidadeEstado(endereco);
                }
            } catch (error) {
                alert("Erro ao buscar CEP: " + error);
                thisVM.mensagemCep = "Erro ao buscar o CEP. Verifique sua conexão.";
            } finally {
                thisVM.$store.commit("stopLoading");
                thisVM.carregandoCep = false;
            }
        },

        // Método auxiliar para tentar diferentes serviços de geocodificação
        async obterCoordenadas(endereco) {
            try {


                // Usando o Nominatim com parâmetros otimizados para precisão de rua
                const geocodeResponse = await fetch(
                    `https://nominatim.openstreetmap.org/search?` +
                    `format=json&` +
                    `street=${encodeURIComponent(endereco.split(',')[0].trim())}&` + // Tenta extrair a rua
                    `city=${encodeURIComponent(endereco.split(',')[2]?.trim() || endereco.split(',')[1]?.trim() || '')}&` +
                    `state=${encodeURIComponent(endereco.split(',')[3]?.trim() || '')}&` +
                    `country=Brasil&` +
                    `addressdetails=1&` +
                    `limit=1`,
                    {
                        headers: {
                            'User-Agent': 'PostosTrabalhoApp/1.0',
                            'Accept-Language': 'pt-BR'
                        }
                    }
                );

                const localizacoes = await geocodeResponse.json();

                // Se não funcionou com parâmetros estruturados, tenta com query completa
                if (!localizacoes || localizacoes.length === 0) {
                    const geocodeResponse2 = await fetch(
                        `https://nominatim.openstreetmap.org/search?` +
                        `format=json&` +
                        `q=${encodeURIComponent(endereco)}&` +
                        `addressdetails=1&` +
                        `limit=1`,
                        {
                            headers: {
                                'User-Agent': 'PostosTrabalhoApp/1.0',
                                'Accept-Language': 'pt-BR'
                            }
                        }
                    );

                    const localizacoes2 = await geocodeResponse2.json();

                    if (localizacoes2 && localizacoes2.length > 0) {
                        return {
                            lat: parseFloat(localizacoes2[0].lat),
                            lng: parseFloat(localizacoes2[0].lon),
                            formatoUsado: endereco
                        };
                    }

                    return null;
                }

                return {
                    lat: parseFloat(localizacoes[0].lat),
                    lng: parseFloat(localizacoes[0].lon),
                    formatoUsado: endereco
                };
            } catch (error) {
                alert("Erro ao obter coordenadas: " + error);
                return null;
            }
        },

        // Método para tentar pelo menos geocodificar a cidade
        async geocodificarCidadeEstado(endereco) {
            var thisVM = this;
            try {
                const cidadeEstado = `${endereco.localidade}, ${endereco.uf}, Brasil`;
                const coordenadas = await thisVM.obterCoordenadas(cidadeEstado);

                if (coordenadas) {
                    thisVM.mapaInstance.setView([coordenadas.lat, coordenadas.lng], 13); // Zoom para nível de cidade
                    thisVM.mensagemCep += " Mostrando a localização da cidade.";
                }
            } catch (error) {
                alert("Erro ao geocodificar cidade: " + error);
            }
        },
        // Novo método para verificar existência de postos com o mesmo nome
        async verificarNomeDuplicado(nome, idAtual = null) {
            var thisVM = this;

            // Normaliza o nome para comparação (converte para lowercase)
            const nomeNormalizado = nome.trim().toLowerCase();

            // Verifica se já existe na lista local primeiro (mais rápido)
            const postoExistente = thisVM.postosSalvos.find(posto =>
                posto.nome.trim().toLowerCase() === nomeNormalizado &&
                posto.id !== idAtual // Ignora o próprio posto ao editar
            );

            if (postoExistente) {
                return true; // Nome duplicado encontrado na lista local
            }

            // Verificação no Firebase para garantir dados atualizados
            try {
                const snapshot = await firebase.database()
                    .ref(thisVM.$route.params.time + "/postosTrabalho")
                    .once("value");

                let duplicadoEncontrado = false;

                snapshot.forEach(child => {
                    // Ignora o contador e o próprio registro sendo editado
                    if (child.key !== "_count" && child.key !== idAtual) {
                        const postoNome = child.val().nome;
                        if (postoNome && postoNome.trim().toLowerCase() === nomeNormalizado) {
                            duplicadoEncontrado = true;
                            return true; // Sai do forEach
                        }
                    }
                });

                return duplicadoEncontrado;
            } catch (error) {
                alert("Erro ao verificar nome duplicado:", error);
                return false; // Em caso de erro, permite continuar
            }
        },

        editarPosto(posto) {
            var thisVM = this;

            // Preenche o formulário com os dados do posto selecionado
            thisVM.form.id = posto.id;
            thisVM.form.nome = posto.nome;
            thisVM.form.responsavel = posto.responsavel || '';
            thisVM.form.margemDistancia = posto.margemDistancia || 100;

            // Garante que a estrutura de localização existe
            thisVM.form.localizacao = posto.localizacao || {
                latitude: '',
                longitude: ''
            };

            // Converte para números se for string
            if (typeof thisVM.form.localizacao.latitude === 'string') {
                thisVM.form.localizacao.latitude = parseFloat(thisVM.form.localizacao.latitude) || '';
            }
            if (typeof thisVM.form.localizacao.longitude === 'string') {
                thisVM.form.localizacao.longitude = parseFloat(thisVM.form.localizacao.longitude) || '';
            }

            // Abre o modal de edição
            thisVM.isModalEdicaoActive = true;
        },
        abrirMapaSelecaoParaEdicao() {
            var thisVM = this;
            thisVM.cepBusca = ""; // Limpa o campo de CEP
            thisVM.mensagemCep = ""; // Limpa a mensagem
            thisVM.modoMapaParaEdicao = true; // Flag para identificar que estamos editando
            thisVM.isMapModalActive = true;

            thisVM.$nextTick(() => {
                thisVM.inicializarMapa();

                // Se já tiver coordenadas no formulário, centraliza o mapa nelas
                if (thisVM.form.localizacao.latitude && thisVM.form.localizacao.longitude) {
                    const lat = parseFloat(thisVM.form.localizacao.latitude);
                    const lng = parseFloat(thisVM.form.localizacao.longitude);

                    // Aguarda o mapa estar pronto
                    setTimeout(() => {
                        if (thisVM.mapaInstance) {
                            thisVM.mapaInstance.setView([lat, lng], 17); // Zoom 17 para vista mais próxima
                            thisVM.adicionarMarcador({ lat, lng });
                            thisVM.coordenadasSelecionadas = { lat, lng };
                        }
                    }, 300);
                }
            });
        },
        async salvarEdicao() {
            var thisVM = this;

            try {
                // Verifica campos obrigatórios
                if (!thisVM.form.nome || !thisVM.form.localizacao.latitude || !thisVM.form.localizacao.longitude) {
                    thisVM.$buefy.toast.open({
                        message: 'Preencha todos os campos obrigatórios',
                        type: 'is-warning'
                    });
                    return;
                }

                // Verifica se o nome já existe (ignorando o próprio posto)
                const nomeDuplicado = await thisVM.verificarNomeDuplicado(thisVM.form.nome, thisVM.form.id);
                if (nomeDuplicado) {
                    thisVM.$buefy.toast.open({
                        message: 'Já existe um posto com este nome. Por favor, escolha outro nome.',
                        type: 'is-danger',
                        duration: 5000
                    });
                    return;
                }

                const postoData = {
                    nome: thisVM.form.nome,
                    localizacao: {
                        latitude: thisVM.form.localizacao.latitude,
                        longitude: thisVM.form.localizacao.longitude
                    },
                    responsavel: thisVM.form.responsavel,
                    margemDistancia: parseInt(thisVM.form.margemDistancia) || 100
                };

                // Atualiza no Firebase Realtime Database
                await firebase.database()
                    .ref(`${thisVM.$route.params.time}/postosTrabalho/${thisVM.form.id}`)
                    .update(postoData);

                // Atualiza a lista local
                const index = thisVM.postosSalvos.findIndex(p => p.id === thisVM.form.id);
                if (index !== -1) {
                    thisVM.postosSalvos.splice(index, 1, {
                        ...thisVM.postosSalvos[index],
                        ...postoData
                    });
                }

                // Fecha o modal e limpa o formulário
                thisVM.isModalEdicaoActive = false;
                thisVM.$buefy.toast.open({
                    message: 'Posto atualizado com sucesso!',
                    type: 'is-success'
                });

            } catch (error) {
                thisVM.$buefy.toast.open({
                    message: 'Erro ao atualizar posto: ' + error.message,
                    type: 'is-danger'
                });
            }
        },

        resetarFormulario() {
            var thisVM = this;
            thisVM.novoPosto = {
                nome: "",
                latitude: "",
                longitude: "",
                responsavel: "",
                setor: "",
                descricao: "",
                ativo: true
            };
            thisVM.editandoId = null;
        },

        abrirMapaSelecao() {
            var thisVM = this;
            thisVM.cepBusca = ""; // Limpa o campo de CEP
            thisVM.mensagemCep = ""; // Limpa a mensagem
            thisVM.isMapModalActive = true;
            thisVM.$nextTick(() => {
                thisVM.inicializarMapa();
            });
        },

        inicializarMapaPostos() {
            var thisVM = this;

            // Remove o mapa anterior se já existir
            if (thisVM.mapaPostosInstance) {
                thisVM.mapaPostosInstance.remove();
                thisVM.mapaPostosInstance = null;
            }

            const divMapa = document.getElementById('mapa-postos');
            if (!divMapa) return;

            // Coordenadas iniciais (centro do Brasil como fallback)
            let coordenadasIniciais = [-15.77972, -47.92972];
            let zoomInicial = 5;

            // Se houver postos, centraliza no primeiro posto com zoom maior
            if (thisVM.postosSalvos.length > 0 && thisVM.postosSalvos[0].localizacao) {
                coordenadasIniciais = [
                    parseFloat(thisVM.postosSalvos[0].localizacao.latitude),
                    parseFloat(thisVM.postosSalvos[0].localizacao.longitude)
                ];
                zoomInicial = 15;
            }

            // Inicializa o mapa
            thisVM.mapaPostosInstance = L.map('mapa-postos').setView(coordenadasIniciais, zoomInicial);

            
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(thisVM.mapaPostosInstance);

            thisVM.postosSalvos.forEach(posto => {
                if (posto.localizacao && posto.localizacao.latitude && posto.localizacao.longitude) {
                    const lat = parseFloat(posto.localizacao.latitude);
                    const lng = parseFloat(posto.localizacao.longitude);

                    // Cria um ícone personalizado com o nome
                    const iconHtml = `
                <div style="position:relative; text-align:center;">
                    <img src="https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png" 
                         style="width:25px;height:41px;">
                    <div style="position:absolute; 
                                top:-10px; 
                                left:0; 
                                right:0; 
                                font-size:12px; 
                                font-weight:bold; 
                                color:#333;
                                text-shadow: -1px -1px 0 #fff, 1px -1px 0 #fff, -1px 1px 0 #fff, 1px 1px 0 #fff;
                                white-space:nowrap;">
                        ${posto.nome}
                    </div>
                </div>
            `;

                    const customIcon = L.divIcon({
                        html: iconHtml,
                        className: 'custom-marker',
                        iconSize: [25, 41],
                        iconAnchor: [12, 41]
                    });

                    const marcador = L.marker([lat, lng], { icon: customIcon })
                        .addTo(thisVM.mapaPostosInstance);

                    // Adiciona popup com informações do posto
                    marcador.bindPopup(`
                <strong>${posto.nome}</strong><br>
                <small>${posto.responsavel || 'Sem responsável'}</small><br>
                Lat: ${lat.toFixed(6)}<br>
                Lng: ${lng.toFixed(6)}<br>
                Margem: ${posto.margemDistancia || 100}m<br>
                <button class="button is-small is-info" onclick="app.verDetalhesPosto(${JSON.stringify(posto).replace(/"/g, '&quot;')})">
                    Ver detalhes
                </button>
            `);
                }
            });
        },
        inicializarMapa() {
            var thisVM = this;
            if (thisVM.mapaInstance) {
                thisVM.mapaInstance.remove();
                thisVM.mapaInstance = null;
            }

            const mapDiv = document.getElementById('mapa-selecao');
            if (!mapDiv) return;

            // Coordenadas iniciais (Brasil)
            let coordenadas = { lat: -15.77972, lng: -47.92972 };
            let zoomInicial = 5;

            // Verifica se já existe alguma coordenada definida
            if (thisVM.modoMapaParaEdicao) {
                if (thisVM.form.localizacao.latitude && thisVM.form.localizacao.longitude) {
                    coordenadas.lat = parseFloat(thisVM.form.localizacao.latitude);
                    coordenadas.lng = parseFloat(thisVM.form.localizacao.longitude);
                    zoomInicial = 15;
                }
            } else {
                if (thisVM.novoPosto.latitude && thisVM.novoPosto.longitude) {
                    coordenadas.lat = parseFloat(thisVM.novoPosto.latitude);
                    coordenadas.lng = parseFloat(thisVM.novoPosto.longitude);
                    zoomInicial = 15;
                }
            }

            // Inicializa o mapa
            thisVM.mapaInstance = L.map('mapa-selecao').setView([coordenadas.lat, coordenadas.lng], zoomInicial);

            // Adiciona o tile layer do OpenStreetMap
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(thisVM.mapaInstance);

            // Adiciona marcadores dos postos existentes
            thisVM.adicionarMarcadoresPostosExistentes();

            // Adiciona o marcador inicial se houver coordenadas
            if ((thisVM.modoMapaParaEdicao && thisVM.form.localizacao.latitude) ||
                (!thisVM.modoMapaParaEdicao && thisVM.novoPosto.latitude)) {
                thisVM.adicionarMarcador(coordenadas);
                thisVM.coordenadasSelecionadas = coordenadas;
            }

            // Adiciona evento de clique no mapa
            thisVM.mapaInstance.on('click', (event) => {
                const novasCoordenadas = {
                    lat: event.latlng.lat,
                    lng: event.latlng.lng
                };
                thisVM.adicionarMarcador(novasCoordenadas);
                thisVM.coordenadasSelecionadas = novasCoordenadas;
            });
        },

        adicionarMarcador(coordenadas) {
            var thisVM = this;

            // Remove marcador existente, se houver
            if (thisVM.marcador) {
                thisVM.mapaInstance.removeLayer(thisVM.marcador);
            }

            // Adiciona novo marcador com possibilidade de arrastar
            thisVM.marcador = L.marker([coordenadas.lat, coordenadas.lng], {
                draggable: true
            }).addTo(thisVM.mapaInstance);

            // Adiciona popup com as coordenadas
            thisVM.marcador.bindPopup(`Latitude: ${coordenadas.lat.toFixed(6)}<br>Longitude: ${coordenadas.lng.toFixed(6)}`);

            // Atualiza coordenadas quando o marcador é arrastado
            thisVM.marcador.on('dragend', (event) => {
                const position = event.target.getLatLng();
                thisVM.coordenadasSelecionadas = {
                    lat: position.lat,
                    lng: position.lng
                };
                // Atualiza o popup com as novas coordenadas
                thisVM.marcador.bindPopup(`Latitude: ${position.lat.toFixed(6)}<br>Longitude: ${position.lng.toFixed(6)}`);
                thisVM.marcador.openPopup();
            });
        },

        confirmarLocalizacao() {
            var thisVM = this;
            if (!thisVM.coordenadasSelecionadas) return;

            if (thisVM.modoMapaParaEdicao) {
                // Se estiver editando, atualiza o form
                thisVM.form.localizacao.latitude = thisVM.coordenadasSelecionadas.lat.toFixed(6);
                thisVM.form.localizacao.longitude = thisVM.coordenadasSelecionadas.lng.toFixed(6);
                thisVM.modoMapaParaEdicao = false; // Reseta o flag
            } else {
                // Se estiver criando, atualiza o novoPosto
                thisVM.novoPosto.latitude = thisVM.coordenadasSelecionadas.lat.toFixed(6);
                thisVM.novoPosto.longitude = thisVM.coordenadasSelecionadas.lng.toFixed(6);
            }

            thisVM.isMapModalActive = false;
        },

        getPostos() {
            var thisVM = this;
            thisVM.$store.commit("startLoading");
            thisVM.postosSalvos = [];

            firebase.database()
                .ref(thisVM.$route.params.time + "/postosTrabalho")
                .once("value") //modificar para .on
                .then(snapshot => {
                    snapshot.forEach(child => {
                        if (child.key !== "_count") {
                            thisVM.postosSalvos.push({
                                id: child.key,
                                ...child.val()
                            });
                        }
                    });
                    thisVM.$store.commit("stopLoading");
                    thisVM.inicializarMapaPostos(); // Recarrega o mapa com os novos dados
                });
        },

        // Método salvarPosto() modificado com verificação de duplicação
        async salvarPosto() {
            var thisVM = this;

            // Verificar campos obrigatórios
            if (!thisVM.novoPosto.nome || !thisVM.novoPosto.latitude || !thisVM.novoPosto.longitude) {
                thisVM.$buefy.toast.open({
                    message: 'Preencha todos os campos obrigatórios',
                    type: 'is-warning'
                });
                return;
            }

            if (!thisVM.novoPosto.latitude || !thisVM.novoPosto.longitude) {
                thisVM.$buefy.toast.open({
                    message: 'Erro ao salvar o posto: Latitude e longitude são obrigatórios',
                    type: 'is-danger'
                });
                return; // Interrompe a operação de salvar
            }

            try {
                // Verificar se já existe um posto com este nome
                const nomeDuplicado = await thisVM.verificarNomeDuplicado(thisVM.novoPosto.nome, thisVM.editandoId);
                if (nomeDuplicado) {
                    thisVM.$buefy.toast.open({
                        message: 'Já existe um posto com este nome. Por favor, escolha outro nome.',
                        type: 'is-danger',
                        duration: 5000
                    });
                    return;
                }

                const postoData = {
                    nome: thisVM.novoPosto.nome,
                    localizacao: {
                        latitude: thisVM.novoPosto.latitude,
                        longitude: thisVM.novoPosto.longitude
                    },
                    responsavel: thisVM.novoPosto.responsavel,
                };

                const postosRef = firebase.database().ref(thisVM.$route.params.time + "/postosTrabalho");

                if (thisVM.editandoId) {
                    await postosRef.child(thisVM.editandoId).update(postoData);
                } else {
                    const newPostoRef = postosRef.push();
                    await newPostoRef.set(postoData);
                }

                // Feedback e recarregar dados
                thisVM.$buefy.toast.open({
                    message: 'Posto salvo com sucesso!',
                    type: 'is-success'
                });
                thisVM.resetarFormulario();
                thisVM.getPostos();
            } catch (error) {
                thisVM.$buefy.toast.open({
                    message: 'Erro ao salvar o posto: ' + error.message,
                    type: 'is-danger'
                });
            }
        },

        // Método para gerar QR Code
        gerarQRCode(posto) {
            var thisVM = this;
            if (!posto || !posto.id) {
                thisVM.$buefy.toast.open({
                    message: 'Posto inválido para gerar QR Code',
                    type: 'is-warning'
                });
                return;
            }

            const url = `${window.location.origin}/#/${thisVM.$route.params.time}/ControlePonto/${posto.id}`;

            QRCode.toDataURL(url, { width: 200 }, (err, qrUrl) => {
                if (!err) {
                    thisVM.qrCodeData = qrUrl;
                }
            });
        },

        // Método para ver detalhes do posto
        verDetalhesPosto(posto) {
            var thisVM = this;
            if (!posto || !posto.id) {
                thisVM.$buefy.toast.open({
                    message: 'Posto inválido selecionado',
                    type: 'is-danger'
                });
                return;
            }

            thisVM.postoSelecionado = posto;
            thisVM.buscarColaboradoresDoPosto(posto.nome);
            thisVM.gerarQRCode(posto);
            thisVM.isModalActive = true;
        },

        // Método para buscar colaboradores do posto
        buscarColaboradoresDoPosto(nomePosto) {
            var thisVM = this;
            thisVM.$store.commit("startLoading");
            thisVM.colaboradoresDoPosto = [];

            firebase
                .database()
                .ref(thisVM.$route.params.time + "/Colaboradores")
                .orderByChild("postoTrabalho")
                .equalTo(nomePosto)
                .once("value", (snapshot) => {
                    snapshot.forEach((childSnapshot) => {
                        var childData = childSnapshot.val();
                        childData.id = childSnapshot.key;
                        thisVM.colaboradoresDoPosto.push(childData);
                    });
                    thisVM.$store.commit("stopLoading");
                });
        },

        // Método para gerar PDF do QR Code
        gerarPDFQRCode() {
            var thisVM = this;
            if (!thisVM.postoSelecionado || !thisVM.postoSelecionado.id || !thisVM.qrCodeData) {
                thisVM.$buefy.toast.open({
                    message: 'Selecione um posto e gere o QR Code primeiro',
                    type: 'is-warning'
                });
                return;
            }

            const doc = new jsPDF();
            const idPuro = thisVM.postoSelecionado.id;
            const urlPura = `${window.location.origin}/#/${thisVM.$route.params.time}/ControlePonto/${idPuro}`;

            // Configuração do PDF
            doc.setFontSize(16);
            doc.text('QR Code do Posto', 105, 20, { align: 'center' });

            // Informações básicas
            doc.text(`ID do Posto: ${idPuro}`, 20, 40);
            doc.text(`Nome: ${thisVM.postoSelecionado.nome}`, 20, 50);

            // QR Code
            const imgWidth = 80;
            const imgHeight = 80;
            const x = (doc.internal.pageSize.width - imgWidth) / 2;
            doc.addImage(thisVM.qrCodeData, 'PNG', x, 60, imgWidth, imgHeight);

            // URL embaixo
            doc.text(`URL: ${urlPura}`, 20, 150);

            doc.save(`QRCode_Posto_${thisVM.postoSelecionado.nome}.pdf`);
        },

        // Método adicional para selecionar posto
        selecionarPosto(posto) {
            var thisVM = this;
            thisVM.postoSelecionado = posto;
        }
    },

    mounted() {
        var thisVM = this;
        thisVM.getPostos();

    }
}
</script>
