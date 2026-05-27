## Get the required files first.
#
# 
# !wget -O exo_24_033_12.csv "https://www.hepdata.net/download/table/ins3081697/Figure%2011a%20(upper%20left)%2C%20exclusion%20curves/1/csv"
# !wget -O exo_24_033_15.csv "https://www.hepdata.net/download/table/ins3081697/Figure%2011b%20(upper%20right)%2C%20exclusion%20curves/1/csv"
# !wget -O exo_24_033_20.csv "https://www.hepdata.net/download/table/ins3081697/Figure%2011c%20(lower%20left)%2C%20exclusion%20curves/1/csv"
# !wget -O exo_24_033_25.csv "https://www.hepdata.net/download/table/ins3081697/Figure%2011d%20(lower%20right)%2C%20exclusion%20curves/1/csv"
# These contain two tables per csv file, one for obs, one for exp.
# Manually split them into observed and expected csv files to easily read them as pandas dataframes.
#
#
# SUS-18-004 limits are obtained by eye from the Figure 8a of https://arxiv.org/pdf/2111.06296.
# SUS-21-008 limits are obtained by eye from the Figure 11b of https://arxiv.org/pdf/2402.01888.


import numpy as np
import pandas as pd
from array import array
import ROOT
ROOT.gROOT.SetBatch(True)

sus_18_004_plus_obs = pd.read_csv('sus_18_004_plus_obs.csv', comment="#")
sus_18_004_plus_exp = pd.read_csv('sus_18_004_plus_exp.csv', comment="#")

sus_18_004_mins_obs = pd.read_csv('sus_18_004_mins_obs.csv', comment="#")
sus_18_004_mins_exp = pd.read_csv('sus_18_004_mins_exp.csv', comment="#")

exo_24_033_12_obs = pd.read_csv('exo_24_033_12_obs.csv', comment="#")
exo_24_033_15_obs = pd.read_csv('exo_24_033_15_obs.csv', comment="#")
exo_24_033_20_obs = pd.read_csv('exo_24_033_20_obs.csv', comment="#")
exo_24_033_25_obs = pd.read_csv('exo_24_033_25_obs.csv', comment="#")

exo_24_033_12_exp = pd.read_csv('exo_24_033_12_exp.csv', comment="#")
exo_24_033_15_exp = pd.read_csv('exo_24_033_15_exp.csv', comment="#")
exo_24_033_20_exp = pd.read_csv('exo_24_033_20_exp.csv', comment="#")
exo_24_033_25_exp = pd.read_csv('exo_24_033_25_exp.csv', comment="#")


# --- global style tweaks (CMS-like) ---
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

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
    Assumes graph is ordered in y.
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
        array("d", poly_y),
    )

# -----------------------------
# input columns
# -----------------------------
xcol = r'Observed $m$ excluded at 95%% CL [GeV]'
xcol_exp = r'Median expected $m$ excluded at 95%% CL [GeV]'
ycol = r'$c\tau$ [mm]'

# --- build observed / expected graphs ---
g_exo_24_033_12 = make_graph(exo_24_033_12_obs[xcol], exo_24_033_12_obs[ycol], sort=2)
g_exo_24_033_25 = make_graph(exo_24_033_25_obs[xcol], exo_24_033_25_obs[ycol], sort=2)

g_exo_24_033_12_exp = make_graph(exo_24_033_12_exp[xcol_exp], exo_24_033_12_exp[ycol], sort=2)
g_exo_24_033_25_exp = make_graph(exo_24_033_25_exp[xcol_exp], exo_24_033_25_exp[ycol], sort=2)

# --- colors / styles ---
col_sus_18_004_12 = ROOT.kOrange
col_sus_18_004_25 = ROOT.kOrange + 10
col_sus_21_008_12 = ROOT.kGreen + 1
col_sus_21_008_25 = ROOT.kGreen + 3
col_exo_24_033_12 = ROOT.kAzure + 10
col_exo_24_033_25 = ROOT.kAzure

g_exo_24_033_12.SetLineColor(col_exo_24_033_12)
g_exo_24_033_12.SetLineWidth(2)

g_exo_24_033_25.SetLineColor(col_exo_24_033_25)
g_exo_24_033_25.SetLineWidth(2)

