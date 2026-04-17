import pytest
from app.pagamentos import (
    calcular_desconto,
    aplicar_juros_atraso,
    validar_metodo_pagamento,
    processar_reembolso
)

def test_calcular_desconto():
    # Arrange
    valor = 100
    percentual = 10
    
    # Act
    resultado = calcular_desconto(valor, percentual)
    
    # Assert
    assert resultado == 90


def test_aplicar_juros_atraso():
    # Arrange
    valor_pago = 100
    dias_atraso = 5
    dias_ok = 0
    
    # Act
    resultado_com_atraso = aplicar_juros_atraso(valor_pago, dias_atraso)
    resultado_sem_atraso = aplicar_juros_atraso(valor_pago, dias_ok)
    
    # Assert
    # Correção: 1% ao dia → 100 + (100 * 0.01 * 5) = 105.0
    assert resultado_com_atraso == 105.0
    assert resultado_sem_atraso == 100.0


def test_validar_metodo_pagamento():
    """
    MISSÃO: Cobrir método aceito e rejeitado
    """
    # Arrange
    metodo_valido = "pix"
    metodo_invalido = "cheque"
    
    # Act
    resultado_valido = validar_metodo_pagamento(metodo_valido)
    resultado_invalido = validar_metodo_pagamento(metodo_invalido)
    
    # Assert
    assert resultado_valido == True
    assert resultado_invalido == False


def test_processar_reembolso():
    """
    MISSÃO: Testar válido, limite e inválido
    """
    # Arrange
    valor_pago = 200
    valor_reembolso_valido = 100
    valor_reembolso_exato = 200  # Caso de Valor Limite
    valor_reembolso_invalido = 201  # Caso de Valor Limite
    
    # Act
    resultado_valido = processar_reembolso(valor_pago, valor_reembolso_valido)
    resultado_exato = processar_reembolso(valor_pago, valor_reembolso_exato)
    resultado_invalido = processar_reembolso(valor_pago, valor_reembolso_invalido)
    
    # Assert
    assert resultado_valido == 100
    assert resultado_exato == 0
    assert resultado_invalido == -1