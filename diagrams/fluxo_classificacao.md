# Diagrama de Fluxo - Classificador de Reclamações

## Fluxo Principal de Classificação

```mermaid
graph TD
    A["📥 ENTRADA<br/>Texto Reclamação"] -->|JSON| B["Lambda Handler<br/>lambda_handler event"]
    
    B -->|Extrai campo 'texto'| C{"Texto<br/>válido?"}
    
    C -->|Não| D["❌ Erro 400<br/>Campo 'texto' obrigatório"]
    C -->|Sim| E["✅ ClassificacaoRequest<br/>texto.strip()"]
    
    E -->|Passa para| F["ClassificacaoHandler<br/>use_cases.py"]
    
    F -->|1. Valida| G{"Request<br/>válida?"}
    G -->|Não| H["❌ ClassificacaoResponse<br/>tem_erros=True"]
    G -->|Sim| I["2. Chama ClassificadorReclamacoes<br/>classificar()"]
    
    I -->|Preprocessa texto| J["📝 Normalização<br/>acentos, pontuação, lowercase"]
    
    J -->|Processa com 3 estratégias| K["1️⃣ Match Exato<br/>peso 100"]
    K -->|Calcula scores| L["2️⃣ Palavra Completa<br/>peso 80"]
    L -->|Por categoria| M["3️⃣ Contains<br/>peso 50"]
    
    M -->|Combina pesos| N["📊 Calcula Score Final<br/>por categoria"]
    
    N -->|Normaliza para| O["📈 Normalização [0,1]<br/>com filtro >= 30%"]
    
    O -->|Ordena| P["🏆 Ordena por<br/>Confiança (descendente)"]
    
    P -->|Retorna| Q["ClassificacaoResultado<br/>categorias + tem_erros"]
    
    Q -->|Monta resposta| R["ClassificacaoResponse<br/>texto_original + categorias"]
    
    H -->|Erro| S["❌ HTTP 400<br/>JSON: erro + texto"]
    R -->|Sucesso| T["✅ HTTP 200<br/>JSON: texto + categorias + sucesso"]
    
    D --> U["📤 SAÍDA"]
    S --> U
    T --> U
    
    style A fill:#e1f5ff
    style B fill:#fff3e0
    style E fill:#f3e5f5
    style F fill:#e8f5e9
    style I fill:#fce4ec
    style J fill:#fff9c4
    style K fill:#f1f8e9
    style L fill:#f1f8e9
    style M fill:#f1f8e9
    style N fill:#f0f4c3
    style O fill:#fff59d
    style P fill:#ffd54f
    style Q fill:#ffcc80
    style U fill:#b3e5fc
    style D fill:#ffcdd2
    style S fill:#ffcdd2
    style T fill:#c8e6c9
```

## Detalhamento das 3 Estratégias de Matching

```mermaid
graph TD
    A["Texto Processado<br/>ex: 'problemas de acesso à conta'"] -->|Para cada categoria| B["Categoria<br/>ex: 'acesso'"]
    
    B -->|Palavras-chave| C["['acesso', 'bloqueio', 'senha',<br/>'login', 'autenticacao', ...]"]
    
    C -->|Estratégia 1| D["Match Exato<br/>\\bacessso\\b<br/>peso: 100"]
    C -->|Estratégia 2| E["Palavra Completa<br/>startswith 'acess'<br/>peso: 80"]
    C -->|Estratégia 3| F["Contains<br/>'acess' em qualquer lugar<br/>peso: 50"]
    
    D -->|Encontra: SIM| G["Score = 100 + 100 + 100<br/>(múltiplas ocorrências)"]
    E -->|Encontra: SIM| H["Score = 100 + 80"]
    F -->|Encontra: SIM| I["Score = 100 + 50"]
    
    G -->|Combina| J["Score Final<br/>= 300"]
    H -->|Combina| J
    I -->|Combina| J
    
    J -->|Normaliza| K["Confiança = 300 / max_score<br/>= 0.95 ou 95%"]
    
    K -->|Se >= 30%| L["✅ Incluir<br/>categoria"]
    K -->|Se < 30%| M["❌ Descartar<br/>categoria"]
    
    L -->|Resultado| N["CategoriaReclamacao<br/>nome: 'acesso'<br/>confianca: 0.95"]
    
    style A fill:#e3f2fd
    style B fill:#f3e5f5
    style C fill:#fff9c4
    style D fill:#c8e6c9
    style E fill:#c8e6c9
    style F fill:#c8e6c9
    style G fill:#fff59d
    style H fill:#fff59d
    style I fill:#fff59d
    style J fill:#ffcc80
    style K fill:#ffab91
    style L fill:#a5d6a7
    style M fill:#ef9a9a
    style N fill:#b3e5fc
```

