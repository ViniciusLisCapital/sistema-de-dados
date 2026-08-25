"""Modelo agregado semiestrutural do BC (boxe RI jun/2024): estimacao, decomposicao,
cenarios.

## As equacoes, como publicadas

(1)  pi^L_t = a1L pi^L_{t-1} + a1I (sum_{i=1..4} pi^IPCA_{t-i})/4
              + (1 - a1L - a1I) pi^e_{t,t+4|t}/4 + a2 pi*_t + a3 De_hat_{t-1} + a4 h_t
              + [sum_{i=0..2}(a5 d^el + a6 d^la) Clima^2]/3
              - [sum_{i=3..5}(a5 d^el + a6 d^la) Clima^2]/3 + eps
(1.1) pi*_t = w_a pi*^agri + w_m pi*^metal + w_e pi*^energia,  w somando 1
(2)  h_t = b1 h_{t-1} - b2 r_hat_{t-1}/4 - b3 rp_hat_t + b4 h*_t + s^h_t + eps^cr08 + eps^cr20
(2.1) r_hat_t = i^e_{t,t+4|t} - pi^e_{t,t+4|t} - rr^IS_t
(2.2) s^h_t = b5 s^h_{t-1} + eps^h
(2.3) rr^IS_t = rr^trend_t + rr_hat^IS_t          rr^trend = tendencia HP do juro real Focus
(2.4) rr_hat^IS_t = rr_hat^IS_{t-1} + eps         passeio aleatorio
(3)  i_t = t1 i_{t-1} + t2 i_{t-2}
           + (1 - t1 - t2)[rr^taylor_t + pi^meta_t + t3(pi^e_{t,t+4|t} - pi^meta_t)] + eps
(3.1) rr^taylor_t = rr^trend_t + rr_hat^taylor_t   (mesma tendencia da IS, desvio proprio)
(4)  De_t = De^ppc_t - delta(i^dif_t - i^dif_{t-1}) + eps
(4.1) i^dif_t = i_t - (i*_t + CDS_t)
(4.2) De^ppc_t = (pi^meta_t - pi*^ss)/4            pi*^ss = 2%
(5)  pi^e_{t,t+4|t} = f1 pi^e_{t-1,t+3|t-1} + f2 E_t pi_{t,t+4}
                      + f3 sum_{i=1..4} pi^IPCA_{t-i} + (1-f1-f2-f3) pi^meta_t + eps
(6)-(9) fpib = h_t + sh e ; fnuci/gn = h_t + sh e ; femp/ge = h_{t-1} + sh e ;
        fcaged/gc = h_{t-1} + sh e

## O que esta e o que nao esta aqui

No filtro: (1), (2), (3), (4), (6)-(9). Fora do filtro, mas no simulador: (5).
Nao implementado: o termo b4 h*_t e o bloco de precos administrados.

A equacao (5) esta RESOLVIDA na simulacao e nao na estimacao, e a assimetria e
proposital. Num cenario os condicionantes exogenos sao dados por construcao, entao
`E_t pi_{t,t+4}` e a soma da propria trajetoria simulada quatro trimestres a frente:
um ponto fixo no CAMINHO, que `simular()` resolve por iteracao (ganho do laco ~0,1;
converge em ~10 passos ate 1e-11, e o residuo vem em `C.attrs`). No filtro o mesmo
objeto exigiria fixar o que o modelo espera de pi^A, pi*, De e rp em cada trimestre da
amostra -- convencao que o boxe nao publica e que moveria E_t pi mais do que os phi.
Enquanto isso pi^e entra como dado observado da Focus em (1), (2.1) e (3), que e o que
ele de fato e.

Os phi vem de `estimar_eq5()`, em dois passos (previsao do proprio modelo a partir do
estado FILTRADO, depois minimos quadrados restrito), nao do filtro -- por isso aparecem
na tabela de validacao com a coluna de metodo.

O hiato mundial (b4) foi excluido por decisao explicita: b4 = 0,054 com IC 90% de
[0; 0,23], o termo mais dispensavel da IS.

## Cenarios: o que o simulador faz e nao faz

Faz: dado um caminho de Selic, propaga (2.1) -> (2) -> (1) -> IPCA. O caminho de Selic
resolve de graca o `i^e_{t,t+4|t}` que estourou a replicacao antiga -- num cenario a
trajetoria e conhecida por construcao, entao a expectativa de juro e exata, sem curva
forward estimada. Com `expectativa="eq5"` a expectativa de inflacao tambem responde,
e com `cambio="uip"` o cambio responde ao diferencial de juros pela eq. (4) -- que
tambem nao tem ponto fixo, porque i* e o CDS ficam constantes.

Nao faz: precos administrados. pi^A segue premissa (meta/4), e e o que separa o nosso
IRF completo da primeira linha do C2 Boxe3 Graf 4B -- o BC simula "incorporando tambem
o modelo de precos administrados", cuja repasse cambial e o dobro do de livres. As tres
configuracoes do simulador batem nas tres colunas do Graf 4B nesta ordem:
so_demanda -> "Expectativa IPCA e cambio fixos"; +eq5 -> "Cambio fixo";
+eq5+uip -> modelo cheio. Ver `irf()` e `validar_irf()`.

Uso:
    from analytics.brasil.monetary_policy import modelo_agregado as M
    res = M.rodar()          # estima, extende os estados, decompoe, valida; grava data/
"""
from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import beta as beta_dist
from statsmodels.tsa.statespace.mlemodel import MLEModel

from analytics.brasil.monetary_policy import modelo_painel as MP

warnings.filterwarnings("ignore")

DATA = MP.DATA
PI_EXT = MP.PI_EXT

AMOSTRA = (pd.Period("2003Q4", "Q"), pd.Period("2023Q4", "Q"))
CR08 = ("2008Q4", "2009Q4")
CR20 = ("2020Q1", "2020Q4")
PHI_ALTA = ("2020Q2", "2022Q4")
OBS = ["fpib", "fnuci", "femp", "fcaged", "pi_L", "selic", "de"]
ESTADOS = ["h", "h_l1", "s_h", "rr_IS", "rr_TAY"]

# modas publicadas (C2 Boxe3 Tab 1) -- ponto de partida da otimizacao e alvo da validacao
BCB = dict(a1L=0.24, a1I=0.38, a2=0.023, a3=0.011, a4=0.120, a5=0.0012, a6=0.0007,
           b1=0.85, b2=0.44, b3=0.030, b5=0.84, t1=1.48, t2=-0.58, t3=2.03,
           delta=1.90, gn=1.87, ge=1.10, gc=0.69, sh=1.09)
