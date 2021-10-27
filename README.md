# Hackerlink Solana Vote Scraper

Change `Voteaccount` to scrap another voting acoount

You can visit Solana Explorer to find the voting acoount

This is the voting account for Scallop at Solana Ignition Hackathon East Asia 

https://explorer.solana.com/address/3rXHdF7CfwG6K2VVFpvBRwdbRwyR5Zn7kQhLgxn4mjk7

## How to use

 - Update

`ignition_update.py`

`ignition_addup.py`

`final_list.py`

And output is in `ignition_addup_final.txt`

 - Scrap it from 0 (Don't run it without you must to, it will take a long time!)

 `backup/ignition.py`

## RPC Node Rate Limits

https://api.mainnet-beta.solana.com - Solana-hosted api node cluster, backed by a load balancer; rate-limited

https://solana-api.projectserum.com - Project Serum-hosted api node

 - Maximum number of requests per 10 seconds per IP: 100
 - Maximum number of requests per 10 seconds per IP for a single RPC: 40
 - Maximum concurrent connections per IP: 40
 - Maximum connection rate per 10 seconds per IP: 40
 - Maximum amount of data per 30 second: 100 MB

## Improvement

 - We can use Solana Python SDK.
 - More efficient.
 - More readable.
 - We can use txt to store tx and no need to send many requests every time
