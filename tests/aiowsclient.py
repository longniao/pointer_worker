# -*- coding: utf-8 -*-

import asyncio
import logging
from datetime import datetime
from aiowebsocket.converses import AioWebSocket


async def startup(uri):
    async with AioWebSocket(uri) as aws:
        converse = aws.manipulator

        # 客户端给服务端发送消息
        await converse.send('{"id":956988,"method":"server.ping","params":[]}')
        #await converse.send('{"id":956988,"method":"depth.subscribe","params":["BTC_USDT",30,"0.01"]}')
        await converse.send('{"id":956988,"method":"trades.subscribe","params":["BTC_USDT"]}')
        #await converse.send('{"id":956988,"method":"price.subscribe","params":["BTC_USDT","BCH_USDT","ETH_USDT","ETC_USDT","QTUM_USDT","LTC_USDT","DASH_USDT","ZEC_USDT","BTM_USDT","EOS_USDT","REQ_USDT","SNT_USDT","OMG_USDT","PAY_USDT","CVC_USDT","ZRX_USDT","TNT_USDT","XMR_USDT","XRP_USDT","DOGE_USDT","BAT_USDT","PST_USDT","BTG_USDT","DPY_USDT","LRC_USDT","STORJ_USDT","RDN_USDT","STX_USDT","KNC_USDT","LINK_USDT","CDT_USDT","AE_USDT","RLC_USDT","RCN_USDT","TRX_USDT","KICK_USDT","VET_USDT","MCO_USDT","FUN_USDT","DATA_USDT","ZSC_USDT","MDA_USDT","XTZ_USDT","GNT_USDT","GEM_USDT","RFR_USDT","DADI_USDT","ABT_USDT","OST_USDT","XLM_USDT","MOBI_USDT","OCN_USDT","ZPT_USDT","COFI_USDT","JNT_USDT","BLZ_USDT","GXS_USDT","MTN_USDT","RUFF_USDT","TNC_USDT","ZIL_USDT","BTO_USDT","THETA_USDT","DDD_USDT","MKR_USDT","DAI_USDT","SMT_USDT","MDT_USDT","MANA_USDT","LUN_USDT","SALT_USDT","FUEL_USDT","ELF_USDT","DRGN_USDT","GTC_USDT","QLC_USDT","DBC_USDT","BNTY_USDT","LEND_USDT","ICX_USDT","BTF_USDT","ADA_USDT","LSK_USDT","WAVES_USDT","BIFI_USDT","MDS_USDT","DGD_USDT","QASH_USDT","POWR_USDT","FIL_USDT","BCD_USDT","SBTC_USDT","GOD_USDT","BCX_USDT","QSP_USDT","INK_USDT","MED_USDT","QBT_USDT","TSL_USDT","GNX_USDT","NEO_USDT","GAS_USDT","IOTA_USDT","NAS_USDT","OAX_USDT","BCDN_USDT","SNET_USDT","BTS_USDT","GT_USDT","ATOM_USDT","XEM_USDT","BU_USDT","BCHSV_USDT","DCR_USDT","BCN_USDT","XMC_USDT","PPS_USDT","ATP_USDT","NBOT_USDT","MEDX_USDT","GRIN_USDT","BEAM_USDT","BTT_USDT","TFUEL_USDT","CELR_USDT","CS_USDT","MAN_USDT","REM_USDT","LYM_USDT","ONG_USDT","ONT_USDT","BFT_USDT","IHT_USDT","SENC_USDT","TOMO_USDT","ELEC_USDT","HAV_USDT","SWTH_USDT","NKN_USDT","SOUL_USDT","LRN_USDT","EOSDAC_USDT","DOCK_USDT","GSE_USDT","RATING_USDT","HSC_USDT","HIT_USDT","DX_USDT","CNNS_USDT","DREP_USDT","MBL_USDT","GMAT_USDT","MIX_USDT","LAMB_USDT","LEO_USDT","WICC_USDT","SERO_USDT","VIDY_USDT","KGC_USDT","ARPA_USDT","ALGO_USDT","BKC_USDT","BXC_USDT","PAX_USDT","USDC_USDT","TUSD_USDT","HC_USDT","GARD_USDT","FTI_USDT","SOP_USDT","LEMO_USDT","QKC_USDT","IOTX_USDT","RED_USDT","LBA_USDT","OPEN_USDT","MITH_USDT","SKM_USDT","XVG_USDT","NANO_USDT","HT_USDT","BNB_USDT","MET_USDT","TCT_USDT","MXC_USDT"]}')
        #await converse.send('{"id":956988,"method":"kline.subscribe","params":["BTC_USDT",86400]}')

        while True:
            mes = await converse.receive()
            print('{time}-Client receive: {rec}'
                  .format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rec=mes))


if __name__ == '__main__':
    count = 0
    remote = 'wss://webws.gateio.live/v3/?v=972062'
    while True:
        try:
            asyncio.get_event_loop().run_until_complete(startup(remote))
            print('try')
        except KeyboardInterrupt as exc:
            print('KeyboardInterrupt')
            logging.info('Quit.')
            break
        except Exception as e:
            count += 1
            print(e, "Try again %s times..." % count)
            continue

