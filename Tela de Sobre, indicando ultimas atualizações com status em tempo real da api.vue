<template>
  <layout-default>
    <div class="box">
      <h1 class="title is-3">🌱 Sobre o Sistema</h1>
      <div class="content">
        <p>O <strong>RBManager</strong> é uma plataforma moderna e intuitiva desenvolvida para otimizar a
          gestão de processos de reciclagem. Nosso sistema oferece ferramentas completas para o controle operacional,
          administrativo e financeiro, contribuindo para um mundo mais sustentável através da tecnologia.</p>

        <p>Construído com tecnologias de ponta, o sistema oferece uma experiência fluida e eficiente para todos os
          usuários, desde operadores até gestores, facilitando o dia a dia das operações de reciclagem.</p>
      </div>
    </div>

    <div class="box">
      <h2 class="title is-4">📊 Principais Funcionalidades</h2>
      <div class="columns is-multiline">
        <div class="column is-half">
          <div class="card">
            <div class="card-content">
              <div class="media">
                <div class="media-left">
                  <span class="icon is-large has-text-info">
                    <i class="fas fa-users fa-2x"></i>
                  </span>
                </div>
                <div class="media-content">
                  <p class="title is-5">Gestão de Colaboradores</p>
                  <p class="subtitle is-6">Controle completo de funcionários, cargos e departamentos com interface
                    intuitiva</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="column is-half">
          <div class="card">
            <div class="card-content">
              <div class="media">
                <div class="media-left">
                  <span class="icon is-large has-text-success">
                    <i class="fas fa-money-bill-wave fa-2x"></i>
                  </span>
                </div>
                <div class="media-content">
                  <p class="title is-5">Sistema de Holerites</p>
                  <p class="subtitle is-6">Geração automática e envio de holerites diretamente pelo sistema</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="column is-half">
          <div class="card">
            <div class="card-content">
              <div class="media">
                <div class="media-left">
                  <span class="icon is-large has-text-warning">
                    <i class="fas fa-shield-alt fa-2x"></i>
                  </span>
                </div>
                <div class="media-content">
                  <p class="title is-5">Autenticação Segura</p>
                  <p class="subtitle is-6">Sistema robusto de login e controle de acesso com tokens JWT</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="column is-half">
          <div class="card">
            <div class="card-content">
              <div class="media">
                <div class="media-left">
                  <span class="icon is-large has-text-primary">
                    <i class="fas fa-mobile-alt fa-2x"></i>
                  </span>
                </div>
                <div class="media-content">
                  <p class="title is-5">Interface Responsiva</p>
                  <p class="subtitle is-6">Acesso completo via web em qualquer dispositivo</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="box">
      <h2 class="title is-4">⚡ Status dos Serviços</h2>
      <div class="field is-grouped">
        <div class="control">
          <div class="tags has-addons">
            <span class="tag is-medium">API Status</span>
            <span class="tag is-medium" :class="apiStatusClass">
              {{ apiStatusText }}
            </span>
          </div>
        </div>
        <div class="control">
          <b-button type="is-info" @click="checkApiStatus()" :loading="isCheckingApi" icon-left="refresh">
            Atualizar Status
          </b-button>
        </div>
      </div>

      <div class="notification is-light">
        <strong>Endpoints da API:</strong><br>
        {{ apiUrl }}<br>
        <small class="has-text-grey">
          Ambiente: {{ currentEnvironment }}
        </small>
      </div>
    </div>

    <div class="box">
      <h2 class="title is-4">📋 Histórico de Versões</h2>
      <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
        <thead>
          <tr>
            <td>Versão</td>
            <td>Descrição</td>
            <td>Data</td>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <span class="tag is-primary">v0.6.8</span>
            </td>
            <td>
              <ul>
                <li>
                  <strong>Ajustes no novo holerite. Campos com valor padrão</strong><br>
                  <span class="has-text-grey">
                    Agora é possível definir um valor padrão para os campos editáveis do holerite, facilitando o
                    preenchimento e garantindo consistência nos dados.
                  </span>
                </li>
              </ul>
            </td>
            <td>
              <span class="tag is-success">01/10/2025</span>
            </td>
          </tr>
          <tr data-v-0b7905dc="">
            <td data-v-0b7905dc="">
              <span data-v-0b7905dc="" class="tag is-primary">v0.6.7</span>
            </td>
            <td data-v-0b7905dc="">
              <ul data-v-0b7905dc="">
                <li data-v-0b7905dc="">
                  <strong data-v-0b7905dc="">Novo placar de produção</strong><br data-v-0b7905dc="">
                  <span data-v-0b7905dc="" class="has-text-grey">
                    Tela de monitoramento em tempo real da produção diária, desenvolvida para exibição em placares e
                    dashboards operacionais.
                    A tela permite acompanhamento visual imediato dos indicadores de produtividade da equipe.
                  </span>
                </li>
              </ul>
            </td>
            <td data-v-0b7905dc="">
              <span data-v-0b7905dc="" class="tag is-success">26/09/2025</span>
            </td>
          </tr>
          <tr>
            <td data-v-0b7905dc="">
              <span data-v-0b7905dc="" class="tag is-primary">v0.6.6</span>
            </td>
            <td data-v-0b7905dc="">
              <ul data-v-0b7905dc="">
                <li data-v-0b7905dc="">
                  <strong data-v-0b7905dc="">Nova tela de Holerites</strong><br data-v-0b7905dc="">
                  <span data-v-0b7905dc="" class="has-text-grey">
                    Nova tela com tabela geradora de holerites, dessa vez tendo a possibilidade do usuario editar e
                    personalizar os campos da tabela de acordo
                    com a necessidade encontrada.
                  </span>
                </li>
                <li data-v-0b7905dc="">
                  <strong data-v-0b7905dc="">Cadastro de Campos na Tabela de Holerite</strong><br data-v-0b7905dc="">
                  <span data-v-0b7905dc="" class="has-text-grey">
                    Tela de cadastro de campos usados na tabela geradora de holerites, nessa tela se é possivel detalhar
                    com especificações
                    cada detalhe da coluna, dês de sua descrição, ordem na tabela, até um montador de formulas para o
                    calculo atribuido ao tipo
                    de informação que estará presente naquele determinado campo.
                  </span>
                </li>
                <li data-v-0b7905dc="">
                  <strong data-v-0b7905dc="">Cadastro de Lembretes</strong><br data-v-0b7905dc="">
                  <span data-v-0b7905dc="" class="has-text-grey">
                    Sendo agora possivel acessar a nova tela de cadastro de lembretes, onde o usuario é capaz de
                    programar notificações especificas
                    definindo aonde deseja receber esta determinada notificação, e o conteúdo da mensagem.
                  </span>
                </li>
              </ul>
            </td>
            <td data-v-0b7905dc="">
              <span data-v-0b7905dc="" class="tag is-success">19/09/2025</span>
            </td>

          </tr>
          <tr data-v-0b7905dc="">
            <td data-v-0b7905dc="">
              <span data-v-0b7905dc="" class="tag is-primary">v0.6.5</span>
            </td>
            <td data-v-0b7905dc="">
              <ul data-v-0b7905dc="">
                <li data-v-0b7905dc="">
                  <strong data-v-0b7905dc="">Lista de Contas</strong><br data-v-0b7905dc="">
                  <span data-v-0b7905dc="" class="has-text-grey">
                    Versão baseada na nova tela de extrato de separações, nessa versão vista pela tela de "🕑Produção".
                    Onde a tabela é vista como primeira informação UI e agora com carregamento automatico
                  </span>
                </li>
              </ul>
            </td>
            <td data-v-0b7905dc="">
              <span data-v-0b7905dc="" class="tag is-success">09/09/2025</span>
            </td>
          </tr>
          <tr data-v-0b7905dc="">
            <td data-v-0b7905dc="">
              <span data-v-0b7905dc="" class="tag is-primary">v0.6.4</span>
            </td>
            <td data-v-0b7905dc="">
              <ul data-v-0b7905dc="">
                <li data-v-0b7905dc="">
                  <strong data-v-0b7905dc="">Lista de Contas</strong><br data-v-0b7905dc="">
                  <span data-v-0b7905dc="" class="has-text-grey">
                    Nesta versão foi implementada a tela de Lista de Contas, que permite visualizar de forma organizada
                    todas as contas a pagar e a receber. A tela traz filtros por tipo e status, resumo com indicadores
                    (total, pendentes, vencidas e pagas) e uma tabela detalhada com informações como ID, tipo, fato
                    gerador, valor, parcelas, status e data de criação.
                    Também foi adicionada a possibilidade de navegar para os detalhes da conta diretamente pela
                    listagem.
                  </span>
                </li>
              </ul>
            </td>
            <td data-v-0b7905dc="">
              <span data-v-0b7905dc="" class="tag is-success">09/09/2025</span>
            </td>
          </tr>
          <tr data-v-0b7905dc="">
            <td data-v-0b7905dc="">
              <span data-v-0b7905dc="" class="tag is-primary">v0.6.3</span>
            </td>
            <td data-v-0b7905dc="">
              <ul data-v-0b7905dc="">
                <li data-v-0b7905dc="">
                  <strong data-v-0b7905dc="">Resolução de Bugs</strong><br data-v-0b7905dc="">
                  <span data-v-0b7905dc="" class="has-text-grey">
                    Bugs onde comprovantes de endereço não conseguiam ser cadastrados corrigido, Bugs de visibilidade e
                    permissões corrigido.
                  </span>
                </li>
              </ul>
            </td>
            <td data-v-0b7905dc="">
              <span data-v-0b7905dc="" class="tag is-success">07/08/2025</span>
            </td>
          </tr>
          <tr data-v-0b7905dc="">
            <td data-v-0b7905dc="">
              <span data-v-0b7905dc="" class="tag is-primary">v0.6.2</span>
            </td>
            <td data-v-0b7905dc="">
              <ul data-v-0b7905dc="">
                <li data-v-0b7905dc="">
                  <strong data-v-0b7905dc="">Premiação – Ranking de produção</strong><br data-v-0b7905dc="">
                  <span data-v-0b7905dc="" class="has-text-grey">
                    Implementa a funcionalidade de ranking de produção, permitindo visualizar a posição de cada
                    colaborador e incentivando o alcance de metas mensais.
                  </span>
                </li>
                <li data-v-0b7905dc="">
                  <strong data-v-0b7905dc="">Separação simplificada</strong><br data-v-0b7905dc="">
                  <span data-v-0b7905dc="" class="has-text-grey">
                    Nova tela de separação que permite lançar entradas automaticamente, economizando tempo e reduzindo
                    erros operacionais.
                  </span>
                </li>
                <li data-v-0b7905dc="">
                  <strong data-v-0b7905dc="">Melhoria na tela de separação</strong><br data-v-0b7905dc="">
                  <span data-v-0b7905dc="" class="has-text-grey">
                    Correções visuais para evitar que o botão de estorno apareça fora do momento adequado.
                  </span>
                </li>
                <li data-v-0b7905dc="">
                  <strong data-v-0b7905dc="">Notificações no sistema</strong><br data-v-0b7905dc="">
                  <span data-v-0b7905dc="" class="has-text-grey">
                    Implementada área de notificações visível no menu, com separação entre lidas e não lidas.
                  </span>
                </li>
                <li data-v-0b7905dc="">
                  <strong data-v-0b7905dc="">Melhoria no cadastro de colaboradores</strong><br data-v-0b7905dc="">
                  <span data-v-0b7905dc="" class="has-text-grey">
                    Ajuste no campo de data de nascimento para seguir o padrão de outros campos e melhorias nas
                    mensagens exibidas ao usuário.
                  </span>
                </li>
                <li data-v-0b7905dc="">
                  <strong data-v-0b7905dc="">Centralização do método getFichas</strong><br data-v-0b7905dc="">
                  <span data-v-0b7905dc="" class="has-text-grey">
                    Código de carregamento de fichas unificado para evitar duplicações e garantir carregamento completo
                    das propriedades.
                  </span>
                </li>
                <li data-v-0b7905dc="">
                  <strong data-v-0b7905dc="">Novo menu para visualização de contas</strong><br data-v-0b7905dc="">
                  <span data-v-0b7905dc="" class="has-text-grey">
                    Implementada visualização de contas a pagar e a receber diretamente pelo sistema.
                  </span>
                </li>
              </ul>
            </td>
            <td data-v-0b7905dc="">
              <span data-v-0b7905dc="" class="tag is-success">28/07/2025</span>
            </td>
          </tr>

          <tr>
            <td>
              <span class="tag is-primary">v0.6</span>
            </td>
            <td>
              <ul>

                <li> <strong>Sistema de atualização de aplicativo automático</strong><br>
                  <span class="has-text-grey">Sistema tenta se atualizar automaticamente quando percebe que tem uma nova
                    versão disponível</span>
                </li>
                <li> <strong>🐞 Bugs no cadastro de colaborador corrigidos</strong><br>
                  <span class="has-text-grey">Nem todos os campos dos colaboradores estavam sendo atualizados num
                    cadastro ou edição</span>
                </li>

              </ul>

            </td>
            <td>
              <span class="tag is-success">14/07/2025</span>
            </td>
          </tr>
          <tr>
            <td>
              <span class="tag is-primary">v0.5.2</span>
            </td>
            <td>
              <ul>

                <li> <strong>Permissão de Separação</strong><br>
                  <span class="has-text-grey">Implementa a nova funcionalidade de permissão de separação de itens,
                    garantindo que apenas usuários autorizados possam realizar essa ação.</span>
                </li>
                <li> <strong>Visualização de INSS na tela de prontuário</strong><br>
                  <span class="has-text-grey">Implementa a nova funcionalidade de visualização de INSS na tela de
                    prontuário.</span>
                </li>
                <li> <strong>Página Sobre</strong><br>
                  <span class="has-text-grey">
                    Nova funcionalidade de visualização de informações na página Sobre, contendo as principais mudanças
                    feitas naquela versão e indicando se a API do RecibrasManager está no ar.
                  </span>
                </li>
                <li> <strong>Compra no Ato</strong><br>
                  <span class="has-text-grey">
                    Funcionalidade de compra no ato, permitindo que os usuários anexem comprovantes diretamente no
                    cadastro da compra.
                  </span>
                </li>
                <li> <strong>Ferramenta de recorte de comprovante de movimentações</strong><br>
                  <span class="has-text-grey">
                    Funcionalidade de recorte de comprovante de movimentações, permitindo que os usuários recortem e
                    anexem comprovantes diretamente no cadastro da movimentação.
                  </span>
                </li>
                <li> <strong>Bug no logoff corrigido</strong><br>
                  <span class="has-text-grey">
                    Quando o logoff estava sendo feito, o sistema dava uma mensagem de erro e parava de funcionar.
                  </span>
                </li>
                <li> <strong>Bug no cálculo do holerite quando não havia separações ou pessoas no
                    prontuário</strong><br>
                  <span class="has-text-grey">
                    Quando o cálculo do holerite era realizado sem separações ou pessoas no prontuário, o sistema
                    apresentava um erro.
                  </span>
                </li>
                <li> <strong>Melhoria na tela de entrada e despesas nas versões mobile </strong><br>
                  <span class="has-text-grey">
                    Novas implementações de melhorias na tela de entrada e despesas, tornando-as mais responsivas e
                    amigáveis para dispositivos móveis.
                  </span>
                </li>
                <li> <strong>Lista de itens separados no detalhe da entrada</strong><br>
                  <span class="has-text-grey">
                    Implementa a visualização dos itens separados no detalhe da entrada, permitindo uma melhor
                    organização e visualização das informações.
                  </span>
                </li>
              </ul>

            </td>
            <td>
              <span class="tag is-success">12/07/2025</span>
            </td>
          </tr>
          <tr>
            <td>
              <span class="tag is-primary">v0.5.1</span>
            </td>
            <td>
              <strong>Bugs na assinatura</strong><br>
              <span class="has-text-grey">A versão anterior havia introduzido um bug que impedia todos os navegadores a
                assinar o holerite. Problema corrigido, mas pode fazer com que a tela volte a "sambar" em alguns
                navegadores. Corrigiremos isso em versões futuras.</span>
            </td>
            <td>
              <span class="tag is-success">05/07/2025</span>
            </td>
          </tr>
          <tr>
            <td>
              <span class="tag is-primary">v0.5.0</span>
            </td>
            <td>
              <strong>Recolhimento INSS</strong><br>
              <span class="has-text-grey">Implementação completa do sistema de gestão de documentos INSS, incluindo
                funcionalidades para recolhimento automático, validação de contribuições e controle documental
                integrado.</span>
            </td>
            <td>
              <span class="tag is-success">22/06/2025</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </layout-default>
