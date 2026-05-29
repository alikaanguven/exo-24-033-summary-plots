## Get the required files first.
#
# 
# sus-18-004.csv      "https://www.hepdata.net/download/table/ins1966342/Figure%2010a/1/csv"
# sus-20-002_obs.csv  "https://www.hepdata.net/download/table/ins1893826/Figure%209a%20(observed%20limit%20contour)/1/csv"
# sus-20-002_exp.csv  "https://www.hepdata.net/download/table/ins1893826/Figure%209a%20(expected%20limit%20contour)/1/csv"
# exo-24-033.csv      "https://www.hepdata.net/download/table/ins3081697/Figure%2010c%20(lower)%2C%20exclusion%20curves/1/csv"
# sus-21-003_exp.csv  "https://www.hepdata.net/download/table/ins2624652/Figure%2010%20expected%20lines/1/csv"
# sus-21-003_obs.csv  "https://www.hepdata.net/download/table/ins2624652/Figure%2010%20observed%20lines/1/csv"

import pandas as pd
import ROOT
import numpy as np
from array import array

ROOT.gROOT.SetBatch(True)

# -----------------------------
# input
# -----------------------------
sus_20_002_obs = pd.read_csv('sus-20-002_obs.csv', comment="#")
sus_20_002_obs['\\DeltaM [GeV]'] = (
    sus_20_002_obs['m_{stop} [GeV]'] - sus_20_002_obs['m_{LSP} [pb]']
)

sus_20_002_exp = pd.read_csv('sus-20-002_exp.csv', comment="#")
sus_20_002_exp['\\DeltaM [GeV]'] = (
    sus_20_002_exp['m_{stop} [GeV]'] - sus_20_002_exp['m_{LSP} [pb]']
)

exo_24_033_obs = pd.read_csv('exo-24-033_obs.csv', comment="#")
exo_24_033_exp = pd.read_csv('exo-24-033_exp.csv', comment="#")

sus_18_004_obs = pd.read_csv('sus-18-004_obs.csv', comment="#")
sus_18_004_exp = pd.read_csv('sus-18-004_exp.csv', comment="#")

sus_23_003_obs = pd.read_csv('SUS-23-003_obs.csv', comment="#")
sus_23_003_exp = pd.read_csv('SUS-23-003_exp.csv', comment="#")

# -----------------------------
# Cross-sections for SUS-18-004
# -----------------------------
with open('SUSYCrossSections13TeVstopsbottom.txt') as xs_file:
    txt = xs_file.read()

rows = []
for line in txt.splitlines():
    if line.strip().startswith("|"):
        cols = [c.strip() for c in line.strip("|").split("|")]
        rows.append(cols)

xs_df = pd.DataFrame(rows[1:], columns=rows[0])
xs_df['*Stop / sbottom mass (!GeV)*'] = (
    xs_df['*Stop / sbottom mass (!GeV)*']
    .str.replace(r'[^\d\.]', '', regex=True)
    .astype(float)
)

sus_18_004_obs_merged = pd.merge(
    left=sus_18_004_obs,
    right=xs_df,
    left_on=r'$m_{\tilde{\text{t}}}$ [GeV]',
    right_on='*Stop / sbottom mass (!GeV)*'
)
sus_18_004_obs_merged['*Cross section (pb)*'] = sus_18_004_obs_merged['*Cross section (pb)*'].astype(float)
exclude_mask = (
    sus_18_004_obs_merged['95% CL upper limit on the cross section [pb]']
    < sus_18_004_obs_merged['*Cross section (pb)*']
)
sus_18_004_obs_merged = sus_18_004_obs_merged[exclude_mask].sort_values([
    r'$m_{\tilde{\text{t}}}$ [GeV]',
    r'$\Delta m (\tilde{\text{t}}, \tilde{\chi}^0_1)$ [GeV]'
])

sus_18_004_obs_max = (
    sus_18_004_obs_merged
    .sort_values(r'$m_{\tilde{\text{t}}}$ [GeV]')
    .groupby(r'$\Delta m (\tilde{\text{t}}, \tilde{\chi}^0_1)$ [GeV]', as_index=False)
    .last()
)

