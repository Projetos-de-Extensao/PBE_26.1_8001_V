const API_BASE = 'http://127.0.0.1:8000/api';

// --- Estado Global ---
let accessToken = localStorage.getItem('access_token') || null;
let currentRole = localStorage.getItem('current_role') || null;

// --- Roteamento e UI ---
function showView(viewId) {
    document.querySelectorAll('.view').forEach(el => el.classList.remove('active'));
    document.getElementById(viewId).classList.add('active');
}

function showSection(sectionId) {
    document.querySelectorAll('.content-section').forEach(el => el.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');
}

function showCoordSection(sectionId) {
    showSection(sectionId);
    if(sectionId === 'coord-listagem') {
        carregarSolicitacoesCoord();
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    if (accessToken && currentRole) {
        rotearParaDashboard(currentRole);
    } else {
        showView('view-login');
    }

    // Handlers
    document.getElementById('form-login').addEventListener('submit', handleLogin);
    document.getElementById('form-nova-solicitacao').addEventListener('submit', handleNovaSolicitacao);
    document.getElementById('form-avaliacao-coord').addEventListener('submit', handleAvaliacaoCoord);
    document.getElementById('form-enviar-documento').addEventListener('submit', handleEnviarDocumento);
    document.getElementById('form-encaminhar-coord').addEventListener('submit', handleEncaminharCoord);
});

// --- Login e Autenticação ---
async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_BASE}/token/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            const data = await response.json();
            accessToken = data.access;
            localStorage.setItem('access_token', accessToken);
            
            // Inferir papel (role) baseado no username para o playground
            if (username.startsWith('aluno')) currentRole = 'aluno';
            else if (username.startsWith('coord')) currentRole = 'coordenador';
            else if (username.startsWith('empresa')) currentRole = 'empresa';
            else currentRole = 'aluno'; // fallback
            
            localStorage.setItem('current_role', currentRole);
            rotearParaDashboard(currentRole);
        } else {
            alert('Falha no login. Verifique as credenciais.');
        }
    } catch (error) {
        console.error(error);
        alert('Erro ao conectar com a API.');
    }
}

function logout() {
    accessToken = null;
    currentRole = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('current_role');
    showView('view-login');
}

function rotearParaDashboard(role) {
    if (role === 'aluno') {
        showView('view-aluno');
        showSection('aluno-minhas-solicitacoes');
        carregarSolicitacoesAluno();
    } else if (role === 'coordenador') {
        showView('view-coordenador');
        showCoordSection('coord-listagem');
    } else if (role === 'empresa') {
        showView('view-empresa');
        carregarSolicitacoesEmpresa();
    }
}

// --- Funções Auxiliares de API ---
async function apiFetch(endpoint, options = {}) {
    if (!options.headers) options.headers = {};
    if (accessToken && !options.headers['Authorization']) {
        options.headers['Authorization'] = `Bearer ${accessToken}`;
    }
    const res = await fetch(`${API_BASE}${endpoint}`, options);
    if (res.status === 401) {
        logout();
        throw new Error('Não autorizado');
    }
    return res;
}

