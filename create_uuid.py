import uuid
import base64

def gerar_uuid_limitado(tamanho=8, usar_base64=False):
    """
    Gera um UUID limitado a um número específico de caracteres.

    :param tamanho: Número de caracteres desejados para o UUID gerado.
    :param usar_base64: Se True, utiliza Base64 para gerar uma versão mais curta do UUID.
    :return: Um UUID limitado ao número de caracteres especificado.
    """
    # Gerar o UUID aleatório
    uuid_gerado = uuid.uuid4()

    if usar_base64:
        # Codificar o UUID em Base64 e limitar a quantidade de caracteres
        uuid_base64 = base64.urlsafe_b64encode(uuid_gerado.bytes).decode('utf-8')[:tamanho]
        return uuid_base64
    else:
        # Limitar a quantidade de caracteres do UUID padrão (sem Base64)
        return str(uuid_gerado).replace('-', '')[:tamanho]


# Exemplos de uso

# Gerando um UUID limitado a 8 caracteres (sem Base64)
uuid_8_caracteres = gerar_uuid_limitado(8)


# Gerando um UUID limitado a 12 caracteres (sem Base64)
uuid_12_caracteres = gerar_uuid_limitado(12)


# Gerando um UUID usando Base64 limitado a 16 caracteres
uuid_base64_16 = gerar_uuid_limitado(16, usar_base64=True)