sus_18_004_exp_merged = pd.merge(
    left=sus_18_004_exp,
    right=xs_df,
    left_on=r'$m_{\tilde{\text{t}}}$ [GeV]',
    right_on='*Stop / sbottom mass (!GeV)*'
)
sus_18_004_exp_merged['*Cross section (pb)*'] = sus_18_004_exp_merged['*Cross section (pb)*'].astype(float)
exclude_mask = (
    sus_18_004_exp_merged['95% CL upper limit on the cross section [pb]']
    < sus_18_004_exp_merged['*Cross section (pb)*']
)
sus_18_004_exp_merged = sus_18_004_exp_merged[exclude_mask].sort_values([
    r'$m_{\tilde{\text{t}}}$ [GeV]',
    r'$\Delta m (\tilde{\text{t}}, \tilde{\chi}^0_1)$ [GeV]'
])

sus_18_004_exp_max = (
    sus_18_004_exp_merged
    .sort_values(r'$m_{\tilde{\text{t}}}$ [GeV]')
    .groupby(r'$\Delta m (\tilde{\text{t}}, \tilde{\chi}^0_1)$ [GeV]', as_index=False)
    .last()
)

def read_sus21003_central(path):
    m_col = r'$m(\mathrm{\widetilde{t}}_{1})$ [GeV]'
    dm_col = r'max($\Delta {m}$) excluded [GeV]'
    df = pd.read_csv(path, comment="#")

    repeated_headers = df.index[df[m_col] == m_col]
    if len(repeated_headers) > 0:
        df = df.loc[:repeated_headers[0] - 1]

    df = df.rename(columns={m_col: 'M', dm_col: 'dM'})
    df['M']  = pd.to_numeric(df['M'],  errors='coerce')
    df['dM'] = pd.to_numeric(df['dM'], errors='coerce')
    return df.dropna(subset=['M', 'dM'])

sus_21_003_obs = read_sus21003_central('sus-21-003_obs.csv')
sus_21_003_exp = read_sus21003_central('sus-21-003_exp.csv')

# -----------------------------
# style
# -----------------------------
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetLegendBorderSize(0)

def make_graph(x, y, sort=2):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    m = np.isfinite(x) & np.isfinite(y)
    x = x[m]
    y = y[m]

    if sort == 2:
        order = np.argsort(y)
    elif sort == 1:
        order = np.argsort(x)
    else:
        order = np.arange(len(x))

    x = x[order]
    y = y[order]

    return ROOT.TGraph(len(x), array("d", x.tolist()), array("d", y.tolist()))

def make_left_exclusion(graph, xmin):
    """
    Create filled polygon for region LEFT of curve.
    """
    n = graph.GetN()
    xs = [graph.GetPointX(i) for i in range(n)]
    ys = [graph.GetPointY(i) for i in range(n)]

    x0, y0 = xs[0], ys[0]
    x1, y1 = xs[-1], ys[-1]

    poly_x = [xmin, x0] + xs + [xmin, xmin]
    poly_y = [y0,   y0] + ys + [y1,   y0]

    return ROOT.TGraph(
        len(poly_x),
        array("d", poly_x),
        array("d", poly_y)
    )

# -----------------------------
# graphs
# -----------------------------
g_sus20002_obs = make_graph(
    sus_20_002_obs['m_{stop} [GeV]'],
    sus_20_002_obs['\\DeltaM [GeV]'],
    sort=1
)

g_exo24033_obs = make_graph(
    exo_24_033_obs['Observed $m$ excluded at 95%% CL [GeV]'],
    exo_24_033_obs[r'$\Delta m$ [GeV]'],
    sort=2
)

g_sus18004_obs = make_graph(
    sus_18_004_obs_max[r'$m_{\tilde{\text{t}}}$ [GeV]'],
    sus_18_004_obs_max[r'$\Delta m (\tilde{\text{t}}, \tilde{\chi}^0_1)$ [GeV]'],
    sort=2
)

g_sus21003_obs = make_graph(
    sus_21_003_obs['M'],
    sus_21_003_obs['dM'],
    sort=2
)

g_sus20002_exp = make_graph(
    sus_20_002_exp['m_{stop} [GeV]'],
    sus_20_002_exp['\\DeltaM [GeV]'],
    sort=1
)

