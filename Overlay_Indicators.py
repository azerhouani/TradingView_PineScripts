////////////////////////////////////////////////////////////////
//@version=5
////////////////////////////////////////////////////////////////
// Author: A.Zerhouani
// Inspired from : TradingView, juanmirocks, Belkhayate, drsweets, PatekCharts1, dysrupt
// Source: https://github.com/azerhouani/TradingView_PineScripts
// Updated: 2022/03/17
// Version: 12.0
////////////////////////////////////////////////////////////////

indicator(title="Pivot lines + 4 EMA + EmaTrend + Bollinger bands + VWAP 4 lines + VWAP bands + Ichimoku Cloud by AZer", shorttitle="PP+4EMA+EmaTrend+VWAP4L+VWAPB+Ichimoku_Azer", overlay=true)

/////////////////////////////////////////////////
//// **** Pivot lines | shorttitle="PP" **** ////
/////////////////////////////////////////////////
// Pivot Points indicator, calculated in the "traditional" way, also called "floor-trader pivots".
// Additionally, and optional to the user, the halves between the key levels are also shown.
// The Default chosen Time Frame to calculate the pivot points is: 
//      Daily (D) if within intraday
//      Weekly (W) if within daily chart
//      Monthly (M) if within weekly chart
//      3 Months (3M) if within monthly chart
// Advantages over TV's indicator "Pivot Points Standard"
//      1. Show pivot lines for all history, which lets you gauge trading strategies throughout time
//      2. More sensible Default/Auto time frame; e.g. on intradays only and always the market values of yesterday's Day are used
//      3. The halves between the key levels are also shown, which it's useful for some trading strategies
//      4. Arguably out-of-the-box nicer interface
///////////////////////////////

// Group section
gPivotLines = "[01]========[ Pivot lines ]============================="

// Show section
showPivotLines = input.bool(true, title="Show Pivot lines ?", group=gPivotLines)
pivotLineInputInfo = "Select one of the following Time Frame to calculate the pivot points :\n+ D (default) for Daily, if within intraday\n+ W for Weekly, if within daily chart\n+ M for Monthly, if within weekly chart\n+ 3M for 3 Months, if within monthly chart"

defaultTimeFrame = ((timeframe.isintraday) ? "D" : ((timeframe.isdaily) ? "W" : ((timeframe.isweekly) ? "M" : "3M")))
inputTimeFrame = input.string(title="Time Frame", defval="D", options=["D", "W", "M", "3M"], group=gPivotLines, tooltip=pivotLineInputInfo)
chosenTimeFrame = (inputTimeFrame == "Default") ? defaultTimeFrame : inputTimeFrame

getSeries(e) => request.security(syminfo.tickerid, chosenTimeFrame, e, lookahead=barmerge.lookahead_on)

// Calculation section
H = getSeries(high[1])
L = getSeries(low[1])
C = getSeries(close[1])

// Main Pivot
P = (H + L + C) / 3

// yesterday's closing
YC = C

// Resistence Levels
R3 = H + 2*(P - L)
R2 = P + (H - L)
R1 = (P * 2) - L
// Support Levels
S1 = (P * 2) - H
S2 = P - (H - L)
S3 = L - 2*(H - P)

// Optional Halves between Resistence levels
R2_5 = (R2 + R3) / 2 //aka R2.5
R1_5 = (R1 + R2) / 2 //aka R1.5
R0_5 = (P + R1) / 2 //aka R0.5

// Optional Halves between Support levels
S0_5 = (P + S1) / 2 //aka S0.5
S1_5 = (S1 + S2) / 2 //aka S1.5
S2_5 = (S2 + S3) / 2 //aka S2.5


// Style section
pColor = #0053ff // color.blue
ycColor = #fcff00 // color.yellow
pivotLinesTransp = 50 //Pivot lines transparency
fillPivotClosingTransp = 90 //Transparency between Pivot and Yesterday's closing