g_exo_24_033_12_exp.SetLineColor(col_exo_24_033_12)
g_exo_24_033_12_exp.SetLineWidth(2)
g_exo_24_033_12_exp.SetLineStyle(2)

g_exo_24_033_25_exp.SetLineColor(col_exo_24_033_25)
g_exo_24_033_25_exp.SetLineWidth(2)
g_exo_24_033_25_exp.SetLineStyle(2)

col_sus_23_003_12 = ROOT.kMagenta
col_sus_23_003_25 = ROOT.kMagenta-5


# --- canvas ---
c = ROOT.TCanvas("c", "", 1200, 800)
c.SetLogy()

c.SetLeftMargin(0.14)
c.SetRightMargin(0.34)
c.SetTopMargin(0.08)
c.SetBottomMargin(0.12)

xmin, xmax = 100, 700
ymin, ymax = 1e-2, 3e2

# --- frame ---
frame = ROOT.TH1F("frame", "", 100, xmin, xmax)
frame.SetMinimum(ymin)
frame.SetMaximum(ymax)

frame.GetXaxis().SetTitle("m_{#tilde{#chi}^{0}_{2}} (GeV)")
frame.GetYaxis().SetTitle("c#tau (mm)")

frame.GetXaxis().SetTitleSize(0.045)
frame.GetYaxis().SetTitleSize(0.045)
frame.GetXaxis().SetLabelSize(0.04)
frame.GetYaxis().SetLabelSize(0.04)
frame.GetYaxis().SetTitleOffset(1.4)

frame.Draw()

# -------------------------------------------------
# Hide ROOT y-axis ticks and labels
# -------------------------------------------------
frame.GetYaxis().SetTickLength(0)
frame.GetYaxis().SetMoreLogLabels(False)
frame.GetYaxis().SetNoExponent(True)
frame.GetYaxis().SetLabelOffset(999)

# -------------------------------------------------
# Draw custom major + minor ticks only for y >= 1e-1
# -------------------------------------------------
major_tick = ROOT.TLine()
major_tick.SetLineWidth(1)

minor_tick = ROOT.TLine()
minor_tick.SetLineWidth(1)

major_len = (xmax - xmin) * 0.015
minor_len = (xmax - xmin) * 0.008

major_ticks = [1, 10, 100]
for y in major_ticks:
    if ymin <= y <= ymax:
        major_tick.DrawLine(xmin, y, xmin + major_len, y)

for decade in [-1, 0, 1, 2]:
    base = 10 ** decade
    for m in range(2, 10):
        y = m * base
        if y < 1e-1:
            continue
        if ymin <= y <= ymax:
            minor_tick.DrawLine(xmin, y, xmin + minor_len, y)

# -------------------------------------------------
# Draw custom y-axis labels
# -------------------------------------------------
latex_axis = ROOT.TLatex()
latex_axis.SetTextFont(42)
latex_axis.SetTextSize(0.035)
latex_axis.SetTextAlign(32)

labels = [
    (1, "10^{0}"),
    (10, "10^{1}"),
    (100, "10^{2}"),
]

for y, label in labels:
    latex_axis.DrawLatex(xmin - 35, y, label)

# --- shaded exclusion region ---
h_exo_24_033_12 = make_left_exclusion(g_exo_24_033_12, xmin)
h_exo_24_033_12.SetFillColorAlpha(col_exo_24_033_12, 0.08)
h_exo_24_033_12.SetLineWidth(0)
h_exo_24_033_12.Draw("F SAME")

h_exo_24_033_25 = make_left_exclusion(g_exo_24_033_25, xmin)
h_exo_24_033_25.SetFillColorAlpha(col_exo_24_033_25, 0.08)
h_exo_24_033_25.SetLineWidth(0)
h_exo_24_033_25.Draw("F SAME")

# --- observed / expected curves ---
g_exo_24_033_12.Draw("L SAME")
g_exo_24_033_25.Draw("L SAME")
g_exo_24_033_12_exp.Draw("L SAME")
g_exo_24_033_25_exp.Draw("L SAME")


# --- prompt region from SUS-21-008 (by eye) ---
ymin_frame = frame.GetMinimum()