// --- Funções do Aluno ---
async function carregarSolicitacoesAluno() {
    try {
        const res = await apiFetch('/solicitacoes/');
        const data = await res.json();
        
        const tbody = document.getElementById('tbody-solicitacoes-aluno');
        tbody.innerHTML = '';
        
        const lista = data.results || data;
        lista.forEach(sol => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>#${sol.id}</td>
                <td>${sol.curso} - ${sol.campus}</td>
                <td><strong>${sol.status}</strong></td>
                <td>
                    <button class="btn-primary" style="padding: 0.2rem 0.5rem; width:auto;" onclick="abrirEnvioDocumento(${sol.id})">Anexar Doc</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
        if (lista.length === 0) tbody.innerHTML = '<tr><td colspan="4">Nenhuma solicitação criada.</td></tr>';
    } catch (e) {
        console.error(e);
    }
}

async function handleNovaSolicitacao(e) {
    e.preventDefault();
    const curso = document.getElementById('curso').value;
    const campus = document.getElementById('campus').value;
    
    try {
        // Obter ID do aluno
        const alunoRes = await apiFetch('/alunos/');
        const alunos = await alunoRes.json();
        const lista = alunos.results || alunos;
        let alunoId = lista.length > 0 ? lista[0].id : 1; 

        const payload = {
            aluno: alunoId,
            curso: curso,
            campus: campus,
            status: "CRIADA"
        };

        const res = await apiFetch('/solicitacoes/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            alert('Solicitação iniciada com sucesso! Agora anexe os documentos necessários.');
            document.getElementById('form-nova-solicitacao').reset();
            showSection('aluno-minhas-solicitacoes');
            carregarSolicitacoesAluno();
        } else {
            alert('Erro ao criar solicitação.');
        }
    } catch(e) {
        console.error(e);
    }
}

function abrirEnvioDocumento(solicitacaoId) {
    document.getElementById('doc-solicitacao-id').value = solicitacaoId;
    document.getElementById('doc-solicitacao-id-display').innerText = solicitacaoId;
    document.getElementById('form-enviar-documento').reset();
    showSection('aluno-enviar-documentos');
}

async function handleEnviarDocumento(e) {
    e.preventDefault();
    const solicitacaoId = document.getElementById('doc-solicitacao-id').value;
    const nome = document.getElementById('doc-nome').value;
    const tipo = document.getElementById('doc-tipo').value;
    const fileInput = document.getElementById('doc-arquivo');
    
    if(fileInput.files.length === 0) {
        alert("Selecione um arquivo PDF.");
        return;
    }

    const formData = new FormData();
    formData.append('solicitacao', solicitacaoId);
    formData.append('nome', nome);
    formData.append('tipo', tipo);
    formData.append('arquivo', fileInput.files[0]);

    try {
        const headers = { 'Authorization': `Bearer ${accessToken}` };
        // Não definir Content-Type ao enviar FormData, o navegador define boundary automático
        const res = await fetch(`${API_BASE}/documentos/`, {
            method: 'POST',
            headers: headers,
            body: formData
        });

        if (res.ok) {
            alert('Documento enviado com sucesso!');
            showSection('aluno-minhas-solicitacoes');
        } else {
            alert('Erro ao enviar o documento.');
            const error = await res.json();
            console.error(error);
        }
    } catch(e) {
        console.error(e);
    }
}

async function carregarModelos() {
    try {
        const res = await apiFetch('/modelos-documento/');
        const data = await res.json();
        
        const tbody = document.getElementById('tbody-modelos');
        tbody.innerHTML = '';
        
        const lista = data.results || data;
        lista.forEach(mod => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${mod.nome}</strong></td>
                <td>${mod.descricao}</td>
                <td>${mod.obrigatorio ? 'Sim' : 'Não'}</td>
            `;
            tbody.appendChild(tr);
        });
        if (lista.length === 0) tbody.innerHTML = '<tr><td colspan="3">Nenhum modelo cadastrado.</td></tr>';
    } catch (e) {
        console.error(e);
    }
}

async function carregarNotificacoes() {
    try {
        const res = await apiFetch('/notificacoes/');
        const data = await res.json();
        
        const tbody = document.getElementById('tbody-notificacoes');
        tbody.innerHTML = '';
        
        const lista = data.results || data;
        lista.forEach(not => {
            const tr = document.createElement('tr');
            const dataData = new Date(not.data_criacao).toLocaleString();
            tr.innerHTML = `
                <td>${dataData}</td>
                <td>${not.mensagem}</td>
                <td>Req #${not.solicitacao}</td>
            `;
            tbody.appendChild(tr);
        });
        if (lista.length === 0) tbody.innerHTML = '<tr><td colspan="3">Nenhuma notificação recebida.</td></tr>';
    } catch (e) {
        console.error(e);
    }
}

// --- Funções do Coordenador ---
async function carregarSolicitacoesCoord() {
    try {
        const res = await apiFetch('/solicitacoes/');
        const data = await res.json();
        
        const tbody = document.getElementById('tbody-solicitacoes-coord');
        tbody.innerHTML = '';
        
        const lista = data.results || data;
        lista.forEach(sol => {
            const tr = document.createElement('tr');
            const alunoNome = sol.aluno_detalhe ? sol.aluno_detalhe.nome : 'Aluno ID ' + sol.aluno;
            const qtdeDocs = sol.documentos ? sol.documentos.length : 0;
            
            tr.innerHTML = `
                <td>#${sol.id}</td>
                <td>${alunoNome}</td>
                <td>${qtdeDocs} arquivo(s) anexado(s)</td>
                <td><strong>${sol.status}</strong></td>
                <td>
                    <button class="btn-secondary" style="padding:0.2rem 0.5rem" onclick="abrirAvaliacao(${sol.id}, '${alunoNome}')">Avaliar</button>
                    <button class="btn-primary" style="padding:0.2rem 0.5rem" onclick="abrirEncaminhamento(${sol.id})">Encaminhar</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error(e);
    }
}

function abrirAvaliacao(id, alunoNome) {
    document.getElementById('eval-id').innerText = id;
    document.getElementById('eval-aluno-nome').innerText = alunoNome;
    document.getElementById('eval-solicitacao-id').value = id;
    document.getElementById('form-avaliacao-coord').reset();
    showSection('coord-avaliacao');
}

async function handleAvaliacaoCoord(e) {
    e.preventDefault();
    const id = document.getElementById('eval-solicitacao-id').value;
    const form = new FormData(e.target);
    const conceito = form.get('conceito');
    const observacoes = form.get('observacoes');

    let endpoint = '';
    if (conceito === 'APROVADA') endpoint = `/solicitacoes/${id}/aprovar/`;
    else if (conceito === 'REPROVADA') endpoint = `/solicitacoes/${id}/reprovar/`;
    else endpoint = `/solicitacoes/${id}/solicitar-correcao/`;

    try {
        const res = await apiFetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ observacoes })
        });
        
        if (res.ok) {
            alert('Avaliação registrada com sucesso!');
            showCoordSection('coord-listagem');
        } else {
            alert('Erro ao registrar avaliação.');
        }
    } catch (e) {
        console.error(e);
    }
}