g_exo24033_exp = make_graph(
    exo_24_033_exp['Median expected $m$ excluded at 95%% CL [GeV]'],
    exo_24_033_exp[r'$\Delta m$ [GeV]'],
    sort=2
)

g_sus18004_exp = make_graph(
    sus_18_004_exp_max[r'$m_{\tilde{\text{t}}}$ [GeV]'],
    sus_18_004_exp_max[r'$\Delta m (\tilde{\text{t}}, \tilde{\chi}^0_1)$ [GeV]'],
    sort=2
)

g_sus21003_exp = make_graph(
    sus_21_003_exp['M'],
    sus_21_003_exp['dM'],
    sort=2
)

g_sus23003_obs = make_graph(
	sus_23_003_obs['M'],
	sus_23_003_obs['dM'],
	sort=2
)
g_sus23003_exp = make_graph(
	sus_23_003_exp['M'],
	sus_23_003_exp['dM'],
	sort=2
)


# -----------------------------
# colors / line styles
# Avoid black for EXO-24-033
# -----------------------------
col_sus20002 = ROOT.kBlue + 1
col_sus18004 = ROOT.kYellow + 1
col_sus21003 = ROOT.kOrange - 1
col_exo24033 = ROOT.kRed + 1
col_sus23003 = ROOT.kGreen + 1

for g in [g_sus20002_obs, g_sus20002_exp]:
    g.SetLineColor(col_sus20002)

for g in [g_sus18004_obs, g_sus18004_exp]:
    g.SetLineColor(col_sus18004)

for g in [g_sus21003_obs, g_sus21003_exp]:
    g.SetLineColor(col_sus21003)

for g in [g_exo24033_obs, g_exo24033_exp]:
    g.SetLineColor(col_exo24033)
    
for g in [g_sus23003_obs, g_sus23003_exp]:
	g.SetLineColor(col_sus23003)

g_sus20002_obs.SetLineWidth(3)
g_sus18004_obs.SetLineWidth(3)
g_sus21003_obs.SetLineWidth(3)
g_exo24033_obs.SetLineWidth(3)
g_sus23003_obs.SetLineWidth(3)

g_sus20002_exp.SetLineWidth(2)
g_sus18004_exp.SetLineWidth(2)
g_sus21003_exp.SetLineWidth(2)
g_exo24033_exp.SetLineWidth(2)
g_sus23003_exp.SetLineWidth(2)

g_sus20002_exp.SetLineStyle(2)
g_sus18004_exp.SetLineStyle(2)
g_sus21003_exp.SetLineStyle(2)
g_exo24033_exp.SetLineStyle(2)
g_sus23003_exp.SetLineStyle(2)

# -----------------------------
# canvas
# -----------------------------
c = ROOT.TCanvas("c", "", 1200, 800)
c.SetLogy()

# make room on the right for legend
c.SetLeftMargin(0.12)
c.SetRightMargin(0.33)
c.SetTopMargin(0.08)
c.SetBottomMargin(0.12)

# shrink x axis because legend is outside
xmin, xmax = 250, 1450
ymin, ymax = 9, 1330

frame = ROOT.TH1F("frame", "", 100, xmin, xmax)
frame.SetMinimum(ymin)
frame.SetMaximum(ymax)

frame.GetXaxis().SetTitle("m_{#tilde{t}} (GeV)")
frame.GetYaxis().SetTitle("#Delta m(#tilde{t}, #tilde{#chi}^{0}_{1}) (GeV)")

frame.GetXaxis().SetTitleSize(0.045)
frame.GetYaxis().SetTitleSize(0.045)
frame.GetXaxis().SetLabelSize(0.04)
frame.GetYaxis().SetLabelSize(0.04)
frame.GetYaxis().SetTitleOffset(1.25)

frame.Draw()

# -----------------------------
# shaded exclusion regions
# -----------------------------
h_sus20002 = make_left_exclusion(g_sus20002_obs, xmin)
h_sus20002.SetFillColorAlpha(col_sus20002, 0.12)
h_sus20002.SetLineWidth(0)
h_sus20002.Draw("F SAME")

h_sus18004 = make_left_exclusion(g_sus18004_obs, xmin)
h_sus18004.SetFillColorAlpha(col_sus18004, 0.12)
h_sus18004.SetLineWidth(0)
h_sus18004.Draw("F SAME")

