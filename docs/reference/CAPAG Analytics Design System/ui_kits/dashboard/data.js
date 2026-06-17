// CAPAG Analytics — sample balance-sheet data for the UI kit.
// Values in BRL. Codes follow a typical plano de contas público.
window.CAPAG_DATA = {
  exercicio: "2024",
  entidade: "Município de Exemplo",
  indicadores: [
    { label: "Indicador CAPAG", value: "B", tone: "success", hint: "Capacidade de pagamento boa" },
    { label: "Liquidez Corrente", value: "1,84", tone: "neutral", hint: "Meta ≥ 1,00" },
    { label: "Endividamento", value: "42,6%", tone: "warning", hint: "Dívida / RCL" },
    { label: "Poupança Corrente", value: "11,2%", tone: "primary", hint: "Resultado corrente positivo" },
  ],
  ativos: [
    {
      id: "ac",
      name: "Ativo Circulante",
      percent: "44%",
      total: "R$ 21.430.000,00",
      contas: [
        { id: "ac1", name: "Caixa e Equivalentes de Caixa", code: "1.1.1.01", value: "R$ 4.210.500,00", included: true },
        { id: "ac2", name: "Aplicações Financeiras", code: "1.1.1.02", value: "R$ 8.900.000,00", included: true },
        { id: "ac3", name: "Créditos a Receber", code: "1.1.2.01", value: "R$ 6.319.500,00", included: true },
        { id: "ac4", name: "Estoques", code: "1.1.4.01", value: "R$ 1.200.000,00", included: true },
        { id: "ac5", name: "VPD Pagas Antecipadamente", code: "1.1.9.01", value: "R$ 800.000,00", included: false },
      ],
    },
    {
      id: "anc",
      name: "Ativo Não Circulante",
      percent: "56%",
      total: "R$ 26.770.000,00",
      contas: [
        { id: "anc1", name: "Realizável a Longo Prazo", code: "1.2.1.01", value: "R$ 3.270.000,00", included: true },
        { id: "anc2", name: "Investimentos", code: "1.2.2.01", value: "R$ 2.500.000,00", included: true },
        { id: "anc3", name: "Imobilizado", code: "1.2.3.01", value: "R$ 19.500.000,00", included: true },
        { id: "anc4", name: "Intangível", code: "1.2.4.01", value: "R$ 1.500.000,00", included: true },
      ],
    },
  ],
  passivos: [
    {
      id: "pc",
      name: "Passivo Circulante",
      percent: "24%",
      total: "R$ 11.640.000,00",
      contas: [
        { id: "pc1", name: "Fornecedores e Contas a Pagar", code: "2.1.3.01", value: "R$ 5.140.000,00", included: true },
        { id: "pc2", name: "Obrigações Trabalhistas", code: "2.1.1.01", value: "R$ 3.500.000,00", included: true },
        { id: "pc3", name: "Empréstimos a Curto Prazo", code: "2.1.2.01", value: "R$ 3.000.000,00", included: true },
      ],
    },
    {
      id: "pnc",
      name: "Passivo Não Circulante",
      percent: "31%",
      total: "R$ 15.000.000,00",
      contas: [
        { id: "pnc1", name: "Empréstimos a Longo Prazo", code: "2.2.2.01", value: "R$ 12.000.000,00", included: true },
        { id: "pnc2", name: "Provisões a Longo Prazo", code: "2.2.7.01", value: "R$ 3.000.000,00", included: true },
      ],
    },
    {
      id: "pl",
      name: "Patrimônio Líquido",
      percent: "45%",
      total: "R$ 21.560.000,00",
      contas: [
        { id: "pl1", name: "Patrimônio Social e Capital Social", code: "2.3.1.01", value: "R$ 14.000.000,00", included: true },
        { id: "pl2", name: "Resultados Acumulados", code: "2.3.7.01", value: "R$ 7.560.000,00", included: true },
      ],
    },
  ],
  // Sample analytical ledger for the audit dialog
  lancamentos: [
    { data: "08/01/2024", hist: "Recebimento de tributos — IPTU", doc: "ARR-0412", deb: "—", cred: "1.204.000,00" },
    { data: "22/02/2024", hist: "Resgate de aplicação automática", doc: "APL-0098", deb: "—", cred: "980.000,00" },
    { data: "15/03/2024", hist: "Pagamento de fornecedor — obra praça", doc: "PG-3391", deb: "842.000,00", cred: "—" },
    { data: "30/04/2024", hist: "Transferência intragrupo conta única", doc: "TR-1180", deb: "350.000,00", cred: "—" },
    { data: "19/05/2024", hist: "Rendimento de aplicação financeira", doc: "REN-0571", deb: "—", cred: "120.400,00" },
    { data: "27/06/2024", hist: "Estorno de lançamento duplicado", doc: "EST-0042", deb: "—", cred: "84.200,00" },
  ],
};