exp_sus_21_008_12 = 300
obs_sus_21_008_12 = 280+2
exp_sus_21_008_25 = 270
obs_sus_21_008_25 = 220

h_sus_21_008_12 = ROOT.TBox(xmin, ymin_frame, obs_sus_21_008_12, 0.1)
h_sus_21_008_12.SetFillColorAlpha(col_sus_21_008_12, 0.05+0.1)
h_sus_21_008_12.SetFillStyle(3345)
h_sus_21_008_12.SetLineWidth(0)
h_sus_21_008_12.Draw("SAME")

h_sus_21_008_25 = ROOT.TBox(xmin, ymin_frame, obs_sus_21_008_25, 0.1)
h_sus_21_008_25.SetFillColorAlpha(col_sus_21_008_25, 0.05+0.1)
h_sus_21_008_25.SetFillStyle(3345)
h_sus_21_008_25.SetLineWidth(0)
h_sus_21_008_25.Draw("SAME")


g_sus_21_008_12 = ROOT.TLine(obs_sus_21_008_12, ymin_frame, obs_sus_21_008_12, 0.1)
g_sus_21_008_12.SetLineStyle(1)
g_sus_21_008_12.SetLineColor(col_sus_21_008_12)
g_sus_21_008_12.SetLineWidth(2)
g_sus_21_008_12.Draw()

g_sus_21_008_12_exp = ROOT.TLine(exp_sus_21_008_12, ymin_frame, exp_sus_21_008_12, 0.1)
g_sus_21_008_12_exp.SetLineStyle(2)
g_sus_21_008_12_exp.SetLineColor(col_sus_21_008_12)
g_sus_21_008_12_exp.SetLineWidth(2)
g_sus_21_008_12_exp.Draw()

g_sus_21_008_25 = ROOT.TLine(obs_sus_21_008_25, ymin_frame, obs_sus_21_008_25, 0.1)
g_sus_21_008_25.SetLineStyle(1)
g_sus_21_008_25.SetLineColor(col_sus_21_008_25)
g_sus_21_008_25.SetLineWidth(2)
g_sus_21_008_25.Draw()

g_sus_21_008_25_exp = ROOT.TLine(exp_sus_21_008_25, ymin_frame, exp_sus_21_008_25, 0.1)
g_sus_21_008_25_exp.SetLineStyle(2)
g_sus_21_008_25_exp.SetLineColor(col_sus_21_008_25)
g_sus_21_008_25_exp.SetLineWidth(2)
g_sus_21_008_25_exp.Draw()


# --- prompt region from SUS-18-004 (by eye) ---
ymin_frame = frame.GetMinimum()

h_sus_18_004_12 = ROOT.TBox(xmin, ymin_frame, 250, 0.1)
h_sus_18_004_12.SetFillColorAlpha(ROOT.kOrange, 0.05+0.1)
h_sus_18_004_12.SetFillStyle(3144)
h_sus_18_004_12.SetLineWidth(0)
h_sus_18_004_12.Draw("SAME")

h_sus_18_004_25 = ROOT.TBox(xmin, ymin_frame, 210, 0.1)
h_sus_18_004_25.SetFillColorAlpha(ROOT.kOrange+10, 0.05+0.1)
h_sus_18_004_25.SetFillStyle(3144)
h_sus_18_004_25.SetLineWidth(0)
h_sus_18_004_25.Draw("SAME")

g_sus_18_004_12 = ROOT.TLine(250, ymin_frame, 250, 0.1)
g_sus_18_004_12.SetLineStyle(1)
g_sus_18_004_12.SetLineColor(col_sus_18_004_12)
g_sus_18_004_12.SetLineWidth(2)
g_sus_18_004_12.Draw()

g_sus_18_004_12_exp = ROOT.TLine(280, ymin_frame, 280, 0.1)
g_sus_18_004_12_exp.SetLineStyle(2)
g_sus_18_004_12_exp.SetLineColor(col_sus_18_004_12)
g_sus_18_004_12_exp.SetLineWidth(2)
g_sus_18_004_12_exp.Draw()