# intervalos de credibilidade de 90% publicados, para a tabela de validacao
BCB_IC = dict(a1L=(0.02, 0.38), a1I=(0.13, 0.69), a2=(0.006, 0.039), a3=(0.0, 0.025),
              a4=(0.072, 0.198), a5=(0.0004, 0.0019), a6=(0.0, 0.0021),
              b1=(0.70, 0.95), b2=(0.21, 0.66), b3=(0.027, 0.032), b5=(0.59, 0.99),
              t1=(1.41, 1.54), t2=(-0.63, -0.52), t3=(1.47, 2.64), delta=(0.77, 3.22),
              gn=(1.65, 2.12), ge=(0.96, 1.25), gc=(0.61, 0.79), sh=(0.98, 1.21))
# eq. (5) -- bloco "Expectativas de inflacao" da mesma tabela publicada. f2 = 0,11
# e o peso da expectativa consistente com o modelo: e ele que faz o ganho do laco de
# ponto fixo ser pequeno, e por isso a iteracao do simulador converge sem amortecimento.
PHI = dict(f1=0.75, f2=0.11, f3=0.021)
PHI_IC = dict(f1=(0.68, 0.82), f2=(0.06, 0.13), f3=(0.0, 0.049))

DESC = dict(a1L="Inercia da inflacao de livres", a1I="Inercia da inflacao IPCA",
            a2="Inflacao importada", a3="Variacao do cambio", a4="Hiato do produto",
            a5="Anomalia climatica, El Nino", a6="Anomalia climatica, La Nina",
            b1="Autorregressivo da IS", b2="Juro real", b3="Resultado primario",
            b5="Autorregressivo do choque da IS",
            t1="Suavizacao dos juros, 1a defasagem",
            t2="Suavizacao dos juros, 2a defasagem",
            t3="Desvio da expectativa em relacao a meta",
            delta="Diferencial de juros interna e externa",
            gn="Proporcionalidade da Nuci", ge="Proporcionalidade do emprego",
            gc="Proporcionalidade do Caged", sh="Desvio padrao do erro de mensuracao",
            f1="Inercia das expectativas", f2="Expectativa consistente com o modelo",
            f3="Inflacao passada nas expectativas")

NOMES = ["a1L", "a1I", "a2", "a3", "a4", "a5", "a6", "b1", "b2", "b3", "b5",
         "t1", "t2", "t3", "delta", "gn", "ge", "gc", "sh",
         "s_h", "k08", "k20", "s_pi", "k_pi", "s_i", "s_e"]
# caixa = suporte das prioris uniformes do boxe; as variancias, positivas
CAIXA = dict(a1L=(0, 1), a1I=(0, 1), a2=(0, 1), a3=(0, 1), a4=(0, 1),
             a5=(0, 0.01), a6=(0, 0.01), b1=(0, 1), b2=(0, 1), b3=(1e-4, 1), b5=(0, 1),
             t1=(0, 2), t2=(-1, 1), t3=(0, 4), delta=(0, 10),
             gn=(1e-3, 3), ge=(1e-3, 3), gc=(1e-3, 3), sh=(1e-3, 2),
             s_h=(1e-3, 10), k08=(0, 20), k20=(0, 20), s_pi=(1e-3, 10), k_pi=(0, 20),
             s_i=(1e-3, 10), s_e=(1e-2, 40))
INI_VAR = dict(s_h=0.6, k08=2.0, k20=4.0, s_pi=0.35, k_pi=2.0, s_i=0.8, s_e=6.0)

# Beta(media 0,03; sd 0,002) do boxe -- a unica priori informativa, reparametrizada
_m, _v = 0.03, 0.002 ** 2
_kk = _m * (1 - _m) / _v - 1
B3_A, B3_B = _m * _kk, (1 - _m) * _kk


FOLGA = 40        # buffer alem do horizonte reportado, para os leads da eq. (5).
                  # Calibrado: a condicao terminal (IPCA constante depois do buffer)
                  # influencia para tras, e a 40 o efeito no trecho reportado cai a
                  # 5e-10 -- contra 7e-05 a 16 e 1e-06 a 24.


def _janela(idx, ini, fim):
    return ((idx >= pd.Period(ini, "Q")) & (idx <= pd.Period(fim, "Q"))).astype(float)


def _em(s: pd.Series, t0: pd.Period) -> float:
    """Valor da serie em t0; se faltar, o ultimo valido ATE t0.

    O simulador partia sempre do fim da amostra, e por isso lia varios condicionantes
    com `.iloc[-1]`. `estimar_eq5()` simula a partir de cada trimestre do historico,
    onde `.iloc[-1]` seria o futuro -- daqui em diante tudo e lido em t0.
    """
    if t0 in s.index:
        v = s.loc[t0]
        v = float(v.iloc[0]) if hasattr(v, "iloc") else float(v)
        if np.isfinite(v):
            return v
    d = s[s.index <= t0].dropna()
    return float(d.iloc[-1]) if len(d) else 0.0


