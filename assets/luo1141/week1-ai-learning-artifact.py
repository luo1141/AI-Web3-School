#!/usr/bin/env python3
"""
Web3 Concept Explainer - Interactive CLI Tool
==============================================
A learning tool for AI x Web3 School Week 1.
Type a Web3 concept name to get an explanation, example, and security tip.
Type 'list' to see all concepts, or 'quit' to exit.
"""

# ── Knowledge Base ──────────────────────────────────────────────────────────

CONCEPTS = {
    "account": {
        "name": "Account",
        "explanation": (
            "An account in Web3 is an entity that can hold assets (tokens, NFTs) "
            "and interact with the blockchain. On Ethereum, there are two types: "
            "Externally Owned Accounts (EOAs), controlled by a private key, and "
            "Contract Accounts, controlled by deployed smart contract code. Each "
            "account has a unique address and a balance of the chain's native "
            "token (e.g., ETH on Ethereum)."
        ),
        "example": (
            "Alice creates a MetaMask wallet. MetaMask generates a private key "
            "and derives an EOA with address 0xAb58...e1Cf. This account can "
            "send ETH and interact with dApps."
        ),
        "security_tip": (
            "Never share your private key or seed phrase with anyone. Use a "
            "hardware wallet for large holdings and enable 2FA on any exchange "
            "accounts."
        ),
    },
    "address": {
        "name": "Address",
        "explanation": (
            "A blockchain address is a unique identifier (usually 20 bytes / "
            "42 hex characters) that represents an account on the network. It is "
            "publicly visible and is used to send and receive tokens. Addresses "
            "are derived from public keys (for EOAs) or from the deployer's "
            "address and nonce (for contract accounts)."
        ),
        "example": (
            "Ethereum address: 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD68. "
            "You share this with someone so they can send you ETH or ERC-20 tokens."
        ),
        "security_tip": (
            "Always double-check the first and last few characters of an address "
            "before sending funds. Malware can swap addresses in your clipboard. "
            "Consider using ENS (e.g., alice.eth) to avoid manual errors."
        ),
    },
    "wallet": {
        "name": "Wallet",
        "explanation": (
            "A wallet is a software application (or hardware device) that stores "
            "your private keys and provides an interface to manage your blockchain "
            "accounts. The wallet itself does NOT store your tokens—tokens live on "
            "the blockchain. The wallet holds the keys that prove ownership and "
            "allow you to sign transactions."
        ),
        "example": (
            "MetaMask is a browser-extension wallet that manages Ethereum "
            "accounts. Other examples include Trust Wallet (mobile), Ledger "
            "(hardware), and Rainbow (mobile/desktop)."
        ),
        "security_tip": (
            "Back up your seed phrase on paper (not digitally) and store it in a "
            "secure location. Never enter your seed phrase on any website or share "
            "it with support staff—no legitimate service will ever ask for it."
        ),
    },
    "private key": {
        "name": "Private Key",
        "explanation": (
            "A private key is a 256-bit (32-byte) secret number used to sign "
            "transactions and prove ownership of an account. It is mathematically "
            "linked to your public key and address. Whoever controls the private "
            "key controls the funds in that account. Private keys are typically "
            "represented as 64 hexadecimal characters."
        ),
        "example": (
            "Private key: 0x4c0883a69102937d6231471b5dbb6204fe51296170827937ea52b9e3..."
            " This key signs the transaction that moves your ETH."
        ),
        "security_tip": (
            "Treat your private key like the PIN to your bank vault. Never store "
            "it in plain text on a computer, cloud service, or chat. Use a "
            "hardware wallet or encrypted keystore file. If compromised, all "
            "funds are at risk instantly."
        ),
    },
    "seed phrase": {
        "name": "Seed Phrase",
        "explanation": (
            "A seed phrase (also called a recovery phrase or mnemonic) is a set "
            "of 12 or 24 human-readable words generated when you create a wallet. "
            "It is derived from a BIP-39 standard and is used to deterministically "
            "regenerate all the private keys for your wallet. It is the master "
            "backup of your crypto identity."
        ),
        "example": (
            "Your MetaMask wallet shows: \"witch collapse practice feed "
            "oppose open sunset pave damage zone answer ...\" These 12 words "
            "can regenerate your entire wallet on any compatible software."
        ),
        "security_tip": (
            "Write your seed phrase on metal (fire/water resistant) and store it "
            "in a physical safe. NEVER type it into any website, app, or "
            "extension. Anyone who asks for it is trying to steal your funds. "
            "Consider using Shamir's Secret Sharing for redundancy."
        ),
    },
    "signature": {
        "name": "Signature (Digital Signature)",
        "explanation": (
            "A digital signature is a cryptographic proof that a transaction was "
            "authorized by the holder of a specific private key. When you send a "
            "transaction, your wallet signs it with your private key. The network "
            "verifies the signature using your public key—without ever revealing "
            "the private key itself. This ensures authenticity and non-repudiation."
        ),
        "example": (
            "When Alice sends 1 ETH to Bob, her wallet signs the transaction "
            "with her private key. Nodes verify the signature against Alice's "
            "public address before including it in a block."
        ),
        "security_tip": (
            "Be cautious about what you sign. Malicious dApps may present "
            "harmless-looking messages that grant token approvals or transfer "
            "rights. Always read the full signing request before confirming. Use "
            "tools like revoke.cash to monitor and revoke approvals."
        ),
    },
    "transaction": {
        "name": "Transaction",
        "explanation": (
            "A transaction is a signed instruction sent to the blockchain that "
            "changes its state. Common transaction types include: transferring "
            "tokens, deploying a smart contract, or calling a function on an "
            "existing contract. Each transaction has a gas cost, a nonce (sequence "
            "number), and is permanently recorded on-chain."
        ),
        "example": (
            "Alice sends 0.5 ETH to Bob. The transaction includes: sender "
            "(Alice's address), recipient (Bob's address), value (0.5 ETH), "
            "gas limit, gas price, nonce, and Alice's signature. Once mined, it "
            "is irreversible."
        ),
        "security_tip": (
            "Always verify transaction details (recipient, amount, function "
            "called) before confirming. Set appropriate gas limits to avoid "
            "wasting funds. For large transactions, send a small test amount "
            "first."
        ),
    },
    "gas": {
        "name": "Gas",
        "explanation": (
            "Gas is the unit of measurement for the computational effort required "
            "to execute operations on the Ethereum network. Every operation (add, "
            "store, transfer) costs a certain amount of gas. Users pay for gas "
            "using ETH. After EIP-1559, each transaction includes a base fee "
            "(burned) and an optional priority fee (tip to validators). Gas "
            "prices fluctuate based on network demand."
        ),
        "example": (
            "A simple ETH transfer costs 21,000 gas. If gas price is 30 gwei, "
            "the fee is 21,000 × 30 gwei = 630,000 gwei = 0.00063 ETH. During "
            "network congestion, gas prices can spike to 100+ gwei."
        ),
        "security_tip": (
            "Monitor gas prices using tools like Etherscan Gas Tracker or "
            "ethgasstation. Avoid transacting during peak congestion. Consider "
            "using Layer 2 solutions (Arbitrum, Optimism, Base) for lower fees."
        ),
    },
    "smart contract": {
        "name": "Smart Contract",
        "explanation": (
            "A smart contract is a self-executing program stored on the "
            "blockchain that automatically enforces the terms of an agreement "
            "when predefined conditions are met. Written in languages like "
            "Solidity (Ethereum), they are immutable once deployed and execute "
            "exactly as coded. They power DeFi, NFTs, DAOs, and more."
        ),
        "example": (
            "Uniswap's smart contract allows users to swap ERC-20 tokens "
            "automatically. When you send ETH to the contract, it calculates "
            "the exchange rate and sends you the corresponding tokens—no "
            "intermediary needed."
        ),
        "security_tip": (
            "Smart contracts can have bugs that lead to exploits (e.g., "
            "reentrancy attacks). Only interact with audited, well-known "
            "contracts. Check for audit reports on the project's website. Never "
            "blindly trust unaudited contracts with large funds."
        ),
    },
    "testnet": {
        "name": "Testnet",
        "explanation": (
            "A testnet is a parallel blockchain network used for testing and "
            "development before deploying to mainnet. Testnets use the same "
            "technology as mainnet but tokens have no real value. Popular "
            "Ethereum testnets include Sepolia and Holesky. Developers use them "
            "to debug smart contracts and test dApp functionality risk-free."
        ),
        "example": (
            "Before deploying a DeFi protocol on Ethereum mainnet, you can "
            "deploy it on Sepolia testnet. Use a Sepolia faucet to get free "
            "test ETH and experiment without spending real money."
        ),
        "security_tip": (
            "NEVER send real (mainnet) assets to a testnet address—they will be "
            "irrecoverable. Testnet wallets and mainnet wallets can have the "
            "same address, so double-check which network your wallet is "
            "connected to before transacting."
        ),
    },
    "block explorer": {
        "name": "Block Explorer",
        "explanation": (
            "A block explorer is a web-based tool that allows you to search and "
            "browse all data on a blockchain—transactions, blocks, addresses, "
            "smart contracts, token transfers, and more. It serves as a "
            "transparent window into the ledger. Major explorers include "
            "Etherscan (Ethereum), Solscan (Solana), and Blockchair (multi-chain)."
        ),
        "example": (
            "Go to etherscan.io and paste any Ethereum address to see its "
            "balance, transaction history, token holdings, and smart contract "
            "interactions. You can also verify contract source code there."
        ),
        "security_tip": (
            "Use block explorers to verify transaction status and recipient "
            "addresses before considering a transaction complete. Bookmark "
            "official explorer URLs to avoid phishing sites that mimic them."
        ),
    },
    "eoa": {
        "name": "EOA (Externally Owned Account)",
        "explanation": (
            "An EOA is an account controlled by a private key, as opposed to a "
            "contract account controlled by code. EOAs can initiate transactions, "
            "hold ETH, and sign messages. They are the most common type of account "
            "used by individual users. Every wallet (MetaMask, Ledger, etc.) "
            "manages one or more EOAs."
        ),
        "example": (
            "Your MetaMask wallet generates an EOA. You use it to send ETH, "
            "connect to Uniswap, mint NFTs, and vote in DAOs. Unlike contract "
            "accounts, EOAs can initiate transactions on their own."
        ),
        "security_tip": (
            "EOAs are only as secure as the private key protecting them. Use a "
            "hardware wallet (Ledger, Trezor) to keep the key offline. Consider "
            "using a separate EOA for high-value holdings versus daily dApp "
            "interactions."
        ),
    },
}