</template>

<script>
export default {
  name: "sobre",
  data() {
    return {
      isProduction: process.env.NODE_ENV === "production",
      apiStatus: 'checking',
      isCheckingApi: false,
      apiStatusInterval: null, // Intervalo para verificação do status da API

      apiUrl: process.env.VUE_APP_API_LINK || 'URL não encontrada'
    };
  },
  computed: {
    apiStatusClass() {
      switch (this.apiStatus) {
        case 'online':
          return 'is-success';
        case 'offline':
          return 'is-danger';
        case 'checking':
        default:
          return 'is-warning';
      }
    },
    apiStatusText() {
      switch (this.apiStatus) {
        case 'online':
          return '🟢 Online';
        case 'offline':
          return '🔴 Offline';
        case 'checking':
        default:
          return '🔄 Verificando...';
      }
    },
    currentEnvironment() {
      return process.env.NODE_ENV === 'production' ? 'Produção' : 'Desenvolvimento';
    }
  },
  methods: {
    async checkApiStatus() {
      const thisVM = this;
      thisVM.isCheckingApi = true;
      thisVM.apiStatus = 'checking';

      try {
        // ✅ MODIFICADO - Continua usando o $apiService normalmente
        const response = await thisVM.$apiService.get('/');

        if (response.status === 200) {
          thisVM.apiStatus = 'online';
        } else {
          throw new Error(`Status: ${response.status}`);
        }
      } catch (error) {
        thisVM.apiStatus = 'offline';
      } finally {
        thisVM.isCheckingApi = false;
      }
    },
    startApiMonitoring() {
      // Verificar status a cada 30 segundos
      this.apiStatusInterval = setInterval(() => {
        this.checkApiStatus();
      }, 30000);
    },
    stopApiMonitoring() {
      if (this.apiStatusInterval) {
        clearInterval(this.apiStatusInterval);
        this.apiStatusInterval = null;
      }
    }
  },
  mounted() {
    this.checkApiStatus();
    this.startApiMonitoring();
  },
  beforeDestroy() {
    this.stopApiMonitoring();
  }
};
</script>

<style scoped>
.card {
  height: 100%;
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
}

.tags.has-addons .tag:not(:last-child) {
  margin-right: 0;
}
</style>