class Agregado(MLEModel):
    """Forma de espaco de estados com x_t = [h_t, h_{t-1}, s^h_t, rr_IS_t, rr_TAY_t]."""

    # Se um regressor exigido faltar em t, a observacao vira FALTANTE e o filtro pula.
    # Sem isso, uma defasagem ausente no inicio da amostra gera residuo artificial
    # contra intercepto zero -- na Taylor isso chega a +18 p.p. e o filtro despeja em
    # rr_TAY, que nao volta porque sigma(eps_rr) e calibrado pequeno. E o que tambem
    # mantem a UIP genuinamente inativa antes de 2008T1 (o CDS comeca ali).
    EXIGE = {"pi_L": ["piL_l1", "ma4", "pie", "pistar", "deh_l1", "Zel", "Yla"],
             "selic": ["sel_l1", "sel_l2", "rrtr", "meta", "pie"],
             "de": ["meta", "didif"]}

    @staticmethod
    def exog(P: pd.DataFrame) -> dict:
        return dict(
            piL_l1=P["pi_L"].shift(1).values,
            ma4=P["pi_IPCA"].shift(1).rolling(4).mean().values,
            pie=P["pi_e"].values, pistar=P["pi_star"].values,
            deh_l1=P["de_hat"].shift(1).values,
            Zel=P["Zel"].values, Yla=P["Yla"].values,
            hpc_l1=P["hp_ciclo"].shift(1).values, rp=P["rp_hat"].values,
            sel_l1=P["selic"].shift(1).values, sel_l2=P["selic"].shift(2).values,
            rrtr=P["rr_trend"].values, meta=P["meta"].values,
            didif=(P["i_dif"] - P["i_dif"].shift(1)).values,
        )

    def __init__(self, P: pd.DataFrame, sigma_rr: float, burn_ate: pd.Period | None = None):
        y = P[OBS].astype(float).values.copy()
        x = self.exog(P)
        for eq, req in self.EXIGE.items():
            ruim = np.zeros(len(P), bool)
            for k in req:
                ruim |= ~np.isfinite(x[k])
            y[ruim, OBS.index(eq)] = np.nan
        # Prior propria, nao difusa: com variancia inicial de 1e6 o filtro usa os
        # primeiros trimestres para fixar rr_TAY num nivel arbitrario do qual nao sai.
        # sd de 2 p.p. para o desvio de r* da tendencia, 3 p.p. para o hiato.
        super().__init__(y, k_states=5, k_posdef=5, initialization="known",
                         initial_state=np.zeros(5),
                         initial_state_cov=np.diag([9.0, 9.0, 4.0, 4.0, 4.0]))
        self.Pn, self.x, self.sigma_rr = P, x, sigma_rr
        n, idx = self.nobs, P.index
        self.d08, self.d20 = _janela(idx, *CR08), _janela(idx, *CR20)
        self.dpi = _janela(idx, *PHI_ALTA)
        alvo = AMOSTRA[0] if burn_ate is None else burn_ate
        self.loglikelihood_burn = int((idx < alvo).sum())

        self["selection"] = np.zeros((5, 5))
        for i, j in ((0, 0), (0, 1), (0, 2), (2, 0), (3, 3), (4, 4)):
            self["selection"][i, j] = 1.0
        self["transition"] = np.zeros((5, 5))
        self["transition"][1, 0] = 1.0
        self["transition"][3, 3] = 1.0
        self["transition"][4, 4] = 1.0
        self["design"] = np.zeros((7, 5))
        self["obs_cov"] = np.zeros((7, 7, n))
        self["state_cov"] = np.zeros((5, 5, n))
        self["obs_intercept"] = np.zeros((7, n))
        self["state_intercept"] = np.zeros((5, n))

    @property
    def param_names(self):
        return NOMES

    @property
    def start_params(self):
        return np.array([BCB.get(k, INI_VAR.get(k)) for k in NOMES], float)

    def update(self, params, **kw):
        params = super().update(params, **kw)
        p = dict(zip(NOMES, params))
        x = self.x

        T = self["transition"]
        T[0, 0], T[0, 2], T[0, 3] = p["b1"], p["b5"], p["b2"] / 4.0
        T[2, 2] = p["b5"]
        self["state_intercept"][0] = np.nan_to_num(
            -(p["b2"] / 4.0) * x["hpc_l1"] - p["b3"] * x["rp"])

        Q = self["state_cov"]
        Q[0, 0, :] = p["s_h"] ** 2
        Q[1, 1, :] = (p["k08"] * p["s_h"]) ** 2 * self.d08
        Q[2, 2, :] = (p["k20"] * p["s_h"]) ** 2 * self.d20
        Q[3, 3, :] = Q[4, 4, :] = self.sigma_rr ** 2

        Z = self["design"]
        Z[0, 0], Z[1, 0], Z[2, 1], Z[3, 1] = 1.0, p["gn"], p["ge"], p["gc"]
        Z[4, 0] = p["a4"]
        Z[5, 4] = 1.0 - p["t1"] - p["t2"]

        d = self["obs_intercept"]
        d[4] = np.nan_to_num(
            p["a1L"] * x["piL_l1"] + p["a1I"] * x["ma4"]
            + (1 - p["a1L"] - p["a1I"]) * x["pie"] / 4.0 + p["a2"] * x["pistar"]
            + p["a3"] * x["deh_l1"] + p["a5"] * x["Zel"] + p["a6"] * x["Yla"])
        d[5] = np.nan_to_num(
            p["t1"] * x["sel_l1"] + p["t2"] * x["sel_l2"]
            + (1 - p["t1"] - p["t2"]) * (x["rrtr"] + x["meta"]
                                         + p["t3"] * (x["pie"] - x["meta"])))
        d[6] = np.nan_to_num((x["meta"] - PI_EXT) / 4.0 - p["delta"] * x["didif"])

        H = self["obs_cov"]
        vh = p["sh"] ** 2
        H[0, 0, :], H[1, 1, :] = vh, (p["gn"] ** 2) * vh
        H[2, 2, :], H[3, 3, :] = (p["ge"] ** 2) * vh, (p["gc"] ** 2) * vh
        H[4, 4, :] = p["s_pi"] ** 2 * (1.0 + (p["k_pi"] ** 2 - 1.0) * self.dpi)
        H[5, 5, :], H[6, 6, :] = p["s_i"] ** 2, p["s_e"] ** 2


# ── estimacao ────────────────────────────────────────────────────────────────
def _neg_logpost(v, mod):
    p = dict(zip(NOMES, v))
    if p["a1L"] + p["a1I"] >= 1.0 or p["t1"] + p["t2"] >= 1.0:
        return 1e10                       # pesos implicitos precisam ser positivos
    try:
        ll = mod.loglike(np.asarray(v, float))
    except Exception:
        return 1e10
    if not np.isfinite(ll):
        return 1e10
    lp = beta_dist.logpdf(p["b3"], B3_A, B3_B)
    return -(ll + (lp if np.isfinite(lp) else -1e10))


def estimar(P: pd.DataFrame, sigma_rr: float, n_partidas: int = 6,
            verbose: bool = True) -> tuple[dict, float]:
    """Moda a posteriori. Prioris uniformes = caixa; a Beta de b3 = penalidade."""
    P = P.loc[:AMOSTRA[1]]
    mod = Agregado(P, sigma_rr)
    v0 = mod.start_params
    bnds = [CAIXA[k] for k in NOMES]
    rng = np.random.default_rng(11)
    melhor = None
    for k in range(n_partidas):
        v = v0.copy()
        if k:
            v = np.clip(v0 * np.exp(rng.normal(0, 0.25, len(v0))),
                        [b[0] for b in bnds], [b[1] for b in bnds])
            v[NOMES.index("t2")] = BCB["t2"] * np.exp(rng.normal(0, 0.1))
        r = minimize(_neg_logpost, v, args=(mod,), method="L-BFGS-B", bounds=bnds,
                     options=dict(maxiter=4000, maxfun=40000, ftol=1e-10, gtol=1e-7))
        if melhor is None or r.fun < melhor.fun:
            melhor = r
        if verbose:
            print("    partida %d: -logpost %.4f%s" % (k, r.fun, "  <<" if melhor is r else ""))
    par = dict(zip(NOMES, map(float, melhor.x)))
    par["_logL"] = float(mod.loglike(melhor.x))
    par["_logL_bcb"] = float(mod.loglike(v0))
    par["_sigma_rr"] = float(sigma_rr)
    return par, melhor.fun


