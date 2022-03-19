////////////////////////////////////////////////////////////////
//@version=5
////////////////////////////////////////////////////////////////
// Author: A.Zerhouani
// Inspired from : tradingview, LazyBear, RicardoSantos
// Source: https://github.com/azerhouani/TradingView_PineScripts
// Updated: 2022/03/19
// Version: 4.0
////////////////////////////////////////////////////////////////

indicator(title="Stochastic RSI + Divergence + Money Flow Index + VWAP Z-Scope by AliZer", shorttitle="StochRSI+Div+MFI+VWAPZ_Azer", overlay=false, timeframe="", timeframe_gaps=true)

//////////////////////////////////////////////////
//// **** Offset and Coeficient settings **** ////
//////////////////////////////////////////////////
stochRsiMFI_offset = 40
vwapz_coeficient = 10

//////////////////////////////////////////////////////////
//// **** Stochastic RSI | shorttitle="StochRSI" **** ////
//////////////////////////////////////////////////////////

//indicator(title="Stochastic RSI", shorttitle="StochRSI", format=format.price, precision=2, timeframe="", timeframe_gaps=true)

// Group section
gStochRsi = "[01]========[ Stochastic RSI ]=========================="

// Show section
showStochRsi = input.bool(true, title="Show stochastic RSI indicator ?", group=gStochRsi)

// Input section
stochRsi__SmoothK = input.int(3, "Stoch Smooth K", minval=1, group=gStochRsi)
stochRsi__SmoothD = input.int(3, "Stoch Smooth D", minval=1, group=gStochRsi)
stochRsi__RsiLength = input.int(14, "RSI Length", minval=1, group=gStochRsi)
stochRsi__StochLength = input.int(14, "Stochastic Length", minval=1, group=gStochRsi)
stochRsi__RsiSrc = input(close, title="RSI Source", group=gStochRsi)

// Style section
kLineColor = #ffe001
dLineColor = #fc0518

// Calculation section
stochRsi__rsi1 = ta.rsi(stochRsi__RsiSrc, stochRsi__RsiLength)
stochRsi__K = ta.sma(ta.stoch(stochRsi__rsi1, stochRsi__rsi1, stochRsi__rsi1, stochRsi__StochLength), stochRsi__SmoothK)
stochRsi__d = ta.sma(stochRsi__K, stochRsi__SmoothD)

// Plot section
plot(showStochRsi ? stochRsi__K + stochRsiMFI_offset : na, "K", color=kLineColor)
plot(showStochRsi ? stochRsi__d + stochRsiMFI_offset : na, "D", color=dLineColor)

/////////////////////////////////////////////////
//// **** Divergence | shorttitle="Div" **** ////
/////////////////////////////////////////////////

// Show section
showDiverg = input(true, title="Show Divergences on StochRSI ?", group=gStochRsi)

// Calculation section
f_top_fractal(_src)=>_src[4] < _src[2] and _src[3] < _src[2] and _src[2] > _src[1] and _src[2] > _src[0]
f_bot_fractal(_src)=>_src[4] > _src[2] and _src[3] > _src[2] and _src[2] < _src[1] and _src[2] < _src[0]
f_fractalize(_src)=>
    _var_top = f_top_fractal(_src)
    _var_bot = f_bot_fractal(_src)
    if(_var_top)
        1
    else if(_var_bot)
        -1
    else
        0

fractal_top = f_fractalize(stochRsi__K) > 0 ? stochRsi__K[2] : na
fractal_bot = f_fractalize(stochRsi__K) < 0 ? stochRsi__K[2] : na

high_prev = ta.valuewhen(fractal_top, stochRsi__K[2], 0)[2]
high_price = ta.valuewhen(fractal_top, high[2], 0)[2]
low_prev = ta.valuewhen(fractal_bot, stochRsi__K[2], 0)[2]
low_price = ta.valuewhen(fractal_bot, low[2], 0)[2]

regular_bearish_div = fractal_top and high[2] > high_price and stochRsi__K[2] < high_prev
regular_bullish_div = fractal_bot and low[2] < low_price and stochRsi__K[2] > low_prev

// Style section
col1 = regular_bearish_div ? color.red : na
col2 = regular_bullish_div ? color.green : na

// Plot section
plot((showStochRsi and showDiverg and fractal_top) ? stochRsi__K[2] + stochRsiMFI_offset : na, title="Bullish", color=col1, linewidth=2, offset=-2)
plot((showStochRsi and showDiverg and fractal_bot) ? stochRsi__K[2] + stochRsiMFI_offset : na, title="Brearish", color=col2, linewidth=2, offset=-2)

plotshape((showStochRsi and showDiverg and regular_bearish_div) ? stochRsi__K[2] + stochRsiMFI_offset : na, text='D', title='+RBD', style=shape.labeldown, location=location.absolute, color=color.red, textcolor=color.white, offset=-2)
plotshape((showStochRsi and showDiverg and regular_bullish_div) ? stochRsi__K[2] + stochRsiMFI_offset : na, text='U', title='-RBD', style=shape.labelup, location=location.absolute, color=color.green, textcolor=color.white, offset=-2)