g_sus_18_004_25 = ROOT.TLine(210, ymin_frame, 210, 0.1)
g_sus_18_004_25.SetLineStyle(1)
g_sus_18_004_25.SetLineColor(col_sus_18_004_25)
g_sus_18_004_25.SetLineWidth(2)
g_sus_18_004_25.Draw()

g_sus_18_004_25_exp = ROOT.TLine(266, ymin_frame, 266, 0.1)
g_sus_18_004_25_exp.SetLineStyle(2)
g_sus_18_004_25_exp.SetLineColor(col_sus_18_004_25)
g_sus_18_004_25_exp.SetLineWidth(2)
g_sus_18_004_25_exp.Draw()


# -- prompt region SUS-23-003
h_sus_23_003_12 = ROOT.TBox(xmin, ymin_frame, 302.995 , 0.1)
h_sus_23_003_12.SetFillColorAlpha(ROOT.kMagenta, 0.05)
h_sus_23_003_12.SetLineWidth(0)
h_sus_23_003_12.Draw("SAME")

h_sus_23_003_25 = ROOT.TBox(xmin, ymin_frame, 352.912, 0.1)
h_sus_23_003_25.SetFillColorAlpha(ROOT.kMagenta-5, 0.05)
h_sus_23_003_25.SetLineWidth(0)
h_sus_23_003_25.Draw("SAME")

g_sus_23_003_12_obs = ROOT.TLine(302.995, ymin_frame, 302.995, 0.1)
g_sus_23_003_12_obs.SetLineStyle(1)
g_sus_23_003_12_obs.SetLineColor(col_sus_23_003_12)
g_sus_23_003_12_obs.SetLineWidth(2)
g_sus_23_003_12_obs.Draw()

g_sus_23_003_12_exp = ROOT.TLine(370.882, ymin_frame, 370.882, 0.1)
g_sus_23_003_12_exp.SetLineStyle(2)
g_sus_23_003_12_exp.SetLineColor(col_sus_23_003_12)
g_sus_23_003_12_exp.SetLineWidth(2)
g_sus_23_003_12_exp.Draw()

g_sus_23_003_25_obs = ROOT.TLine(307.987, ymin_frame, 307.987, 0.1)
g_sus_23_003_25_obs.SetLineStyle(1)
g_sus_23_003_25_obs.SetLineColor(col_sus_23_003_25)
g_sus_23_003_25_obs.SetLineWidth(2)
g_sus_23_003_25_obs.Draw()

g_sus_23_003_25_exp = ROOT.TLine(352.912, ymin_frame, 352.912, 0.1)
g_sus_23_003_25_exp.SetLineStyle(2)
g_sus_23_003_25_exp.SetLineColor(col_sus_23_003_25)
g_sus_23_003_25_exp.SetLineWidth(2)
g_sus_23_003_25_exp.Draw()


# --- horizontal dashed line for prompt region boundary ---
line_ctau = ROOT.TLine(xmin, 0.1, xmax, 0.1)
line_ctau.SetLineColor(ROOT.kBlack)
line_ctau.SetLineStyle(3)
line_ctau.SetLineWidth(2)
line_ctau.Draw("SAME")

# --- prompt text on y-axis, rotated 90 degrees ---
latex_prompt = ROOT.TLatex()
latex_prompt.SetNDC(True)
latex_prompt.SetTextFont(42)
latex_prompt.SetTextSize(0.032)
latex_prompt.SetTextAngle(90)
latex_prompt.SetTextAlign(22)   # centered
latex_prompt.DrawLatex(0.105, 0.21, "Prompt")


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

# panel geometry
x_box1 = 0.695
x_box2 = 0.740
x_text = 0.755

box_h = 0.020
#dy = 0.145
dy = 0.11
y = 0.855

# --- SUS-18-004, Δm = 12 GeV
y -= dy
b_sus_18_004_12 = ROOT.TPave(x_box1, y - box_h - 0.010, x_box2, y + box_h - 0.010, 1, "NDC")
b_sus_18_004_12.SetFillColorAlpha(col_sus_18_004_12, 0.18)
b_sus_18_004_12.SetLineColor(col_sus_18_004_12)
b_sus_18_004_12.SetLineWidth(2)
b_sus_18_004_12.Draw()
panel_objs.append(b_sus_18_004_12)