h_sus21003 = make_left_exclusion(g_sus21003_obs, xmin)
h_sus21003.SetFillColorAlpha(col_sus21003, 0.12)
h_sus21003.SetLineWidth(0)
h_sus21003.Draw("F SAME")

h_exo24033 = make_left_exclusion(g_exo24033_obs, xmin)
h_exo24033.SetFillColorAlpha(col_exo24033, 0.12)
h_exo24033.SetLineWidth(0)
h_exo24033.Draw("F SAME")

h_sus23003 = make_left_exclusion(g_sus23003_obs, xmin)
h_sus23003.SetFillColorAlpha(col_sus23003, 0.12)
h_sus23003.SetLineWidth(0)
h_sus23003.Draw("F SAME")

# -----------------------------
# curves
# -----------------------------
g_sus20002_obs.Draw("L SAME")
g_sus18004_obs.Draw("L SAME")
g_sus21003_obs.Draw("L SAME")
g_exo24033_obs.Draw("L SAME")
g_sus23003_obs.Draw("L SAME")

g_sus20002_exp.Draw("L SAME")
g_sus18004_exp.Draw("L SAME")
g_sus21003_exp.Draw("L SAME")
g_exo24033_exp.Draw("L SAME")
g_sus23003_exp.Draw("L SAME")

# -----------------------------
# custom right-side panel
# -----------------------------
panel_objs = []

panel = ROOT.TPave(0.68, 0.12, 0.98, 0.92, 1, "brNDC")
panel.SetFillColor(ROOT.kWhite)
panel.SetFillStyle(1001)
panel.SetLineColor(ROOT.kBlack)
panel.SetLineWidth(1)
panel.Draw()
panel_objs.append(panel)

# normal text
latex_leg = ROOT.TLatex()
latex_leg.SetNDC()
latex_leg.SetTextFont(42)
latex_leg.SetTextSize(0.020)
panel_objs.append(latex_leg)

# larger bold text
latex_leg_bold = ROOT.TLatex()
latex_leg_bold.SetNDC()
latex_leg_bold.SetTextFont(42)
latex_leg_bold.SetTextSize(0.024)
panel_objs.append(latex_leg_bold)

# geometry
x_box1 = 0.695
x_box2 = 0.740
x_text = 0.755

box_h = 0.024
dy = 0.115
y = 0.865
dy_sub = dy*0.9

# --- SUS-20-002
y -= dy
b_sus20002 = ROOT.TPave(x_box1, y - box_h, x_box2, y + box_h, 1, "NDC")
b_sus20002.SetFillColorAlpha(col_sus20002, 0.18)
b_sus20002.SetLineColor(col_sus20002)
b_sus20002.SetLineWidth(2)
b_sus20002.Draw()
panel_objs.append(b_sus20002)

latex_leg_bold.DrawLatex(x_text, y + 0.024, "#bf{0-, 1- and 2-lepton combination}")
latex_leg.DrawLatex(x_text, y - 0.002, "137 fb^{-1} (13 TeV)")
latex_leg.DrawLatex(x_text, y - 0.030, "Eur. Phys. J. C 81 (2021) 970")

# --- SUS-18-004
y -= dy_sub
b_sus18004 = ROOT.TPave(x_box1, y - box_h, x_box2, y + box_h, 1, "NDC")
b_sus18004.SetFillColorAlpha(col_sus18004, 0.18)
b_sus18004.SetLineColor(col_sus18004)
b_sus18004.SetLineWidth(2)
b_sus18004.Draw()
panel_objs.append(b_sus18004)

latex_leg_bold.DrawLatex(x_text, y + 0.024, "#bf{Two soft leptons}")
latex_leg.DrawLatex(x_text, y - 0.002, "137 fb^{-1} (13 TeV)")
latex_leg.DrawLatex(x_text, y - 0.030, "JHEP 04 (2022) 091")

# --- SUS-21-003
y -= dy_sub
b_sus21003 = ROOT.TPave(x_box1, y - box_h, x_box2, y + box_h, 1, "NDC")
b_sus21003.SetFillColorAlpha(col_sus21003, 0.18)
b_sus21003.SetLineColor(col_sus21003)
b_sus21003.SetLineWidth(2)
b_sus21003.Draw()
panel_objs.append(b_sus21003)

