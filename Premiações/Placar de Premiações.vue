<template>
    <layout-default>
        <div class="container">
            <div class="section">
                <h1 class="title is-2 has-text-centered">
                    <i class="fas fa-trophy"></i> Sistema de Premiação
                </h1>

                <!-- Seletor de Pasta de Operação -->
                <div class="field">
                    <label class="label">Selecione a Ficha de Prontuário:</label>
                    <div class="select is-fullwidth">
                        <select v-model="selectedFicha" @change="carregarDadosProducao">
                            <option v-for="ficha in fichas" :value="ficha" :key="ficha.id">
                                {{ ficha.nome }}
                            </option>
                        </select>
                    </div>
                </div>

                <!-- Controles -->
                <div class="columns">
                    <div class="column">
                        <div class="field">
                            <label class="label">Período de Apuração</label>
                            <div class="control">
                                <input class="input" type="text" v-model="periodoApuracao" placeholder="Ex: Julho 2024">
                            </div>
                        </div>
                    </div>
                    <div class="column">
                        <div class="field">
                            <label class="label">Meta Total do Período</label>
                            <div class="control">
                                <input class="input" type="number" v-model="metaTotal" placeholder="Ex: 18000">
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Botões de Ação -->
                <div class="buttons is-centered">
                    <button class="button is-primary is-large" @click="abrirModalPremios">
                        <i class="fas fa-cog"></i> Configurar Premiação
                        <i class="fas fa-external-link-alt" style="margin-left: 5px; font-size: 0.8em;"></i>
                    </button>
                    <button class="button is-success is-large" @click="simularDados">
                        <i class="fas fa-random"></i> Simular Dados
                    </button>
                    <button class="button is-info is-large" @click="atualizarRanking">
                        <i class="fas fa-sync"></i> Atualizar Ranking
                    </button>
                </div>
                <!-- Novos controles para visualização em tabela -->
                <div class="field is-grouped is-grouped-multiline" v-if="selectedFicha">
                    <div class="control">
                        <label class="checkbox">
                            <input type="checkbox" v-model="exibirComoTabela"> Exibir como Tabela
                        </label>
                    </div>
                    <div class="control" v-if="exibirComoTabela">
                        <label class="checkbox">
                            <input type="checkbox" v-model="inverterEixos"> Inverter Linhas/Colunas
                        </label>
                    </div>
                </div>

                <!-- Visualização em Tabela -->
                <div class="table-container" v-if="exibirComoTabela && selectedFicha">
                    <h2 class="title is-4">
                        <i class="fas fa-table"></i> Visualização Tabular
                    </h2>
                    <div class="table-wrapper">
                        <table class="table is-bordered is-striped is-fullwidth">
                            <thead>
                                <tr>
                                    <th v-if="!inverterEixos">Colaborador</th>
                                    <th v-else>Produto</th>
                                    <th v-for="item in cabecalhoTabela" :key="item">
                                        {{ item }}
                                    </th>
                                    <th>Total</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(linha, index) in dadosTabela" :key="index">
                                    <td><strong>{{ linha.nome }}</strong></td>
                                    <td v-for="(valor, idx) in linha.valores" :key="idx">
                                        {{ valor.toLocaleString('pt-BR') }} kg
                                    </td>
                                    <td><strong>{{ linha.total.toLocaleString('pt-BR') }} kg</strong></td>
                                </tr>
                            </tbody>
                            <tfoot v-if="!inverterEixos">
                                <tr>
                                    <td><strong>Total por Produto</strong></td>
                                    <td v-for="(total, idx) in totaisPorProduto" :key="idx">
                                        <strong>{{ total.toLocaleString('pt-BR') }} kg</strong>
                                    </td>
                                    <td><strong>{{ totalAcumulado.toLocaleString('pt-BR') }} kg</strong></td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                </div>
                <!-- Placar Dinâmico -->
                <div class="placar-dinamico" v-if="selectedFicha">
                    <h2 class="title is-3 has-text-white">
                        <i class="fas fa-chart-line"></i> Placar Dinâmico - {{ periodoApuracao }}
                    </h2>
                    <div class="columns">
                        <div class="column">
                            <div class="has-text-centered">
                                <p class="title is-4 has-text-white">Total Acumulado</p>
                                <p class="title is-2 has-text-warning">{{ totalAcumulado.toLocaleString('pt-BR') }} kg
                                </p>
                            </div>
                        </div>
                        <div class="column">
                            <div class="has-text-centered">
                                <p class="title is-4 has-text-white">Meta do Período</p>
                                <p class="title is-2 has-text-info">{{ metaTotal.toLocaleString('pt-BR') }} kg</p>
                            </div>
                        </div>
                        <div class="column">
                            <div class="has-text-centered">
                                <p class="title is-4 has-text-white">Progresso</p>
                                <div class="progress-container">
                                    <div class="progress-bar" :style="{ width: progressoPercentual + '%' }"></div>
                                </div>
                                <p class="title is-3 has-text-white">{{ progressoPercentual }}%</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Tabela de Premiação -->
                <div class="tabela-premiacao" v-if="selectedFicha">
                    <h3 class="title is-4 has-text-white">
                        <i class="fas fa-medal"></i> Tabela de Premiação
                    </h3>
                    <div class="columns is-multiline">
                        <div class="column is-4" v-for="(premio, index) in configuracaoPremios" :key="index">
                            <div class="premio-item">
                                <div class="has-text-centered">
                                    <p class="title is-5 has-text-white">{{ premio.posicao }}º Lugar</p>
                                    <p class="title is-3 has-text-warning">R$ {{ premio.valor.toLocaleString('pt-BR') }}
                                    </p>
                                    <p class="subtitle is-6 has-text-white">{{ premio.descricao }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Ranking de Colaboradores -->
                <div class="ranking-container" v-if="selectedFicha">
                    <h2 class="title is-3">
                        <i class="fas fa-users"></i> Ranking de Produção - {{ selectedFicha.nome }}
                    </h2>

                    <div class="columns is-multiline">
                        <div class="column is-12" v-for="(colaborador, index) in rankingColaboradores"
                            :key="colaborador.id">
                            <div class="ranking-card" :class="getClassePosicao(index + 1)">
                                <div class="columns is-vcentered">
                                    <div class="column is-narrow">
                                        <div class="has-text-centered">
                                            <span class="title is-1">{{ index + 1 }}º</span>
                                            <div>
                                                <i class="fas fa-medal" v-if="index < 3"></i>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="column">
                                        <div class="content">
                                            <p class="title is-4">{{ colaborador.nome }}</p>
                                            <p class="subtitle is-5">
                                                <strong>{{ colaborador.volumeTotalProducao.toLocaleString('pt-BR') }}
                                                    kg</strong>
                                            </p>
                                            <div class="tags">
                                                <span class="produto-tag"
                                                    v-for="(produto, pIndex) in colaborador.Produtos"
                                                    :key="getProdutoKey(produto, pIndex)">
                                                    {{ produto.nome }}: {{ produto.volume.toLocaleString('pt-BR') }}kg
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="column is-narrow">
                                        <div class="has-text-centered">
                                            <p class="title is-4 premio-valor"
                                                v-if="index < configuracaoPremios.length">
                                                R$ {{ configuracaoPremios[index].valor.toLocaleString('pt-BR') }}
                                            </p>
                                            <p class="subtitle is-6" v-if="index < configuracaoPremios.length">
                                                {{ configuracaoPremios[index].descricao }}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Modal de Configuração de Prêmios -->
            <div class="modal" :class="{ 'is-active': modalPremiosAtivo }">
                <div class="modal-background" @click="modalPremiosAtivo = false"></div>
                <div class="modal-card">
                    <header class="modal-card-head">
                        <p class="modal-card-title">
                            <i class="fas fa-cog"></i> Configurar Premiação
                        </p>
                        <button class="delete" @click="modalPremiosAtivo = false"></button>
                    </header>
                    <section class="modal-card-body">
                        <div class="field">
                            <label class="label">Número de Posições Premiadas</label>
                            <div class="control">
                                <input class="input" type="number" v-model="numeroPosicoesPremios" min="1" max="10">
                            </div>
                        </div>

                        <div class="field" v-for="(premio, index) in configuracaoPremios" :key="index">
                            <label class="label">{{ index + 1 }}º Lugar</label>
                            <div class="columns">
                                <div class="column">
                                    <div class="control">
                                        <input class="input" type="number" v-model="premio.valor"
                                            placeholder="Valor do prêmio">
                                    </div>
                                </div>
                                <div class="column">
                                    <div class="control">
                                        <input class="input" type="text" v-model="premio.descricao"
                                            placeholder="Descrição do prêmio">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>
                    <footer class="modal-card-foot">
                        <button class="button is-success" @click="salvarConfiguracaoPremios">
                            <i class="fas fa-save"></i> Salvar Configuração
                        </button>
                        <button class="button" @click="modalPremiosAtivo = false">Cancelar</button>
                    </footer>
                </div>
            </div>
        </div>
    </layout-default>
</template>

<script>
import firebase from "firebase"; 
import fichasService from '@/services/fichas.service'; // Importando o service
import holeritesService from '@/services/holerites.service';

export default {
    name: "TabelaPremiacaoRanking",
    data() {
        return {
            exibirComoTabela: false,
            inverterEixos: false,
            recalculoInterval: null,
            intervaloAtualizacaoRecalculo: 600000,
            periodoApuracao: 'Julho 2024',
            metaTotal: 18000,
            modalPremiosAtivo: false,
            numeroPosicoesPremios: 5,
            configuracaoPremios: [
                { posicao: 1, valor: 500, descricao: 'Primeiro Lugar + Smartphone' },
                { posicao: 2, valor: 300, descricao: 'Segundo Lugar' },
                { posicao: 3, valor: 200, descricao: 'Terceiro Lugar' },
                { posicao: 4, valor: 150, descricao: 'Quarto Lugar' },
                { posicao: 5, valor: 100, descricao: 'Quinto Lugar' }
            ],
            fichas: [],
            fichasListener: null, // Para armazenar a função de desconexão
            selectedFicha: null,
            dadosProducao: {},
            rankingColaboradores: [],
            rankingListener: null, // Listener para o ranking de produção
        };
    },
    computed: {
        dadosTabela() {
            if (!this.selectedFicha || !this.rankingColaboradores.length) return [];

            if (!this.inverterEixos) {
                return this.rankingColaboradores.map(colab => {
                    const valores = this.produtosUnicos.map(produto => {
                        const produtoColab = colab.Produtos != null ? colab.Produtos.find(p => p.nome === produto) : null;
                        return produtoColab ? produtoColab.volume : 0;
                    });

                    return {
                        nome: colab.nome,
                        valores: valores,
                        total: colab.volumeTotalProducao
                    };
                });
            } else {
                return this.produtosUnicos.map(produto => {
                    const valores = this.rankingColaboradores.map(colab => {
                        const produtoColab = colab.Produtos != null ? colab.Produtos.find(p => p.nome === produto) : null;
                        return produtoColab ? produtoColab.volume : 0;
                    });

                    const total = valores.reduce((sum, val) => sum + val, 0);

                    return {
                        nome: produto,
                        valores: valores,
                        total: total
                    };
                });
            }
        },
        cabecalhoTabela() {
            if (!this.inverterEixos) {
                return this.produtosUnicos;
            } else {
                return this.rankingColaboradores.map(c => c.nome);
            }
        },
        produtosUnicos() {
            if (!this.rankingColaboradores.length) return [];

            const produtos = new Set();
            this.rankingColaboradores.forEach(colab => {
                if (colab.Produtos != null) {
                    colab.Produtos.forEach(prod => {
                        produtos.add(prod.nome);
                    });
                }
            });

            return Array.from(produtos).sort();
        },
        totaisPorProduto() {
            if (this.inverterEixos) return [];

            return this.produtosUnicos.map(produto => {
                return this.rankingColaboradores.reduce((total, colab) => {
                    const prod = colab.Produtos != null ? colab.Produtos.find(p => p.nome === produto) : null;
                    return total + (prod ? prod.volume : 0);
                }, 0);
            });
        },
        totalAcumulado() {
            return this.rankingColaboradores.reduce((total, colaborador) => {
                return total + colaborador.volumeTotalProducao;
            }, 0);
        },
        progressoPercentual() {
            return Math.min(Math.round((this.totalAcumulado / this.metaTotal) * 100), 100);
        }
    },
    methods: {
        getProdutoKey(produto, index) {
            return `${produto.nome}-${index}-${Date.now()}`;
        },
        showNotification(message, type = 'is-success') {
            this.$buefy.toast.open({
                message,
                type,
                position: 'is-top'
            });
        },
        abrirModalPremios() {
            this.$router.push(`/${this.$route.params.time}/TabelaPremiacao/ConfigurarPremiacao`);
        },
        async salvarConfiguracaoPremios() {
            while (this.configuracaoPremios.length < this.numeroPosicoesPremios) {
                const novoIndex = this.configuracaoPremios.length;
                this.configuracaoPremios.push({
                    posicao: novoIndex + 1,
                    valor: 50,
                    descricao: `${novoIndex + 1}º Lugar`
                });
            }

            if (this.configuracaoPremios.length > this.numeroPosicoesPremios) {
                this.configuracaoPremios = this.configuracaoPremios.slice(0, this.numeroPosicoesPremios);
            }

            try {
                await firebase.database()
                    .ref(`${this.$route.params.time}/ConfiguracaoPremios`)
                    .set({
                        periodo: this.periodoApuracao,
                        metaTotal: this.metaTotal,
                        premios: this.configuracaoPremios
                    });

                this.modalPremiosAtivo = false;
                this.showNotification('Configuração salva com sucesso!');
            } catch (error) {
                this.showNotification('Erro ao salvar configuração', 'is-danger');
            }
        },
        getClassePosicao(posicao) {
            switch (posicao) {
                case 1: return 'primeiro-lugar';
                case 2: return 'segundo-lugar';
                case 3: return 'terceiro-lugar';
                default: return '';
            }
        },
        async simularDados() {
            if (!this.selectedFicha) {
                this.showNotification('Selecione uma ficha primeiro!', 'is-danger');
                return;
            }

            const nomes = ['João Silva', 'Maria Santos', 'Carlos Oliveira', 'Ana Costa', 'Pedro Alves', 'Lucia Lima', 'Roberto Cruz', 'Silvia Rocha'];
            const materiais = ['Papelão', 'Papel Misto', 'Vidro', 'Plástico', 'Alumínio', 'Ferro', 'PVC/Mang', 'Aparas'];

            const novoRanking = {};
            novoRanking[this.selectedFicha.id] = {};

            for (let i = 0; i < 6; i++) {
                const colaboradorId = 'colab_' + Math.random().toString(36).substr(2, 9);

                const produtos = [];
                const numProdutos = Math.floor(Math.random() * 4) + 1;
                let volumeTotal = 0;

                for (let j = 0; j < numProdutos; j++) {
                    const volume = Math.floor(Math.random() * 2000) + 500;
                    volumeTotal += volume;
                    produtos.push({
                        nome: materiais[Math.floor(Math.random() * materiais.length)],
                        volume: volume
                    });
                }

                novoRanking[this.selectedFicha.id][colaboradorId] = {
                    nome: nomes[Math.floor(Math.random() * nomes.length)],
                    volumeTotalProducao: volumeTotal,
                    Produtos: produtos
                };
            }

            try {
                await firebase.database()
                    .ref(`${this.$route.params.time}/Analytics/RankingProducao/${this.selectedFicha.id}`)
                    .set(novoRanking[this.selectedFicha.id]);

                this.showNotification('Dados simulados salvos com sucesso!');
                this.carregarDadosProducao();
            } catch (error) {
                this.showNotification('Erro ao salvar dados simulados', 'is-danger');
            }
        },
        async atualizarRanking() {
            await this.carregarDadosProducao();
            this.showNotification('Ranking atualizado com sucesso!');
        },
        async carregarDadosProducao() {
            if (!this.selectedFicha) return;

            try {
                const snapshot = await firebase.database()
                    .ref(`${this.$route.params.time}/Analytics/RankingProducao/${this.selectedFicha.id}`)
                    .once('value');

                this.dadosProducao = snapshot.exists() ? snapshot.val() : {};
                this.processarDadosRanking();
            } catch (error) {
                this.showNotification('Erro ao carregar dados de produção', 'is-danger');
            }
        },
        processarDadosRanking() {
            this.rankingColaboradores = [];

            for (const colaboradorId in this.dadosProducao) {
                const colaborador = this.dadosProducao[colaboradorId];
                this.rankingColaboradores.push({
                    id: colaboradorId,
                    ...colaborador
                });
            }

            this.rankingColaboradores.sort((a, b) => b.volumeTotalProducao - a.volumeTotalProducao);
        },
        getFichas() {
            const thisVM = this;
            thisVM.$store.commit("startLoading");

            // Desconecta listener anterior se existir
            if (this.fichasListener) {
                this.fichasListener();
            }

            // Usa o service para buscar as fichas
            this.fichasListener = fichasService.getFichas(
                this.$route.params.time,
                (fichas) => {
                    // MODIFICAÇÃO: Filtrar apenas fichas ativas
                    thisVM.fichas = fichas.filter(ficha => ficha.ativa);

                    if (thisVM.fichas.length > 0) {
                        thisVM.selectedFicha = thisVM.fichas[0];
                        thisVM.carregarDadosProducao();
                    }
                    thisVM.$store.commit("stopLoading");
                },
                (error) => {
                    thisVM.showNotification('Erro ao carregar fichas: ' + error, 'is-danger');
                    thisVM.$store.commit("stopLoading");
                }
            );
        },
        async carregarConfiguracao() {
            try {
                const snapshot = await firebase.database()
                    .ref(`${this.$route.params.time}/ConfiguracaoPremios`)
                    .once('value');

                if (snapshot.exists()) {
                    const config = snapshot.val();
                    this.periodoApuracao = config.periodo || this.periodoApuracao;
                    this.metaTotal = config.metaTotal || this.metaTotal;
                    this.configuracaoPremios = config.premios || this.configuracaoPremios;
                    this.numeroPosicoesPremios = this.configuracaoPremios.length;
                }
            } catch (error) {
                this.showNotification('Erro ao carregar configuração', 'is-danger');
            }
        },
        async recalcularValoresProducao() {
            try {
                await holeritesService.recalcularValoresProducao(this.$route.params.time, this.selectedFicha.id);
                this.showNotification('Valores de produção recalculados com sucesso!');
            } catch (error) {
                this.showNotification('Erro ao recalcular valores de produção', 'is-danger');
            }
        },
        startRecalculo() {
            this.recalculoInterval = setInterval(() => {
                this.recalcularValoresProducao();
            }, this.intervaloAtualizacaoRecalculo);
        },
        stopRecalculo() {
            if (this.recalculoInterval) {
                clearInterval(this.recalculoInterval);
                this.recalculoInterval = null;
            }
        },
        // Método para lidar com mudanças no tipo de listener
        handleListenerChange() {
            if (this.fichasListener) {
                this.fichasListener();
            }
            this.getFichas();
        }
    },
    mounted() {
        // Adiciona listener para mudanças no service
        window.addEventListener('fichas-service-listener-changed', this.handleListenerChange);
        this.startRecalculo();
    },
    watch: {
        numeroPosicoesPremios(novoValor) {
            while (this.configuracaoPremios.length < novoValor) {
                const novoIndex = this.configuracaoPremios.length;
                this.configuracaoPremios.push({
                    posicao: novoIndex + 1,
                    valor: 50,
                    descricao: `${novoIndex + 1}º Lugar`
                });
            }

            if (this.configuracaoPremios.length > novoValor) {
                this.configuracaoPremios = this.configuracaoPremios.slice(0, novoValor);
            }
        }
    },
    async created() {
        await this.carregarConfiguracao();
        this.getFichas();

        // Configura listener para ranking de produção
        this.rankingListener = firebase.database()
            .ref(`${this.$route.params.time}/Analytics/RankingProducao`)
            .on('value', (snapshot) => {
                if (this.selectedFicha && snapshot.exists() && snapshot.hasChild(this.selectedFicha.id)) {
                    this.dadosProducao = snapshot.child(this.selectedFicha.id).val() || {};
                    this.processarDadosRanking();
                }
            });
    },
    beforeDestroy() {
        // Remove listeners
        window.removeEventListener('fichas-service-listener-changed', this.handleListenerChange);
        this.stopRecalculo();

        if (this.fichasListener) {
            this.fichasListener();
        }

        if (this.rankingListener) {
            firebase.database().ref(`${this.$route.params.time}/Analytics/RankingProducao`).off('value', this.rankingListener);
        }
    }
};
</script>

<style scoped>
.ranking-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
}