latex_leg_bold.DrawLatex(x_text - 0.060, y + 0.042, "#bf{Two or three soft leptons}")
latex_leg.DrawLatex(x_text - 0.060, y + 0.020, "JHEP 04 (2022) 091")
latex_leg.DrawLatex(x_text, y - 0.012, "#Delta m = 12 GeV, 137 fb^{-1} (13 TeV)")

# --- SUS-18-004, Δm = 25 GeV
y -= dy * 0.50
b_sus_18_004_25 = ROOT.TPave(x_box1, y - box_h, x_box2, y + box_h, 1, "NDC")
b_sus_18_004_25.SetFillColorAlpha(col_sus_18_004_25, 0.18)
b_sus_18_004_25.SetLineColor(col_sus_18_004_25)
b_sus_18_004_25.SetLineWidth(2)
b_sus_18_004_25.Draw()
panel_objs.append(b_sus_18_004_25)

latex_leg.DrawLatex(x_text, y - 0.002, "#Delta m = 25 GeV, 137 fb^{-1} (13 TeV)")
# latex_leg.DrawLatex(x_text, y - 0.030, "JHEP 04 (2022) 091")


# --- SUS-23-003 dm = 12 GeV
y -= dy
b_sus_23_003_12 = ROOT.TPave(x_box1, y - box_h - 0.010, x_box2, y + box_h - 0.010, 1, "NDC")
b_sus_23_003_12.SetFillColorAlpha(col_sus_23_003_12, 0.18)
b_sus_23_003_12.SetLineColor(col_sus_23_003_12)
b_sus_23_003_12.SetLineWidth(2)
b_sus_23_003_12.Draw()
panel_objs.append(b_sus_18_004_12)

latex_leg_bold.DrawLatex(x_text - 0.060, y + 0.042, "#bf{General compressed SUSY}")
latex_leg.DrawLatex(x_text - 0.060, y + 0.020, "Phys. Rev. D 112 (2025) 112023")
latex_leg.DrawLatex(x_text, y - 0.012, "#Delta m = 12 GeV, 138 fb^{-1} (13 TeV)")
# --- SUS-23-003 dm = 25 GeV
y -= dy * 0.50
b_sus_23_003_25 = ROOT.TPave(x_box1, y - box_h, x_box2, y + box_h, 1, "NDC")
b_sus_23_003_25.SetFillColorAlpha(col_sus_23_003_25, 0.18)
b_sus_23_003_25.SetLineColor(col_sus_23_003_25)
b_sus_23_003_25.SetLineWidth(2)
b_sus_23_003_25.Draw()
panel_objs.append(b_sus_23_003_25)
latex_leg.DrawLatex(x_text, y - 0.002, "#Delta m = 25 GeV, 138 fb^{-1} (13 TeV)")

# --- EXO-24-033, Δm = 12 GeV
y -= dy
b_exo_24_033_12 = ROOT.TPave(x_box1, y - box_h - 0.010, x_box2, y + box_h - 0.010, 1, "NDC")
b_exo_24_033_12.SetFillColorAlpha(col_exo_24_033_12, 0.18)
b_exo_24_033_12.SetLineColor(col_exo_24_033_12)
b_exo_24_033_12.SetLineWidth(2)
b_exo_24_033_12.Draw()
panel_objs.append(b_exo_24_033_12)

latex_leg_bold.DrawLatex(x_text - 0.060, y + 0.042, "#bf{Soft displaced vertices}")
latex_leg.DrawLatex(x_text - 0.060, y + 0.020, "arXiv:2511.08212")
latex_leg.DrawLatex(x_text, y - 0.012, "#Delta m = 12 GeV, 100 fb^{-1} (13 TeV)")
# latex_leg.DrawLatex(x_text, y - 0.030, "arXiv:2511.08212")

# --- EXO-24-033, Δm = 25 GeV
y -= dy * 0.50
b_exo_24_033_25 = ROOT.TPave(x_box1, y - box_h, x_box2, y + box_h, 1, "NDC")
b_exo_24_033_25.SetFillColorAlpha(col_exo_24_033_25, 0.18)
b_exo_24_033_25.SetLineColor(col_exo_24_033_25)
b_exo_24_033_25.SetLineWidth(2)
b_exo_24_033_25.Draw()
panel_objs.append(b_exo_24_033_25)