rMainLevelColor = color.new(#FF1800, pivotLinesTransp) //color.red
rHalfLevelColor = color.new(#FF1800, pivotLinesTransp + 10) //color.red

sMainLevelColor = color.new(#00AE47, pivotLinesTransp) //color.green
sHalfLevelColor = color.new(#00AE47, pivotLinesTransp + 10) //color.green

widthOfMainLevels = 1
widthOfHalfLevels = 1

lineStyle = plot.style_circles
pivotStyle = plot.style_linebr


// Plot section
plot(showPivotLines ? R3 : na, title="R3", color=rMainLevelColor, linewidth=widthOfMainLevels, style=lineStyle)
plot(showPivotLines ? R2 : na, title="R2", color=rMainLevelColor, linewidth=widthOfMainLevels, style=lineStyle)
plot(showPivotLines ? R1 : na, title="R1", color=rMainLevelColor, linewidth=widthOfMainLevels, style=lineStyle)

pivotPlot = plot(showPivotLines ? P : na, title="Pivot", color=pColor, linewidth=widthOfMainLevels, style=pivotStyle)
closePlot = plot(showPivotLines ? YC : na, title="Yesterday's closing", color=ycColor, linewidth=widthOfMainLevels, style=pivotStyle)
fill(pivotPlot, closePlot, YC > P ? color.new(color.green, fillPivotClosingTransp) : color.new(color.red, fillPivotClosingTransp), title="Daily Trend Background (Pivot based)")

plot(showPivotLines ? S1 : na, title="S1", color=sMainLevelColor, linewidth=widthOfMainLevels, style=lineStyle)
plot(showPivotLines ? S2 : na, title="S2", color=sMainLevelColor, linewidth=widthOfMainLevels, style=lineStyle)
plot(showPivotLines ? S3 : na, title="S3", color=sMainLevelColor, linewidth=widthOfMainLevels, style=lineStyle)

plot(showPivotLines ? R2_5 : na, title="R2.5", color=rHalfLevelColor, linewidth=widthOfHalfLevels, style=lineStyle, display=display.none)
plot(showPivotLines ? R1_5 : na, title="R1.5", color=rHalfLevelColor, linewidth=widthOfHalfLevels, style=lineStyle, display=display.none)
plot(showPivotLines ? R0_5 : na, title="R0.5", color=rHalfLevelColor, linewidth=widthOfHalfLevels, style=lineStyle, display=display.none)

plot(showPivotLines ? S0_5 : na, title="S0.5", color=sHalfLevelColor, linewidth=widthOfHalfLevels, style=lineStyle, display=display.none)
plot(showPivotLines ? S1_5 : na, title="S1.5", color=sHalfLevelColor, linewidth=widthOfHalfLevels, style=lineStyle, display=display.none)
plot(showPivotLines ? S2_5 : na, title="S2.5", color=sHalfLevelColor, linewidth=widthOfHalfLevels, style=lineStyle, display=display.none)


/////////////////////////////////////////////////////////////////////////////////////////////
//// **** 4 EMA (20, 50, 100, 200) and EmaTrend[20,50] | shorttitle="4EMA+EmaTrend" **** ////
/////////////////////////////////////////////////////////////////////////////////////////////

// Group section
g4EmaTrend = "[02]========[ 4 EMA and EMA Trend ]====================="

// Show section
show4EmaLines = input.bool(true, title="Show 4 EMA lines ?", group=g4EmaTrend)

// Input section
ema1 = input(20, title="EMA1 length", group=g4EmaTrend)
ema2 = input(50, title="EMA2 length", group=g4EmaTrend)
ema3 = input(100, title="EMA3 length", group=g4EmaTrend)
ema4 = input(200, title="EMA4 length", group=g4EmaTrend)

// Calculation section
positifTrendLine = ta.ema(close, ema1)
negatifTrendLine = ta.ema(close, ema2)

// Style section
emaLinesTransparency = 60
fillEma1Ema2Transp = 95
ema1Color = color.new(#66ff6c, emaLinesTransparency) // color.green
ema2Color = color.new(#ff2334, emaLinesTransparency) // color.red
ema3and4Color = color.new(#ffee73, emaLinesTransparency) // color.yellow

// Plot section
ema1Plot = plot(show4EmaLines ? ta.ema(close, ema1) : na, title="EMA1 Line", color=ema1Color, linewidth=1)
ema2Plot = plot(show4EmaLines ? ta.ema(close, ema2) : na, title="EMA2 Line",color=ema2Color, linewidth=1)
fill(ema1Plot, ema2Plot, positifTrendLine > negatifTrendLine ? color.new(color.green, fillEma1Ema2Transp) : color.new(color.red, fillEma1Ema2Transp), title="Trend Background (EMA 1,2 based)")

plot(show4EmaLines ? ta.ema(close, ema3) : na, title="EMA3 Line", color=ema3and4Color, linewidth=1)
plot(show4EmaLines ? ta.ema(close, ema4) : na, title="EMA4 Line", color=ema3and4Color, linewidth=2)


/////////////////////////////////////////////////////
//// **** Bollinger bands | shorttitle="BB" **** ////
/////////////////////////////////////////////////////

// Group section
gBollingerBands = "[03]========[ Bollinger bands ]========================="

// Show section
showBollingerB = input.bool(true, title="Show Bollinger bands ?", group=gBollingerBands)

// Input section
bbLength = input.int(20, title="BB Length", minval=1, group=gBollingerBands)
bbSrc = input(close, title="BB Source", group=gBollingerBands)
bbMult = input.float(2.0, title="BB StdDev", minval=0.001, maxval=50, group=gBollingerBands)
bbOffset = input.int(0, title="BB Offset", minval=-500, maxval=500, group=gBollingerBands)

// Calculation section
[bbBasis, bbUpper, bbLower] = ta.bb(bbSrc, bbLength, bbMult)

// Plot section
plot(showBollingerB ? bbBasis : na, title="BB SMA", color=#ff6d00, offset=bbOffset)
bbUpperPlot = plot(showBollingerB ? bbUpper : na, title="BB Upper line", color=#2196f3, linewidth=1, offset=bbOffset)
bbLowerPlot = plot(showBollingerB ? bbLower : na, title="BB Lower line", color=#2196f3, linewidth=1, offset=bbOffset)
fill(bbUpperPlot, bbLowerPlot, color=color.new(#2196f3, 95), title="BB Background")


//////////////////////////////////////////////////////
//// **** VWAP 4 lines | shorttitle="VWAP4L" **** ////
//////////////////////////////////////////////////////

// Group section
gVwapLines  = "[04]========[ VWAP lines ]=============================="

// Show section
showVwapLines = input.bool(true, title="Show VWAP lines ?", group=gVwapLines)

// Calculation section
typicalPrice = (high + low + close) / 3
typicalPriceVolume = typicalPrice * volume

// Style section
vwapLine1Color = #d2b4de //color.purple and Transp=75
vwapLine2Color = #bb8fce //color.purple and Transp=70
vwapLine3Color = #a569bd //color.purple and Transp=65
vwapLine4Color = #8e44ad //color.purple and Transp=60

vwapLinesStyle = plot.style_cross // plot.style_linebr

cumulativePeriod1 = input(48, "VWAP Period1", group=gVwapLines)
cumulativeTypicalPriceVolume1 = math.sum(typicalPriceVolume, cumulativePeriod1)
cumulativeVolume1 = math.sum(volume, cumulativePeriod1)
vwapValue1 = cumulativeTypicalPriceVolume1 / cumulativeVolume1
plot(showVwapLines ? vwapValue1 : na, color=vwapLine1Color, style=vwapLinesStyle)


cumulativePeriod2 = input(96, "VWAP Period2", group=gVwapLines)
cumulativeTypicalPriceVolume2 = math.sum(typicalPriceVolume, cumulativePeriod2)
cumulativeVolume2 = math.sum(volume, cumulativePeriod2)
vwapValue2 = cumulativeTypicalPriceVolume2 / cumulativeVolume2
plot(showVwapLines ? vwapValue2 : na, color=vwapLine2Color, style=vwapLinesStyle,linewidth=1)


cumulativePeriod3 = input(196, "VWAP Period3", group=gVwapLines)
cumulativeTypicalPriceVolume3 = math.sum(typicalPriceVolume, cumulativePeriod3)
cumulativeVolume3 = math.sum(volume, cumulativePeriod3)
vwapValue3 = cumulativeTypicalPriceVolume3 / cumulativeVolume3
plot(showVwapLines ? vwapValue3 : na, color=vwapLine3Color, style=vwapLinesStyle, linewidth=1)


cumulativePeriod4 = input(484, "VWAP Period4", group=gVwapLines)
cumulativeTypicalPriceVolume4 = math.sum(typicalPriceVolume, cumulativePeriod4)
cumulativeVolume4 = math.sum(volume, cumulativePeriod4)
vwapValue4 = cumulativeTypicalPriceVolume4 / cumulativeVolume4
plot(showVwapLines ? vwapValue4 : na, color=vwapLine4Color, style=vwapLinesStyle, linewidth=1)


///////////////////////////////////////////////////
//// **** VWAP bands | shorttitle="VWAPB" **** ////
///////////////////////////////////////////////////

// Group section
gVwapBands  = "[05]========[ VWAP bands ]=============================="

// Show section
showBands = input(true, title="Show VWAP bands ?", group=gVwapBands)
hideonDWM = input(true, title="Hide VWAP on 1D or Above ?", group=gVwapBands)
vwapSa = input(true, title="Show Alert Signals ?", group=gVwapBands)

// INPUTS
vwapBndAnchor = input.string(defval = "Session", title="Anchor Period", options=["Session", "Week", "Month", "Quarter", "Earnings", "Year", "Decade", "Century"], group=gVwapBands)
vwapBndSrc = input.source(title = "Source", defval = hlc3, group=gVwapBands)
vwapOffset = 0
stdevMult2 = input.float(1.61, step=0.01, minval=0, title="Stdev Bands Multiplier", group=gVwapBands)

// VWAP
timeChange(period) =>
	ta.change(time(period))

EPS = request.security("ESD_FACTSET:" + syminfo.prefix + ";" + syminfo.ticker + ";EARNINGS", "1", time, lookahead=barmerge.lookahead_on)

isNewPeriod = vwapBndAnchor == "Earnings" ? ta.change(EPS) :
 na(vwapBndSrc[1]) ? true :
 vwapBndAnchor == "Session" ? timeChange("D") :
 vwapBndAnchor == "Week" ? timeChange("W") :
 vwapBndAnchor == "Month" ? timeChange("M") :
 vwapBndAnchor == "Quarter" ? timeChange("M") and month % 3 == 0 :
 vwapBndAnchor == "Year" ? timeChange("12M") :
 vwapBndAnchor == "Decade" ? timeChange("12M") and year % 10 == 0 :
 vwapBndAnchor == "Century" ? timeChange("12M") and year % 100 == 0 :
 false

float myvwap = na
if not (hideonDWM and timeframe.isdwm) 
	sumSrc = vwapBndSrc * volume
	sumVol = volume
	sumSrc := isNewPeriod ? sumSrc : sumSrc + sumSrc[1]
	sumVol := isNewPeriod ? sumVol : sumVol + sumVol[1]
	myvwap := sumSrc / sumVol

vwapStdev() =>
	var int vwapLen = na
	var float vwapSum = na
	var float vwapStdev = na
	var vwapArray = array.new_float(na, na)
	vwapDividend = 0.0
 
	if isNewPeriod
		vwapLen := 0
		vwapSum := 0
		vwapStdev := 0
		array.clear(vwapArray)
 
	vwapLen := vwapLen + 1
	vwapSum := vwapSum + myvwap
	vwapMean = vwapSum / vwapLen
	
	if showBands
		array.push(vwapArray, myvwap)	
		for i=0 to vwapLen-1
			vwapDividend := vwapDividend + math.pow(array.get(vwapArray, i)-vwapMean, 2)
		vwapStdev := math.sqrt(vwapDividend/vwapLen)

// DEVS

dev1 = 1.28*stdevMult2
dev2 = 2.01*stdevMult2
dev3 = 2.51*stdevMult2
dev4 = 3.09*stdevMult2
dev5 = 4.01*stdevMult2
std = vwapStdev()

// DEV PLOTS
vwapUpperBandColor = color.new(color.red, 80)
vwapLowerBandColor = color.new(color.green, 80)


U5 = plot(showBands ? myvwap + std * dev5 : na, title="Upper Band 5", color=vwapUpperBandColor, offset=vwapOffset)
U4 = plot(showBands ? myvwap + std * dev4 : na, title="Upper Band 4", color=vwapUpperBandColor, offset=vwapOffset)
U3 = plot(showBands ? myvwap + std * dev3 : na, title="Upper Band 3", color=vwapUpperBandColor, offset=vwapOffset)
U2 = plot(showBands ? myvwap + std * dev2 : na, title="Upper Band 2", color=vwapUpperBandColor, offset=vwapOffset)
U1 = plot(showBands ? myvwap + std * dev1 : na, title="Upper Band 1", color=vwapUpperBandColor, offset=vwapOffset)

plot(showBands ? myvwap : na, title="VWAP", offset=vwapOffset, color=color.white)

D1 = plot(showBands ? myvwap - std * dev1 : na, title="Lower Band 1", color=vwapLowerBandColor, offset=vwapOffset)
D2 = plot(showBands ? myvwap - std * dev2 : na, title="Lower Band 2", color=vwapLowerBandColor, offset=vwapOffset)
D3 = plot(showBands ? myvwap - std * dev3 : na, title="Lower Band 3", color=vwapLowerBandColor, offset=vwapOffset)
D4 = plot(showBands ? myvwap - std * dev4 : na, title="Lower Band 4", color=vwapLowerBandColor, offset=vwapOffset)
D5 = plot(showBands ? myvwap - std * dev5 : na, title="Lower Band 5", color=vwapLowerBandColor, offset=vwapOffset)

// FILL CONDITIONS

U11 = myvwap + std * dev1
D11 = myvwap - std * dev1
U22 = myvwap + std * dev2
D22 = myvwap - std * dev2
U33 = myvwap + std * dev3
D33 = myvwap - std * dev3
U44 = myvwap + std * dev4
D44 = myvwap - std * dev4
U55 = myvwap + std * dev5
D55 = myvwap - std * dev5

// FILLS

fill(U4, U5, color=color.new(#cc0066, 90), title="Over Bought Fill 4")
fill(U3, U4, color=color.new(#ff6699, 90), title="Over Bought Fill 3")
fill(U2, U3, color=color.new(#ffccff, 90), title="Over Bought Fill 2")
fill(U1, U2, color=color.new(#ffccff, 95), title="Over Bought Fill 1")

fill(D1, D2, color=color.new(#99ff99, 95), title="Over Sold Fill 1")
fill(D2, D3, color=color.new(#99ff99, 90), title="Over Sold Fill 2")
fill(D3, D4, color=color.new(#33ff33, 90), title="Over Sold Fill 3")
fill(D4, D5, color=color.new(#00cc00, 90), title="Over Sold Fill 4")

// SMA

src2 = (low)
ma = ta.sma(src2, 1)

// ALERT CONDITIONS

VW = ta.crossunder(ma, myvwap)
DV1 = ta.crossunder(ma, D11)
DV2 = ta.crossunder(ma, D22)
DV3 = ta.crossunder(ma, D33)
DV4 = ta.crossunder(ma, D44)
DVUP1 = ta.crossover(ma, U11)
DVUP2 = ta.crossover(ma, U22)
DVUP3 = ta.crossover(ma, U33)
DVUP4 = ta.crossover(ma, U44)

// ALERT CONDITIONS

//alertcondition(VW, title='Vwap', message='Vwap')
//alertcondition(DV1, title='Low Deviation 1', message='Vwap Low Deviation 1')
//alertcondition(DV2, title='Low Deviation 2', message='Vwap Low Deviation 2')
//alertcondition(DV3, title='Low Deviation 3', message='Vwap Low Deviation 3')
//alertcondition(DV4, title='Low Deviation 4', message='Vwap Low Deviation 4')
//
//alertcondition(DVUP1, title='High Deviation 1', message='Vwap High Deviation 1')
//alertcondition(DVUP2, title='High Deviation 2', message='Vwap High Deviation 2')
//alertcondition(DVUP3, title='High Deviation 3', message='Vwap High Deviation 3')
//alertcondition(DVUP4, title='High Deviation 4', message='Vwap High Deviation 4')

// SIGNALS

plotshape(vwapSa ? DV4 : na, style=shape.triangleup, location=location.belowbar, color = color.new(#006600, 0), size = size.tiny, title="Lower Dev4 Arrow")
plotshape(vwapSa ? DV3 : na, style=shape.triangleup, location=location.belowbar, color = color.new(#00cc00, 0), size = size.tiny, title="Lower Dev3 Arrow")
plotshape(vwapSa ? DV2 : na, style=shape.triangleup, location=location.belowbar, color = color.new(#33ff33, 0), size = size.tiny, title="Lower Dev2 Arrow")
plotshape(vwapSa ? DV1 : na, style=shape.triangleup, location=location.belowbar, color = color.new(#99ff99, 0), size = size.tiny, title="Lower Dev1 Arrow")

plotshape(vwapSa ? VW : na, style=shape.triangleup, location=location.belowbar, color = color.new(#ffffff, 0), size = size.tiny, title="VWAP Alert")

plotshape(vwapSa ? DVUP1 : na, style=shape.triangledown, location=location.abovebar, color = color.new(#ff9999, 0), size = size.tiny, title="Upper Dev1 Arrow")
plotshape(vwapSa ? DVUP2 : na, style=shape.triangledown, location=location.abovebar, color = color.new(#ff3333, 0), size = size.tiny, title="Upper Dev2 Arrow")
plotshape(vwapSa ? DVUP3 : na, style=shape.triangledown, location=location.abovebar, color = color.new(#cc0000, 0), size = size.tiny, title="Upper Dev3 Arrow")
plotshape(vwapSa ? DVUP4 : na, style=shape.triangledown, location=location.abovebar, color = color.new(#660000, 0), size = size.tiny, title="Upper Dev4 Arrow")


//////////////////////////////////////////////////////////
//// **** Ichimoku Cloud | shorttitle="Ichimoku" **** ////
//////////////////////////////////////////////////////////

// Group section
gIchimokuCloud  = "[06]========[ Ichimoku cloud ]=========================="

// Show section
showIchimokuCloud = input(true, title="Show Ichimoku cloud ?", group=gIchimokuCloud)

// Input section
ichiConversionPeriods = input.int(9, minval=1, title="Conversion Line Length", group=gIchimokuCloud)
ichiBasePeriods = input.int(26, minval=1, title="Base Line Length", group=gIchimokuCloud)
ichiLaggingSpan2Periods = input.int(52, minval=1, title="Leading Span B Length", group=gIchimokuCloud)
ichiDisplacement = input.int(26, minval=1, title="Displacement", group=gIchimokuCloud)

// Calculation section
donchian(len) => math.avg(ta.lowest(len), ta.highest(len))
conversionLine = donchian(ichiConversionPeriods)
baseLine = donchian(ichiBasePeriods)
leadLine1 = math.avg(conversionLine, baseLine)
leadLine2 = donchian(ichiLaggingSpan2Periods)

// Plot section
plot(showIchimokuCloud ? conversionLine : na, color=#2962FF, title="Conversion Line")
plot(showIchimokuCloud ? baseLine : na, color=#B71C1C, title="Base Line")
plot(showIchimokuCloud ? close : na, offset = -ichiDisplacement + 1, color=#43A047, title="Lagging Span")
p1 = plot(showIchimokuCloud ? leadLine1 : na, offset = ichiDisplacement - 1, color=#A5D6A7, title="Leading Span A")
p2 = plot(showIchimokuCloud ? leadLine2 : na, offset = ichiDisplacement - 1, color=#EF9A9A, title="Leading Span B")
fill(p1, p2, color = leadLine1 > leadLine2 ? color.rgb(67, 160, 71, 90) : color.rgb(244, 67, 54, 90))