.primeiro-lugar {
    background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
    color: #333;
    border: 3px solid #FFD700;
    box-shadow: 0 8px 32px rgba(255, 215, 0, 0.3);
}

.segundo-lugar {
    background: linear-gradient(135deg, #C0C0C0 0%, #A8A8A8 100%);
    color: #333;
    border: 3px solid #C0C0C0;
    box-shadow: 0 8px 32px rgba(192, 192, 192, 0.3);
}

.terceiro-lugar {
    background: linear-gradient(135deg, #CD7F32 0%, #B8860B 100%);
    color: white;
    border: 3px solid #CD7F32;
    box-shadow: 0 8px 32px rgba(205, 127, 50, 0.3);
}

.premio-valor {
    font-size: 1.5em;
    font-weight: bold;
    color: #00d1b2;
}

.placar-dinamico {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.02);
    }

    100% {
        transform: scale(1);
    }
}

.produto-tag {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 5px 10px;
    margin: 2px;
    display: inline-block;
}

.progress-bar {
    background: linear-gradient(90deg, #00d1b2, #48c774);
    height: 20px;
    border-radius: 10px;
    transition: width 0.3s ease;
}

.tabela-premiacao {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
}

.premio-item {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 10px;
    margin: 5px 0;
    border-left: 4px solid #FFD700;
}

.progress-container {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    height: 20px;
    margin: 10px 0;
    overflow: hidden;
}

.table-container {
    margin: 2rem 0;
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.table-wrapper {
    overflow-x: auto;
}

.table {
    min-width: 100%;
}

.table th {
    background-color: #f5f5f5;
    font-weight: bold;
}

.table tbody tr:hover {
    background-color: #f9f9f9;
}

.table tfoot td {
    background-color: #f0f0f0;
    font-weight: bold;
}

/* Responsividade */
@media screen and (max-width: 768px) {
    .table-container {
        padding: 0.5rem;
    }

    .table th,
    .table td {
        padding: 0.5em 0.75em;
    }
}
</style>