# latex_leg_bold.DrawLatex(x_text, y + 0.022, "#bf{Soft displaced vertices}")
latex_leg.DrawLatex(x_text, y - 0.002, "#Delta m = 25 GeV, 100 fb^{-1} (13 TeV)")
# latex_leg.DrawLatex(x_text, y - 0.030, "arXiv:2511.08212")

# --- observed / expected samples: line + marker + text
y -= dy

# observed row
obs_line = ROOT.TLine(x_box1, y, x_box2, y)
obs_line.SetNDC()
obs_line.SetLineColor(ROOT.kBlack)
obs_line.SetLineStyle(1)
obs_line.SetLineWidth(3)
obs_line.Draw()
panel_objs.append(obs_line)

latex_leg.DrawLatex(x_text, y + 0.010, "Observed")
latex_leg.DrawLatex(x_text, y - 0.018, "exclusion 95% CL")

# expected row
y -= dy * 0.72

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
#latex_leg.SetTextSize(0.020)
latex_leg.SetTextSize(0.022)
panel_objs.append(latex_leg)

# larger bold text
latex_leg_bold = ROOT.TLatex()
latex_leg_bold.SetNDC()
latex_leg_bold.SetTextFont(42)
#latex_leg_bold.SetTextSize(0.024)
latex_leg_bold.SetTextSize(0.028)
panel_objs.append(latex_leg_bold)

# panel geometry
x_box1 = 0.695
x_box2 = 0.740
x_text = 0.755

box_h = 0.020
box_h_leg = 0.012
#dy = 0.105          # <-- reduced from 0.145
dy = 0.0975 # <-- reduced again to incorporate 23-003
dy_sub = dy * 0.50  # sub-entry spacing
y = 0.855

# =============================================
# --- SUS-18-004, Δm = 12 GeV
# =============================================
y -= dy
#b_sus_18_004_12 = ROOT.TPave(x_box1, y - box_h - 0.010, x_box2, y + box_h - 0.010, 1, "NDC")
b_sus_18_004_12 = ROOT.TPave(x_box1, y - box_h_leg - 0.010, x_box2, y + box_h_leg - 0.010, 1, "NDC")
b_sus_18_004_12.SetFillColorAlpha(col_sus_18_004_12, 0.18)
b_sus_18_004_12.SetLineColor(col_sus_18_004_12)
b_sus_18_004_12.SetLineWidth(2)
b_sus_18_004_12.SetFillStyle(3144)
b_sus_18_004_12.Draw()
panel_objs.append(b_sus_18_004_12)

latex_leg_bold.DrawLatex(x_text - 0.060, y + 0.042, "#bf{Two or three soft leptons}")
latex_leg.DrawLatex(x_text - 0.060, y + 0.020, "JHEP 04 (2022) 091")
latex_leg.DrawLatex(x_text, y - 0.012, "#Delta m = 12 GeV, 137 fb^{-1} (13 TeV)")

# --- SUS-18-004, Δm = 25 GeV
y -= dy_sub
#b_sus_18_004_25 = ROOT.TPave(x_box1, y - box_h, x_box2, y + box_h, 1, "NDC")
b_sus_18_004_25 = ROOT.TPave(x_box1, y - box_h_leg, x_box2, y + box_h_leg, 1, "NDC")
b_sus_18_004_25.SetFillColorAlpha(col_sus_18_004_25, 0.18)
b_sus_18_004_25.SetLineColor(col_sus_18_004_25)
b_sus_18_004_25.SetLineWidth(2)
b_sus_18_004_25.SetFillStyle(3144)
b_sus_18_004_25.Draw()
panel_objs.append(b_sus_18_004_25)

latex_leg.DrawLatex(x_text, y - 0.002, "#Delta m = 25 GeV, 137 fb^{-1} (13 TeV)")