## Arquitetura em Camadas

```mermaid
graph LR
    A["🌐 API Gateway<br/>AWS Lambda"] -->|event| B["lambda_handler.py<br/>ENTRY POINT"]
    
    B -->|ClassificacaoRequest| C["application/use_cases.py<br/>ClassificacaoHandler<br/>CAMADA APLICAÇÃO"]
    
    C -->|texto_processado| D["domain/services.py<br/>ClassificadorReclamacoes<br/>CAMADA DOMÍNIO"]
    
    D -->|preprocessar| E["domain/services.py<br/>Normalizador de Texto<br/>UTILITÁRIO"]
    
    E -->|texto_normalizado| D
    
    D -->|CategoriaReclamacao| C
    
    C -->|ClassificacaoResponse| B
    
    B -->|JSON| F["✅ Response HTTP<br/>statusCode + body"]
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style D fill:#fce4ec
    style E fill:#fff9c4
    style F fill:#b3e5fc
```

## Fluxo de Validação de Dados

```mermaid
graph TD
    A["Dados de Entrada"] -->|Body com 'texto'| B{"Body é<br/>string ou dict?"}
    
    B -->|String| C["json.loads()"]
    B -->|Dict| D["Usa direto"]
    
    C -->|Retorna dict| E["Extrai body.get texto"]
    D -->|Dict| E
    
    E -->|Valida| F{"Texto<br/>não vazio?"}
    
    F -->|Não| G["❌ Erro: Campo obrigatório"]
    F -->|Sim| H["Aplica .strip()"]
    
    H -->|ClassificacaoRequest| I{"Dentro do<br/>Handler valida"}
    
    I -->|request.validar()| J{"Comprimento<br/>adequado?"}
    
    J -->|Não| K["❌ Erro validação"]
    J -->|Sim| L["✅ Prossegue para<br/>classificação"]
    
    style A fill:#e3f2fd
    style G fill:#ffcdd2
    style K fill:#ffcdd2
    style L fill:#c8e6c9
    style H fill:#fff9c4
```

## Fluxo de Normalização de Texto

```mermaid
graph TD
    A["Texto Original<br/>ex: 'Tenho Acesso Bloqueado!'"] 
    
    A -->|1. Remove acentos| B["'Tenho Acesso Bloqueado!'<br/>unicodedata.normalize()"]
    
    B -->|2. Lowercase| C["'tenho acesso bloqueado!'"]
    
    C -->|3. Remove pontuação| D["'tenho acesso bloqueado'"]
    
    D -->|4. Remove extra spaces| E["'tenho acesso bloqueado'<br/>re.sub()"]
    
    E -->|5. Tokeniza| F["['tenho', 'acesso', 'bloqueado']"]
    
    F -->|Resultado final| G["Texto Processado<br/>pronto para matching"]
    
    style A fill:#e3f2fd
    style B fill:#f3e5f5
    style C fill:#fff9c4
    style D fill:#fff59d
    style E fill:#ffcc80
    style F fill:#ffab91
    style G fill:#b3e5fc
```

## Fluxo de Tratamento de Erros

```mermaid
graph TD
    A["Processamento"] -->|Try/Catch| B{"Exceção<br/>capturada?"}
    
    B -->|Não| C["✅ ClassificacaoResponse<br/>tem_erros=False"]
    B -->|Sim| D["❌ Exception"]
    
    D -->|Em ClassificacaoHandler| E["ClassificacaoResponse<br/>tem_erros=True<br/>mensagem_erro"]
    
    D -->|Em lambda_handler| F["HTTP 500<br/>Erro ao processar"]
    
    E -->|Via handler| G["ClassificacaoResponse"]
    
    C -->|Response| H["lambda_handler<br/>retorna resposta"]
    G -->|Response| H
    F -->|Response| H
    
    H -->|JSON formatado| I["📤 Cliente recebe<br/>statusCode + body"]
    
    style C fill:#c8e6c9
    style E fill:#ffcdd2
    style F fill:#ffcdd2
    style I fill:#b3e5fc
```

---

## Legenda

| Componente | Descrição |
|-----------|-----------|
| 🌐 | API/Entrada externa |
| 📥 | Entrada de dados |
| 📤 | Saída de dados |
| ✅ | Sucesso |
| ❌ | Erro |
| 📝 | Processamento textual |
| 📊 | Cálculo/Processamento |
| 📈 | Normalização |
| 🏆 | Ordenação/Ranking |
| 1️⃣ 2️⃣ 3️⃣ | Múltiplas estratégias |
