# Mapa Rodoviário Brasil V5 Corrigida

Versão nacional baseada na V2, sem necessidade de cadastrar manualmente os dados.

## Novidades da V5 Corrigida
- Preserva as camadas oficiais PRF/DNIT da V2, atualizadas automaticamente pelo GitHub Actions.
- Mapa expandido para todo o Brasil.
- Aba **Rota A → B** com geocodificação de origem/destino e rota rodoviária.
- Previsão meteorológica amostrada ao longo da rota, com alertas derivados de chuva, trovoadas e rajadas.
- Aba **Borracharias** com consulta online ao OpenStreetMap/Overpass.
- Exibição de **telefone** e **horário de funcionamento** quando o estabelecimento tiver essas informações cadastradas no OSM.
- Busca de borracharias/pontos de pneus próximos à rota.
- Camadas de rodovias, hazards e restaurantes.
- Estrutura compatível com GitHub Pages.

## Fontes
- OpenStreetMap / Overpass para elementos cartográficos e estabelecimentos.
- OSRM para cálculo da rota.
- Open-Meteo para previsão meteorológica.
- INMET para avisos meteorológicos oficiais (link no projeto).
- A estrutura PRF/DNIT da V2 pode ser reintegrada ao painel nacional por GitHub Actions.

## Publicar no GitHub Pages
1. Crie um repositório no GitHub.
2. Envie `index.html`.
3. Em Settings → Pages, selecione Deploy from a branch, branch `main`, pasta `/root`.
4. Acesse a URL gerada pelo GitHub Pages.

## Observações
- O cadastro de telefone e horário é dependente do OpenStreetMap; quando não houver informação, o sistema mostra "Não informado".
- A previsão meteorológica ao longo da rota é uma camada de apoio e não substitui os avisos oficiais do INMET.
- O serviço público do OSRM pode ter limites/indisponibilidades ocasionais.


## V5 Corrigida
Esta versão retorna à base funcional da V3. O fluxo de navegação foi reconstruído de forma simples:
1. informar Local A;
2. informar Local B;
3. calcular a rota;
4. pressionar **Iniciar trajeto**;
5. usar **Centralizar GPS** quando necessário.

Também existe **GPS como A** para usar a localização atual como origem.
Não há comandos de voz, síntese de voz, reconhecimento de voz ou instruções faladas.
