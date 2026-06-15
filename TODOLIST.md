# Todolist

- [x] PRD
- [ ] ARCHITETURE
- [ ] DESIGN
- [ ] AGENTS.md inicial
- [ ] SPECs
- [ ] TASKs
- [ ] AGENTS.md refinado
- [ ] Implementacao
- [ ] Testes
- [ ] Revisao
- [ ] Entrega
- [ ] Aprendizados


# Configurações em config.toml

# =========================================================
# VARIÁVEIS GLOBAIS (Obrigatório vir no topo do arquivo)
# =========================================================

# Modelo e Cognição
model = "gpt-5.5"
model_reasoning_effort = "medium"

# Autonomia Total sem Prompts
approval_policy = "never"
default_permissions = "user-edit"

# Sandbox e Rede Local Morta
# sandbox_mode = "workspace-write"
web_search = "disabled"

[permissions.user-edit.filesystem]
glob_scan_max_depth = 4
":minimal" = "read"
":tmpdir" = "write"
":slash_tmp" = "write"

[permissions.user-edit.filesystem.":workspace_roots"]
"." = "write"
".agents" = "write"
".git" = "read"
".codex" = "read"
"**/*.env" = "deny"

[permissions.user-edit.network]
enabled = true