def estados(P: pd.DataFrame, par: dict, burn_ate: pd.Period | None = None,
            filtrado: bool = False) -> pd.DataFrame:
    """Estados suavizados. Com o painel `full` e os parametros congelados, estende ate hoje.

    `filtrado=True` devolve o estado filtrado, que e o que existe em tempo real -- e o
    que `estimar_eq5()` usa, para a previsao do passo 1 nao olhar o futuro.
    """
    mod = Agregado(P, par["_sigma_rr"], burn_ate=burn_ate)
    res = mod.smooth(np.array([par[k] for k in NOMES], float))
    X = res.filtered_state if filtrado else res.smoothed_state
    S = pd.DataFrame(X.T, index=P.index, columns=ESTADOS)
    S["rr_IS_total"] = P["rr_trend"] + S["rr_IS"]
    S["rr_TAY_total"] = P["rr_trend"] + S["rr_TAY"]
    S["r_hat"] = P["hp_ciclo"] - S["rr_IS"]      # hiato de juro real, eq. (2.1)
    return S


# ── decomposicoes ────────────────────────────────────────────────────────────
def decompor_phillips(P: pd.DataFrame, par: dict, S: pd.DataFrame) -> pd.DataFrame:
    """Contribuicoes da eq. (1) para pi^L. Somam pi^L exatamente, por construcao."""
    x = Agregado.exog(P)
    w = 1 - par["a1L"] - par["a1I"]
    D = pd.DataFrame(index=P.index)
    D["inercia_livres"] = par["a1L"] * x["piL_l1"]
    D["inercia_ipca"] = par["a1I"] * x["ma4"]
    D["expectativa"] = w * x["pie"] / 4.0
    D["commodities"] = par["a2"] * x["pistar"]
    D["cambio"] = par["a3"] * x["deh_l1"]
    D["hiato"] = par["a4"] * S["h"].values
    D["clima"] = par["a5"] * x["Zel"] + par["a6"] * x["Yla"]
    D["total"] = P["pi_L"].values
    D["residuo"] = D["total"] - D.drop(columns=["total"]).sum(axis=1)
    return D


def decompor_hiato(P: pd.DataFrame, par: dict, S: pd.DataFrame) -> pd.DataFrame:
    """Contribuicoes da eq. (2) para h. `politica_monetaria` = -(b2/4) r_hat_{t-1}.

    O termo de politica e aberto em dois: o juro observado contra a tendencia de r* e
    o desvio de r* em relacao a essa tendencia. Somados dao a contribuicao total, e
    separados mostram quanto do aperto medido vem da premissa de neutro.
    """
    x = Agregado.exog(P)
    D = pd.DataFrame(index=P.index)
    D["inercia"] = par["b1"] * S["h_l1"].values
    D["mp_juro"] = -(par["b2"] / 4.0) * x["hpc_l1"]
    D["mp_neutro"] = (par["b2"] / 4.0) * S["rr_IS"].shift(1).values
    D["politica_monetaria"] = D["mp_juro"] + D["mp_neutro"]
    D["fiscal"] = -par["b3"] * x["rp"]
    D["choque_persistente"] = S["s_h"].values
    D["total"] = S["h"].values
    D["residuo"] = D["total"] - D[["inercia", "politica_monetaria", "fiscal",
                                   "choque_persistente"]].sum(axis=1)
    return D


def decompor_taylor(P: pd.DataFrame, par: dict, S: pd.DataFrame) -> pd.DataFrame:
    """Contribuicoes da eq. (3) para a Selic."""
    x = Agregado.exog(P)
    w = 1 - par["t1"] - par["t2"]
    D = pd.DataFrame(index=P.index)
    D["persistencia"] = par["t1"] * x["sel_l1"] + par["t2"] * x["sel_l2"]
    D["ancora_real"] = w * S["rr_TAY_total"].values
    D["meta"] = w * x["meta"]
    D["desvio_expectativa"] = w * par["t3"] * (x["pie"] - x["meta"])
    D["total"] = P["selic"].values
    D["residuo"] = D["total"] - D.drop(columns=["total"]).sum(axis=1)
    return D