///////////////////////////////////////////////////////
//// **** Money Flow Index | shorttitle="MFI" **** ////
///////////////////////////////////////////////////////

//indicator(title="Money Flow Index", shorttitle="MFI", format=format.price, precision=2, timeframe="", timeframe_gaps=true)

// Group section
gMfi = "[02]========[ Money Flow Index ]========================"

// Show section
showMfi = input.bool(true, title="Show MFI indicator ?", group=gMfi)
mfiLength = input.int(title="MFI Length", defval=12, minval=1, maxval=2000, group=gMfi)

// Style section
mfiColor = #00FFFF

// Calculation section
mfiSrc = hlc3
mfi = ta.mfi(mfiSrc, mfiLength)

// Plot section
plot(showMfi ? mfi + stochRsiMFI_offset : na, "MF", color=mfiColor)

//////////////////////////////////////////
//// **** StochRSI and MFI Bands **** ////
//////////////////////////////////////////

stochRsiMfi__UBand = hline((showStochRsi or showMfi) ? 80 + stochRsiMFI_offset : na, "Upper Band", color=#787B86)
stochRsiMFI__LBand = hline((showStochRsi or showMfi) ? 20 + stochRsiMFI_offset : na, "Lower Band", color=#787B86)
fill(stochRsiMfi__UBand, stochRsiMFI__LBand, color=color.rgb(33, 150, 243, 95), title="Background")

/////////////////////////////////////////////////////
//// **** VWAP Z-Score | shorttitle="VWAPZ" **** ////
/////////////////////////////////////////////////////

//indicator("VWAP Z-Score", shorttitle="VWAPZ")

// Group section
gVwapz = "[03]========[ VWAP Z-Score ]============================"

// Show section
showVwapz = input(true, title="Show VWAP Z-Score ?", group=gVwapz)

// Input section
vwapz__length1 = input(48,  title="VWAP1 Z-Score Lenght", group=gVwapz)
vwapz__length2 = input(199, title="VWAP2 Z-Score Lenght", group=gVwapz)
vwapz__length3 = input(484, title="VWAP3 Z-Score Lenght", group=gVwapz)
vwapz__upperBandTop     = input(3.0,  title="VWAP Z-Score Upper Band Top", group=gVwapz)
vwapz__upperBandBottom  = input(2.5,  title="VWAP Z-Score Upper Band Bottom", group=gVwapz)
vwapz__lowerBandBottom  = input(-2.5, title="VWAP Z-Score Lower Band Bottom", group=gVwapz)
vwapz__lowerBandTop     = input(-3.0, title="VWAP Z-Score Lower Band Top", group=gVwapz)

// Calculation section
calc_vwapZ(pds) =>
    mean = math.sum(volume*close,pds)/math.sum(volume,pds)
    vwapsd = math.sqrt(ta.sma(math.pow(close-mean, 2), pds) )
    (close-mean)/vwapsd

// Style section
vwapz__uppBandCol = color.new(#FF3366, 80) // red
vwapz__botBandCol = color.new(#33FF66, 80) // green

// Plot section
ul1=hline(showVwapz ? (vwapz__upperBandTop * vwapz_coeficient) : na, "Upper Band Top", color=vwapz__uppBandCol)
ul2=hline(showVwapz ? (vwapz__upperBandBottom * vwapz_coeficient) : na, "Upper Band Bottom", color=vwapz__uppBandCol)
fill(ul1, ul2, color=vwapz__uppBandCol)

ll1=hline(showVwapz ? (vwapz__lowerBandTop * vwapz_coeficient) : na, "Lower Band Top", color=vwapz__botBandCol)
ll2=hline(showVwapz ? (vwapz__lowerBandBottom * vwapz_coeficient) : na, "Lower Band Bottom", color=vwapz__botBandCol)
fill(ll1, ll2, color=vwapz__botBandCol)

vwapz_UpBand = hline(showVwapz ? (vwapz__lowerBandBottom * vwapz_coeficient) : na, "Lower Band Bottom")
vwapz_LoBand = hline(showVwapz ? (vwapz__upperBandBottom * vwapz_coeficient) : na, "Upper Band Bottom")
fill(vwapz_UpBand, vwapz_LoBand, color=color.rgb(33, 150, 243, 95))

vwapz__Line1 = calc_vwapZ(vwapz__length1)
vwapz__Line2 = calc_vwapZ(vwapz__length2)
vwapz__Line3 = calc_vwapZ(vwapz__length3)

plot(showVwapz ? (vwapz__Line1 * vwapz_coeficient) : na,title="ZVWAP1", color=#2196f3, linewidth=1)
plot(showVwapz ? (vwapz__Line2 * vwapz_coeficient) : na,title="ZVWAP2", color=#673ab7, linewidth=1)
plot(showVwapz ? (vwapz__Line3 * vwapz_coeficient) : na,title="ZVWAP3", color=#e91e63, linewidth=1)

