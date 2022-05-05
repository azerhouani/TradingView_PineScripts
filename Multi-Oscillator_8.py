////////////////////////////////////////////////////////////////
//@version=5
////////////////////////////////////////////////////////////////
// Author: A.Zerhouani
// Inspired from : shayankm, LazyBear, RicardoSantos, Wborsa, TradingView
// Source: https://github.com/azerhouani/TradingView_PineScripts
// Updated: 2022/05/05
// Version: 5.0
////////////////////////////////////////////////////////////////

indicator(title="Multi-Oscillator 8 [RSI + StochRSI + Div + MFI + Highlighting + VWAP Z-Scope + MACD + STC + CCI] by AZer", shorttitle="Multi-Oscillator_8_[RSI+StochRSI+Div+MFI+Highlighting+VWAPZ+MACD+STC+CCI]_Azer", overlay=false, timeframe="", timeframe_gaps=true, explicit_plot_zorder=true)

//////////////////////////////////////////////////
//// **** Offset and Coeficient settings **** ////
//////////////////////////////////////////////////

CCI_coef                = 2     // divided by
CCI_offset              = 0

VWAPZ_coef              = 40    // multiplied by    
VWAPZ_offset            = 300  + CCI_offset

RsiStochRsiMfi_coef     = 6     // multiplied by
RsiStochRsiMfi_offset   = 150  + VWAPZ_offset

STC_coef                = 1.5   // multiplied by
STC_offset              = 600  + RsiStochRsiMfi_offset

MACD_coef               = 3     // multiplied by
MACD_offset             = 300  + STC_offset


////////////////////////////////////////////////////////////////////////

// Calculation section
rsi_cci__ma(source, length, type) =>
    switch type
        "SMA" => ta.sma(source, length)
        "Bollinger Bands" => ta.sma(source, length)
        "EMA" => ta.ema(source, length)
        "SMMA (RMA)" => ta.rma(source, length)
        "WMA" => ta.wma(source, length)
        "VWMA" => ta.vwma(source, length)


////////////////////////////////////////////////////////////////////////
//// **** Commodity Channel Index + MA | shorttitle="CCI+MA" **** ////// source and inspiration : TradingView
////////////////////////////////////////////////////////////////////////

//@version=5
//indicator(title="Commodity Channel Index + MA", shorttitle="CCI+MA", format=format.price, precision=2, timeframe="", timeframe_gaps=true)

// Group section
cci_ma__group = "[01]========[ CCI + MA ]================================"

// Show section
cci_ma__Show = input.bool(true, title="Show CCI indicator ?", group=cci_ma__group)

// Input section
cci__Length     = input.int(40, minval=1, group=cci_ma__group)
cci__Src        = input(hl2, title="CCI Source", group=cci_ma__group)

cci__MaType     = input.string(title = "MA Type", defval = "EMA", options=["SMA", "EMA", "SMMA (RMA)", "WMA", "VWMA"], group=cci_ma__group)
cci__MaLength   = input.int(title = "MA Length", defval = 13, minval = 1, maxval = 100, group=cci_ma__group)

// Calculation section
cci = ta.cci(cci__Src, cci__Length)
cci__Ma = rsi_cci__ma(cci, cci__MaLength, cci__MaType)