# =============================================
# --- SUS-21-008, Δm = 12 GeV
# =============================================
y -= dy
#b_sus_21_008_12 = ROOT.TPave(x_box1, y - box_h - 0.010, x_box2, y + box_h - 0.010, 1, "NDC")
b_sus_21_008_12 = ROOT.TPave(x_box1, y - box_h_leg - 0.010, x_box2, y + box_h_leg - 0.010, 1, "NDC")
b_sus_21_008_12.SetFillColorAlpha(col_sus_21_008_12, 0.18)
b_sus_21_008_12.SetLineColor(col_sus_21_008_12)
b_sus_21_008_12.SetLineWidth(2)
b_sus_21_008_12.SetFillStyle(3345)
b_sus_21_008_12.Draw()
panel_objs.append(b_sus_21_008_12)

latex_leg_bold.DrawLatex(x_text - 0.060, y + 0.042, "#bf{Two or three leptons, combination}")  # <-- update title as needed
latex_leg.DrawLatex(x_text - 0.060, y + 0.020, "PRD 109 (2024) 112001")       # <-- update reference
latex_leg.DrawLatex(x_text, y - 0.012, "#Delta m = 12 GeV, 129-137 fb^{-1} (13 TeV)")

# --- SUS-21-008, Δm = 25 GeV
y -= dy_sub
#b_sus_21_008_25 = ROOT.TPave(x_box1, y - box_h, x_box2, y + box_h, 1, "NDC")
b_sus_21_008_25 = ROOT.TPave(x_box1, y - box_h_leg, x_box2, y + box_h_leg, 1, "NDC")
b_sus_21_008_25.SetFillColorAlpha(col_sus_21_008_25, 0.18)
b_sus_21_008_25.SetLineColor(col_sus_21_008_25)
b_sus_21_008_25.SetLineWidth(2)
b_sus_21_008_25.SetFillStyle(3345)
b_sus_21_008_25.Draw()
panel_objs.append(b_sus_21_008_25)

latex_leg.DrawLatex(x_text, y - 0.002, "#Delta m = 25 GeV, 129-137 fb^{-1} (13 TeV)")


# --- SUS-23-003 dm = 12 GeV
y -= dy
#b_sus_23_003_12 = ROOT.TPave(x_box1, y - box_h - 0.010, x_box2, y + box_h - 0.010, 1, "NDC")
b_sus_23_003_12 = ROOT.TPave(x_box1, y - box_h_leg - 0.010, x_box2, y + box_h_leg - 0.010, 1, "NDC")
b_sus_23_003_12.SetFillColorAlpha(col_sus_23_003_12, 0.18)
b_sus_23_003_12.SetLineColor(col_sus_23_003_12)
b_sus_23_003_12.SetLineWidth(2)
b_sus_23_003_12.Draw()
panel_objs.append(b_sus_18_004_12)

latex_leg_bold.DrawLatex(x_text - 0.060, y + 0.042, "#bf{General compressed SUSY}")
latex_leg.DrawLatex(x_text - 0.060, y + 0.020, "Phys. Rev. D 112 (2025) 112023")
latex_leg.DrawLatex(x_text, y - 0.012, "#Delta m = 12 GeV, 138 fb^{-1} (13 TeV)")
# --- SUS-23-003 dm = 25 GeV
y -= dy_sub
#b_sus_23_003_25 = ROOT.TPave(x_box1, y - box_h, x_box2, y + box_h, 1, "NDC")
#b_sus_23_003_25 = ROOT.TPave(x_box1, y - box_h_leg - 0.010, x_box2, y + box_h_leg - 0.010, 1, "NDC")
b_sus_23_003_25 = ROOT.TPave(x_box1, y - box_h_leg, x_box2, y + box_h_leg, 1, "NDC")
b_sus_23_003_25.SetFillColorAlpha(col_sus_23_003_25, 0.18)
b_sus_23_003_25.SetLineColor(col_sus_23_003_25)
b_sus_23_003_25.SetLineWidth(2)
b_sus_23_003_25.Draw()
panel_objs.append(b_sus_23_003_25)
latex_leg.DrawLatex(x_text, y - 0.002, "#Delta m = 25 GeV, 138 fb^{-1} (13 TeV)")

