////////////////////////////////////////////////////////////////
//@version=5
////////////////////////////////////////////////////////////////
// Author: A.Zerhouani
// Inspired from : shayankm, Rick3712, TradingView
// Source: https://github.com/azerhouani/TradingView_PineScripts
// Updated: 2022/05/01
// Version: 4.0
////////////////////////////////////////////////////////////////

indicator(title="Scalping STC+RSI+CCI+MA by AZer", shorttitle="Scalping_STC+RSI+CCI+MA_Azer", overlay=false, timeframe="", timeframe_gaps=true)

//////////////////////////////////////////////////
//// **** Offset and Coeficient settings **** ////
//////////////////////////////////////////////////
STC_offset = 500
RSI_offset = 100
RSI_coef   = 4
CCI_coef   = 2


//////////////////////////////////////////
//// **** STC | shorttitle="STC" **** //// source and inspiration : shayankm
//////////////////////////////////////////
// Group section
group_Stc = "[01]========[ STC ]====================================="

// Show section
stc__Show = input.bool(true, title="Show STC indicator ?", group=group_Stc)

// Input section
stc__Length = input(12, 'Length', group=group_Stc)
stc__FastLength = input(26, 'FastLength', group=group_Stc)
stc__SlowLength = input(50, 'SlowLength', group=group_Stc)

// Calculation section
stc__DiffFastSlow(BBB, stc__FastLength, stc__SlowLength) =>
    fastMA = ta.ema(BBB, stc__FastLength)
    slowMA = ta.ema(BBB, stc__SlowLength)
    stc__DiffFastSlow = fastMA - slowMA
    stc__DiffFastSlow

AAAAA(stc__Length, stc__FastLength, stc__SlowLength) =>
    // Input section
    AAA = input(0.5, group=group_Stc)
    
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
plot(           stc__Show ? mAAAAA  + STC_offset : na, color=mColor, title='STC', linewidth=2)

stc__ul = hline( stc__Show ? 25     + STC_offset : na, color=color.new(color.yellow, 0))
stc__ll = hline( stc__Show ? 75     + STC_offset : na, color=color.new(color.gray, 70))

fill(stc__ul, stc__ll, color=color.new(color.gray, 96))


//////////////////////////////////////////////////////////////
//// **** Relative Strength Index | shorttitle="RSI" **** //// source and inspiration : TradingView
//////////////////////////////////////////////////////////////

//@version=5
//indicator(title="Relative Strength Index", shorttitle="RSI", format=format.price, precision=2, timeframe="", timeframe_gaps=true)

// Group section
group_Rsi = "[02]========[ RSI ]====================================="

// Show section
rsi__Show = input.bool(true, title="Show RSI indicator ?", group=group_Rsi)

// Input section
rsi__Length = input.int(14, minval=1, title="RSI Length", group=group_Rsi)
rsi__Source = input.source(close, "RSI Source", group=group_Rsi)

rsi__ShowMA = input.bool(false, title="Show MA Line ?", group=group_Rsi)

rsi__MaType = input.string("EMA", title="MA Type", options=["SMA", "Bollinger Bands", "EMA", "SMMA (RMA)", "WMA", "VWMA"], group=group_Rsi)
rsi__MaLength = input.int(50, title="MA Length", group=group_Rsi)
rsi__bbMult = input.float(2.0, minval=0.001, maxval=50, title="MA BB StdDev", group=group_Rsi)

// Calculation section
rsi_cci__ma(source, length, type) =>
    switch type
        "SMA" => ta.sma(source, length)
        "Bollinger Bands" => ta.sma(source, length)
        "EMA" => ta.ema(source, length)
        "SMMA (RMA)" => ta.rma(source, length)
        "WMA" => ta.wma(source, length)
        "VWMA" => ta.vwma(source, length)

rsi__Up = ta.rma(math.max(ta.change(rsi__Source), 0), rsi__Length)
rsi__Down = ta.rma(-math.min(ta.change(rsi__Source), 0), rsi__Length)
rsi = rsi__Down == 0 ? 100 : rsi__Up == 0 ? 0 : 100 - (100 / (1 + rsi__Up / rsi__Down))
rsi__MA = rsi_cci__ma(rsi, rsi__MaLength, rsi__MaType)
isBB = rsi__MaType == "Bollinger Bands"

