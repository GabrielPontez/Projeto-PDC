import csv
from datetime import datetime

ARQUIVO = "gastos.csv"
CATEGORIAS = ["Alimentação", "Transporte", "Lazer", "Educação", "Saúde", "Outros"]

def menu():
    print("\n=== Controle de Gastos Pessoais ===")
    print("1. Adicionar despesa")
    print("2. Relatório por categoria")
    print("3. Relatório mensal")
    print("4. Relatório geral")
    print("5. Sair")
    return input("Escolha uma opção: ")

def adicionar_despesa():
    data = input("Data (AAAA-MM-DD): ")
    descricao = input("Descrição: ")
    print("Categorias disponíveis:")
    for i, cat in enumerate(CATEGORIAS):
        print(f"{i+1}. {cat}")
    categoria_index = int(input("Escolha a categoria (número): ")) - 1
    categoria = CATEGORIAS[categoria_index]
    valor = float(input("Valor (R$): "))

    with open(ARQUIVO, "a", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow([data, descricao, categoria, valor])
    print("Despesa registrada com sucesso!")

def carregar_despesas():
    despesas = []
    try:
        with open(ARQUIVO, newline="") as f:
            leitor = csv.reader(f)
            for linha in leitor:
                data, descricao, categoria, valor = linha
                despesas.append({
                    "data": data,
                    "descricao": descricao,
                    "categoria": categoria,
                    "valor": float(valor)
                })
    except FileNotFoundError:
        pass
    return despesas

def relatorio_por_categoria():
    despesas = carregar_despesas()
    resumo = {}
    for d in despesas:
        resumo[d["categoria"]] = resumo.get(d["categoria"], 0) + d["valor"]

    print("\n=== Relatório por Categoria ===")
    for cat in sorted(resumo.keys()):
        print(f"{cat}: R$ {resumo[cat]:.2f}")

def relatorio_mensal():
    despesas = carregar_despesas()
    ano = input("Digite o ano (AAAA): ")
    mes = input("Digite o mês (MM): ")
    total = 0
    print(f"\n=== Relatório de {mes}/{ano} ===")
    for d in despesas:
        data = datetime.strptime(d["data"], "%Y-%m-%d")
        if data.year == int(ano) and data.month == int(mes):
            print(f"{d['data']} | {d['descricao']} | {d['categoria']} | R$ {d['valor']:.2f}")
            total += d["valor"]
    print(f"Total gasto no mês: R$ {total:.2f}")

def relatorio_geral():
    despesas = carregar_despesas()
    total = sum(d["valor"] for d in despesas)
    media = total / len(despesas) if despesas else 0
    print("\n=== Relatório Geral ===")
    print(f"Total gasto: R$ {total:.2f}")
    print(f"Média por despesa: R$ {media:.2f}")

def main():
    while True:
        opcao = menu()
        if opcao == "1":
            adicionar_despesa()
        elif opcao == "2":
            relatorio_por_categoria()
        elif opcao == "3":
            relatorio_mensal()
        elif opcao == "4":
            relatorio_geral()
        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
