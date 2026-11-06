import logging

LOGGER = logging.getLogger("devops")
LOGGER.setLevel(logging.INFO)

saida_padrao = logging.StreamHandler()
arquivo = logging.FileHandler("aplicacao.log", encoding='utf-8')

formatador = logging.Formatter("%(name)s | %(levelname)s | %(asctime)s | %(filename)s:%(lineno)s | %(message)s")

saida_padrao.setFormatter(formatador)
arquivo.setFormatter(formatador)

LOGGER.addHandler(saida_padrao)
LOGGER.addHandler(arquivo)

LOGGER.info("Esse é um log de informação")
LOGGER.debug("Esse é um log de depuração. Não aparecerá")
LOGGER.warning("Esse é um log de aviso. Sempre aparecerá")