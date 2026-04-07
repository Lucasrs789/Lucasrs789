<template>
    <layout-default>
        <div class="container">
            <div class="section">
                <div class="level">
                    <div class="level-left">
                        <div class="level-item">
                            <h1 class="title is-2">
                                <i class="fas fa-cog"></i> Configurar Premiação
                            </h1>
                        </div>
                    </div>
                    <div class="level-right">
                        <div class="level-item">
                            <button class="button is-light" @click="voltarPagina">
                                <i class="fas fa-arrow-left"></i> Voltar
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Configurações Gerais -->
                <div class="card">
                    <header class="card-header">
                        <p class="card-header-title">
                            <i class="fas fa-settings"></i>&nbsp; Configurações Gerais
                        </p>
                    </header>
                    <div class="card-content">
                        <div class="columns">
                            <div class="column">
                                <div class="field">
                                    <label class="label">Período de Apuração</label>
                                    <div class="control">
                                        <input class="input" type="text" v-model="periodoApuracao" 
                                               placeholder="Ex: Julho 2024">
                                    </div>
                                </div>
                            </div>
                            <div class="column">
                                <div class="field">
                                    <label class="label">Meta Total do Período (kg)</label>
                                    <div class="control">
                                        <input class="input" type="number" v-model="metaTotal" 
                                               placeholder="Ex: 18000">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Configuração de Premiação -->
                <div class="card">
                    <header class="card-header">
                        <p class="card-header-title">
                            <i class="fas fa-trophy"></i>&nbsp; Configuração de Prêmios
                        </p>
                    </header>
                    <div class="card-content">
                        <div class="field">
                            <label class="label">Número de Posições Premiadas</label>
                            <div class="control">
                                <input class="input is-large" type="number" v-model="numeroPosicoesPremios" 
                                       min="1" max="10" style="max-width: 200px;">
                            </div>
                            <p class="help">Defina quantas posições receberão prêmios (máximo 10)</p>
                        </div>

                        <hr>

                        <div class="premio-configuracao" v-for="(premio, index) in configuracaoPremios" :key="index">
                            <div class="card premio-card" :class="getClassePremio(index + 1)">
                                <div class="card-content">
                                    <div class="columns is-vcentered">
                                        <div class="column is-narrow">
                                            <div class="has-text-centered">
                                                <span class="title is-2 posicao-numero">{{ index + 1 }}º</span>
                                                <div>
                                                    <i class="fas fa-medal medal-icon" v-if="index < 3"></i>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="column">
                                            <div class="field">
                                                <label class="label">Valor do Prêmio (R$)</label>
                                                <div class="control has-icons-left">
                                                    <input class="input is-large" type="number" v-model="premio.valor"
                                                           placeholder="Ex: 500">
                                                    <span class="icon is-small is-left">
                                                        <i class="fas fa-dollar-sign"></i>
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="column">
                                            <div class="field">
                                                <label class="label">Descrição do Prêmio</label>
                                                <div class="control has-icons-left">
                                                    <input class="input is-large" type="text" v-model="premio.descricao"
                                                           placeholder="Ex: Primeiro Lugar + Smartphone">
                                                    <span class="icon is-small is-left">
                                                        <i class="fas fa-tag"></i>
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Preview da Configuração -->
                <div class="card">
                    <header class="card-header">
                        <p class="card-header-title">
                            <i class="fas fa-eye"></i>&nbsp; Preview da Premiação
                        </p>
                    </header>
                    <div class="card-content">
                        <div class="preview-container">
                            <div class="columns is-multiline">
                                <div class="column is-4" v-for="(premio, index) in configuracaoPremios" :key="index">
                                    <div class="preview-item" :class="getClassePreview(index + 1)">
                                        <div class="has-text-centered">
                                            <p class="title is-4">{{ premio.posicao }}º Lugar</p>
                                            <p class="title is-2 valor-preview">
                                                R$ {{ premio.valor.toLocaleString('pt-BR') }}
                                            </p>
                                            <p class="subtitle is-6">{{ premio.descricao }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Botões de Ação -->
                <div class="buttons is-centered is-large">
                    <button class="button is-success is-large" @click="salvarConfiguracaoPremios" 
                            :class="{ 'is-loading': salvando }">
                        <i class="fas fa-save"></i>&nbsp; Salvar Configuração
                    </button>
                    <button class="button is-warning is-large" @click="resetarConfiguracoes">
                        <i class="fas fa-undo"></i>&nbsp; Resetar
                    </button>
                    <button class="button is-light is-large" @click="voltarPagina">
                        <i class="fas fa-times"></i>&nbsp; Cancelar
                    </button>
                </div>
            </div>
        </div>
    </layout-default>
</template>

<script>
import firebase from "firebase";

export default {
    name: "ConfigurarPremiacao",
    data() {
        return {
            salvando: false,
            periodoApuracao: 'Julho 2024',
            metaTotal: 18000,
            numeroPosicoesPremios: 5,
            configuracaoPremios: [
                { posicao: 1, valor: 500, descricao: 'Primeiro Lugar + Smartphone' },
                { posicao: 2, valor: 300, descricao: 'Segundo Lugar' },
                { posicao: 3, valor: 200, descricao: 'Terceiro Lugar' },
                { posicao: 4, valor: 150, descricao: 'Quarto Lugar' },
                { posicao: 5, valor: 100, descricao: 'Quinto Lugar' }
            ],
            configuracaoOriginal: null
        };
    },
    methods: {
        showNotification(message, type = 'is-success') {
            this.$buefy.toast.open({
                message,
                type,
                position: 'is-top'
            });
        },

        getClassePremio(posicao) {
            switch (posicao) {
                case 1: return 'primeiro-lugar-config';
                case 2: return 'segundo-lugar-config';
                case 3: return 'terceiro-lugar-config';
                default: return 'outros-lugares-config';
            }
        },

        getClassePreview(posicao) {
            switch (posicao) {
                case 1: return 'preview-primeiro';
                case 2: return 'preview-segundo';
                case 3: return 'preview-terceiro';
                default: return 'preview-outros';
            }
        },

        async salvarConfiguracaoPremios() {
            this.salvando = true;
            
            try {
                // Validações
                if (!this.periodoApuracao.trim()) {
                    throw new Error('Período de apuração é obrigatório');
                }
                
                if (!this.metaTotal || this.metaTotal <= 0) {
                    throw new Error('Meta total deve ser maior que zero');
                }

                // Validar prêmios
                for (let i = 0; i < this.configuracaoPremios.length; i++) {
                    const premio = this.configuracaoPremios[i];
                    if (!premio.valor || premio.valor <= 0) {
                        throw new Error(`Valor do ${i + 1}º lugar deve ser maior que zero`);
                    }
                    if (!premio.descricao.trim()) {
                        throw new Error(`Descrição do ${i + 1}º lugar é obrigatória`);
                    }
                }

                await firebase.database()
                    .ref(`${this.$route.params.time}/ConfiguracaoPremios`)
                    .set({
                        periodo: this.periodoApuracao,
                        metaTotal: this.metaTotal,
                        premios: this.configuracaoPremios,
                        dataUltimaAtualizacao: firebase.database.ServerValue.TIMESTAMP
                    });

                this.showNotification('Configuração salva com sucesso!');
                
                // Voltar para a página anterior após salvar
                setTimeout(() => {
                    this.voltarPagina();
                }, 1500);

            } catch (error) {
                this.showNotification(error.message || 'Erro ao salvar configuração', 'is-danger');
            } finally {
                this.salvando = false;
            }
        },

        resetarConfiguracoes() {
            this.$buefy.dialog.confirm({
                title: 'Resetar Configurações',
                message: 'Tem certeza que deseja resetar todas as configurações para os valores padrão?',
                confirmText: 'Sim, Resetar',
                cancelText: 'Cancelar',
                type: 'is-warning',
                onConfirm: () => {
                    this.periodoApuracao = 'Julho 2024';
                    this.metaTotal = 18000;
                    this.numeroPosicoesPremios = 5;
                    this.configuracaoPremios = [
                        { posicao: 1, valor: 500, descricao: 'Primeiro Lugar + Smartphone' },
                        { posicao: 2, valor: 300, descricao: 'Segundo Lugar' },
                        { posicao: 3, valor: 200, descricao: 'Terceiro Lugar' },
                        { posicao: 4, valor: 150, descricao: 'Quarto Lugar' },
                        { posicao: 5, valor: 100, descricao: 'Quinto Lugar' }
                    ];
                    this.showNotification('Configurações resetadas!', 'is-info');
                }
            });
        },

        voltarPagina() {
            // Verificar se houve mudanças
            const configAtual = {
                periodo: this.periodoApuracao,
                metaTotal: this.metaTotal,
                premios: JSON.stringify(this.configuracaoPremios)
            };

            const configOriginal = this.configuracaoOriginal ? {
                periodo: this.configuracaoOriginal.periodo,
                metaTotal: this.configuracaoOriginal.metaTotal,
                premios: JSON.stringify(this.configuracaoOriginal.premios)
            } : null;

            const houveAlteracoes = !configOriginal || 
                JSON.stringify(configAtual) !== JSON.stringify(configOriginal);

            if (houveAlteracoes) {
                this.$buefy.dialog.confirm({
                    title: 'Alterações não salvas',
                    message: 'Você tem alterações não salvas. Deseja sair mesmo assim?',
                    confirmText: 'Sim, Sair',
                    cancelText: 'Cancelar',
                    type: 'is-warning',
                    onConfirm: () => {
                        this.$router.go(-1);
                    }
                });
            } else {
                this.$router.go(-1);
            }
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
                    
                    // Salvar configuração original para comparação
                    this.configuracaoOriginal = {
                        periodo: this.periodoApuracao,
                        metaTotal: this.metaTotal,
                        premios: JSON.parse(JSON.stringify(this.configuracaoPremios))
                    };
                }
            } catch (error) {
                this.showNotification('Erro ao carregar configuração', 'is-danger');
            }
        }
    },
    watch: {
        numeroPosicoesPremios(novoValor) {
            // Adicionar novos prêmios se necessário
            while (this.configuracaoPremios.length < novoValor) {
                const novoIndex = this.configuracaoPremios.length;
                this.configuracaoPremios.push({
                    posicao: novoIndex + 1,
                    valor: 50,
                    descricao: `${novoIndex + 1}º Lugar`
                });
            }

            // Remover prêmios se necessário
            if (this.configuracaoPremios.length > novoValor) {
                this.configuracaoPremios = this.configuracaoPremios.slice(0, novoValor);
            }

            // Atualizar posições
            this.configuracaoPremios.forEach((premio, index) => {
                premio.posicao = index + 1;
            });
        }
    },
    async created() {
        await this.carregarConfiguracao();
    }
};
</script>

