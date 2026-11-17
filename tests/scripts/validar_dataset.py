"""Valida o dataset de casos de teste (formato JSONL: um caso por linha).

Uso: python tests/scripts/validar_dataset.py
Retorna codigo de saida 0 se valido e 1 se houver erros.
"""
import json
import sys
from collections import Counter
from pathlib import Path

# Caminho calculado a partir deste script (tests/scripts/ -> tests/dataset/),
# para funcionar independentemente da pasta de onde o comando e executado.
ARQUIVO = Path(__file__).resolve().parents[1] / "dataset" / "casos-de-teste.jsonl"

CAMPOS = {"id", "categoria", "entrada", "comportamento_esperado",
          "criterios", "nao_deve", "severidade", "referencias"}
CAMPOS_LISTA = ("criterios", "nao_deve", "referencias")
CATEGORIAS = {"caminho_feliz", "fora_de_escopo", "sem_informacao", "ambiguidade",
              "handoff", "pii", "menor_de_idade", "prompt_injection",
              "vazamento_contexto", "conteudo_nocivo", "consumo_excessivo",
              "saida_insegura"}
COMPORTAMENTOS = {"responder", "recusar", "encaminhar_humano",
                  "pedir_esclarecimento", "dizer_que_nao_sabe"}
SEVERIDADES = {"baixa", "media", "alta", "critica"}


def validar_caso(caso: dict, n: int, ids: set) -> list[str]:
    """Retorna a lista de erros de esquema de um caso."""
    erros = []

    faltando = CAMPOS - caso.keys()
    if faltando:
        erros.append(f"linha {n}: faltam campos {sorted(faltando)}")

    sobrando = caso.keys() - CAMPOS
    if sobrando:
        erros.append(f"linha {n}: campos desconhecidos {sorted(sobrando)}")

    if "id" in caso:
        if caso["id"] in ids:
            erros.append(f"linha {n}: id repetido {caso['id']}")
        ids.add(caso["id"])

    if "categoria" in caso and caso["categoria"] not in CATEGORIAS:
        erros.append(f"linha {n}: categoria invalida '{caso['categoria']}'")

    if ("comportamento_esperado" in caso
            and caso["comportamento_esperado"] not in COMPORTAMENTOS):
        erros.append(f"linha {n}: comportamento invalido "
                     f"'{caso['comportamento_esperado']}'")

    if "severidade" in caso and caso["severidade"] not in SEVERIDADES:
        erros.append(f"linha {n}: severidade invalida '{caso['severidade']}'")

    for campo in CAMPOS_LISTA:
        if campo in caso and (not isinstance(caso[campo], list) or not caso[campo]):
            erros.append(f"linha {n}: '{campo}' deve ser uma lista nao vazia")

    return erros


def main() -> int:
    if not ARQUIVO.exists():
        print(f"[ERRO] arquivo nao encontrado: {ARQUIVO}")
        return 1

    erros, ids, por_categoria = [], set(), Counter()

    for n, linha in enumerate(ARQUIVO.read_text(encoding="utf-8").splitlines(), 1):
        if not linha.strip():
            continue
        try:
            caso = json.loads(linha)
        except json.JSONDecodeError as e:
            erros.append(f"linha {n}: JSON invalido ({e.msg})")
            continue
        if not isinstance(caso, dict):
            erros.append(f"linha {n}: cada linha deve ser um objeto JSON")
            continue

        erros.extend(validar_caso(caso, n, ids))
        por_categoria[caso.get("categoria")] += 1

    print("Casos por categoria:")
    for cat in sorted(CATEGORIAS):
        marca = "  [AVISO] sem casos" if por_categoria[cat] == 0 else ""
        print(f"  {cat:20} {por_categoria[cat]}{marca}")
    print(f"TOTAL: {sum(por_categoria.values())}")

    if erros:
        print(f"\n[ERRO] {len(erros)} erro(s):")
        for e in erros:
            print(f"  - {e}")
        return 1

    print("\n[OK] Dataset valido")
    return 0


if __name__ == "__main__":
    sys.exit(main())