# ── cenarios ─────────────────────────────────────────────────────────────────
def simular(P: pd.DataFrame, par: dict, S: pd.DataFrame, n: int = 16, *,
            selic=None, pi_e=None, pi_A=None, de=None, pi_star=None, rp=None,
            clima: bool = False, w_ipca=(0.7672, 0.2328), t0=None,
            expectativa: str = "premissa", cambio: str = "premissa", phi=None,
            folga: int = FOLGA, tol: float = 1e-9) -> pd.DataFrame:
    """Propaga (2.1) -> (2) -> (1) -> IPCA por `n` trimestres a partir de t0.

    Cada condicionante aceita um escalar (constante), um array (prolongado pelo ultimo
    valor se for mais curto que o horizonte interno), ou None (default). Defaults, todos
    lidos EM t0: Selic no ultimo valor observado; pi^e no ultimo valor da Focus; pi^A na
    meta/4; De no valor de PPC (cambio neutro); pi* em zero; rp no ultimo valor; clima
    nulo.

    `i^e_{t,t+4|t}` sai do PROPRIO caminho de Selic quatro trimestres a frente -- num
    cenario a trajetoria e conhecida, entao a expectativa de juro e exata. E a correcao
    da lacuna que fazia o IRF da replicacao antiga sair 4-5x grande demais.

    `expectativa`:
      "premissa"  pi^e segue o argumento `pi_e`. Nao reage ao cenario.
      "eq5"       pi^e resolve a eq. (5), com `E_t pi_{t,t+4}` igual a soma dos quatro
                  trimestres seguintes da PROPRIA simulacao -- um ponto fixo no caminho,
                  resolvido de forma EXATA (ver abaixo). `pi_e` deixa de ser usado.
                  Residuo e condicionamento ficam em `C.attrs`.

    `cambio`:
      "premissa"  De segue o argumento `de` (default: PPC, cambio neutro).
      "uip"       De responde ao caminho de juros pela eq. (4), com i* e CDS constantes.
                  Nao ha ponto fixo aqui: o diferencial se move so pela Selic, que e
                  dada.

    Como o modelo e linear, `T(pi^e) = eq5(ipca(pi^e))` e AFIM: T(v) = G v + g. A eq.
    (5) e portanto o sistema linear (I - G) pi^e = g, montado coluna a coluna e resolvido
    de uma vez, em vez de iterado. Custa `n+folga` propagacoes (menos que a iteracao,
    que precisava de ~100 com o f2 estimado) e nao tem tolerancia de que depender: o
    residuo sai em 1e-14 em vez de 1e-11.

    O raio espectral de G e o teste de estabilidade, e ele e real: com o f2 daqui fica em
    0,68, mas passa de 1 em f2 = 0,32 e ai a solucao deixa de ser unica --
    dobrar `folga` muda a resposta em p.p. inteiros, porque a condicao terminal e que
    passa a determina-la. Por isso o solve levanta erro quando o raio cruza 1: resolver
    o sistema evita a tolerancia da iteracao, nao amplia a regiao valida.

    Reconciliacao com a tentativa anterior neste projeto, onde "Fair-Taylor divergiu":
    aquele motor aproximava a Selic esperada pela corrente, o que inflava o proprio laco
    (e o IRF, 4-5x) -- com `i^e` lido do caminho de juros o raio cai para 0,76 e a
    iteracao converge. Era consequencia do bug de i^e, nao instabilidade do modelo.

    O horizonte interno e `n + folga`: a eq. (5) precisa de quatro trimestres a frente
    de cada trimestre reportado, e os condicionantes seguem constantes depois de `n`.
    Com expectativa exogena a recursao e causal e estender o horizonte NAO altera as `n`
    primeiras linhas; com a eq. (5) a condicao terminal (IPCA constante depois do
    horizonte interno) influencia para tras, e o default de `folga` foi calibrado para
    essa influencia ficar abaixo de 1e-9 no trecho reportado.

    Fica fora: precos administrados. pi^A e premissa, e e o que separa este simulador
    do modelo cheio do BC -- ver `irf()`.
    """
    if expectativa not in ("premissa", "eq5"):
        raise ValueError("expectativa: 'premissa' ou 'eq5', nao %r" % expectativa)
    if cambio not in ("premissa", "uip"):
        raise ValueError("cambio: 'premissa' ou 'uip', nao %r" % cambio)

    obs = P[["pi_L", "pi_IPCA", "selic", "pi_e", "meta"]].dropna(subset=["pi_L", "selic"])
    t0 = obs.index.max() if t0 is None else pd.Period(t0, "Q")
    nn = n + max(int(folga), 8)
    idx_t = pd.period_range(t0 + 1, periods=nn, freq="Q")

    def vec(v, default):
        if v is None:
            v = default
        if np.isscalar(v):
            return np.full(nn, float(v))
        v = np.asarray(v, float)
        return v[:nn] if len(v) >= nn else np.r_[v, np.full(nn - len(v), v[-1])]

    meta = P["meta"].reindex(idx_t).ffill()
    meta = meta.fillna(_em(P["meta"], t0)).values
    de_ppc = (meta - PI_EXT) / 4.0

    i0 = _em(P["selic"], t0)
    i_path = vec(selic, i0)
    pie_prem = vec(pi_e, _em(P["pi_e"], t0))
    piA_p = vec(pi_A, 0.0) if pi_A is not None else meta / 4.0
    pis_p = vec(pi_star, 0.0)
    rp_p = vec(rp, _em(P["rp_hat"], t0))
    Z_p = np.zeros(nn) if not clima else P["Zel"].reindex(idx_t).fillna(0.0).values
    Y_p = np.zeros(nn) if not clima else P["Yla"].reindex(idx_t).fillna(0.0).values
    if cambio == "uip":
        de_p = de_ppc - par["delta"] * np.diff(np.r_[i0, i_path])
    else:
        de_p = vec(de, 0.0) if de is not None else de_ppc.copy()

    # estado inicial e historico necessario as defasagens, tudo lido EM t0
    h0, sh0 = _em(S["h"], t0), _em(S["s_h"], t0)
    rr_fix = _em(P["rr_trend"], t0) + _em(S["rr_IS"], t0)   # r* segue passeio aleatorio
    rhat0 = _em(S["r_hat"], t0)
    piL0 = _em(P["pi_L"], t0)
    pie0 = _em(P["pi_e"], t0)
    ipca0 = list(P["pi_IPCA"][P["pi_IPCA"].index <= t0].dropna().iloc[-4:].values)
    dehat0 = _em(P["de_hat"], t0)
    wL, wA = w_ipca
    COLS = ["selic", "i_e", "r_hat", "h", "s_h", "pi_L", "pi_IPCA", "de", "de_hat"]
    J = {c: i for i, c in enumerate(COLS)}

    def _prop(pie):
        h_l, sh_l, piL_l, rhat_l, dehat_l = h0, sh0, piL0, rhat0, dehat0
        hist = list(ipca0)
        o = np.empty((nn, len(COLS)))
        for k in range(nn):
            i_e = i_path[min(k + 4, nn - 1)]
            r_hat = i_e - pie[k] - rr_fix
            sh = par["b5"] * sh_l
            h = (par["b1"] * h_l - (par["b2"] / 4.0) * rhat_l
                 - par["b3"] * rp_p[k] + sh)
            piL = (par["a1L"] * piL_l + par["a1I"] * float(np.mean(hist[-4:]))
                   + (1 - par["a1L"] - par["a1I"]) * pie[k] / 4.0
                   + par["a2"] * pis_p[k] + par["a3"] * dehat_l + par["a4"] * h
                   + par["a5"] * Z_p[k] + par["a6"] * Y_p[k])
            ipca = wL * piL + wA * piA_p[k]
            o[k] = (i_path[k], i_e, r_hat, h, sh, piL, ipca, de_p[k], de_p[k] - de_ppc[k])
            h_l, sh_l, piL_l, rhat_l = h, sh, piL, r_hat
            dehat_l = de_p[k] - de_ppc[k]
            hist.append(ipca)
        return o

    f = dict(PHI) if phi is None else {k: float(phi[k]) for k in ("f1", "f2", "f3")}
    w_meta = 1.0 - f["f1"] - f["f2"] - f["f3"]

    def _eq5(ipca):
        """pi^e pela eq. (5), com E_t pi_{t,t+4} = soma dos 4 trimestres seguintes."""
        ac = np.r_[ipca, np.full(4, ipca[-1])]
        hist, out, ant = list(ipca0), np.empty(nn), pie0
        for k in range(nn):
            out[k] = (f["f1"] * ant + f["f2"] * ac[k + 1:k + 5].sum()
                      + f["f3"] * sum(hist[-4:]) + w_meta * meta[k])
            ant = out[k]
            hist.append(ipca[k])
        return out

    info = {}
    if expectativa == "premissa":
        pie, o = pie_prem, _prop(pie_prem)
    else:
        def T(v):
            return _eq5(_prop(v)[:, J["pi_IPCA"]])

        g = T(np.zeros(nn))
        G = np.empty((nn, nn))
        e = np.zeros(nn)
        for j in range(nn):
            e[j] = 1.0
            G[:, j] = T(e) - g
            e[j] = 0.0
        raio = float(np.abs(np.linalg.eigvals(G)).max())
        if not np.isfinite(raio) or raio > 0.999:
            raise RuntimeError(
                "eq. (5) fora da regiao de estabilidade: raio espectral de G = %.4f. "
                "Acima de 1 a solucao passa a depender da condicao terminal (dobrar "
                "`folga` muda a resposta em p.p. inteiros), entao nao existe caminho "
                "de expectativa bem definido para este phi." % raio)
        M_ = np.eye(nn) - G
        cond = float(np.linalg.cond(M_))
        pie = np.linalg.solve(M_, g)
        resid = float(np.abs(T(pie) - pie).max())
        if resid > tol:
            raise RuntimeError("eq. (5) resolvida com residuo %.3e (> %.1e)" % (resid, tol))
        o = _prop(pie)
        info = dict(eq5_resid=resid, eq5_cond=cond, eq5_raio=raio, phi=f)

    C = pd.DataFrame(o[:n], index=idx_t[:n], columns=COLS)
    C["pi_e"] = pie[:n]
    C["pi_A"] = piA_p[:n]
    C["rr_IS_total"] = rr_fix
    # IPCA acumulado em 4 trimestres, emendando os 3 ultimos observados
    hist3 = list(P["pi_IPCA"][P["pi_IPCA"].index <= t0].dropna().iloc[-3:].values)
    acum = hist3 + list(o[:, J["pi_IPCA"]])
    C["ipca_4t"] = [sum(acum[i:i + 4]) for i in range(n)]
    C.attrs.update(info)
    return C