# =============================================
# --- EXO-24-033, Δm = 12 GeV
# =============================================
y -= dy
#b_exo_24_033_12 = ROOT.TPave(x_box1, y - box_h - 0.010, x_box2, y + box_h - 0.010, 1, "NDC")
b_exo_24_033_12 = ROOT.TPave(x_box1, y - box_h_leg - 0.010, x_box2, y + box_h_leg - 0.010, 1, "NDC")
b_exo_24_033_12.SetFillColorAlpha(col_exo_24_033_12, 0.18)
b_exo_24_033_12.SetLineColor(col_exo_24_033_12)
b_exo_24_033_12.SetLineWidth(2)
b_exo_24_033_12.Draw()
panel_objs.append(b_exo_24_033_12)

latex_leg_bold.DrawLatex(x_text - 0.060, y + 0.042, "#bf{Soft displaced vertices}")
latex_leg.DrawLatex(x_text - 0.060, y + 0.020, "arXiv:2511.08212")
latex_leg.DrawLatex(x_text, y - 0.012, "#Delta m = 12 GeV, 100 fb^{-1} (13 TeV)")

# --- EXO-24-033, Δm = 25 GeV
y -= dy_sub
#b_exo_24_033_25 = ROOT.TPave(x_box1, y - box_h, x_box2, y + box_h, 1, "NDC")
b_exo_24_033_25 = ROOT.TPave(x_box1, y - box_h_leg, x_box2, y + box_h_leg, 1, "NDC")
b_exo_24_033_25.SetFillColorAlpha(col_exo_24_033_25, 0.18)
b_exo_24_033_25.SetLineColor(col_exo_24_033_25)
b_exo_24_033_25.SetLineWidth(2)
b_exo_24_033_25.Draw()
panel_objs.append(b_exo_24_033_25)

latex_leg.DrawLatex(x_text, y - 0.002, "#Delta m = 25 GeV, 100 fb^{-1} (13 TeV)")

# =============================================
# --- observed / expected legend
# =============================================
#y -= dy
y -= dy*0.65 #<-- adjusted to fit all four analyses in panel

# observed row
obs_line = ROOT.TLine(x_box1, y, x_box2, y)
obs_line.SetNDC()
obs_line.SetLineColor(ROOT.kBlack)
obs_line.SetLineStyle(1)
obs_line.SetLineWidth(3)
obs_line.Draw()
panel_objs.append(obs_line)

latex_leg.DrawLatex(x_text, y + 0.010, "Observed")
latex_leg.DrawLatex(x_text, y - 0.018, "exclusion 95% CL")

# expected row
#y -= dy * 0.72
y -= dy * 0.65 #<-- adjusted to fit all four analyses in panel

exp_line = ROOT.TLine(x_box1, y, x_box2, y)
exp_line.SetNDC()
exp_line.SetLineColor(ROOT.kBlack)
exp_line.SetLineStyle(2)
exp_line.SetLineWidth(3)
exp_line.Draw()
panel_objs.append(exp_line)

latex_leg.DrawLatex(x_text, y + 0.010, "Expected")
latex_leg.DrawLatex(x_text, y - 0.018, "exclusion 95% CL")

# --- CMS labels ---
latex_ndc = ROOT.TLatex()
latex_ndc.SetNDC()

latex_ndc.SetTextFont(62)
latex_ndc.SetTextSize(0.05)
latex_ndc.DrawLatex(0.14, 0.932, "CMS")

# latex_ndc.SetTextFont(42)
# latex_ndc.SetTextSize(0.04)
# latex_ndc.DrawLatex(0.55, 0.932, "138 fb^{-1} (13 TeV)")

latex_ndc.SetTextFont(42)
latex_ndc.SetTextSize(0.04)
latex_ndc.DrawLatex(0.85, 0.932, "June 2026")

latex_ndc.SetTextFont(42)
latex_ndc.SetTextSize(0.04)
latex_ndc.DrawLatex(
    0.705, 0.84,
    "pp #rightarrow #tilde{#chi}^{#pm}_{1}#tilde{#chi}^{0}_{2} #rightarrow WZ#tilde{#chi}^{0}_{1}#tilde{#chi}^{0}_{1}"
)

c.RedrawAxis()
c.Update()
c.Draw()
c.SaveAs("c1n2_v3.png")
c.SaveAs("c1n2_v3.pdf")