async function abrirEncaminhamento(id) {
    document.getElementById('enc-id').innerText = id;
    document.getElementById('enc-solicitacao-id').value = id;
    document.getElementById('form-encaminhar-coord').reset();
    
    try {
        const res = await apiFetch('/empresas/');
        const data = await res.json();
        const select = document.getElementById('enc-empresa');
        select.innerHTML = '<option value="">Selecione a Empresa...</option>';
        const lista = data.results || data;
        lista.forEach(emp => {
            select.innerHTML += `<option value="${emp.id}">${emp.razao_social}</option>`;
        });
    } catch (e) {
        console.error('Erro ao carregar empresas:', e);
    }

    showCoordSection('coord-encaminhar');
}

async function handleEncaminharCoord(e) {
    e.preventDefault();
    const solicitacaoId = document.getElementById('enc-solicitacao-id').value;
    const empresaId = document.getElementById('enc-empresa').value;
    const observacoes = document.getElementById('enc-observacoes').value;

    try {
        const coordRes = await apiFetch('/coordenadores/');
        const coords = await coordRes.json();
        const lista = coords.results || coords;
        let coordId = lista.length > 0 ? lista[0].id : 1;

        const payload = {
            solicitacao: solicitacaoId,
            organizacao: empresaId,
            coordenador: coordId,
            observacoes: observacoes
        };

        const res = await apiFetch('/encaminhamentos/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            alert('Solicitação encaminhada para a empresa com sucesso!');
            showCoordSection('coord-listagem');
        } else {
            alert('Erro ao encaminhar solicitação.');
            const error = await res.json();
            console.error(error);
        }
    } catch (e) {
        console.error(e);
    }
}

// --- Funções da Empresa ---
async function carregarSolicitacoesEmpresa() {
    try {
        // Usa o endpoint de encaminhamentos para a empresa
        const res = await apiFetch('/encaminhamentos/');
        const data = await res.json();
        
        const tbody = document.getElementById('tbody-solicitacoes-empresa');
        tbody.innerHTML = '';
        
        const lista = data.results || data;
        let propostasRespondidas = JSON.parse(localStorage.getItem('propostasRespondidas')) || {};

        lista.forEach(enc => {
            const tr = document.createElement('tr');
            let acoesHtml = '';
            
            if (propostasRespondidas[enc.id] === 'APROVADA') {
                acoesHtml = '<span style="color: #10b981; font-weight: bold;">✔️ Proposta Aceita</span>';
            } else if (propostasRespondidas[enc.id] === 'RECUSADA') {
                acoesHtml = '<span style="color: #ef4444; font-weight: bold;">❌ Proposta Recusada</span>';
            } else {
                acoesHtml = `
                    <button class="btn-primary" style="padding: 0.2rem 0.5rem; width:auto;" onclick="responderEmpresa(${enc.id}, 'aceitar')">Aceitar</button>
                    <button class="btn-secondary" style="padding: 0.2rem 0.5rem; width:auto;" onclick="responderEmpresa(${enc.id}, 'recusar')">Recusar</button>
                `;
            }

            tr.innerHTML = `
                <td>Aluno Vinculado (ID Req #${enc.solicitacao})</td>
                <td>Tecnologia</td>
                <td>${acoesHtml}</td>
            `;
            tbody.appendChild(tr);
        });
        
        if (lista.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3">Nenhuma proposta pendente no momento.</td></tr>';
        }
    } catch (e) {
        console.error(e);
    }
}

async function responderEmpresa(encId, acao) {
    if (!confirm(`Deseja realmente ${acao} esta proposta?`)) return;
    
    try {
        const res = await apiFetch(`/encaminhamentos/${encId}/${acao}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ observacoes: "Ação realizada via portal web." })
        });
        
        if (res.ok) {
            alert(`Proposta ${acao === 'aceitar' ? 'aceita' : 'recusada'} com sucesso!`);
            let propostasRespondidas = JSON.parse(localStorage.getItem('propostasRespondidas')) || {};
            propostasRespondidas[encId] = acao === 'aceitar' ? 'APROVADA' : 'RECUSADA';
            localStorage.setItem('propostasRespondidas', JSON.stringify(propostasRespondidas));
            carregarSolicitacoesEmpresa();
        } else {
            alert('Erro ao processar ação.');
        }
    } catch (e) {
        console.error(e);
    }
}