def estimar_eq5(P: pd.DataFrame, par: dict, S: pd.DataFrame | None = None,
                amostra=AMOSTRA, verbose: bool = True) -> tuple[dict, dict]:
    """Estima f1, f2, f3 da eq. (5) por minimos quadrados nao lineares.

    O BC estima os phi DENTRO do filtro, junto com o resto. Aqui a eq. (5) e estimada
    a parte, e o cuidado que domina o desenho e nao criar simultaneidade: se a previsao
    `E_t pi_{t,t+4}` for construida condicionando no pi^e OBSERVADO em t, ela herda o
    proprio regressando (pi^e entra na Phillips com peso 1-a1L-a1I ~ 0,69) e f2 sai
    inflado. Medido: com aquela convencao f2 dava 0,42; com esta, o valor abaixo.

    A previsao para o trimestre t e, por isso, ancorada no conjunto de informacao de
    t-1: simula o modelo a partir de t-1 com o estado FILTRADO ali (o que existe em
    tempo real) e com a propria eq. (5) resolvida ao longo do caminho, de forma que
    pi^e_t seja GERADO pelo modelo e nao condicionado no observado. O residuo e um erro
    de previsao genuino. A coincidencia de timing e a favor: a Focus divulgada para o
    trimestre t e coletada com dado que vai ate t-1.

    Condicionantes exogenos na convencao "sem novidade": Selic e rp no valor de t-1,
    pi* em zero e De no PPC (que sao os pontos de partida do modelo para taxas de
    variacao). E o unico lugar onde uma convencao nao publicada entra.

    Um phi que leve o raio espectral de G acima de 1 faz `simular` levantar erro e o
    objetivo devolver penalidade, entao a regiao de estabilidade de expectativas racionais
    e imposta de graca. Ela fica em f2 = 0,32, e o f2 estimado abaixo esta
    dentro mas nao longe -- e um resultado a reportar, nao um detalhe numerico.
    """
    if S is None:
        S = estados(P, par, filtrado=True)
    ini, fim = amostra
    alvo = []
    for t in P.index[(P.index >= ini) & (P.index <= fim)]:
        pie_t = P["pi_e"].get(t, np.nan)
        if np.isfinite(pie_t) and np.isfinite(P["pi_e"].shift(1).get(t, np.nan)):
            alvo.append((t - 1, float(pie_t)))
    t_ant = [t for t, _ in alvo]
    y = np.array([v for _, v in alvo])

    def prever(v):
        f = dict(zip(("f1", "f2", "f3"), v))
        out = np.empty(len(t_ant))
        for i, t in enumerate(t_ant):
            C = simular(P, par, S, n=1, t0=t, expectativa="eq5", phi=f, folga=24)
            out[i] = C["pi_e"].iloc[0]
        return out

    def sse(v):
        if v.sum() > 1.0 or (v < 0).any():
            return 1e12
        try:
            return float(((y - prever(v)) ** 2).sum())
        except RuntimeError:                  # ponto fixo divergiu: phi instavel
            return 1e12

    r = minimize(sse, np.array([PHI["f1"], PHI["f2"], PHI["f3"]]), method="SLSQP",
                 bounds=[(0.0, 1.0)] * 3,
                 constraints=[dict(type="ineq", fun=lambda v: 1.0 - v.sum())],
                 options=dict(maxiter=200, ftol=1e-10))
    phi = dict(zip(("f1", "f2", "f3"), map(float, r.x)))
    res = y - prever(r.x)
    r2 = 1.0 - float((res ** 2).sum()) / float(((y - y.mean()) ** 2).sum())
    info = dict(n=int(len(y)), r2=r2, rmse=float(np.sqrt((res ** 2).mean())),
                w_meta=float(1.0 - sum(phi.values())),
                dentro={k: bool(PHI_IC[k][0] <= phi[k] <= PHI_IC[k][1]) for k in phi})
    if verbose:
        print("  eq. (5), MQ nao linear (n=%d, R2=%.4f, rmse %.3f p.p.):"
              % (info["n"], r2, info["rmse"]))
        for k in ("f1", "f2", "f3"):
            print("    %s = %.4f  (BC %.4f, IC [%.3f; %.3f]) %s"
                  % (k, phi[k], PHI[k], *PHI_IC[k],
                     "dentro" if info["dentro"][k] else "FORA"))
        print("    peso da meta = %.4f  (BC %.4f)"
              % (info["w_meta"], 1 - sum(PHI.values())))
    return phi, info