latex_leg_bold.DrawLatex(x_text, y + 0.024, "#bf{Single lepton}")
latex_leg.DrawLatex(x_text, y - 0.002, "137 fb^{-1} (13 TeV)")
latex_leg.DrawLatex(x_text, y - 0.030, "JHEP 06 (2023) 060")

# --- SUS_23-003
y -= dy_sub
b_sus23003 = ROOT.TPave(x_box1, y - box_h, x_box2, y + box_h, 1, "NDC")
b_sus23003.SetFillColorAlpha(col_sus23003, 0.18)
b_sus23003.SetLineColor(col_sus23003)
b_sus23003.SetLineWidth(2)
b_sus23003.Draw()
panel_objs.append(b_sus23003)

latex_leg_bold.DrawLatex(x_text, y + 0.024, "#bf{General compressed SUSY}")
latex_leg.DrawLatex(x_text, y - 0.002, "138 fb^{-1} (13 TeV)")
latex_leg.DrawLatex(x_text, y - 0.030, "Phys. Rev. D 112 (2025) 112023 ")


# --- EXO-24-033
y -= dy_sub
b_exo24033 = ROOT.TPave(x_box1, y - box_h, x_box2, y + box_h, 1, "NDC")
b_exo24033.SetFillColorAlpha(col_exo24033, 0.18)
b_exo24033.SetLineColor(col_exo24033)
b_exo24033.SetLineWidth(2)
b_exo24033.Draw()
panel_objs.append(b_exo24033)

latex_leg_bold.DrawLatex(x_text, y + 0.024, "#bf{Soft displaced vertices}")
latex_leg.DrawLatex(x_text, y - 0.002, "100 fb^{-1} (13 TeV)")
latex_leg.DrawLatex(x_text, y - 0.030, "arXiv:2511.08212")

# --- observed sample: solid line
y -= dy_sub
obs_line = ROOT.TLine(x_box1, y, x_box2, y)
obs_line.SetNDC()
obs_line.SetLineColor(ROOT.kBlack)
obs_line.SetLineStyle(1)
obs_line.SetLineWidth(3)
obs_line.Draw()
panel_objs.append(obs_line)

latex_leg.DrawLatex(x_text, y + 0.010, "Observed")
latex_leg.DrawLatex(x_text, y - 0.018, "exclusion 95% CL")

# --- expected sample: dashed line
#y -= dy * 0.72
y -= dy * 0.6
exp_line = ROOT.TLine(x_box1, y, x_box2, y)
exp_line.SetNDC()
exp_line.SetLineColor(ROOT.kBlack)
exp_line.SetLineStyle(2)
exp_line.SetLineWidth(3)
exp_line.Draw()
panel_objs.append(exp_line)

latex_leg.DrawLatex(x_text, y + 0.010, "Expected")
latex_leg.DrawLatex(x_text, y - 0.018, "exclusion 95% CL")

# -----------------------------
# date above legend
# -----------------------------
latex = ROOT.TLatex()
latex.SetNDC()

latex.SetTextFont(42)
latex.SetTextSize(0.04)
latex.SetTextAlign(31)
latex.DrawLatex(0.98, 0.932, "June 2026")

# -----------------------------
# CMS labels
# -----------------------------
latex.SetTextAlign(11)
latex.SetTextFont(62)
latex.SetTextSize(0.05)
latex.DrawLatex(0.12, 0.932, "CMS")

# no "Preliminary"

# latex.SetTextFont(42)
# latex.SetTextSize(0.04)
# latex.DrawLatex(0.505, 0.932, "138 fb^{-1} (13 TeV)")

latex.SetTextFont(42)
latex.SetTextSize(0.04)
latex.DrawLatex(
    0.705, 0.84,
    "pp #rightarrow #tilde{t}#bar{#tilde{t}},  #tilde{t} #rightarrow bf#bar{f'}#tilde{#chi}^{0}_{1}"
)

c.RedrawAxis()
c.Update()
c.Draw()
c.SaveAs("stop_v2.png")
c.SaveAs("stop_v2.pdf")
