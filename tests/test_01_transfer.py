#!/usr/bin/python3

import pytest
import brownie

def test_add_liquidity_ETH(WBTC, WETH, accounts, SwapRouter, CellarPoolShareContract):
    SwapRouter.exactOutputSingle([WETH, WBTC, 3000, accounts[0], 2 ** 256 - 1, 6 * 10 ** 7, 10 * 10 ** 18, 0], {"from": accounts[0], "value": 10 * 10 ** 18})
    SwapRouter.exactOutputSingle([WETH, WBTC, 3000, accounts[1], 2 ** 256 - 1, 6 * 10 ** 7, 10 * 10 ** 18, 0], {"from": accounts[1], "value": 10 * 10 ** 18})
    WBTC.approve(CellarPoolShareContract, 3 * 10 ** 7, {"from": accounts[0]})
    WBTC.approve(CellarPoolShareContract, 3 * 10 ** 7, {"from": accounts[1]})
    ETH_amount = 10 ** 18
    WBTC_amount = 10 ** 7
    cellarAddParams = [WBTC_amount, ETH_amount, 0, 0, 2 ** 256 - 1]
    CellarPoolShareContract.addLiquidityForUniV3(cellarAddParams, {"from": accounts[0], "value": 1 * 10 ** 18})
    CellarPoolShareContract.addLiquidityForUniV3(cellarAddParams, {"from": accounts[0], "value": 1 * 10 ** 18})
    CellarPoolShareContract.addLiquidityForUniV3(cellarAddParams, {"from": accounts[0], "value": 1 * 10 ** 18})
    cellarAddParams = [WBTC_amount, ETH_amount, 0, 0, 2 ** 256 - 1]
    CellarPoolShareContract.addLiquidityForUniV3(cellarAddParams, {"from": accounts[1], "value": 1 * 10 ** 18})
    CellarPoolShareContract.addLiquidityForUniV3(cellarAddParams, {"from": accounts[1], "value": 1 * 10 ** 18})
    CellarPoolShareContract.addLiquidityForUniV3(cellarAddParams, {"from": accounts[1], "value": 1 * 10 ** 18})
    assert CellarPoolShareContract.balanceOf(accounts[0]) == CellarPoolShareContract.balanceOf(accounts[1])

def test_transfer(accounts, CellarPoolShareContract):
    account0_balance = CellarPoolShareContract.balanceOf(accounts[0])
    account1_balance = CellarPoolShareContract.balanceOf(accounts[1])
    CellarPoolShareContract.transfer(accounts[2], account0_balance, {"from": accounts[0]})
    CellarPoolShareContract.transfer(accounts[0], account1_balance, {"from": accounts[1]})
    CellarPoolShareContract.transfer(accounts[1], account0_balance, {"from": accounts[2]})
    assert CellarPoolShareContract.balanceOf(accounts[0]) == account1_balance
    assert CellarPoolShareContract.balanceOf(accounts[1]) == account0_balance

def test_approve(accounts, CellarPoolShareContract):
    account0_balance = CellarPoolShareContract.balanceOf(accounts[0])
    account1_balance = CellarPoolShareContract.balanceOf(accounts[1])
    with brownie.reverts():
        CellarPoolShareContract.transferFrom(accounts[1], accounts[2], account1_balance, {"from": accounts[0]})
    with brownie.reverts():
        CellarPoolShareContract.transferFrom(accounts[0], accounts[2], account0_balance, {"from": accounts[1]})
    CellarPoolShareContract.approve(accounts[1], account0_balance, {"from": accounts[0]})
    CellarPoolShareContract.transferFrom(accounts[0], accounts[2], account0_balance, {"from": accounts[1]})
    assert CellarPoolShareContract.balanceOf(accounts[2]) == account0_balance
    assert CellarPoolShareContract.balanceOf(accounts[0]) == 0
    with brownie.reverts():
        CellarPoolShareContract.transferFrom(accounts[2], accounts[0], account0_balance, {"from": accounts[1]})
    CellarPoolShareContract.approve(accounts[1], account0_balance, {"from": accounts[2]})
    CellarPoolShareContract.transferFrom(accounts[2], accounts[0], account0_balance, {"from": accounts[1]})
    assert CellarPoolShareContract.balanceOf(accounts[0]) == account0_balance