def caminho_selic_focus(P: pd.DataFrame, n: int) -> np.ndarray:
    """Trajetoria de Selic implicita na ultima pesquisa Focus, trimestre a trimestre."""
    obs = P[["selic"]].dropna()
    t0 = obs.index.max()
    g = MP._ultima_curva(t0)
    S = g[g["indicador"] == "Selic"].sort_values("h")
    i0 = float(obs["selic"].iloc[-1])
    if S.empty:
        return np.full(n, i0)
    hs = np.r_[0.0, S["h"].values]
    vs = np.r_[i0, S["mediana"].values]
    alvo = np.array([(k + 1) / 4.0 for k in range(n)])
    return np.interp(np.clip(alvo, 0, hs.max()), hs, vs)


def cenarios_padrao(P: pd.DataFrame, par: dict, S: pd.DataFrame, n: int = 16,
                    phi=None) -> dict:
    """Grade de cenarios pre-calculados para o relatorio.

    Duas dimensoes: a trajetoria de Selic e o tratamento da expectativa de inflacao. A
    segunda continua na interface, mas mudou de natureza: com a eq. (5) resolvida existe
    a opcao ENDOGENA, e as duas premissas fixas ficam como contrafactual -- servem para
    ler quanto do resultado vem do canal de expectativa e quanto do de demanda.
    """
    i0 = float(P["selic"].dropna().iloc[-1])
    pie0 = float(P["pi_e"].dropna().iloc[-1])
    meta = float(P["meta"].dropna().iloc[-1])
    choque = np.r_[np.ones(4), 0.8 ** np.arange(1, n - 3)][:n]

    juros = {
        "focus": ("Selic da Focus", caminho_selic_focus(P, n)),
        "constante": ("Selic constante", np.full(n, i0)),
        "alta100": ("+100 pb por 4T", i0 + choque),
        "baixa100": ("-100 pb por 4T", i0 - choque),
    }
    # pi^e: endogena pela eq. (5), ancorada na Focus, ou convergindo a meta em 8T
    conv = np.r_[np.linspace(pie0, meta, 9)[1:], np.full(max(n - 8, 0), meta)][:n]
    exp = {"eq5": ("Expectativa endogena (eq. 5)", None),
           "focus": ("Expectativa fixa na Focus", np.full(n, pie0)),
           "meta": ("Expectativa convergindo a meta", conv)}

    out = {}
    for jk, (jl, ip) in juros.items():
        for ek, (el, pe) in exp.items():
            kw = dict(expectativa="eq5", phi=phi) if ek == "eq5" else dict(pi_e=pe)
            C = simular(P, par, S, n=n, selic=ip, cambio="uip", **kw)
            out["%s__%s" % (jk, ek)] = dict(rotulo="%s / %s" % (jl, el), df=C)
    return out


# as tres configuracoes do simulador e a coluna do Graf 4B que cada uma tem de bater
IRF_CONF = (("so_demanda", dict(expectativa="premissa", cambio="premissa"),
             "publicado_so_demanda", "expectativa e cambio fixos"),
            ("com_expectativa", dict(expectativa="eq5", cambio="premissa"),
             "publicado_sem_cambio", "cambio fixo, expectativa reagindo"),
            ("completo", dict(expectativa="eq5", cambio="uip"),
             "publicado_completo", "modelo cheio"))


def irf(P: pd.DataFrame, par: dict, S: pd.DataFrame, n: int = 17, phi=None) -> pd.DataFrame:
    """Replica o experimento do C2 Boxe3 Graf 4A: +1 p.p. por 4 trimestres, depois 0,8^k.

    Caminho exogeno de proposito -- e a escolha do BC para silenciar a regra de Taylor
    e tornar os cenarios comparaveis. Devolve a resposta em desvio do cenario base.

    Roda as TRES configuracoes de `simular()` contra as TRES colunas do Graf 4B, que e
    a escada de validacao inteira: cada canal que se liga tem uma linha publicada
    correspondente. O que sobra na terceira e o bloco de precos administrados, que o BC
    inclui nas simulacoes dele e nao existe aqui.
    """
    pub = MP.irf_publicada()
    choque = pub["selic"].reindex(range(n)).ffill().fillna(0.0).values
    base_i = _em(P["selic"], P[["pi_L", "selic"]].dropna().index.max())
    D = pd.DataFrame(index=range(n))
    D["selic_choque"] = choque
    for nome, kw, _, _ in IRF_CONF:
        kw = dict(kw, phi=phi) if kw["expectativa"] == "eq5" else kw
        base = simular(P, par, S, n=n, selic=base_i, **kw)
        alt = simular(P, par, S, n=n, selic=base_i + choque, **kw)
        D["ipca_4t_" + nome] = alt["ipca_4t"].values - base["ipca_4t"].values
        for c in ("h", "pi_L", "pi_e", "de"):
            D["%s_%s" % (c, nome)] = alt[c].values - base[c].values
    # o mesmo motor com os parametros publicados: separa "o codigo esta certo?" de
    # "as nossas estimativas batem?". Se esta linha bate na publicada, o que sobra e
    # diferenca de parametro, nao de implementacao.
    kw = dict(expectativa="eq5", cambio="premissa", phi=PHI)
    pb = dict(par, **BCB)
    D["ipca_4t_motor_bcb"] = (simular(P, pb, S, n=n, selic=base_i + choque, **kw)["ipca_4t"].values
                              - simular(P, pb, S, n=n, selic=base_i, **kw)["ipca_4t"].values)
    # nomes sem sufixo = canal de demanda, para nao quebrar o que ja le o CSV
    for c in ("ipca_4t", "h", "pi_L"):
        D[c] = D[c + "_so_demanda"]
    D["publicado_so_demanda"] = pub["so_demanda"].reindex(range(n)).values
    D["publicado_sem_cambio"] = pub["sem_cambio"].reindex(range(n)).values
    D["publicado_completo"] = pub["canal_completo"].reindex(range(n)).values
    return D


