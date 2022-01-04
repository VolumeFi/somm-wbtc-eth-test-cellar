from brownie import CellarPoolShare, accounts

def main():
    acct = accounts.load("deployer_account")
    name = "Test SOMM WBTC-ETH"
    symbol = "TESTSOMMWBTCETH"
    token0 = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
    token1 = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    cellarTickInfo = [[0, 259260, 248280, 1]]
    CellarPoolShare.deploy(name, symbol, token0, token1, 3000, cellarTickInfo, {"from":acct})