<style scoped>
.premio-configuracao {
    margin-bottom: 20px;
}

.premio-card {
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.primeiro-lugar-config {
    background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
    border-left: 5px solid #FFD700;
}

.segundo-lugar-config {
    background: linear-gradient(135deg, #C0C0C0 0%, #A8A8A8 100%);
    border-left: 5px solid #C0C0C0;
}

.terceiro-lugar-config {
    background: linear-gradient(135deg, #CD7F32 0%, #B8860B 100%);
    border-left: 5px solid #CD7F32;
}

.outros-lugares-config {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-left: 5px solid #667eea;
    color: white;
}

.posicao-numero {
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.medal-icon {
    font-size: 2rem;
    color: #FFD700;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.preview-container {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    border-radius: 10px;
    padding: 20px;
    color: white;
}

.preview-item {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 15px;
    margin: 5px 0;
    backdrop-filter: blur(10px);
}

.preview-primeiro {
    border-left: 4px solid #FFD700;
}

.preview-segundo {
    border-left: 4px solid #C0C0C0;
}

.preview-terceiro {
    border-left: 4px solid #CD7F32;
}

.preview-outros {
    border-left: 4px solid #667eea;
}

.valor-preview {
    color: #FFD700;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.card {
    margin-bottom: 2rem;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.card-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.field {
    margin-bottom: 1.5rem;
}

.input.is-large {
    font-size: 1.2rem;
}

.buttons.is-large .button {
    min-width: 200px;
}
</style>