// Style section
rsi__pColor = (rsi > 50) ? color.green : color.red

// Plot section
plot(rsi__Show ?                    ( rsi     * RSI_coef ) + RSI_offset    : na, "RSI", color=rsi__pColor, linewidth=2)
plot(rsi__Show and rsi__ShowMA ?    ( rsi__MA * RSI_coef ) + RSI_offset    : na, "RSI-based MA", color=color.yellow)

rsi__UpperBand = hline( rsi__Show ? ( 70      * RSI_coef ) + RSI_offset    : na, "RSI Upper Band", color=#787B86)
hline(                  rsi__Show ? ( 50      * RSI_coef ) + RSI_offset    : na, "RSI Middle Band", color=#787B86, linestyle=hline.style_solid)
rsi__LowerBand = hline( rsi__Show ? ( 30      * RSI_coef ) + RSI_offset    : na, "RSI Lower Band", color=#787B86)

fill(rsi__UpperBand, rsi__LowerBand, color=color.rgb(126, 87, 194, 90), title="RSI Background Fill")

rsi__bbUpperBand = plot( (rsi__Show and isBB ) ? ((rsi__MA + ta.stdev(rsi, rsi__MaLength) * rsi__bbMult) * RSI_coef) + RSI_offset : na, title = "Upper Bollinger Band", color=color.green)
rsi__bbLowerBand = plot( (rsi__Show and isBB ) ? ((rsi__MA - ta.stdev(rsi, rsi__MaLength) * rsi__bbMult) * RSI_coef) + RSI_offset : na, title = "Lower Bollinger Band", color=color.green)

fill(rsi__bbUpperBand, rsi__bbLowerBand, color= isBB ? color.new(color.green, 90) : na, title="Bollinger Bands Background Fill")


////////////////////////////////////////////////////////////////////////
//// **** Commodity Channel Index + MA | shorttitle="CCI+MA" **** //// source and inspiration : Rick3712
////////////////////////////////////////////////////////////////////////

//@version=5
//indicator(title="Commodity Channel Index + MA", shorttitle="CCI+MA", format=format.price, precision=2, timeframe="", timeframe_gaps=true)

// Group section
group_CciMa = "[03]========[ CCI + MA ]================================"

// Show section
cci_ma__Show = input.bool(true, title="Show CCI indicator ?", group=group_CciMa)

// Input section
cci__Length     = input.int(40, minval=1, group=group_CciMa)
cci__Src        = input(hl2, title="CCI Source", group=group_CciMa)

cci__MaType     = input.string(title = "MA Type", defval = "EMA", options=["SMA", "EMA", "SMMA (RMA)", "WMA", "VWMA"], group=group_CciMa)
cci__MaLength   = input.int(title = "MA Length", defval = 13, minval = 1, maxval = 100, group=group_CciMa)

// Calculation section
cci__Sma = ta.sma(cci__Src, cci__Length)
cci = (cci__Src - cci__Sma) / (0.015 * ta.dev(cci__Src, cci__Length))

cci__Ma = rsi_cci__ma(cci, cci__MaLength, cci__MaType)

// Style section
cci__pColor = (cci > cci__Ma) ? color.green : color.red

// Plot section
plot(cci_ma__Show ? (cci__Ma / CCI_coef) : na, "MA", color=color.yellow)
plot(cci_ma__Show ? (cci     / CCI_coef) : na, "CCI", color=cci__pColor, linewidth=2)

cci_ma__UpperBand   = hline(cci_ma__Show ? (200  / CCI_coef) : na, color=color.red, linestyle=hline.style_dashed)
cci__UpperBand      = hline(cci_ma__Show ? (100  / CCI_coef) : na, "Upper Band", color=color.blue, linestyle=hline.style_dashed)
cci__BandZero       = hline(cci_ma__Show ? (0    / CCI_coef) : na, "Zero Band", linestyle=hline.style_dashed)
cci__LowerBand      = hline(cci_ma__Show ? (-100 / CCI_coef) : na, "Lower Band", color=color.blue, linestyle=hline.style_dashed)
cci_ma__LowerBand   = hline(cci_ma__Show ? (-200 / CCI_coef) : na, color=color.red, linestyle=hline.style_dashed)
fill(cci__UpperBand, cci__LowerBand, color=color.new(color.blue, 95), title="Background")
