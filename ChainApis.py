'''
Dict of chains in the following format:

{
    "ticker": [
        "LCD endpoints for proposals",
        {
            "ping": "https://ping.pub/ticker/gov/",
            "mintscan": "https://mintscan.io/ticker/proposals/",
        },
        "@twitter"
    ]
}

Custom links will only be used if true in the GovBot file
'''

# Define custom explorer links, useful when a chain has its own proposals page
customExplorerLinks = {
    "dig": "https://app.digchain.org/proposals",
    "terra": "https://station.terra.money/proposal",
}

DAOs = { # Juno DAO_DAO Chains here
    "raw": {
        "name": "RAW DAO",
        "json": "https://www.rawdao.zone/_next/data/C_gSpGvAyha6p1tAPhVkh/vote", # get from inspect element on chain-website.xyz/vote (Will be like "2.json" name for example)
        "vote": "https://www.rawdao.zone/vote",
        "twitter": "@raw_dao",
    }
}

# Defined all info needed for given tickers. If only 1 explorer is found, that one will be used
# no matter what explorer is defined in GovBot
chainAPIs = {
    "dig": [ 
        'https://api-1-dig.notional.ventures/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/dig/gov',
        },
        "@dig_chain"
        ],
    'juno': [
        'https://lcd-juno.itastakers.com/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/juno/gov',
            "mintscan": 'https://www.mintscan.io/juno/proposals',
            "keplr": 'https://wallet.keplr.app/#/juno/governance?detailId='
        },
        "@JunoNetwork"
        ],
    'huahua': [
        'https://api.chihuahua.wtf/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/chihuahua/gov',
            "mintscan": 'https://www.mintscan.io/chihuahua/proposals',
        },
        "@ChihuahuaChain"
        ],
    'osmo': [
        'https://lcd-osmosis.blockapsis.com/cosmos/gov/v1beta1/proposals',
        {
            # "ping": 'https://ping.pub/osmosis/gov',
            "mintscan": 'https://www.mintscan.io/osmosis/proposals',
            "keplr": 'https://wallet.keplr.app/#/osmosis/governance?detailId='
        },
        '@osmosiszone'
        ],
    'atom': [
        'https://lcd-cosmoshub.blockapsis.com/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/cosmos/gov',
            "mintscan": 'https://www.mintscan.io/cosmos/proposals',
        },
        "@cosmos"
        ],
    'akt': [
        'https://akash.api.ping.pub/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/akash-network/gov',
            "mintscan": 'https://www.mintscan.io/akash/proposals',
            "keplr": 'https://wallet.keplr.app/#/akashnet/governance?detailId='
        },
        '@akashnet_'
        ],
    'stars': [
        "https://rest.stargaze-apis.com/cosmos/gov/v1beta1/proposals",
        {
            "ping": 'https://ping.pub/stargaze/gov',
            "keplr": 'https://wallet.keplr.app/#/stargaze/governance?detailId='
        },        
        '@StargazeZone'
        ],
    'kava': [
        'https://api.data.kava.io/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/kava/gov',
            "mintscan": 'https://www.mintscan.io/kava/proposals',
            "keplr": 'https://wallet.keplr.app/#/kava/governance?detailId='
        },        
        '@kava_platform'
        ],
    'like': [
        'https://mainnet-node.like.co/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/likecoin/gov',
        },        
        '@likecoin'
        ],
    'xprt': [
        'https://rest.core.persistence.one/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/persistence/gov',
            "mintscan": 'https://www.mintscan.io/persistence/proposals',
        },        
        '@PersistenceOne'
        ],
    'cmdx': [
        'https://rest.comdex.one/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/comdex/gov',
            "mintscan": 'https://www.mintscan.io/comdex/proposals',
        },        
        '@ComdexOfficial'
        ],
    "bcna": [ 
        'https://lcd.bitcanna.io/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/bitcanna/gov',
            "mintscan": 'https://www.mintscan.io/bitcanna/proposals',
        },        
        '@BitCannaGlobal'
        ],
    "btsg": [ 
        'https://lcd-bitsong.itastakers.com/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/bitsong/gov',
            "mintscan": 'https://www.mintscan.io/bitsong/proposals',
        },        
        '@BitSongOfficial'
        ],
    "band": [
        'https://laozi1.bandchain.org/api/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/band-protocol/gov',
            "mintscan": 'https://www.mintscan.io/akash/proposals',
        },        
        '@BandProtocol'
        ],
    "boot": [ # Bostrom
        'https://lcd.bostrom.cybernode.ai/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/bostrom/gov',
        },        
        ''
        ],
    "cheqd": [ 
        'https://api.cheqd.net/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/cheqd/gov',
        },        
        '@cheqd_io'
        ],
    "cro": [  
        'https://mainnet.crypto.org:1317/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/crypto-com-chain/gov',
            "mintscan": 'https://www.mintscan.io/crypto-org/proposals',
            "keplr": 'https://wallet.keplr.app/#/crypto-org/governance?detailId='
        },        
        '@cryptocom'
        ],
    "evmos": [  
        'https://rest.bd.evmos.org:1317/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/evmos/gov',
            "mintscan": 'https://www.mintscan.io/evmos/proposals',
            "keplr": 'https://wallet.keplr.app/#/evmos/governance?detailId='
        },        
        '@EvmosOrg'
        ],
    "fetch": [
        'https://rest-fetchhub.fetch.ai/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/fetchhub/gov',
            "mintscan": 'https://www.mintscan.io/fetchai/proposals',
        },        
        '@Fetch_ai'
        ],
    "grav": [  
        'https://gravitychain.io:1317/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/gravity-bridge/gov',
            "mintscan": 'https://www.mintscan.io/gravity-bridge/proposals',
            "keplr": 'https://wallet.keplr.app/#/gravity-bridge/governance?detailId='
        },        
        '@gravity_bridge'
        ],
    "inj": [  
        'https://public.lcd.injective.network/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/injective/gov',
            "mintscan": 'https://www.mintscan.io/injective/proposals',
        },        
        '@InjectiveLabs'
        ],
    "iris": [  
        'https://lcd-iris.keplr.app/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/iris-network/gov',
            "mintscan": 'https://www.mintscan.io/iris/proposals',
            "keplr": 'https://wallet.keplr.app/#/irishub/governance?detailId='
        },        
        '@irisnetwork'
        ],
    'iov': [ #Starname
        "https://lcd-iov.keplr.app/cosmos/gov/v1beta1/proposals",
        {
            "ping": 'https://ping.pub/starname/gov',
            "mintscan": 'https://www.mintscan.io/starname/proposals',
        },        
        '@starname_me'
        ],
    "lum": [  
        'https://node0.mainnet.lum.network/rest/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/lum-network/gov',
            "mintscan": 'https://www.mintscan.io/lum/proposals',
        },        
        '@lum_network'
        ],
    "regen": [  
        'https://regen.stakesystems.io/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/regen/gov',
            "mintscan": 'https://www.mintscan.io/regen/proposals',
            "keplr": 'https://wallet.keplr.app/#/regen/governance?detailId='
        },        
        '@regen_network'
        ],
    "hash": [  
        'https://api.provenance.io/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/provenance/gov',
        },        
        '@provenancefdn'
        ],
    "secret": [  
        'https://api.scrt.network/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/secret/gov',
            "mintscan": 'https://www.mintscan.io/secret/proposals',
            "keplr": 'https://wallet.keplr.app/#/secret/governance?detailId='
        },        
        '@SecretNetwork'
        ],
    "sent": [  
        'https://lcd-sentinel.keplr.app/cosmos/gov/v1beta1/proposals',        
        {
            "ping": 'https://ping.pub/sentinel/gov',
            "mintscan": 'https://www.mintscan.io/sentinel/proposals',
        },        
        '@Sentinel_co'
        ],
    "sif": [  
        'https://api.sifchain.finance:443/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/sifchain/gov',
            "mintscan": 'https://www.mintscan.io/sifchain/proposals',
            "keplr": 'https://wallet.keplr.app/#/sifchain/governance?detailId='
        },        
        "@sifchain"
        ],
    "terraC": [  
        'https://blockdaemon-terra-lcd.api.bdnodes.net:1317/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/terra-luna/gov',
        },        
        "@terraC_money"
        ],
    "terra": [  
        'https://phoenix-lcd.terra.dev/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/terra2/gov',
        },        
        "@terra_money"
        ],
    "umee": [  
        'https://api.blue.main.network.umee.cc/cosmos/gov/v1beta1/proposals',
        {
            "ping": 'https://ping.pub/umee/gov',
            "mintscan": 'https://www.mintscan.io/umee/proposals',
        },        
        "@Umee_CrossChain"
        ],
}