// Style section
cci__uppBandCol = color.new(#FF3366, 90) // red
cci__botBandCol = color.new(#33FF66, 90) // green
cci__pColor = (cci > cci__Ma) ? #33ff01 : #ff0155
//cci__pColor = (cci > cci__Ma) ? color.green : color.red

// Plot section
plot(cci_ma__Show ?                        ( cci__Ma / CCI_coef ) + CCI_offset : na, "MA", color=color.yellow)
plot(cci_ma__Show ?                        ( cci     / CCI_coef ) + CCI_offset : na, "CCI", color=cci__pColor, linewidth=2)

cci_ma__UpperBand   = hline(cci_ma__Show ? ( 200     / CCI_coef ) + CCI_offset : na,               color=cci__uppBandCol, linestyle=hline.style_solid)
cci__UpperBand      = hline(cci_ma__Show ? ( 100     / CCI_coef ) + CCI_offset : na, "Upper Band", color=cci__uppBandCol, linestyle=hline.style_solid)
cci__BandZero       = hline(cci_ma__Show ? ( 0       / CCI_coef ) + CCI_offset : na, "Zero Band",                         linestyle=hline.style_dotted)
cci__LowerBand      = hline(cci_ma__Show ? ( -100    / CCI_coef ) + CCI_offset : na, "Lower Band", color=cci__botBandCol, linestyle=hline.style_solid)
cci_ma__LowerBand   = hline(cci_ma__Show ? ( -200    / CCI_coef ) + CCI_offset : na,               color=cci__botBandCol, linestyle=hline.style_solid)

fill(cci_ma__UpperBand, cci__UpperBand, color=cci__uppBandCol,           title="UpperBackground")
fill(cci__UpperBand, cci__LowerBand,    color=color.new(color.blue, 95), title="MidleBackground")
fill(cci__LowerBand, cci_ma__LowerBand, color=cci__botBandCol,           title="LowerBackground")


/////////////////////////////////////////////////////
//// **** VWAP Z-Score | shorttitle="VWAPZ" **** //// source and inspiration : Wborsa
/////////////////////////////////////////////////////

//indicator("VWAP Z-Score", shorttitle="VWAPZ")

// Group section
vwapz__group = "[02]========[ VWAP Z-Score ]============================"

// Show section
vwapz__show = input(true, title="Show VWAP Z-Score ?", group=vwapz__group)

// Input section
vwapz__length1          = input(48,   title="VWAP1 Z-Score Lenght", group=vwapz__group)
vwapz__length2          = input(199,  title="VWAP2 Z-Score Lenght", group=vwapz__group)
vwapz__length3          = input(484,  title="VWAP3 Z-Score Lenght", group=vwapz__group)
vwapz__upperBandTop     = input(3.0,  title="VWAP Z-Score Upper Band Top", group=vwapz__group)
vwapz__upperBandBottom  = input(2.5,  title="VWAP Z-Score Upper Band Bottom", group=vwapz__group)
vwapz__lowerBandBottom  = input(-2.5, title="VWAP Z-Score Lower Band Bottom", group=vwapz__group)
vwapz__lowerBandTop     = input(-3.0, title="VWAP Z-Score Lower Band Top", group=vwapz__group)

// Calculation section
calc_vwapZ(pds) =>
    mean = math.sum(volume*close,pds)/math.sum(volume,pds)
    vwapsd = math.sqrt(ta.sma(math.pow(close-mean, 2), pds) )
    (close-mean)/vwapsd

// Style section
vwapz__uppBandCol = color.new(#FF3366, 80) // red
vwapz__botBandCol = color.new(#33FF66, 80) // green

// Plot section
vwapz__ul1 = hline(vwapz__show ?          ( vwapz__upperBandTop    * VWAPZ_coef ) + VWAPZ_offset : na, "Upper Band Top",    color=vwapz__uppBandCol, linestyle=hline.style_solid)
vwapz__ul2 = hline(vwapz__show ?          ( vwapz__upperBandBottom * VWAPZ_coef ) + VWAPZ_offset : na, "Upper Band Bottom", color=vwapz__uppBandCol, linestyle=hline.style_solid)
fill(vwapz__ul1, vwapz__ul2, color=vwapz__uppBandCol)

vwapz__ll1 = hline(vwapz__show ?          ( vwapz__lowerBandTop    * VWAPZ_coef ) + VWAPZ_offset : na, "Lower Band Top",    color=vwapz__botBandCol, linestyle=hline.style_solid)
vwapz__ll2 = hline(vwapz__show ?          ( vwapz__lowerBandBottom * VWAPZ_coef ) + VWAPZ_offset : na, "Lower Band Bottom", color=vwapz__botBandCol, linestyle=hline.style_solid)
fill(vwapz__ll1, vwapz__ll2, color=vwapz__botBandCol)

fill(vwapz__ul2, vwapz__ll1, color=color.rgb(33, 150, 243, 95))

vwapz__Line1 = calc_vwapZ(vwapz__length1)
vwapz__Line2 = calc_vwapZ(vwapz__length2)
vwapz__Line3 = calc_vwapZ(vwapz__length3)

plot(vwapz__show ?                 ( vwapz__Line1 *           VWAPZ_coef ) + VWAPZ_offset : na,title="ZVWAP1", color=#2196f3, linewidth=1)
plot(vwapz__show ?                 ( vwapz__Line2 *           VWAPZ_coef ) + VWAPZ_offset : na,title="ZVWAP2", color=#673ab7, linewidth=1)
plot(vwapz__show ?                 ( vwapz__Line3 *           VWAPZ_coef ) + VWAPZ_offset : na,title="ZVWAP3", color=#e91e63, linewidth=1)


//////////////////////////////////////////////////////////////
//// **** Relative Strength Index | shorttitle="RSI" **** //// source and inspiration : TradingView
//////////////////////////////////////////////////////////////

//@version=5
//indicator(title="Relative Strength Index", shorttitle="RSI", format=format.price, precision=2, timeframe="", timeframe_gaps=true)

// Group section
rsi__group = "[03]========[ RSI ]====================================="

// Show section
rsi__Show = input.bool(true, title="Show RSI indicator ?", group=rsi__group)

// Input section
rsi__Length     = input.int(14, minval=1, title="RSI Length", group=rsi__group)
rsi__Source     = input.source(close, "RSI Source", group=rsi__group)

rsi__ShowMA     = input.bool(false, title="Show MA Line ?", group=rsi__group)

rsi__MaType     = input.string("EMA", title="MA Type", options=["SMA", "Bollinger Bands", "EMA", "SMMA (RMA)", "WMA", "VWMA"], group=rsi__group)
rsi__MaLength   = input.int(50, title="MA Length", group=rsi__group)
rsi__bbMult     = input.float(2.0, minval=0.001, maxval=50, title="MA BB StdDev", group=rsi__group)

// Calculation section
rsi__Up     = ta.rma(math.max(ta.change(rsi__Source), 0), rsi__Length)
rsi__Down   = ta.rma(-math.min(ta.change(rsi__Source), 0), rsi__Length)
rsi         = rsi__Down == 0 ? 100 : rsi__Up == 0 ? 0 : 100 - (100 / (1 + rsi__Up / rsi__Down))
rsi__MA     = rsi_cci__ma(rsi, rsi__MaLength, rsi__MaType)
isBB        = rsi__MaType == "Bollinger Bands"

// Style section
rsi__pColor = (rsi > 50) ? #33ff01 : #ff0155
//rsi__pColor = (rsi > 50) ? color.green : color.red


//////////////////////////////////////////////////////////
//// **** Stochastic RSI | shorttitle="StochRSI" **** //// source and inspiration : TradingView
//////////////////////////////////////////////////////////

//indicator(title="Stochastic RSI", shorttitle="StochRSI", format=format.price, precision=2, timeframe="", timeframe_gaps=true)

// Group section
stochRsi__group = "[04+05]========[ Stochastic RSI + Divergence ]=========="

// Show section
stochRsi__show = input.bool(true, title="Show stochastic RSI indicator ?", group=stochRsi__group)

// Input section
stochRsi__SmoothK       = input.int(3, "Stoch Smooth K", minval=1, group=stochRsi__group)
stochRsi__SmoothD       = input.int(3, "Stoch Smooth D", minval=1, group=stochRsi__group)
stochRsi__RsiLength     = input.int(14, "RSI Length", minval=1, group=stochRsi__group)
stochRsi__StochLength   = input.int(14, "Stochastic Length", minval=1, group=stochRsi__group)
stochRsi__RsiSrc        = input(close, title="RSI Source", group=stochRsi__group)

// Style section
stochRsi__kLineColor = #ffe001 // Yellow
stochRsi__dLineColor = #c701ff // Pink/Violet

// Calculation section
stochRsi__rsi1  = ta.rsi(stochRsi__RsiSrc, stochRsi__RsiLength)
stochRsi__K     = ta.sma(ta.stoch(stochRsi__rsi1, stochRsi__rsi1, stochRsi__rsi1, stochRsi__StochLength), stochRsi__SmoothK)
stochRsi__d     = ta.sma(stochRsi__K, stochRsi__SmoothD)


/////////////////////////////////////////////////
//// **** Divergence | shorttitle="Div" **** ////  source and inspiration : RicardoSantos
/////////////////////////////////////////////////

// Show section
diverg__show = input(true, title="Show Divergences on StochRSI ?", group=stochRsi__group)

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

high_prev   = ta.valuewhen(fractal_top, stochRsi__K[2], 0)[2]
high_price  = ta.valuewhen(fractal_top, high[2], 0)[2]
low_prev    = ta.valuewhen(fractal_bot, stochRsi__K[2], 0)[2]
low_price   = ta.valuewhen(fractal_bot, low[2], 0)[2]

regular_bearish_div = fractal_top and high[2] > high_price and stochRsi__K[2] < high_prev
regular_bullish_div = fractal_bot and low[2] < low_price and stochRsi__K[2] > low_prev

// Style section
col1 = regular_bearish_div ? color.red : na
col2 = regular_bullish_div ? color.green : na


///////////////////////////////////////////////////////
//// **** Money Flow Index | shorttitle="MFI" **** //// source and inspiration : TradingView
///////////////////////////////////////////////////////

//indicator(title="Money Flow Index", shorttitle="MFI", format=format.price, precision=2, timeframe="", timeframe_gaps=true)

// Group section
mfi__group = "[06]========[ Money Flow Index ]========================"

// Show section
mfi__show   = input.bool(true, title="Show MFI indicator ?", group=mfi__group)
mfi__Length = input.int(title="MFI Length", defval=12, minval=1, maxval=2000, group=mfi__group)

// Style section
mfi__Color = #00FFFF

// Calculation section
mfi__Src = hlc3
mfi      = ta.mfi(mfi__Src, mfi__Length)


//////////////////////////////////////////////////////////////////////////////
//// **** Backgroud and Highlighting of : RSI + StochRSI + MFI Bands **** ////
//////////////////////////////////////////////////////////////////////////////

rsiStochRsiMfi__Band100 = hline((stochRsi__show or mfi__show or rsi__Show) ? ( 100 * RsiStochRsiMfi_coef) + RsiStochRsiMfi_offset : na, "Band 100", color=#787B86, display=display.none)
rsiStochRsiMfi__Band80  = hline((stochRsi__show or mfi__show or rsi__Show) ? ( 80  * RsiStochRsiMfi_coef) + RsiStochRsiMfi_offset : na, "Band 80",  color=#787B86, linestyle=hline.style_dotted)
rsiStochRsiMfi__Band70  = hline((stochRsi__show or mfi__show or rsi__Show) ? ( 70  * RsiStochRsiMfi_coef) + RsiStochRsiMfi_offset : na, "Band 70",  color=#787B86, linestyle=hline.style_dotted)
rsiStochRsiMFI__Band50  = hline((stochRsi__show or mfi__show or rsi__Show) ? ( 50  * RsiStochRsiMfi_coef) + RsiStochRsiMfi_offset : na, "Band 50",  color=#787B86)
rsiStochRsiMFI__Band30  = hline((stochRsi__show or mfi__show or rsi__Show) ? ( 30  * RsiStochRsiMfi_coef) + RsiStochRsiMfi_offset : na, "Band 30",  color=#787B86, linestyle=hline.style_dotted)
rsiStochRsiMFI__Band20  = hline((stochRsi__show or mfi__show or rsi__Show) ? ( 20  * RsiStochRsiMfi_coef) + RsiStochRsiMfi_offset : na, "Band 20",  color=#787B86, linestyle=hline.style_dotted)
rsiStochRsiMFI__Band0   = hline((stochRsi__show or mfi__show or rsi__Show) ? ( 0   * RsiStochRsiMfi_coef) + RsiStochRsiMfi_offset : na, "Band 0",   color=#787B86, display=display.none)

// Style section
highLight_BullColor = color.fuchsia
highLight_BearColor = color.lime

highLight_BgColor = if (mfi >= 80) and (stochRsi__K >= 80) and (rsi >= 80)
    color.from_gradient(math.min(rsi, stochRsi__K, mfi), 80, 100, color.new(highLight_BullColor, 75), highLight_BullColor)
else if (mfi <= 20) and (stochRsi__K <= 20) and (rsi <= 35)
    color.from_gradient(mfi, 0, 20, highLight_BearColor, color.new(highLight_BearColor, 75))
else
    color.rgb(33, 150, 243, 95)

fill(rsiStochRsiMFI__Band0, rsiStochRsiMfi__Band100, color=highLight_BgColor, title="Background")


/////////////////////////////////////////////////////////////////
//// **** Plot section for : RSI + StochRSI + MFI Bands **** ////
/////////////////////////////////////////////////////////////////

//---------------------------------
// [RSI] Plot section
//---------------------------------
plot(rsi__Show ?                    ( rsi     * RsiStochRsiMfi_coef ) + RsiStochRsiMfi_offset    : na, "RSI",          color=rsi__pColor, linewidth=2)
plot(rsi__Show and rsi__ShowMA ?    ( rsi__MA * RsiStochRsiMfi_coef ) + RsiStochRsiMfi_offset    : na, "RSI-based MA", color=color.yellow)

rsi__bbUpperBand = plot( (rsi__Show and isBB ) ? ((rsi__MA + ta.stdev(rsi, rsi__MaLength) * rsi__bbMult) * RsiStochRsiMfi_coef) + RsiStochRsiMfi_offset : na, title = "Upper Bollinger Band", color=color.green)
rsi__bbLowerBand = plot( (rsi__Show and isBB ) ? ((rsi__MA - ta.stdev(rsi, rsi__MaLength) * rsi__bbMult) * RsiStochRsiMfi_coef) + RsiStochRsiMfi_offset : na, title = "Lower Bollinger Band", color=color.green)

fill(rsi__bbUpperBand, rsi__bbLowerBand, color= isBB ? color.new(color.green, 90) : na, title="Bollinger Bands Background Fill")

//---------------------------------
// [Stochastic RSI] Plot section
//---------------------------------
plot(stochRsi__show ? stochRsi__K * RsiStochRsiMfi_coef + RsiStochRsiMfi_offset : na, "K", color=stochRsi__kLineColor)
plot(stochRsi__show ? stochRsi__d * RsiStochRsiMfi_coef + RsiStochRsiMfi_offset : na, "D", color=stochRsi__dLineColor)

//---------------------------------
// [Divergence] Plot section
//---------------------------------
plot((stochRsi__show and diverg__show and fractal_top) ?                stochRsi__K[2] * RsiStochRsiMfi_coef + RsiStochRsiMfi_offset : na, title="Bullish", color=col1, linewidth=2, offset=-2)
plot((stochRsi__show and diverg__show and fractal_bot) ?                stochRsi__K[2] * RsiStochRsiMfi_coef + RsiStochRsiMfi_offset : na, title="Brearish", color=col2, linewidth=2, offset=-2)

//plotshape((stochRsi__show and diverg__show and regular_bearish_div) ? stochRsi__K[2] * RsiStochRsiMfi_coef + RsiStochRsiMfi_offset : na, text='D', title='+RBD', style=shape.labeldown, location=location.absolute, color=color.red, textcolor=color.white, offset=-2)
//plotshape((stochRsi__show and diverg__show and regular_bullish_div) ? stochRsi__K[2] * RsiStochRsiMfi_coef + RsiStochRsiMfi_offset : na, text='U', title='-RBD', style=shape.labelup, location=location.absolute, color=color.green, textcolor=color.white, offset=-2)

//---------------------------------
// [MFI] Plot section
//---------------------------------
plot(mfi__show ? mfi * RsiStochRsiMfi_coef + RsiStochRsiMfi_offset : na, "MF", color=mfi__Color)


//////////////////////////////////////////
//// **** STC | shorttitle="STC" **** //// source and inspiration : shayankm
//////////////////////////////////////////
// Group section
stc__group = "[07]========[ STC ]====================================="

// Show section
stc__Show = input.bool(true, title="Show STC indicator ?", group=stc__group)

// Input section
stc__Length     = input(12, 'Length', group=stc__group)
stc__FastLength = input(26, 'FastLength', group=stc__group)
stc__SlowLength = input(50, 'SlowLength', group=stc__group)

// Calculation section
stc__DiffFastSlow(BBB, stc__FastLength, stc__SlowLength) =>
    fastMA = ta.ema(BBB, stc__FastLength)
    slowMA = ta.ema(BBB, stc__SlowLength)
    stc__DiffFastSlow = fastMA - slowMA
    stc__DiffFastSlow

AAAAA(stc__Length, stc__FastLength, stc__SlowLength) =>
    // Input section
    AAA = input(0.5, group=stc__group)
    
    var CCCCC = 0.0
    var DDD = 0.0
    var DDDDDD = 0.0
    var EEEEE = 0.0
    BBBBBB = stc__DiffFastSlow(close, stc__FastLength, stc__SlowLength)
    CCC = ta.lowest(BBBBBB, stc__Length)
    CCCC = ta.highest(BBBBBB, stc__Length) - CCC
    CCCCC := CCCC > 0 ? (BBBBBB - CCC) / CCCC * 100 : nz(CCCCC[1])
    DDD := na(DDD[1]) ? CCCCC : DDD[1] + AAA * (CCCCC - DDD[1])
    DDDD = ta.lowest(DDD, stc__Length)
    DDDDD = ta.highest(DDD, stc__Length) - DDDD
    DDDDDD := DDDDD > 0 ? (DDD - DDDD) / DDDDD * 100 : nz(DDDDDD[1])
    EEEEE := na(EEEEE[1]) ? DDDDDD : EEEEE[1] + AAA * (DDDDDD - EEEEE[1])
    EEEEE

// Style section
mAAAAA = AAAAA(stc__Length, stc__FastLength, stc__SlowLength)
mColor = mAAAAA > mAAAAA[1] ? color.new(color.green, 20) : color.new(color.red, 20)

// Alert section
//if mAAAAA[3] <= mAAAAA[2] and mAAAAA[2] > mAAAAA[1] and mAAAAA > 75
//    alert("Red", alert.freq_once_per_bar)
//if mAAAAA[3] >= mAAAAA[2] and mAAAAA[2] < mAAAAA[1] and mAAAAA < 25
//    alert("Green", alert.freq_once_per_bar)

// Plot section
plot(            stc__Show ? ( mAAAAA * STC_coef ) + STC_offset : na, color=mColor, title='STC', linewidth=2)

stc__ul = hline( stc__Show ? ( 25     * STC_coef ) + STC_offset : na, color=color.new(color.yellow, 0))
stc__ll = hline( stc__Show ? ( 75     * STC_coef ) + STC_offset : na, color=color.new(color.gray, 70))

fill(stc__ul, stc__ll, color=color.new(color.gray, 96))


/////////////////////////////////////////////////////////////////////////////
//// **** Moving Average Convergence Divergence | shorttitle="MACD" **** //// source and inspiration : TradingView
/////////////////////////////////////////////////////////////////////////////

// Group section
macd__group = "[08]========[ MACD ]===================================="

// Show section
macd__show = input(true, title="Show MACD ?", group=macd__group)

// Input section
macd__src           = input(title="Source", defval=close, group=macd__group)
macd__fast_length   = input(title="Fast Length", defval=12, group=macd__group)
macd__slow_length   = input(title="Slow Length", defval=26, group=macd__group)
macd__signal_length = input.int(title="Signal Smoothing",  minval = 1, maxval = 50, defval = 9, group=macd__group)
macd__sma_source    = input.string(title="Oscillator MA Type",  defval="EMA", options=["SMA", "EMA"], group=macd__group)
macd__sma_signal    = input.string(title="Signal Line MA Type", defval="EMA", options=["SMA", "EMA"], group=macd__group)

// Style section
macd__color            = #2962FF // color.blue
macd__signal_color     = #FF6D00 // color.orange
macd__grow_above_color = #26A69A // color.green strong
macd__fall_above_color = #B2DFDB // color.green weak
macd__grow_below_color = #FFCDD2 // color.red weak
macd__fall_below_color = #FF5252 // color.red strong

// Calculation section
macd__fast_ma = macd__sma_source == "SMA" ? ta.sma(macd__src, macd__fast_length) : ta.ema(macd__src, macd__fast_length)
macd__slow_ma = macd__sma_source == "SMA" ? ta.sma(macd__src, macd__slow_length) : ta.ema(macd__src, macd__slow_length)
macd = macd__fast_ma - macd__slow_ma
macd__signal = macd__sma_signal == "SMA" ? ta.sma(macd, macd__signal_length) : ta.ema(macd, macd__signal_length)
macd__hist = macd - macd__signal

//================================
//Normalize Function when min/max unknown
normalize(_src, _min, _max) => 
    // Normalizes series with unknown min/max using historical min/max.
    // _src: series to rescale.
    // _min: minimum value of rescaled series.
    // _max: maximum value of rescaled series.
    var _historicMin = +10e10
    var _historicMax = -10e10
    _historicMin := math.min(nz(_src, _historicMin), _historicMin)
    
    //_historicMax := math.max(nz(_src, _historicMax), _historicMax)
    _historicMax := _historicMin - (_historicMin * 2)
    
    _min + (_max - _min) * (_src - _historicMin) / math.max(_historicMax - _historicMin, 10e-10)
//================================

// Scaling section
hist_scaled = normalize(macd__hist, -70.0, 70.0)
macd_scaled = normalize(macd, -50.0, 50.0)
//sign_scaled = macd_scaled - hist_scaled


// Plot section
plot(  macd__show ? ( hist_scaled * MACD_coef ) + MACD_offset : na, title="Histogram", histbase=MACD_offset, style=plot.style_columns, color=(macd__hist>=0 ? (macd__hist[1] < macd__hist ? macd__grow_above_color : macd__fall_above_color) : (macd__hist[1] < macd__hist ? macd__grow_below_color : macd__fall_below_color)))
plot(  macd__show ? ( macd_scaled * MACD_coef ) + MACD_offset : na, title="MACD", color=color.yellow, linewidth=1)

hline( macd__show ? MACD_offset : na, "MACD Histogram Base", color=color.new(color.gray, 80))

//plot(macd__show ? (sign_scaled * MACD_coef ) + MACD_offset : na, title="Signal", color=macd__signal_color)