# Additional bonus concepts
EXTRAS = {
    "dapp": {
        "name": "dApp (Decentralized Application)",
        "explanation": (
            "A dApp is an application built on blockchain technology that runs "
            "on a peer-to-peer network instead of a centralized server. It "
            "typically has a front-end (like any web app) but uses smart "
            "contracts for backend logic. Examples include Uniswap, OpenSea, "
            "and Aave."
        ),
        "example": (
            "OpenSea is an NFT marketplace dApp. Instead of a company holding "
            "your NFTs, they live on-chain. The front-end reads from the "
            "blockchain, and smart contracts handle trades."
        ),
        "security_tip": (
            "Always verify you are on the correct dApp URL. Phishing sites "
            "often mimic popular dApps. Check the URL carefully and consider "
            "using bookmarks."
        ),
    },
    "token": {
        "name": "Token",
        "explanation": (
            "A token is a digital asset created on top of an existing "
            "blockchain. Fungible tokens (like ERC-20) are interchangeable "
            "(1 ETH = 1 ETH). Non-fungible tokens (ERC-721) are unique. "
            "Tokens can represent currency, governance rights, access passes, "
            "or real-world assets."
        ),
        "example": (
            "USDC is an ERC-20 stablecoin pegged to $1. Each token is "
            "interchangeable. Bored Ape #1234 is an ERC-721 NFT—unique and "
            "non-interchangeable."
        ),
        "security_tip": (
            "Verify token contract addresses before purchasing. Scammers create "
            "fake tokens with similar names. Check contract addresses on "
            "CoinGecko or the project's official site."
        ),
    },
    "defi": {
        "name": "DeFi (Decentralized Finance)",
        "explanation": (
            "DeFi refers to financial services (lending, borrowing, trading, "
            "insurance) built on blockchain without traditional intermediaries "
            "like banks. Protocols use smart contracts to automate financial "
            "operations. Total Value Locked (TVL) across DeFi protocols can "
            "exceed billions of dollars."
        ),
        "example": (
            "Aave lets you lend crypto and earn interest, or borrow against "
            "your holdings—all without a bank. Rates are determined by supply "
            "and demand in smart contract pools."
        ),
        "security_tip": (
            "DeFi carries risks: smart contract bugs, oracle manipulation, "
            "rug pulls, and impermanent loss. Only use audited protocols, "
            "diversify, and never invest more than you can afford to lose."
        ),
    },
}

