# Balanceador de Equações Químicas ⚖️🧪

Um programa desenvolvido em **Python** 🐍 que permite **balancear equações químicas** de forma automática. Basta que o usuário digite a equação química dos reagentes e dos produtos em um formato pré-definido, e o programa retorna a equação balanceada, utilizando sistemas lineares para encontrar os coeficientes ideais.

---

## ➡Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Formato das Entradas](#formato-das-entradas)
- [Exemplos de Uso](#exemplos-de-uso)
- [Equações Inválidas](#equações-inválidas)
- [Requisitos e Instalação](#requisitos-e-instalação)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Autoria e Contato](#autoria-e-contato)

---

## ➡Visão Geral

Este **balanceador de equações químicas** foi criado para ajudar alunos, professores e entusiastas da química a verificar e obter as equações balanceadas a partir de equações fornecidas em texto.  
A interface é construída com a biblioteca **Flet**, que traz uma experiência gráfica simples e interativa, enquanto a lógica de balanceamento é baseada em operações com frações e matrizes para resolver sistemas lineares.

---

## ➡Funcionalidades

- **Entrada Validada**: Utiliza expressões regulares (_regex_) para validar o formato das equações químicas.
- **Balanceamento Automático**: Processa os reagentes e produtos, monta a matriz do sistema e resolve para obter os coeficientes balanceados.
- **Interface Interativa**: Desenvolvida com a biblioteca Flet para exibir os resultados e fornecer feedback visual em caso de erros.
- **Fácil de Usar**: Basta digitar a equação nos campos indicados e o programa fará todo o processamento.
  
---

## ➡Formato das Entradas

As entradas devem seguir um padrão específico. Alguns exemplos válidos:

- `Na2CO3 + HCl`
- `NaCl + H2O + CO2`
- `CH4 + O2`
- `CO2 + H2O`
- `HCl + Na3PO4`
- `H3PO4 + NaCl`

> **Importante:**  
> Os **espaços** podem ou não existir, mas a estrutura deve ter os **elementos químicos** com seus coeficientes (se houver) separados pelo sinal de **"+"**.

---

## ➡Exemplos de Uso

### Exemplo 1:

**Entrada:**  
- Reagents: `Na2CO3 + HCl`  
- Products: `NaCl + H2O + CO2`

**Saída Esperada:**  
A equação balanceada será exibida nos campos de resultado, por exemplo:  
1 Na2CO3 + 2 HCl >>> 2 NaCl + 1 H2O + 1 CO2.

### Exemplo 2:

**Entrada:**  
- Reagents: `CH4 + O2`  
- Products: `CO2 + H2O`

**Saída Esperada:**  
O programa calculará os coeficientes e mostrará a equação balanceada adequadamente, por exemplo: 1 CH4 + 2 O2 >>> 1 CO2 + 2 H2O.

---

## ➡Equações Inválidas

Alguns exemplos de entradas inválidas e que **não serão processadas**:

- `Na2CO3 + + HCl` (Uso incorreto do operador `+`)
- `Na2CO3 HCl` (Falta o separador `+`)
- `Na2CO3++HCl` (Dois sinais de `+` consecutivos)
- Entradas que apresentem elementos que existam somente em um lado da equação, por exemplo: reagentes e produtos não compartilhando os mesmos elementos.

> **OBS:**  
> Se ocorrer alguma inconsistência, o programa exibe um aviso através de um *SnackBar* indicando *"There is something wrong with the formulas. Check this out."*

    ❗Cuidado ao copiar e colar fórmulas de sites pois podem conter caracteres estranhos (inclusive invisíveis) que não são reconhecidos pelo programa.❗

---

## ➡Requisitos e Instalação

### Requisitos

- **Python 3.13.2+**
- Bibliotecas Python necessárias:
  - [Flet](https://pypi.org/project/flet/)
  - As bibliotecas nativas: `re`, `math`, e `fractions`

### Como Reproduzir

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu_usuario/equilibrador-equacoes-quimicas.git
   cd equilibrador-equacoes-quimicas

1. **Crie um ambiente virtual (opcional, mas recomendado):**
    ```bash
    python -m venv .venv
    # No Windows:
    .venv\Scripts\activate
    # No Linux/macOS:
    source .venv/bin/activate

1. **Instale as dependências:**
    ```bash
    pip install flet

1. **Execute o programa:**
    ```bash
    python main.py

> **OBS:**  
> Substitua "main.py" pelo nome do arquivo principal, caso seja diferente.

---

## ➡Tecnologias Utilizadas

- **Python**: Linguagem de programação usada para desenvolver a lógica de balanceamento.
- **Flet**: Biblioteca para criar a interface gráfica interativa.
- **Regex (re)**: Utilizada para validar os formatos das equações químicas.
- **Fractions e math**: Para manipulação exata de frações e cálculos matemáticos durante o balanceamento.
- **Matrix Computation**: Implementado para converter a equação química em um sistema linear que pode ser resolvido.

---

## ➡Autoria e Contato

- Feito por: Gabriel Monteiro Silva
- Feito em: 04/2025
- [GitHub](https://github.com/krosct): krosct
- [Email](mailto:krosct@gmail.com): krosct@gmail.com

---

#### 📢 Sinta-se à vontade para contribuir e sugerir melhorias. Se você encontrar algum bug ou desejar adicionar novas funcionalidades, por favor, abra uma issue ou envie um pull request.

---

#### ⚠️ TRABALHO EXPERIMENTAL!
#### ⛔ Esse programa ainda **não** foi revisado, ajustado e melhorado. Considere que a **performance é relativamente baixa** e o código ainda possui bugs e possíveis erros.

