# Indexador de ROMs com Tabela Hash própria

<div align = "center">
<table>
  <tr>
    <td align="center"><a href="https://github.com/victorcamaraa"><img style="border-radius: 50%;" src="https://github.com/victorcamaraa.png" width="190px;" alt=""/><br /><sub><b>Victor Camara</b></sub></a><br /><a href="Link git" title="Rocketseat"></a></td>
    <td align="center"><a href="https://github.com/yanzin00"><img style="border-radius: 50%;" src="https://github.com/yanzin00.png" width="190px;" alt=""/><br /><sub><b>Yan Guimarães </b></sub></a><br />
  </tr>
</table>

| Matrícula   | Aluno                             |
| ----------- | ---------------------------------- |
| 222006220  | Yan Lucas Souza Guimarães |
| 221031238  | Victor Augusto de Sousa Camara |
</div> 

## [Vídeo de demonstração](https://drive.google.com/drive/folders/1iFZ5N3bZ-zTFKSO7wrfIlDC-y0j5MnkC?usp=sharing)

## Como funciona

1. O programa varre uma pasta recursivamente.
2. Para cada arquivo, calcula um **hash do conteúdo** (CRC32 via `zlib`).
3. Usa esse hash como **chave** numa tabela hash implementada à mão.
4. Arquivos com o mesmo conteúdo geram a mesma chave → são agrupados como
   duplicatas.

O hash de conteúdo é apenas o *insumo* que gera as chaves; a estrela do trabalho
é a tabela hash (`hash_table.py`).

## Arquivos

| Arquivo                | Papel                                                        |
| ---------------------- | ------------------------------------------------------------ |
| `hash_table.py`        | Classe `HashTable` (encadeamento separado + resize). **Sem `dict`/`set`/`Counter`.** |
| `rom_indexer.py`       | Varredura da pasta, hash de conteúdo, coleta de duplicatas.  |
| `main.py`              | CLI e relatório.                                             |
| `gerar_dados_teste.py` | Gerador de arquivos fake (com cópias propositais) para teste.|

Sem dependências externas — só a stdlib (`zlib`, `os`, `time`, `argparse`).

## Como rodar

```bash
# 1) Self-check da tabela hash (asserts)
python main.py --help        # ver opções da CLI
python hash_table.py         # roda os testes internos

# 2) Gerar dados de teste (50 únicos + 8 cópias)
python gerar_dados_teste.py ./roms_teste --n 50 --duplicatas 8

# 3) Indexar e ver o relatório
python main.py ./roms_teste
```

Para usar com ROMs reais, basta apontar para a pasta: `python main.py /minha/pasta/roms`.

## Decisões de design (o "porquê")

- **Encadeamento separado** como tratamento de colisão: cada posição do array
  guarda uma lista de pares. É simples, nunca "enche" a tabela (fator de carga > 1
  só deixa mais lento, não quebra) e a remoção é trivial — diferente do
  endereçamento aberto, que precisa de *tombstones*. Além disso, encaixa
  naturalmente na detecção de duplicatas: o valor de cada chave já é uma lista de
  caminhos.

- **Tamanho inicial pequeno (8) + resize automático**: reservar um array enorme
  "por precaução" desperdiça memória. Começamos pequeno e dobramos a capacidade
  quando o **fator de carga passa de 0.7** (rehashing). 0.7 é o meio-termo clássico
  entre memória usada e número de colisões.

- **Mapeamento chave → índice na mão**: a chave é um inteiro grande (CRC32, até
  2³²-1). Usamos a função de compressão clássica `índice = chave % capacidade`,
  que garante uma posição válida no array. **Não** chamamos `hash()` do Python às
  cegas — a chave já é um inteiro bem distribuído, então o módulo basta.

- **Contagem de comparações**: `inserir`, `buscar` e `existe` contam quantas
  comparações de chave fazem dentro do bucket. Numa tabela bem dimensionada esse
  número fica perto de 0–1; ele cresce quando há colisões, o que permite discutir
  desempenho no relatório.

- **CRC32 e sua limitação**: CRC32 tem só 32 bits, então dois conteúdos diferentes
  *podem* (raramente) colidir e gerar um falso-positivo. Mitigação barata aplicada
  em `coletar_duplicatas`: dentro de um grupo, só consideramos duplicados os
  arquivos com o **mesmo tamanho**. Não é prova definitiva de igualdade (o upgrade
  seria comparar byte a byte), mas elimina os colisores óbvios sem reler o conteúdo.

## Exemplo de resultado

Execução com `--n 50 --duplicatas 8`:

```
Total de arquivos escaneados : 58
Grupos de duplicatas         : 8
Cópias extras (desperdício)  : 8
Fator de carga final         : 0.391 (50 chaves / 128 posições)
Colisões em inserções        : 28
Comparações médias/inserção  : 0.638
Tempo total                  : 0.0009 s
```

Os 8 grupos detectados batem exatamente com as 8 cópias geradas pelo script de
teste — confirmando que a implementação está correta. O fator de carga final
(0.391) mostra o efeito do resize: a tabela cresceu de 8 para 128 posições ao
longo das inserções, mantendo os buckets curtos e a média de comparações abaixo
de 1.
