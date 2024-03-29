# coding:utf-8
#
# Copyright 2019-2029 shenzhen haibei Media .Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Pressure Indicators
压力型
@author Tab
"""
from ..base import *


def DDI(df, N=13, N1=26, M=1, M1=5):
    """
    方向标准离差指数 分析DDI柱状线，由红变绿(正变负)，卖出信号参考；由绿变红，买入信号参考。
    :param df:
    :param N:
    :param N1:
    :param M:
    :param M1:
    :return:
    """

    H = df['high']
    L = df['low']

    DMZ = IF((H + L) > (REF(H, 1) + REF(L, 1)), MAX(ABS(H - REF(H, 1)), ABS(L - REF(L, 1))), 0)
    DMF = IF((H + L) < (REF(H, 1) + REF(L, 1)), MAX(ABS(H - REF(H, 1)), ABS(L - REF(L, 1))), 0)
    DIZ = SUM(DMZ, N) / (SUM(DMZ, N) + SUM(DMF, N))
    DIF = SUM(DMF, N) / (SUM(DMF, N) + SUM(DMZ, N))

    DDI = DIZ - DIF
    ADDI = SMA(DDI, N1, M)
    AD = MA(ADDI, M1)
    return pd.DataFrame({'DDI': DDI, 'ADDI': ADDI, 'AD': AD})


def shadow(df):
    """
    上下影线指标
    :param df:
    :return:
    """
    return pd.DataFrame({
        'LOW': lower_shadow(df), 'UP': upper_shadow(df),
        'BODY': body(df), 'BODY_ABS': body_abs(df), 'PRICE_PCG': price_pcg(df)
    })