# Merge all concepts
ALL_CONCEPTS = {**CONCEPTS, **EXTRAS}


# ── Display Helpers ─────────────────────────────────────────────────────────

BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
DIM = "\033[2m"
RESET = "\033[0m"

BANNER = rf"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════╗
║         🔗  Web3 Concept Explainer  🔗              ║
║       AI x Web3 School — Week 1 Learning Tool       ║
╚══════════════════════════════════════════════════════╝{RESET}

  Type a {BOLD}concept name{RESET} to learn about it.
  Type {BOLD}list{RESET} to see all available concepts.
  Type {BOLD}help{RESET} for usage tips.
  Type {BOLD}quit{RESET} or press Ctrl+C to exit.

"""


def print_concept(concept_data):
    """Pretty-print a concept's explanation, example, and security tip."""
    d = concept_data
    print(f"\n{'─' * 56}")
    print(f"{BOLD}{CYAN}  📘  {d['name']}{RESET}")
    print(f"{'─' * 56}")
    print(f"\n{GREEN}{BOLD}  📖 Explanation:{RESET}")
    print(f"  {d['explanation']}")
    print(f"\n{YELLOW}{BOLD}  💡 Example:{RESET}")
    print(f"  {d['example']}")
    print(f"\n{RED}{BOLD}  🔒 Security Tip:{RESET}")
    print(f"  {d['security_tip']}")
    print(f"{'─' * 56}\n")


