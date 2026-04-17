#!/usr/bin/env python3

import sqlite3
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.carrinho_db import (
    criar_tabela,
    adicionar_item,
    listar_itens,
    calcular_total,
    limpar_carrinho,
)


# =====================================================================
# FIXTURE — Banco de dados isolado por teste
# =====================================================================

@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    criar_tabela(conn)
    yield conn
    conn.close()


# =====================================================================
# GRUPO 1 — Testes de Inserção e Persistência
# =====================================================================

def test_item_persiste_no_banco(db):
    # Arrange
    adicionar_item(db, "Carne", 50.0, 2)

    # Act
    itens = listar_itens(db)

    # Assert
    assert len(itens) == 1
    assert itens[0]["nome"] == "Carne"
    assert itens[0]["preco"] == 50.0
    assert itens[0]["quantidade"] == 2


def test_multiplos_itens_persistem(db):
    # Arrange
    adicionar_item(db, "Carne", 50.0, 1)
    adicionar_item(db, "Frango", 30.0, 2)
    adicionar_item(db, "Linguiça", 20.0, 3)

    # Act
    itens = listar_itens(db)

    # Assert
    assert len(itens) == 3


def test_preco_negativo_lanca_value_error(db):
    # Assert
    with pytest.raises(ValueError):
        adicionar_item(db, "Carne", -10.0, 1)


# =====================================================================
# GRUPO 2 — Testes de Cálculo de Total
# =====================================================================

def test_carrinho_vazio_retorna_zero(db):
    # Arrange
    # banco vazio

    # Act
    total = calcular_total(db)

    # Assert
    assert total == 0.0


def test_total_considera_quantidade(db):
    # Arrange
    adicionar_item(db, "Carne", 50.0, 3)

    # Act
    total = calcular_total(db)

    # Assert
    assert total == 150.0


def test_total_multiplos_itens(db):
    # Arrange
    adicionar_item(db, "Carne", 50.0, 2)   # 100
    adicionar_item(db, "Frango", 30.0, 1)  # 30
    adicionar_item(db, "Linguiça", 20.0, 3) # 60

    # Act
    total = calcular_total(db)

    # Assert
    assert total == 190.0


# ======================================================================
# GRUPO 3 — Testes de Limpeza do Carrinho
# ======================================================================

def test_limpar_remove_todos_os_itens(db):
    # Arrange
    adicionar_item(db, "Carne", 50.0, 1)
    adicionar_item(db, "Frango", 30.0, 1)

    # Act
    limpar_carrinho(db)
    itens = listar_itens(db)
    total = calcular_total(db)

    # Assert
    assert itens == []
    assert total == 0.0


def test_pode_adicionar_apos_limpar(db):
    # Arrange
    adicionar_item(db, "Carne", 50.0, 1)
    limpar_carrinho(db)

    # Act
    adicionar_item(db, "Frango", 30.0, 2)
    itens = listar_itens(db)

    # Assert
    assert len(itens) == 1
    assert itens[0]["nome"] == "Frango"