def validar_irf(D: pd.DataFrame) -> dict:
    """Compara cada configuracao do simulador com a coluna publicada correspondente."""
    out = {}
    for nome, _, pubc, rot in IRF_CONF:
        m = D[["ipca_4t_" + nome, pubc]].dropna()
        err = m.iloc[:, 0] - m.iloc[:, 1]
        out[nome] = dict(rotulo=rot, n=int(len(m)),
                         pico_nosso=float(m.iloc[:, 0].min()),
                         pico_pub=float(m.iloc[:, 1].min()),
                         tri_pico_nosso=int(m.iloc[:, 0].idxmin()),
                         tri_pico_pub=int(m.iloc[:, 1].idxmin()),
                         erro_medio=float(err.mean()),
                         erro_abs_medio=float(err.abs().mean()),
                         erro_max=float(err.abs().max()),
                         erro_t4=float(err.reindex([4]).iloc[0]))
    m = D[["ipca_4t_motor_bcb", "publicado_sem_cambio"]].dropna()
    out["motor_bcb"] = dict(
        rotulo="nosso motor, parametros do BC", n=int(len(m)),
        pico_nosso=float(m.iloc[:, 0].min()), pico_pub=float(m.iloc[:, 1].min()),
        tri_pico_nosso=int(m.iloc[:, 0].idxmin()), tri_pico_pub=int(m.iloc[:, 1].idxmin()),
        erro_abs_medio=float((m.iloc[:, 0] - m.iloc[:, 1]).abs().mean()))
    # chaves planas da configuracao completa no nivel de cima (compatibilidade)
    out.update({k: v for k, v in out["completo"].items() if k != "rotulo"})
    out["pico_completo"] = out["completo"]["pico_pub"]
    return out


def validacao_parametros(par: dict) -> pd.DataFrame:
    """Tabela nosso vs. publicado, com o IC de 90% do BC e o veredito por parametro."""
    rows = []
    for fonte, ic, metodo in ((BCB, BCB_IC, "filtro"), (PHI, PHI_IC, "dois passos")):
        for k in fonte:
            if k not in par:
                continue
            lo, hi = ic[k]
            rows.append(dict(param=k, descricao=DESC[k], nosso=par[k], bcb=fonte[k],
                             dif=par[k] - fonte[k], ic_lo=lo, ic_hi=hi,
                             dentro=bool(lo <= par[k] <= hi), metodo=metodo))
    return pd.DataFrame(rows)


def comparar_hiato(S: pd.DataFrame) -> pd.DataFrame:
    """Nosso hiato latente vs. o publicado em pm_hiato_produto (deslocado +2 meses)."""
    d = MP.q("macro_brasil", "SELECT date, variavel, value FROM pm_hiato_produto")
    d["date"] = pd.to_datetime(d["date"]) + pd.DateOffset(months=2)
    d["per"] = pd.PeriodIndex(d["date"], freq="Q")
    piv = d.pivot_table(index="per", columns="variavel", values="value", aggfunc="first")
    out = pd.DataFrame({"nosso": S["h"]}).join(piv, how="outer")
    return out


# ── entry point ──────────────────────────────────────────────────────────────
def rodar(verbose: bool = True) -> dict:
    """Estima na amostra do boxe, estende os estados, decompoe, valida. Grava em data/."""
    sig = float((DATA / "modelo_sigma_rr.txt").read_text())
    Pe, Pf = MP.carregar("est"), MP.carregar("full")

    if verbose:
        print("  estimando em %s-%s (sigma_rr calibrado %.4f)..." % (*AMOSTRA, sig))
    par, _ = estimar(Pe, sig, verbose=verbose)
    if verbose:
        print("  logL %.3f (nas modas do BC: %.3f)" % (par["_logL"], par["_logL_bcb"]))

    Se = estados(Pe, par)
    Sf = estados(Pf, par)                        # parametros congelados, painel ate hoje

    phi, phi_info = estimar_eq5(Pe, par, verbose=verbose)
    par.update(phi)
    par["_eq5"] = phi_info

    dec = dict(phillips=decompor_phillips(Pf, par, Sf),
               hiato=decompor_hiato(Pf, par, Sf),
               taylor=decompor_taylor(Pf, par, Sf))
    cen = cenarios_padrao(Pf, par, Sf, phi=phi)
    diag = cen["focus__eq5"]["df"].attrs
    json.dump(dict(raio=diag.get("eq5_raio"), resid=diag.get("eq5_resid"),
                   cond=diag.get("eq5_cond")),
              open(DATA / "modelo_eq5_diag.json", "w"), indent=1)
    for k, v in cen.items():
        v["df"].to_csv(DATA / ("modelo_cenario_%s.csv" % k))
    json.dump({k: v["rotulo"] for k, v in cen.items()},
              open(DATA / "modelo_cenarios_rotulos.json", "w"), indent=1)
    D_irf = irf(Pf, par, Sf, phi=phi)
    val = validar_irf(D_irf)
    tab = validacao_parametros(par)

    DATA.mkdir(parents=True, exist_ok=True)
    json.dump(par, open(DATA / "modelo_params.json", "w"), indent=1)
    Sf.to_csv(DATA / "modelo_estados.csv")
    Se.to_csv(DATA / "modelo_estados_est.csv")
    for k, v in dec.items():
        v.to_csv(DATA / ("modelo_decomp_%s.csv" % k))
    D_irf.to_csv(DATA / "modelo_irf.csv")
    tab.to_csv(DATA / "modelo_validacao.csv", index=False)
    json.dump(val, open(DATA / "modelo_validacao_irf.json", "w"), indent=1)

    if verbose:
        print("  parametros dentro do IC 90%% do BC: %d de %d (%d de %d no filtro)"
              % (tab["dentro"].sum(), len(tab),
                 tab[tab.metodo == "filtro"]["dentro"].sum(), (tab.metodo == "filtro").sum()))
        ch = comparar_hiato(Se).loc[AMOSTRA[0]:AMOSTRA[1]][["nosso", "central"]].dropna()
        print("  hiato vs publicado: corr %.3f | sd %.2f vs %.2f | n=%d"
              % (ch["nosso"].corr(ch["central"]), ch["nosso"].std(), ch["central"].std(), len(ch)))
        for nome in [c[0] for c in IRF_CONF] + ["motor_bcb"]:
            v = val[nome]
            rot = v["rotulo"]
            print("  IRF %-16s pico %6.3f no T%-2d | BC (%s) %6.3f no T%-2d"
                  " | erro |medio| %.3f"
                  % (nome, v["pico_nosso"], v["tri_pico_nosso"], rot,
                     v["pico_pub"], v["tri_pico_pub"], v["erro_abs_medio"]))
        print("  r* hoje (%s): IS %.2f%% | Taylor %.2f%%"
              % (Sf.index.max(), Sf["rr_IS_total"].dropna().iloc[-1],
                 Sf["rr_TAY_total"].dropna().iloc[-1]))
    return dict(par=par, estados=Sf, estados_est=Se, decomp=dec, irf=D_irf,
                validacao=tab, validacao_irf=val)


if __name__ == "__main__":
    print("Rodando o modelo agregado...")
    rodar()