def print_list():
    """Print a numbered list of all available concepts."""
    print(f"\n{BOLD}{CYAN}  📋 Available Concepts:{RESET}\n")
    for i, (key, val) in enumerate(ALL_CONCEPTS.items(), 1):
        print(f"  {i:2d}. {val['name']:<30s}  {DIM}(try: {key}){RESET}")
    print(f"\n  {DIM}Total: {len(ALL_CONCEPTS)} concepts loaded{RESET}\n")


def print_help():
    """Print usage instructions."""
    print(f"""
{BOLD}{CYAN}  ❓ How to use this tool:{RESET}

  • Type a concept name (e.g., {BOLD}wallet{RESET}, {BOLD}gas{RESET}, {BOLD}defi{RESET})
  • Partial names work too — it will find the best match
  • Type {BOLD}list{RESET} to see all available concepts
  • Type {BOLD}list -v{RESET} or {BOLD}list --verbose{RESET} for one-line summaries
  • Type {BOLD}quit{RESET} or press {BOLD}Ctrl+C{RESET} to exit

  {DIM}Tip: Try asking about terms you've seen in Web3 articles!{RESET}
""")


def fuzzy_match(query):
    """Simple fuzzy matching: exact match → prefix match → substring match."""
    q = query.lower().strip()

    # Exact match
    if q in ALL_CONCEPTS:
        return ALL_CONCEPTS[q]

    # Check aliases
    aliases = {"private key": "private key", "privkey": "private key",
               "seed": "seed phrase", "mnemonic": "seed phrase",
               "gas fee": "gas", "fees": "gas",
               "contract": "smart contract", "sc": "smart contract",
               "explorer": "block explorer", "etherscan": "block explorer",
               "test": "testnet", "devnet": "testnet",
               "account": "account", "wallet": "wallet",
               "defi": "defi", "decentralized finance": "defi",
               "dapp": "dapp", "decentralized app": "dapp"}
    if q in aliases:
        return ALL_CONCEPTS[aliases[q]]

    # Prefix match
    for key, val in ALL_CONCEPTS.items():
        if key.startswith(q):
            return val

    # Substring match
    for key, val in ALL_CONCEPTS.items():
        if q in key or q in val["name"].lower():
            return val

    # Word-in-explanation match
    for key, val in ALL_CONCEPTS.items():
        if q in val["explanation"].lower():
            return val

    return None


def get_suggestions(query):
    """Return a list of concepts whose names partially match the query."""
    q = query.lower().strip()
    return [
        val["name"] for key, val in ALL_CONCEPTS.items()
        if q in key or q in val["name"].lower()
    ]


# ── Main Loop ───────────────────────────────────────────────────────────────

def main():
    print(BANNER)

    try:
        while True:
            try:
                user_input = input(f"{BOLD}{CYAN}🔗 web3 >{RESET} ").strip()
            except EOFError:
                break

            if not user_input:
                continue

            lower = user_input.lower()

            # Quit
            if lower in ("quit", "exit", "q", "bye"):
                print(f"\n{GREEN}  👋 Happy learning! See you next time.{RESET}\n")
                break

            # List
            if lower.startswith("list"):
                if "-v" in lower or "--verbose" in lower:
                    print(f"\n{BOLD}{CYAN}  📋 Concept Summaries:{RESET}\n")
                    for key, val in ALL_CONCEPTS.items():
                        short = val["explanation"][:80].rsplit(" ", 1)[0] + "..."
                        print(f"  • {val['name']:<30s} {DIM}{short}{RESET}")
                    print()
                else:
                    print_list()
                continue

            # Help
            if lower in ("help", "h", "?"):
                print_help()
                continue

            # Try to find the concept
            result = fuzzy_match(lower)

            if result:
                print_concept(result)
            else:
                suggestions = get_suggestions(lower)
                print(f"\n{RED}  ❌ Unknown concept: \"{user_input}\"{RESET}")
                if suggestions:
                    print(f"  {YELLOW}Did you mean one of these?{RESET}")
                    for s in suggestions:
                        print(f"    → {s}")
                else:
                    print(f"  {DIM}Type 'list' to see all available concepts.{RESET}")
                print()

    except KeyboardInterrupt:
        print(f"\n\n{GREEN}  👋 Goodbye! Keep exploring Web3!{RESET}\n")


if __name__ == "__main__":
    main()
