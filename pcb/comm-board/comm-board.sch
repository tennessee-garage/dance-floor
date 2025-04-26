<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="8.1.0">
<drawing>
<settings>
<setting alwaysvectorfont="yes"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="no" active="no"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="15" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="11" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="50" name="dxf" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="14" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="53" name="tGND_GNDA" color="7" fill="9" visible="no" active="no"/>
<layer number="54" name="bGND_GNDA" color="1" fill="9" visible="no" active="no"/>
<layer number="56" name="wert" color="7" fill="1" visible="no" active="no"/>
<layer number="57" name="tCAD" color="7" fill="1" visible="no" active="no"/>
<layer number="59" name="tCarbon" color="7" fill="1" visible="no" active="no"/>
<layer number="60" name="bCarbon" color="7" fill="1" visible="no" active="no"/>
<layer number="90" name="Modules" color="5" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
<layer number="99" name="SpiceOrder" color="7" fill="1" visible="no" active="no"/>
<layer number="100" name="Muster" color="7" fill="1" visible="no" active="no"/>
<layer number="101" name="Patch_Top" color="12" fill="4" visible="yes" active="yes"/>
<layer number="102" name="Vscore" color="7" fill="1" visible="yes" active="yes"/>
<layer number="103" name="tMap" color="7" fill="1" visible="yes" active="yes"/>
<layer number="104" name="Name" color="16" fill="1" visible="yes" active="yes"/>
<layer number="105" name="tPlate" color="7" fill="1" visible="yes" active="yes"/>
<layer number="106" name="bPlate" color="7" fill="1" visible="yes" active="yes"/>
<layer number="107" name="Crop" color="7" fill="1" visible="yes" active="yes"/>
<layer number="108" name="tplace-old" color="10" fill="1" visible="yes" active="yes"/>
<layer number="109" name="ref-old" color="11" fill="1" visible="yes" active="yes"/>
<layer number="110" name="fp0" color="7" fill="1" visible="yes" active="yes"/>
<layer number="111" name="LPC17xx" color="7" fill="1" visible="yes" active="yes"/>
<layer number="112" name="tSilk" color="7" fill="1" visible="yes" active="yes"/>
<layer number="113" name="IDFDebug" color="4" fill="1" visible="yes" active="yes"/>
<layer number="114" name="Badge_Outline" color="7" fill="1" visible="yes" active="yes"/>
<layer number="115" name="ReferenceISLANDS" color="7" fill="1" visible="yes" active="yes"/>
<layer number="116" name="Patch_BOT" color="9" fill="4" visible="yes" active="yes"/>
<layer number="118" name="Rect_Pads" color="7" fill="1" visible="yes" active="yes"/>
<layer number="121" name="_tsilk" color="7" fill="1" visible="yes" active="yes"/>
<layer number="122" name="_bsilk" color="7" fill="1" visible="yes" active="yes"/>
<layer number="123" name="tTestmark" color="7" fill="1" visible="yes" active="yes"/>
<layer number="124" name="bTestmark" color="7" fill="1" visible="yes" active="yes"/>
<layer number="125" name="_tNames" color="7" fill="1" visible="yes" active="yes"/>
<layer number="126" name="_bNames" color="7" fill="1" visible="yes" active="yes"/>
<layer number="127" name="_tValues" color="7" fill="1" visible="yes" active="yes"/>
<layer number="128" name="_bValues" color="7" fill="1" visible="yes" active="yes"/>
<layer number="129" name="Mask" color="7" fill="1" visible="yes" active="yes"/>
<layer number="131" name="tAdjust" color="7" fill="1" visible="yes" active="yes"/>
<layer number="132" name="bAdjust" color="7" fill="1" visible="yes" active="yes"/>
<layer number="144" name="Drill_legend" color="7" fill="1" visible="yes" active="yes"/>
<layer number="150" name="Notes" color="7" fill="1" visible="yes" active="yes"/>
<layer number="151" name="HeatSink" color="7" fill="1" visible="yes" active="yes"/>
<layer number="152" name="_bDocu" color="7" fill="1" visible="yes" active="yes"/>
<layer number="153" name="FabDoc1" color="7" fill="1" visible="yes" active="yes"/>
<layer number="154" name="FabDoc2" color="7" fill="1" visible="yes" active="yes"/>
<layer number="155" name="FabDoc3" color="7" fill="1" visible="yes" active="yes"/>
<layer number="199" name="Contour" color="7" fill="1" visible="yes" active="yes"/>
<layer number="200" name="200bmp" color="1" fill="10" visible="yes" active="yes"/>
<layer number="201" name="201bmp" color="2" fill="10" visible="yes" active="yes"/>
<layer number="202" name="202bmp" color="3" fill="10" visible="yes" active="yes"/>
<layer number="203" name="203bmp" color="4" fill="10" visible="yes" active="yes"/>
<layer number="204" name="204bmp" color="5" fill="10" visible="yes" active="yes"/>
<layer number="205" name="205bmp" color="6" fill="10" visible="yes" active="yes"/>
<layer number="206" name="206bmp" color="7" fill="10" visible="yes" active="yes"/>
<layer number="207" name="207bmp" color="8" fill="10" visible="yes" active="yes"/>
<layer number="208" name="208bmp" color="9" fill="10" visible="yes" active="yes"/>
<layer number="209" name="209bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="210" name="210bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="211" name="211bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="212" name="212bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="213" name="213bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="214" name="214bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="215" name="215bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="216" name="216bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="217" name="217bmp" color="18" fill="1" visible="no" active="no"/>
<layer number="218" name="218bmp" color="19" fill="1" visible="no" active="no"/>
<layer number="219" name="219bmp" color="20" fill="1" visible="no" active="no"/>
<layer number="220" name="220bmp" color="21" fill="1" visible="no" active="no"/>
<layer number="221" name="221bmp" color="22" fill="1" visible="no" active="no"/>
<layer number="222" name="222bmp" color="23" fill="1" visible="no" active="no"/>
<layer number="223" name="223bmp" color="24" fill="1" visible="no" active="no"/>
<layer number="224" name="224bmp" color="25" fill="1" visible="no" active="no"/>
<layer number="225" name="225bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="226" name="226bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="227" name="227bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="228" name="228bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="229" name="229bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="230" name="230bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="231" name="231bmp" color="7" fill="1" visible="yes" active="yes"/>
<layer number="248" name="Housing" color="7" fill="1" visible="yes" active="yes"/>
<layer number="249" name="Edge" color="7" fill="1" visible="yes" active="yes"/>
<layer number="250" name="Descript" color="3" fill="1" visible="no" active="no"/>
<layer number="251" name="SMDround" color="12" fill="11" visible="no" active="no"/>
<layer number="254" name="cooling" color="7" fill="1" visible="yes" active="yes"/>
<layer number="255" name="routoute" color="7" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="GARTH">
<description>Part's used for my projects</description>
<packages>
<package name="SOP-16">
<wire x1="4.699" y1="1.9558" x2="-4.699" y2="1.9558" width="0.1524" layer="21"/>
<wire x1="4.699" y1="-1.9558" x2="5.08" y2="-1.5748" width="0.1524" layer="21" curve="90"/>
<wire x1="-5.08" y1="1.5748" x2="-4.699" y2="1.9558" width="0.1524" layer="21" curve="-90"/>
<wire x1="4.699" y1="1.9558" x2="5.08" y2="1.5748" width="0.1524" layer="21" curve="-90"/>
<wire x1="-5.08" y1="-1.5748" x2="-4.699" y2="-1.9558" width="0.1524" layer="21" curve="90"/>
<wire x1="-4.699" y1="-1.9558" x2="4.699" y2="-1.9558" width="0.1524" layer="21"/>
<wire x1="5.08" y1="-1.5748" x2="5.08" y2="1.5748" width="0.1524" layer="21"/>
<wire x1="-5.08" y1="1.5748" x2="-5.08" y2="-1.5748" width="0.1524" layer="21"/>
<wire x1="-5.08" y1="0.508" x2="-5.08" y2="-0.508" width="0.1524" layer="21" curve="-180"/>
<wire x1="-5.08" y1="-1.6002" x2="5.08" y2="-1.6002" width="0.0508" layer="21"/>
<smd name="1" x="-4.445" y="-3.0734" dx="0.6604" dy="2.032" layer="1"/>
<smd name="16" x="-4.445" y="3.0734" dx="0.6604" dy="2.032" layer="1"/>
<smd name="2" x="-3.175" y="-3.0734" dx="0.6604" dy="2.032" layer="1"/>
<smd name="3" x="-1.905" y="-3.0734" dx="0.6604" dy="2.032" layer="1"/>
<smd name="15" x="-3.175" y="3.0734" dx="0.6604" dy="2.032" layer="1"/>
<smd name="14" x="-1.905" y="3.0734" dx="0.6604" dy="2.032" layer="1"/>
<smd name="4" x="-0.635" y="-3.0734" dx="0.6604" dy="2.032" layer="1"/>
<smd name="13" x="-0.635" y="3.0734" dx="0.6604" dy="2.032" layer="1"/>
<smd name="5" x="0.635" y="-3.0734" dx="0.6604" dy="2.032" layer="1"/>
<smd name="12" x="0.635" y="3.0734" dx="0.6604" dy="2.032" layer="1"/>
<smd name="6" x="1.905" y="-3.0734" dx="0.6604" dy="2.032" layer="1"/>
<smd name="7" x="3.175" y="-3.0734" dx="0.6604" dy="2.032" layer="1"/>
<smd name="11" x="1.905" y="3.0734" dx="0.6604" dy="2.032" layer="1"/>
<smd name="10" x="3.175" y="3.0734" dx="0.6604" dy="2.032" layer="1"/>
<smd name="8" x="4.445" y="-3.0734" dx="0.6604" dy="2.032" layer="1"/>
<smd name="9" x="4.445" y="3.0734" dx="0.6604" dy="2.032" layer="1"/>
<text x="-4.064" y="-0.635" size="1.27" layer="27" ratio="10">&gt;VALUE</text>
<text x="-5.461" y="-2.032" size="1.27" layer="25" ratio="10" rot="R90">&gt;NAME</text>
<rectangle x1="-0.889" y1="1.9558" x2="-0.381" y2="3.0988" layer="51"/>
<rectangle x1="-4.699" y1="-3.0988" x2="-4.191" y2="-1.9558" layer="51"/>
<rectangle x1="-3.429" y1="-3.0988" x2="-2.921" y2="-1.9558" layer="51"/>
<rectangle x1="-2.159" y1="-3.0734" x2="-1.651" y2="-1.9304" layer="51"/>
<rectangle x1="-0.889" y1="-3.0988" x2="-0.381" y2="-1.9558" layer="51"/>
<rectangle x1="-2.159" y1="1.9558" x2="-1.651" y2="3.0988" layer="51"/>
<rectangle x1="-3.429" y1="1.9558" x2="-2.921" y2="3.0988" layer="51"/>
<rectangle x1="-4.699" y1="1.9558" x2="-4.191" y2="3.0988" layer="51"/>
<rectangle x1="0.381" y1="-3.0988" x2="0.889" y2="-1.9558" layer="51"/>
<rectangle x1="1.651" y1="-3.0988" x2="2.159" y2="-1.9558" layer="51"/>
<rectangle x1="2.921" y1="-3.0988" x2="3.429" y2="-1.9558" layer="51"/>
<rectangle x1="4.191" y1="-3.0988" x2="4.699" y2="-1.9558" layer="51"/>
<rectangle x1="0.381" y1="1.9558" x2="0.889" y2="3.0988" layer="51"/>
<rectangle x1="1.651" y1="1.9558" x2="2.159" y2="3.0988" layer="51"/>
<rectangle x1="2.921" y1="1.9558" x2="3.429" y2="3.0988" layer="51"/>
<rectangle x1="4.191" y1="1.9558" x2="4.699" y2="3.0988" layer="51"/>
</package>
<package name="RJE01-660-02">
<hole x="0" y="0" drill="3.45"/>
<hole x="21.59" y="0" drill="3.45"/>
<pad name="6@1" x="2.22" y="3.05" drill="0.89"/>
<pad name="4@1" x="4.25" y="3.05" drill="0.89"/>
<pad name="2@1" x="6.28" y="3.05" drill="0.89"/>
<pad name="5@1" x="3.24" y="5.08" drill="0.89"/>
<pad name="3@1" x="5.27" y="5.08" drill="0.89"/>
<pad name="1@1" x="7.3" y="5.08" drill="0.89"/>
<pad name="6@2" x="14.29" y="3.05" drill="0.89"/>
<pad name="4@2" x="16.32" y="3.05" drill="0.89"/>
<pad name="2@2" x="18.35" y="3.05" drill="0.89"/>
<pad name="5@2" x="15.31" y="5.08" drill="0.89"/>
<pad name="3@2" x="17.34" y="5.08" drill="0.89"/>
<pad name="1@2" x="19.37" y="5.08" drill="0.89"/>
<wire x1="-1.725" y1="8.255" x2="23.315" y2="8.255" width="0.127" layer="51"/>
<wire x1="-1.725" y1="-8.255" x2="23.315" y2="-8.255" width="0.127" layer="51"/>
<wire x1="-1.725" y1="8.255" x2="-1.725" y2="-8.255" width="0.127" layer="51"/>
<wire x1="23.315" y1="8.255" x2="23.315" y2="-8.255" width="0.127" layer="51"/>
</package>
<package name="RJSBE-5380-C2">
<hole x="0" y="0" drill="3.45"/>
<hole x="28.45" y="0" drill="3.45"/>
<pad name="12@1" x="-0.51" y="4.19" drill="0.89"/>
<pad name="11@1" x="2.03" y="4.19" drill="0.89"/>
<pad name="1@1" x="1.91" y="8.25" drill="0.89"/>
<pad name="3@1" x="4.45" y="8.25" drill="0.89"/>
<pad name="5@1" x="6.99" y="8.25" drill="0.89"/>
<pad name="7@1" x="9.53" y="8.25" drill="0.89"/>
<pad name="2@1" x="3.18" y="10.79" drill="0.89"/>
<pad name="4@1" x="5.72" y="10.79" drill="0.89"/>
<pad name="6@1" x="8.26" y="10.79" drill="0.89"/>
<pad name="8@1" x="10.8" y="10.79" drill="0.89"/>
<pad name="10@1" x="10.67" y="4.19" drill="0.89"/>
<pad name="9@1" x="13.21" y="4.19" drill="0.89"/>
<pad name="12@2" x="15.24" y="4.19" drill="0.89"/>
<pad name="11@2" x="17.78" y="4.19" drill="0.89"/>
<pad name="1@2" x="17.66" y="8.25" drill="0.89"/>
<pad name="3@2" x="20.2" y="8.25" drill="0.89"/>
<pad name="5@2" x="22.74" y="8.25" drill="0.89"/>
<pad name="7@2" x="25.28" y="8.25" drill="0.89"/>
<pad name="2@2" x="18.93" y="10.79" drill="0.89"/>
<pad name="4@2" x="21.47" y="10.79" drill="0.89"/>
<pad name="6@2" x="24.01" y="10.79" drill="0.89"/>
<pad name="8@2" x="26.55" y="10.79" drill="0.89"/>
<pad name="10@2" x="26.42" y="4.19" drill="0.89"/>
<pad name="9@2" x="28.96" y="4.19" drill="0.89"/>
<pad name="SHIELD@1" x="-1.78" y="7.11" drill="1.57"/>
<pad name="SHIELD@2" x="30.23" y="7.11" drill="1.57"/>
<wire x1="-1.78" y1="-5.46" x2="30.23" y2="-5.46" width="0.127" layer="51"/>
<wire x1="-1.78" y1="12.2" x2="30.23" y2="12.2" width="0.127" layer="51"/>
<wire x1="-1.78" y1="12.2" x2="-1.78" y2="-5.46" width="0.127" layer="51"/>
<wire x1="30.23" y1="12.2" x2="30.23" y2="-5.46" width="0.127" layer="51"/>
</package>
</packages>
<symbols>
<symbol name="SN65C1167">
<pin name="DE" x="-15.24" y="12.7" length="middle"/>
<pin name="!RE" x="-15.24" y="7.62" length="middle"/>
<pin name="1D" x="-15.24" y="2.54" length="middle"/>
<pin name="1R" x="-15.24" y="-2.54" length="middle"/>
<pin name="2D" x="-15.24" y="-7.62" length="middle"/>
<pin name="2R" x="-15.24" y="-12.7" length="middle"/>
<pin name="1Y" x="10.16" y="17.78" length="middle" rot="R180"/>
<pin name="1Z" x="10.16" y="12.7" length="middle" rot="R180"/>
<pin name="1A" x="10.16" y="7.62" length="middle" rot="R180"/>
<pin name="1B" x="10.16" y="2.54" length="middle" rot="R180"/>
<pin name="2Y" x="10.16" y="-2.54" length="middle" rot="R180"/>
<pin name="2Z" x="10.16" y="-7.62" length="middle" rot="R180"/>
<pin name="2A" x="10.16" y="-12.7" length="middle" rot="R180"/>
<pin name="2B" x="10.16" y="-17.78" length="middle" rot="R180"/>
<pin name="VCC" x="-15.24" y="17.78" length="middle"/>
<pin name="GND" x="-15.24" y="-17.78" length="middle"/>
<wire x1="-10.16" y1="20.32" x2="-10.16" y2="-20.32" width="0.254" layer="94"/>
<wire x1="-10.16" y1="-20.32" x2="5.08" y2="-20.32" width="0.254" layer="94"/>
<wire x1="5.08" y1="-20.32" x2="5.08" y2="20.32" width="0.254" layer="94"/>
<wire x1="5.08" y1="20.32" x2="-10.16" y2="20.32" width="0.254" layer="94"/>
<text x="-10.16" y="21.59" size="1.27" layer="95">&gt;NAME</text>
<text x="-10.16" y="-22.86" size="1.27" layer="96">&gt;VALUE</text>
</symbol>
<symbol name="RJE01-660-02">
<pin name="1@1" x="-12.7" y="12.7" length="middle"/>
<pin name="2@1" x="-12.7" y="7.62" length="middle"/>
<pin name="3@1" x="-12.7" y="2.54" length="middle"/>
<pin name="4@1" x="-12.7" y="-2.54" length="middle"/>
<pin name="5@1" x="-12.7" y="-7.62" length="middle"/>
<pin name="6@1" x="-12.7" y="-12.7" length="middle"/>
<pin name="1@2" x="12.7" y="12.7" length="middle" rot="R180"/>
<pin name="2@2" x="12.7" y="7.62" length="middle" rot="R180"/>
<pin name="3@2" x="12.7" y="2.54" length="middle" rot="R180"/>
<pin name="4@2" x="12.7" y="-2.54" length="middle" rot="R180"/>
<pin name="5@2" x="12.7" y="-7.62" length="middle" rot="R180"/>
<pin name="6@2" x="12.7" y="-12.7" length="middle" rot="R180"/>
<wire x1="-7.62" y1="15.24" x2="-7.62" y2="-15.24" width="0.254" layer="94"/>
<wire x1="-7.62" y1="-15.24" x2="7.62" y2="-15.24" width="0.254" layer="94"/>
<wire x1="7.62" y1="-15.24" x2="7.62" y2="15.24" width="0.254" layer="94"/>
<wire x1="7.62" y1="15.24" x2="-7.62" y2="15.24" width="0.254" layer="94"/>
<text x="-5.08" y="16.51" size="1.27" layer="95">&gt;NAME</text>
<text x="-5.08" y="-17.78" size="1.27" layer="96">&gt;VALUE</text>
</symbol>
<symbol name="RJSBE-5380-C2">
<pin name="1@1" x="-15.24" y="15.24" length="middle"/>
<pin name="2@1" x="-15.24" y="12.7" length="middle"/>
<pin name="3@1" x="-15.24" y="10.16" length="middle"/>
<pin name="4@1" x="-15.24" y="7.62" length="middle"/>
<pin name="5@1" x="-15.24" y="5.08" length="middle"/>
<pin name="6@1" x="-15.24" y="2.54" length="middle"/>
<pin name="7@1" x="-15.24" y="0" length="middle"/>
<pin name="8@1" x="-15.24" y="-2.54" length="middle"/>
<pin name="9@1" x="-15.24" y="-5.08" length="middle"/>
<pin name="10@1" x="-15.24" y="-7.62" length="middle"/>
<pin name="11@1" x="-15.24" y="-10.16" length="middle"/>
<pin name="12@1" x="-15.24" y="-12.7" length="middle"/>
<pin name="1@2" x="15.24" y="15.24" length="middle" rot="R180"/>
<pin name="2@2" x="15.24" y="12.7" length="middle" rot="R180"/>
<pin name="3@2" x="15.24" y="10.16" length="middle" rot="R180"/>
<pin name="4@2" x="15.24" y="7.62" length="middle" rot="R180"/>
<pin name="5@2" x="15.24" y="5.08" length="middle" rot="R180"/>
<pin name="6@2" x="15.24" y="2.54" length="middle" rot="R180"/>
<pin name="7@2" x="15.24" y="0" length="middle" rot="R180"/>
<pin name="8@2" x="15.24" y="-2.54" length="middle" rot="R180"/>
<pin name="9@2" x="15.24" y="-5.08" length="middle" rot="R180"/>
<pin name="10@2" x="15.24" y="-7.62" length="middle" rot="R180"/>
<pin name="11@2" x="15.24" y="-10.16" length="middle" rot="R180"/>
<pin name="12@2" x="15.24" y="-12.7" length="middle" rot="R180"/>
<wire x1="-10.16" y1="17.78" x2="-10.16" y2="-20.32" width="0.254" layer="94"/>
<wire x1="-10.16" y1="-20.32" x2="10.16" y2="-20.32" width="0.254" layer="94"/>
<wire x1="10.16" y1="-20.32" x2="10.16" y2="17.78" width="0.254" layer="94"/>
<wire x1="10.16" y1="17.78" x2="-10.16" y2="17.78" width="0.254" layer="94"/>
<text x="-7.62" y="19.05" size="1.27" layer="95">&gt;NAME</text>
<text x="-7.62" y="-22.86" size="1.27" layer="96">&gt;VALUE</text>
<pin name="SHIELD@1" x="-15.24" y="-15.24" length="middle"/>
<pin name="SHIELD@2" x="15.24" y="-17.78" length="middle" rot="R180"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="SN65C1167">
<gates>
<gate name="G$1" symbol="SN65C1167" x="0" y="0"/>
</gates>
<devices>
<device name="" package="SOP-16">
<connects>
<connect gate="G$1" pin="!RE" pad="4"/>
<connect gate="G$1" pin="1A" pad="2"/>
<connect gate="G$1" pin="1B" pad="1"/>
<connect gate="G$1" pin="1D" pad="15"/>
<connect gate="G$1" pin="1R" pad="3"/>
<connect gate="G$1" pin="1Y" pad="14"/>
<connect gate="G$1" pin="1Z" pad="13"/>
<connect gate="G$1" pin="2A" pad="6"/>
<connect gate="G$1" pin="2B" pad="7"/>
<connect gate="G$1" pin="2D" pad="9"/>
<connect gate="G$1" pin="2R" pad="5"/>
<connect gate="G$1" pin="2Y" pad="10"/>
<connect gate="G$1" pin="2Z" pad="11"/>
<connect gate="G$1" pin="DE" pad="12"/>
<connect gate="G$1" pin="GND" pad="8"/>
<connect gate="G$1" pin="VCC" pad="16"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="RJE01-660-02">
<description>Multi Port Non-Shielded 6P6C RJ-11 connector</description>
<gates>
<gate name="G$1" symbol="RJE01-660-02" x="0" y="0"/>
</gates>
<devices>
<device name="" package="RJE01-660-02">
<connects>
<connect gate="G$1" pin="1@1" pad="1@1"/>
<connect gate="G$1" pin="1@2" pad="1@2"/>
<connect gate="G$1" pin="2@1" pad="2@1"/>
<connect gate="G$1" pin="2@2" pad="2@2"/>
<connect gate="G$1" pin="3@1" pad="3@1"/>
<connect gate="G$1" pin="3@2" pad="3@2"/>
<connect gate="G$1" pin="4@1" pad="4@1"/>
<connect gate="G$1" pin="4@2" pad="4@2"/>
<connect gate="G$1" pin="5@1" pad="5@1"/>
<connect gate="G$1" pin="5@2" pad="5@2"/>
<connect gate="G$1" pin="6@1" pad="6@1"/>
<connect gate="G$1" pin="6@2" pad="6@2"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="RJSBE-5380-C2">
<gates>
<gate name="G$1" symbol="RJSBE-5380-C2" x="0" y="0"/>
</gates>
<devices>
<device name="" package="RJSBE-5380-C2">
<connects>
<connect gate="G$1" pin="10@1" pad="10@1"/>
<connect gate="G$1" pin="10@2" pad="10@2"/>
<connect gate="G$1" pin="11@1" pad="11@1"/>
<connect gate="G$1" pin="11@2" pad="11@2"/>
<connect gate="G$1" pin="12@1" pad="12@1"/>
<connect gate="G$1" pin="12@2" pad="12@2"/>
<connect gate="G$1" pin="1@1" pad="1@1"/>
<connect gate="G$1" pin="1@2" pad="1@2"/>
<connect gate="G$1" pin="2@1" pad="2@1"/>
<connect gate="G$1" pin="2@2" pad="2@2"/>
<connect gate="G$1" pin="3@1" pad="3@1"/>
<connect gate="G$1" pin="3@2" pad="3@2"/>
<connect gate="G$1" pin="4@1" pad="4@1"/>
<connect gate="G$1" pin="4@2" pad="4@2"/>
<connect gate="G$1" pin="5@1" pad="5@1"/>
<connect gate="G$1" pin="5@2" pad="5@2"/>
<connect gate="G$1" pin="6@1" pad="6@1"/>
<connect gate="G$1" pin="6@2" pad="6@2"/>
<connect gate="G$1" pin="7@1" pad="7@1"/>
<connect gate="G$1" pin="7@2" pad="7@2"/>
<connect gate="G$1" pin="8@1" pad="8@1"/>
<connect gate="G$1" pin="8@2" pad="8@2"/>
<connect gate="G$1" pin="9@1" pad="9@1"/>
<connect gate="G$1" pin="9@2" pad="9@2"/>
<connect gate="G$1" pin="SHIELD@1" pad="SHIELD@1"/>
<connect gate="G$1" pin="SHIELD@2" pad="SHIELD@2"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="SparkFun">
<description>Spark Fun Electronics' preferred foot prints. &lt;b&gt;Not to be used for commercial purposes.&lt;/b&gt; We've spent an enormous amount of time creating and checking these footprints and parts. If you enjoy using this library, please buy one of our products at www.sparkfun.com.</description>
<packages>
<package name="CAP-PTH-SMALL">
<wire x1="1.27" y1="0.635" x2="1.27" y2="-0.635" width="0.2032" layer="21"/>
<pad name="1" x="0" y="0" drill="0.7" diameter="1.651"/>
<pad name="2" x="2.54" y="0" drill="0.7" diameter="1.651"/>
<text x="0.508" y="1.27" size="0.4064" layer="25">&gt;Name</text>
<text x="0.254" y="-1.524" size="0.4064" layer="27">&gt;Value</text>
</package>
<package name="CAP-PTH-SMALL2">
<wire x1="1.27" y1="0.635" x2="1.27" y2="-0.635" width="0.2032" layer="21"/>
<wire x1="-1.27" y1="1.27" x2="3.81" y2="1.27" width="0.2032" layer="21"/>
<wire x1="3.81" y1="1.27" x2="3.81" y2="-1.27" width="0.2032" layer="21"/>
<wire x1="3.81" y1="-1.27" x2="-1.27" y2="-1.27" width="0.2032" layer="21"/>
<wire x1="-1.27" y1="-1.27" x2="-1.27" y2="1.27" width="0.2032" layer="21"/>
<pad name="1" x="0" y="0" drill="0.7" diameter="1.651"/>
<pad name="2" x="2.54" y="0" drill="0.7" diameter="1.651"/>
<text x="-1.27" y="1.905" size="0.6096" layer="25">&gt;Name</text>
<text x="-1.27" y="-2.54" size="0.6096" layer="27">&gt;Value</text>
</package>
<package name="0805">
<wire x1="-0.3" y1="0.6" x2="0.3" y2="0.6" width="0.1524" layer="21"/>
<wire x1="-0.3" y1="-0.6" x2="0.3" y2="-0.6" width="0.1524" layer="21"/>
<smd name="1" x="-0.9" y="0" dx="0.8" dy="1.2" layer="1"/>
<smd name="2" x="0.9" y="0" dx="0.8" dy="1.2" layer="1"/>
<text x="-0.762" y="0.8255" size="0.4064" layer="25">&gt;NAME</text>
<text x="-1.016" y="-1.397" size="0.4064" layer="27">&gt;VALUE</text>
</package>
<package name="CAP-PTH-LARGE">
<wire x1="0" y1="0.635" x2="0" y2="0" width="0.2032" layer="21"/>
<wire x1="0" y1="0" x2="0" y2="-0.635" width="0.2032" layer="21"/>
<wire x1="0" y1="0" x2="-2.54" y2="0" width="0.2032" layer="21"/>
<wire x1="0" y1="0" x2="2.54" y2="0" width="0.2032" layer="21"/>
<pad name="1" x="-4.826" y="0" drill="0.7" diameter="1.651"/>
<pad name="2" x="4.572" y="0" drill="0.7" diameter="1.651"/>
<text x="-0.762" y="1.27" size="0.4064" layer="25">&gt;Name</text>
<text x="-1.016" y="-1.524" size="0.4064" layer="27">&gt;Value</text>
</package>
<package name="GRM43D">
<wire x1="2.25" y1="1.6" x2="1.1" y2="1.6" width="0.127" layer="51"/>
<wire x1="1.1" y1="1.6" x2="-1.1" y2="1.6" width="0.127" layer="51"/>
<wire x1="-1.1" y1="1.6" x2="-2.25" y2="1.6" width="0.127" layer="51"/>
<wire x1="-2.25" y1="1.6" x2="-2.25" y2="-1.6" width="0.127" layer="51"/>
<wire x1="-2.25" y1="-1.6" x2="-1.1" y2="-1.6" width="0.127" layer="51"/>
<wire x1="-1.1" y1="-1.6" x2="1.1" y2="-1.6" width="0.127" layer="51"/>
<wire x1="1.1" y1="-1.6" x2="2.25" y2="-1.6" width="0.127" layer="51"/>
<wire x1="2.25" y1="-1.6" x2="2.25" y2="1.6" width="0.127" layer="51"/>
<wire x1="1.1" y1="1.6" x2="1.1" y2="-1.6" width="0.127" layer="51"/>
<wire x1="-1.1" y1="1.6" x2="-1.1" y2="-1.6" width="0.127" layer="51"/>
<wire x1="-2.3" y1="1.8" x2="2.3" y2="1.8" width="0.127" layer="21"/>
<wire x1="-2.3" y1="-1.8" x2="2.3" y2="-1.8" width="0.127" layer="21"/>
<smd name="A" x="1.927" y="0" dx="3.2" dy="1.65" layer="1" rot="R90"/>
<smd name="C" x="-1.927" y="0" dx="3.2" dy="1.65" layer="1" rot="R90"/>
<text x="-2" y="2" size="0.4064" layer="25">&gt;NAME</text>
<text x="0" y="-2" size="0.4064" layer="27" rot="R180">&gt;VALUE</text>
<rectangle x1="-2.2" y1="-1.6" x2="-1.1" y2="1.6" layer="51"/>
<rectangle x1="1.1" y1="-1.6" x2="2.2" y2="1.6" layer="51"/>
</package>
<package name="0603-CAP">
<wire x1="-1.473" y1="0.983" x2="1.473" y2="0.983" width="0.0508" layer="39"/>
<wire x1="1.473" y1="0.983" x2="1.473" y2="-0.983" width="0.0508" layer="39"/>
<wire x1="1.473" y1="-0.983" x2="-1.473" y2="-0.983" width="0.0508" layer="39"/>
<wire x1="-1.473" y1="-0.983" x2="-1.473" y2="0.983" width="0.0508" layer="39"/>
<wire x1="-0.356" y1="0.432" x2="0.356" y2="0.432" width="0.1016" layer="51"/>
<wire x1="-0.356" y1="-0.419" x2="0.356" y2="-0.419" width="0.1016" layer="51"/>
<wire x1="0" y1="0.0305" x2="0" y2="-0.0305" width="0.5588" layer="21"/>
<smd name="1" x="-0.85" y="0" dx="1.1" dy="1" layer="1"/>
<smd name="2" x="0.85" y="0" dx="1.1" dy="1" layer="1"/>
<text x="-0.889" y="0.762" size="0.4064" layer="25" font="vector">&gt;NAME</text>
<text x="-1.016" y="-1.143" size="0.4064" layer="27" font="vector">&gt;VALUE</text>
<rectangle x1="-0.8382" y1="-0.4699" x2="-0.3381" y2="0.4801" layer="51"/>
<rectangle x1="0.3302" y1="-0.4699" x2="0.8303" y2="0.4801" layer="51"/>
<rectangle x1="-0.1999" y1="-0.3" x2="0.1999" y2="0.3" layer="35"/>
</package>
<package name="0402-CAP">
<description>&lt;b&gt;CAPACITOR&lt;/b&gt;&lt;p&gt;
chip</description>
<wire x1="-0.245" y1="0.224" x2="0.245" y2="0.224" width="0.1524" layer="51"/>
<wire x1="0.245" y1="-0.224" x2="-0.245" y2="-0.224" width="0.1524" layer="51"/>
<wire x1="-1.473" y1="0.483" x2="1.473" y2="0.483" width="0.0508" layer="39"/>
<wire x1="1.473" y1="0.483" x2="1.473" y2="-0.483" width="0.0508" layer="39"/>
<wire x1="1.473" y1="-0.483" x2="-1.473" y2="-0.483" width="0.0508" layer="39"/>
<wire x1="-1.473" y1="-0.483" x2="-1.473" y2="0.483" width="0.0508" layer="39"/>
<wire x1="0" y1="0.0305" x2="0" y2="-0.0305" width="0.4064" layer="21"/>
<smd name="1" x="-0.65" y="0" dx="0.7" dy="0.9" layer="1"/>
<smd name="2" x="0.65" y="0" dx="0.7" dy="0.9" layer="1"/>
<text x="-0.889" y="0.6985" size="0.4064" layer="25">&gt;NAME</text>
<text x="-1.0795" y="-1.143" size="0.4064" layer="27">&gt;VALUE</text>
<rectangle x1="-0.554" y1="-0.3048" x2="-0.254" y2="0.2951" layer="51"/>
<rectangle x1="0.2588" y1="-0.3048" x2="0.5588" y2="0.2951" layer="51"/>
<rectangle x1="-0.1999" y1="-0.3" x2="0.1999" y2="0.3" layer="35"/>
</package>
<package name="CAP-PTH-5MM">
<wire x1="0" y1="0.635" x2="0" y2="-0.635" width="0.2032" layer="21"/>
<pad name="1" x="-2.5" y="0" drill="0.7" diameter="1.651"/>
<pad name="2" x="2.5" y="0" drill="0.7" diameter="1.651"/>
<text x="-0.762" y="1.27" size="0.4064" layer="25">&gt;Name</text>
<text x="-1.016" y="-1.524" size="0.4064" layer="27">&gt;Value</text>
</package>
</packages>
<symbols>
<symbol name="GND">
<wire x1="-1.905" y1="0" x2="1.905" y2="0" width="0.254" layer="94"/>
<text x="-2.54" y="-2.54" size="1.778" layer="96">&gt;VALUE</text>
<pin name="GND" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
</symbol>
<symbol name="CAP">
<wire x1="0" y1="2.54" x2="0" y2="2.032" width="0.1524" layer="94"/>
<wire x1="0" y1="0" x2="0" y2="0.508" width="0.1524" layer="94"/>
<text x="1.524" y="2.921" size="1.778" layer="95">&gt;NAME</text>
<text x="1.524" y="-2.159" size="1.778" layer="96">&gt;VALUE</text>
<rectangle x1="-2.032" y1="0.508" x2="2.032" y2="1.016" layer="94"/>
<rectangle x1="-2.032" y1="1.524" x2="2.032" y2="2.032" layer="94"/>
<pin name="1" x="0" y="5.08" visible="off" length="short" direction="pas" swaplevel="1" rot="R270"/>
<pin name="2" x="0" y="-2.54" visible="off" length="short" direction="pas" swaplevel="1" rot="R90"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="GND" prefix="GND">
<description>&lt;b&gt;SUPPLY SYMBOL&lt;/b&gt;</description>
<gates>
<gate name="1" symbol="GND" x="0" y="0"/>
</gates>
<devices>
<device name="">
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="CAP" prefix="C" uservalue="yes">
<description>&lt;b&gt;Capacitor&lt;/b&gt;
Standard 0603 ceramic capacitor, and 0.1" leaded capacitor.</description>
<gates>
<gate name="G$1" symbol="CAP" x="0" y="0"/>
</gates>
<devices>
<device name="PTH" package="CAP-PTH-SMALL">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
<device name="PTH2" package="CAP-PTH-SMALL2">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
<device name="0805" package="0805">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
<device name="PTH3" package="CAP-PTH-LARGE">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
<device name="SMD" package="GRM43D">
<connects>
<connect gate="G$1" pin="1" pad="A"/>
<connect gate="G$1" pin="2" pad="C"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
<device name="0603-CAP" package="0603-CAP">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
<device name="0402-CAP" package="0402-CAP">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
<device name="PTH1" package="CAP-PTH-5MM">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="MF_Passives">
<packages>
<package name="R0402">
<description>&lt;b&gt;Description:&lt;/b&gt; Standard 0402 Package for Resistors&lt;br/&gt;</description>
<smd name="P$1" x="-0.55" y="0" dx="0.5" dy="0.6" layer="1" rot="R180"/>
<smd name="P$2" x="0.55" y="0" dx="0.5" dy="0.6" layer="1" rot="R180"/>
<wire x1="-1.1" y1="0.55" x2="-1.1" y2="-0.55" width="0.127" layer="21"/>
<wire x1="-1.1" y1="-0.55" x2="1.1" y2="-0.55" width="0.127" layer="21"/>
<wire x1="1.1" y1="-0.55" x2="1.1" y2="0.55" width="0.127" layer="21"/>
<wire x1="1.1" y1="0.55" x2="-1.1" y2="0.55" width="0.127" layer="21"/>
<text x="-1.1" y="1.1" size="1.016" layer="25" font="vector" ratio="16">&gt;NAME</text>
</package>
<package name="R0603">
<description>&lt;b&gt;Description:&lt;/b&gt; Standard 0603 Package for Resistors&lt;br/&gt;</description>
<smd name="P$1" x="-0.75" y="0" dx="0.6" dy="0.9" layer="1" rot="R180"/>
<smd name="P$2" x="0.75" y="0" dx="0.6" dy="0.9" layer="1" rot="R180"/>
<wire x1="-1.4" y1="0.7" x2="-1.4" y2="-0.7" width="0.127" layer="21"/>
<wire x1="-1.4" y1="-0.7" x2="1.4" y2="-0.7" width="0.127" layer="21"/>
<wire x1="1.4" y1="-0.7" x2="1.4" y2="0.7" width="0.127" layer="21"/>
<wire x1="1.4" y1="0.7" x2="-1.4" y2="0.7" width="0.127" layer="21"/>
<text x="-1.4" y="1.1" size="1.016" layer="25" font="vector" ratio="16">&gt;NAME</text>
</package>
<package name="R0805">
<description>&lt;b&gt;Description:&lt;/b&gt; Standard 0805 Package for Resistors&lt;br/&gt;</description>
<smd name="P$1" x="-0.95" y="0" dx="0.7" dy="1.3" layer="1" rot="R180"/>
<smd name="P$2" x="0.95" y="0" dx="0.7" dy="1.3" layer="1" rot="R180"/>
<wire x1="-1.8" y1="0.9" x2="-1.8" y2="-0.9" width="0.127" layer="21"/>
<wire x1="-1.8" y1="-0.9" x2="1.8" y2="-0.9" width="0.127" layer="21"/>
<wire x1="1.8" y1="-0.9" x2="1.8" y2="0.9" width="0.127" layer="21"/>
<wire x1="1.8" y1="0.9" x2="-1.8" y2="0.9" width="0.127" layer="21"/>
<text x="-1.8" y="1.1" size="1.016" layer="25" font="vector" ratio="16">&gt;NAME</text>
</package>
<package name="R1206">
<description>&lt;b&gt;Description:&lt;/b&gt; Standard 1206 Package for Resistors&lt;br/&gt;</description>
<smd name="P$1" x="-1.45" y="0" dx="0.9" dy="1.6" layer="1" rot="R180"/>
<smd name="P$2" x="1.45" y="0" dx="0.9" dy="1.6" layer="1" rot="R180"/>
<wire x1="-2.2" y1="1.1" x2="-2.2" y2="-1.1" width="0.127" layer="21"/>
<wire x1="-2.2" y1="-1.1" x2="2.2" y2="-1.1" width="0.127" layer="21"/>
<wire x1="2.2" y1="-1.1" x2="2.2" y2="1.1" width="0.127" layer="21"/>
<wire x1="2.2" y1="1.1" x2="-2.2" y2="1.1" width="0.127" layer="21"/>
<text x="-2.2" y="1.3" size="1.016" layer="25" font="vector" ratio="16">&gt;NAME</text>
</package>
<package name="R1210">
<description>&lt;b&gt;Description:&lt;/b&gt; Standard 1210 Package for Resistors&lt;br/&gt;</description>
<smd name="P$1" x="-1.45" y="0" dx="0.9" dy="2.5" layer="1" rot="R180"/>
<smd name="P$2" x="1.45" y="0" dx="0.9" dy="2.5" layer="1" rot="R180"/>
<wire x1="-2.2" y1="1.6" x2="-2.2" y2="-1.6" width="0.127" layer="21"/>
<wire x1="-2.2" y1="-1.6" x2="2.2" y2="-1.6" width="0.127" layer="21"/>
<wire x1="2.2" y1="-1.6" x2="2.2" y2="1.6" width="0.127" layer="21"/>
<wire x1="2.2" y1="1.6" x2="-2.2" y2="1.6" width="0.127" layer="21"/>
<text x="-2.2" y="1.8" size="1.016" layer="25" font="vector" ratio="16">&gt;NAME</text>
</package>
</packages>
<symbols>
<symbol name="RESISTOR">
<description>&lt;b&gt;Library:&lt;/b&gt;  MF_Passives&lt;br/&gt;
&lt;b&gt;Description:&lt;/b&gt; Symbol for Resistors&lt;br/&gt;</description>
<pin name="P$1" x="0" y="5.08" visible="off" length="short" direction="pas" swaplevel="1" rot="R270"/>
<pin name="P$2" x="0" y="-5.08" visible="off" length="short" direction="pas" swaplevel="1" rot="R90"/>
<wire x1="0" y1="2.54" x2="1.016" y2="2.159" width="0.1524" layer="94"/>
<wire x1="1.016" y1="2.159" x2="-1.016" y2="1.524" width="0.1524" layer="94"/>
<wire x1="-1.016" y1="1.524" x2="1.016" y2="0.889" width="0.1524" layer="94"/>
<wire x1="1.016" y1="0.889" x2="-1.016" y2="0.254" width="0.1524" layer="94"/>
<wire x1="-1.016" y1="0.254" x2="1.016" y2="-0.381" width="0.1524" layer="94"/>
<wire x1="1.016" y1="-0.381" x2="-1.016" y2="-1.016" width="0.1524" layer="94"/>
<wire x1="-1.016" y1="-1.016" x2="1.016" y2="-1.651" width="0.1524" layer="94"/>
<wire x1="1.016" y1="-1.651" x2="-1.016" y2="-2.286" width="0.1524" layer="94"/>
<wire x1="-1.016" y1="-2.286" x2="0" y2="-2.54" width="0.1524" layer="94"/>
<text x="2.54" y="1.524" size="1.016" layer="95" font="vector" align="top-left">&gt;NAME</text>
<text x="2.54" y="-1.524" size="1.016" layer="96" font="vector">&gt;VALUE</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="RESISTOR" prefix="R" uservalue="yes">
<description>&lt;b&gt;Library:&lt;/b&gt;  MF_Passives&lt;br/&gt;
&lt;b&gt;Description:&lt;/b&gt; Device for Resistors. Manufacture part number (MPN), Voltage, Tolerance, and Wattage Rating can be added via Attributes.  Check https://factory.macrofab.com/parts for the house parts list.&lt;br/&gt;</description>
<gates>
<gate name="G$1" symbol="RESISTOR" x="0" y="0"/>
</gates>
<devices>
<device name="_0402" package="R0402">
<connects>
<connect gate="G$1" pin="P$1" pad="P$1"/>
<connect gate="G$1" pin="P$2" pad="P$2"/>
</connects>
<technologies>
<technology name="">
<attribute name="HOUSEPART" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="POPULATE" value="1" constant="no"/>
<attribute name="TOLERANCE" value="" constant="no"/>
<attribute name="URL" value="" constant="no"/>
<attribute name="VALUE" value="" constant="no"/>
<attribute name="VOLTAGE" value="" constant="no"/>
<attribute name="WATTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="_0603" package="R0603">
<connects>
<connect gate="G$1" pin="P$1" pad="P$1"/>
<connect gate="G$1" pin="P$2" pad="P$2"/>
</connects>
<technologies>
<technology name="">
<attribute name="HOUSEPART" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="POPULATE" value="1" constant="no"/>
<attribute name="TOLERANCE" value="" constant="no"/>
<attribute name="URL" value="" constant="no"/>
<attribute name="VALUE" value="" constant="no"/>
<attribute name="VOLTAGE" value="" constant="no"/>
<attribute name="WATTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="_0805" package="R0805">
<connects>
<connect gate="G$1" pin="P$1" pad="P$1"/>
<connect gate="G$1" pin="P$2" pad="P$2"/>
</connects>
<technologies>
<technology name="">
<attribute name="HOUSEPART" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="POPULATE" value="1" constant="no"/>
<attribute name="TOLERANCE" value="" constant="no"/>
<attribute name="URL" value="" constant="no"/>
<attribute name="VALUE" value="" constant="no"/>
<attribute name="VOLTAGE" value="" constant="no"/>
<attribute name="WATTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="_1206" package="R1206">
<connects>
<connect gate="G$1" pin="P$1" pad="P$1"/>
<connect gate="G$1" pin="P$2" pad="P$2"/>
</connects>
<technologies>
<technology name="">
<attribute name="HOUSEPART" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="POPULATE" value="1" constant="no"/>
<attribute name="TOLERANCE" value="" constant="no"/>
<attribute name="URL" value="" constant="no"/>
<attribute name="VALUE" value="" constant="no"/>
<attribute name="VOLTAGE" value="" constant="no"/>
<attribute name="WATTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="_1210" package="R1210">
<connects>
<connect gate="G$1" pin="P$1" pad="P$1"/>
<connect gate="G$1" pin="P$2" pad="P$2"/>
</connects>
<technologies>
<technology name="">
<attribute name="HOUSEPART" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="POPULATE" value="" constant="no"/>
<attribute name="TOLERANCE" value="" constant="no"/>
<attribute name="URL" value="" constant="no"/>
<attribute name="VALUE" value="" constant="no"/>
<attribute name="VOLTAGE" value="" constant="no"/>
<attribute name="WATTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0" drill="0">
</class>
</classes>
<parts>
<part name="U$1" library="GARTH" deviceset="SN65C1167" device=""/>
<part name="U$2" library="GARTH" deviceset="SN65C1167" device=""/>
<part name="GND1" library="SparkFun" deviceset="GND" device=""/>
<part name="GND2" library="SparkFun" deviceset="GND" device=""/>
<part name="C1" library="SparkFun" deviceset="CAP" device="0805" value=".1u"/>
<part name="C2" library="SparkFun" deviceset="CAP" device="0805" value=".1u"/>
<part name="R1" library="MF_Passives" deviceset="RESISTOR" device="_0805" value="1k"/>
<part name="R2" library="MF_Passives" deviceset="RESISTOR" device="_0805" value="1k"/>
<part name="R3" library="MF_Passives" deviceset="RESISTOR" device="_0805" value="1k"/>
<part name="R4" library="MF_Passives" deviceset="RESISTOR" device="_0805" value="1k"/>
<part name="R5" library="MF_Passives" deviceset="RESISTOR" device="_0805" value="100"/>
<part name="R6" library="MF_Passives" deviceset="RESISTOR" device="_0805" value="100"/>
<part name="R7" library="MF_Passives" deviceset="RESISTOR" device="_0805" value="100"/>
<part name="GND3" library="SparkFun" deviceset="GND" device=""/>
<part name="GND4" library="SparkFun" deviceset="GND" device=""/>
<part name="U$3" library="GARTH" deviceset="RJE01-660-02" device=""/>
<part name="U$4" library="GARTH" deviceset="RJSBE-5380-C2" device=""/>
<part name="GND5" library="SparkFun" deviceset="GND" device=""/>
</parts>
<sheets>
<sheet>
<plain>
</plain>
<instances>
<instance part="U$1" gate="G$1" x="48.26" y="71.12"/>
<instance part="U$2" gate="G$1" x="48.26" y="22.86"/>
<instance part="GND1" gate="1" x="27.94" y="48.26"/>
<instance part="GND2" gate="1" x="27.94" y="0"/>
<instance part="C1" gate="G$1" x="10.16" y="81.28"/>
<instance part="C2" gate="G$1" x="10.16" y="33.02"/>
<instance part="R1" gate="G$1" x="25.4" y="83.82" rot="R90"/>
<instance part="R2" gate="G$1" x="17.78" y="73.66"/>
<instance part="R3" gate="G$1" x="25.4" y="35.56" rot="R90"/>
<instance part="R4" gate="G$1" x="17.78" y="25.4"/>
<instance part="R5" gate="G$1" x="71.12" y="55.88"/>
<instance part="R6" gate="G$1" x="71.12" y="76.2"/>
<instance part="R7" gate="G$1" x="71.12" y="27.94"/>
<instance part="GND3" gate="1" x="15.24" y="60.96"/>
<instance part="GND4" gate="1" x="15.24" y="12.7"/>
<instance part="U$3" gate="G$1" x="-35.56" y="73.66"/>
<instance part="U$4" gate="G$1" x="124.46" y="73.66"/>
<instance part="GND5" gate="1" x="106.68" y="48.26"/>
</instances>
<busses>
</busses>
<nets>
<net name="VCC" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="VCC"/>
<wire x1="33.02" y1="88.9" x2="17.78" y2="88.9" width="0.1524" layer="91"/>
<label x="0" y="88.9" size="1.778" layer="95"/>
<pinref part="R1" gate="G$1" pin="P$1"/>
<wire x1="17.78" y1="88.9" x2="10.16" y2="88.9" width="0.1524" layer="91"/>
<wire x1="10.16" y1="88.9" x2="5.08" y2="88.9" width="0.1524" layer="91"/>
<wire x1="20.32" y1="83.82" x2="17.78" y2="83.82" width="0.1524" layer="91"/>
<wire x1="17.78" y1="83.82" x2="17.78" y2="88.9" width="0.1524" layer="91"/>
<junction x="17.78" y="88.9"/>
<pinref part="C1" gate="G$1" pin="1"/>
<wire x1="10.16" y1="86.36" x2="10.16" y2="88.9" width="0.1524" layer="91"/>
<junction x="10.16" y="88.9"/>
</segment>
<segment>
<pinref part="U$2" gate="G$1" pin="VCC"/>
<wire x1="33.02" y1="40.64" x2="17.78" y2="40.64" width="0.1524" layer="91"/>
<label x="0" y="40.64" size="1.778" layer="95"/>
<pinref part="R3" gate="G$1" pin="P$1"/>
<wire x1="17.78" y1="40.64" x2="10.16" y2="40.64" width="0.1524" layer="91"/>
<wire x1="10.16" y1="40.64" x2="5.08" y2="40.64" width="0.1524" layer="91"/>
<wire x1="20.32" y1="35.56" x2="17.78" y2="35.56" width="0.1524" layer="91"/>
<wire x1="17.78" y1="35.56" x2="17.78" y2="40.64" width="0.1524" layer="91"/>
<junction x="17.78" y="40.64"/>
<pinref part="C2" gate="G$1" pin="1"/>
<wire x1="10.16" y1="38.1" x2="10.16" y2="40.64" width="0.1524" layer="91"/>
<junction x="10.16" y="40.64"/>
</segment>
<segment>
<pinref part="U$3" gate="G$1" pin="5@1"/>
<wire x1="-48.26" y1="66.04" x2="-50.8" y2="66.04" width="0.1524" layer="91"/>
<label x="-58.42" y="66.04" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$3" gate="G$1" pin="5@2"/>
<wire x1="-22.86" y1="66.04" x2="-20.32" y2="66.04" width="0.1524" layer="91"/>
<label x="-17.78" y="66.04" size="1.778" layer="95"/>
</segment>
</net>
<net name="D1" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="1D"/>
<wire x1="33.02" y1="73.66" x2="30.48" y2="73.66" width="0.1524" layer="91"/>
<label x="25.4" y="73.66" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$3" gate="G$1" pin="4@1"/>
<wire x1="-48.26" y1="71.12" x2="-50.8" y2="71.12" width="0.1524" layer="91"/>
<label x="-58.42" y="71.12" size="1.778" layer="95"/>
</segment>
</net>
<net name="D2" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="2D"/>
<wire x1="33.02" y1="63.5" x2="30.48" y2="63.5" width="0.1524" layer="91"/>
<label x="25.4" y="63.5" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$3" gate="G$1" pin="3@1"/>
<wire x1="-48.26" y1="76.2" x2="-50.8" y2="76.2" width="0.1524" layer="91"/>
<label x="-58.42" y="76.2" size="1.778" layer="95"/>
</segment>
</net>
<net name="D3" class="0">
<segment>
<pinref part="U$2" gate="G$1" pin="1D"/>
<wire x1="33.02" y1="25.4" x2="30.48" y2="25.4" width="0.1524" layer="91"/>
<label x="25.4" y="25.4" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$3" gate="G$1" pin="2@1"/>
<wire x1="-48.26" y1="81.28" x2="-50.8" y2="81.28" width="0.1524" layer="91"/>
<label x="-58.42" y="81.28" size="1.778" layer="95"/>
</segment>
</net>
<net name="GND" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="GND"/>
<wire x1="33.02" y1="53.34" x2="27.94" y2="53.34" width="0.1524" layer="91"/>
<wire x1="27.94" y1="53.34" x2="27.94" y2="50.8" width="0.1524" layer="91"/>
<pinref part="GND1" gate="1" pin="GND"/>
</segment>
<segment>
<pinref part="U$2" gate="G$1" pin="GND"/>
<wire x1="33.02" y1="5.08" x2="27.94" y2="5.08" width="0.1524" layer="91"/>
<wire x1="27.94" y1="5.08" x2="27.94" y2="2.54" width="0.1524" layer="91"/>
<pinref part="GND2" gate="1" pin="GND"/>
</segment>
<segment>
<pinref part="C1" gate="G$1" pin="2"/>
<wire x1="10.16" y1="78.74" x2="10.16" y2="66.04" width="0.1524" layer="91"/>
<pinref part="R2" gate="G$1" pin="P$2"/>
<wire x1="17.78" y1="68.58" x2="17.78" y2="66.04" width="0.1524" layer="91"/>
<wire x1="17.78" y1="66.04" x2="15.24" y2="66.04" width="0.1524" layer="91"/>
<pinref part="GND3" gate="1" pin="GND"/>
<wire x1="15.24" y1="66.04" x2="10.16" y2="66.04" width="0.1524" layer="91"/>
<wire x1="15.24" y1="63.5" x2="15.24" y2="66.04" width="0.1524" layer="91"/>
<junction x="15.24" y="66.04"/>
</segment>
<segment>
<pinref part="C2" gate="G$1" pin="2"/>
<wire x1="10.16" y1="30.48" x2="10.16" y2="17.78" width="0.1524" layer="91"/>
<wire x1="10.16" y1="17.78" x2="15.24" y2="17.78" width="0.1524" layer="91"/>
<pinref part="R4" gate="G$1" pin="P$2"/>
<wire x1="15.24" y1="17.78" x2="17.78" y2="17.78" width="0.1524" layer="91"/>
<wire x1="17.78" y1="17.78" x2="17.78" y2="20.32" width="0.1524" layer="91"/>
<pinref part="GND4" gate="1" pin="GND"/>
<wire x1="15.24" y1="15.24" x2="15.24" y2="17.78" width="0.1524" layer="91"/>
<junction x="15.24" y="17.78"/>
</segment>
<segment>
<pinref part="U$3" gate="G$1" pin="1@1"/>
<wire x1="-48.26" y1="86.36" x2="-50.8" y2="86.36" width="0.1524" layer="91"/>
<label x="-58.42" y="86.36" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$3" gate="G$1" pin="1@2"/>
<wire x1="-22.86" y1="86.36" x2="-20.32" y2="86.36" width="0.1524" layer="91"/>
<label x="-17.78" y="86.36" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="6@1"/>
<wire x1="109.22" y1="76.2" x2="106.68" y2="76.2" width="0.1524" layer="91"/>
<label x="96.52" y="76.2" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="3@1"/>
<wire x1="109.22" y1="83.82" x2="106.68" y2="83.82" width="0.1524" layer="91"/>
<label x="96.52" y="83.82" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="6@2"/>
<wire x1="139.7" y1="76.2" x2="142.24" y2="76.2" width="0.1524" layer="91"/>
<label x="144.78" y="76.2" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="3@2"/>
<wire x1="139.7" y1="83.82" x2="142.24" y2="83.82" width="0.1524" layer="91"/>
<label x="144.78" y="83.82" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="SHIELD@1"/>
<pinref part="GND5" gate="1" pin="GND"/>
<wire x1="109.22" y1="58.42" x2="106.68" y2="58.42" width="0.1524" layer="91"/>
<wire x1="106.68" y1="58.42" x2="106.68" y2="50.8" width="0.1524" layer="91"/>
</segment>
</net>
<net name="R1" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="1R"/>
<wire x1="33.02" y1="68.58" x2="30.48" y2="68.58" width="0.1524" layer="91"/>
<label x="25.4" y="68.58" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$3" gate="G$1" pin="4@2"/>
<wire x1="-22.86" y1="71.12" x2="-20.32" y2="71.12" width="0.1524" layer="91"/>
<label x="-17.78" y="71.12" size="1.778" layer="95"/>
</segment>
</net>
<net name="R2" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="2R"/>
<wire x1="33.02" y1="58.42" x2="30.48" y2="58.42" width="0.1524" layer="91"/>
<label x="25.4" y="58.42" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$3" gate="G$1" pin="3@2"/>
<wire x1="-22.86" y1="76.2" x2="-20.32" y2="76.2" width="0.1524" layer="91"/>
<label x="-17.78" y="76.2" size="1.778" layer="95"/>
</segment>
</net>
<net name="R3" class="0">
<segment>
<pinref part="U$2" gate="G$1" pin="1R"/>
<wire x1="33.02" y1="20.32" x2="30.48" y2="20.32" width="0.1524" layer="91"/>
<label x="25.4" y="20.32" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$3" gate="G$1" pin="2@2"/>
<wire x1="-22.86" y1="81.28" x2="-20.32" y2="81.28" width="0.1524" layer="91"/>
<label x="-17.78" y="81.28" size="1.778" layer="95"/>
</segment>
</net>
<net name="D4" class="0">
<segment>
<pinref part="U$2" gate="G$1" pin="2D"/>
<wire x1="33.02" y1="15.24" x2="30.48" y2="15.24" width="0.1524" layer="91"/>
<label x="25.4" y="15.24" size="1.778" layer="95"/>
</segment>
</net>
<net name="R4" class="0">
<segment>
<pinref part="U$2" gate="G$1" pin="2R"/>
<wire x1="33.02" y1="10.16" x2="30.48" y2="10.16" width="0.1524" layer="91"/>
<label x="25.4" y="10.16" size="1.778" layer="95"/>
</segment>
</net>
<net name="N$1" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="DE"/>
<pinref part="R1" gate="G$1" pin="P$2"/>
<wire x1="33.02" y1="83.82" x2="30.48" y2="83.82" width="0.1524" layer="91"/>
</segment>
</net>
<net name="N$3" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="!RE"/>
<pinref part="R2" gate="G$1" pin="P$1"/>
<wire x1="33.02" y1="78.74" x2="17.78" y2="78.74" width="0.1524" layer="91"/>
</segment>
</net>
<net name="N$5" class="0">
<segment>
<pinref part="U$2" gate="G$1" pin="DE"/>
<pinref part="R3" gate="G$1" pin="P$2"/>
<wire x1="33.02" y1="35.56" x2="30.48" y2="35.56" width="0.1524" layer="91"/>
</segment>
</net>
<net name="N$6" class="0">
<segment>
<pinref part="R4" gate="G$1" pin="P$1"/>
<pinref part="U$2" gate="G$1" pin="!RE"/>
<wire x1="17.78" y1="30.48" x2="33.02" y2="30.48" width="0.1524" layer="91"/>
</segment>
</net>
<net name="D-BR-1" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="1Y"/>
<wire x1="58.42" y1="88.9" x2="60.96" y2="88.9" width="0.1524" layer="91"/>
<label x="63.5" y="88.9" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="8@2"/>
<wire x1="139.7" y1="71.12" x2="142.24" y2="71.12" width="0.1524" layer="91"/>
<label x="144.78" y="71.12" size="1.778" layer="95"/>
</segment>
</net>
<net name="D-BR-2" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="1Z"/>
<wire x1="58.42" y1="83.82" x2="60.96" y2="83.82" width="0.1524" layer="91"/>
<label x="63.5" y="83.82" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="7@2"/>
<wire x1="139.7" y1="73.66" x2="142.24" y2="73.66" width="0.1524" layer="91"/>
<label x="144.78" y="73.66" size="1.778" layer="95"/>
</segment>
</net>
<net name="D-B-2" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="2Z"/>
<wire x1="58.42" y1="63.5" x2="60.96" y2="63.5" width="0.1524" layer="91"/>
<label x="63.5" y="63.5" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="5@2"/>
<wire x1="139.7" y1="78.74" x2="142.24" y2="78.74" width="0.1524" layer="91"/>
<label x="144.78" y="78.74" size="1.778" layer="95"/>
</segment>
</net>
<net name="D-B-1" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="2Y"/>
<wire x1="58.42" y1="68.58" x2="60.96" y2="68.58" width="0.1524" layer="91"/>
<label x="63.5" y="68.58" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="4@2"/>
<wire x1="139.7" y1="81.28" x2="142.24" y2="81.28" width="0.1524" layer="91"/>
<label x="144.78" y="81.28" size="1.778" layer="95"/>
</segment>
</net>
<net name="R-B-1" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="2A"/>
<wire x1="58.42" y1="58.42" x2="68.58" y2="58.42" width="0.1524" layer="91"/>
<wire x1="68.58" y1="58.42" x2="68.58" y2="60.96" width="0.1524" layer="91"/>
<pinref part="R5" gate="G$1" pin="P$1"/>
<wire x1="68.58" y1="60.96" x2="71.12" y2="60.96" width="0.1524" layer="91"/>
<wire x1="71.12" y1="60.96" x2="76.2" y2="60.96" width="0.1524" layer="91"/>
<junction x="71.12" y="60.96"/>
<label x="78.74" y="60.96" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="4@1"/>
<wire x1="109.22" y1="81.28" x2="106.68" y2="81.28" width="0.1524" layer="91"/>
<label x="96.52" y="81.28" size="1.778" layer="95"/>
</segment>
</net>
<net name="R-BR-1" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="1A"/>
<wire x1="58.42" y1="78.74" x2="68.58" y2="78.74" width="0.1524" layer="91"/>
<wire x1="68.58" y1="78.74" x2="68.58" y2="81.28" width="0.1524" layer="91"/>
<pinref part="R6" gate="G$1" pin="P$1"/>
<wire x1="68.58" y1="81.28" x2="71.12" y2="81.28" width="0.1524" layer="91"/>
<wire x1="71.12" y1="81.28" x2="76.2" y2="81.28" width="0.1524" layer="91"/>
<junction x="71.12" y="81.28"/>
<label x="78.74" y="81.28" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="8@1"/>
<wire x1="109.22" y1="71.12" x2="106.68" y2="71.12" width="0.1524" layer="91"/>
<label x="96.52" y="71.12" size="1.778" layer="95"/>
</segment>
</net>
<net name="R-BR-2" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="1B"/>
<wire x1="58.42" y1="73.66" x2="68.58" y2="73.66" width="0.1524" layer="91"/>
<wire x1="68.58" y1="73.66" x2="68.58" y2="71.12" width="0.1524" layer="91"/>
<pinref part="R6" gate="G$1" pin="P$2"/>
<wire x1="68.58" y1="71.12" x2="71.12" y2="71.12" width="0.1524" layer="91"/>
<wire x1="71.12" y1="71.12" x2="76.2" y2="71.12" width="0.1524" layer="91"/>
<junction x="71.12" y="71.12"/>
<label x="78.74" y="71.12" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="7@1"/>
<wire x1="109.22" y1="73.66" x2="106.68" y2="73.66" width="0.1524" layer="91"/>
<label x="96.52" y="73.66" size="1.778" layer="95"/>
</segment>
</net>
<net name="R-B-2" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="2B"/>
<wire x1="58.42" y1="53.34" x2="68.58" y2="53.34" width="0.1524" layer="91"/>
<wire x1="68.58" y1="53.34" x2="68.58" y2="50.8" width="0.1524" layer="91"/>
<pinref part="R5" gate="G$1" pin="P$2"/>
<wire x1="68.58" y1="50.8" x2="71.12" y2="50.8" width="0.1524" layer="91"/>
<wire x1="71.12" y1="50.8" x2="76.2" y2="50.8" width="0.1524" layer="91"/>
<junction x="71.12" y="50.8"/>
<label x="78.74" y="50.8" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="5@1"/>
<wire x1="109.22" y1="78.74" x2="106.68" y2="78.74" width="0.1524" layer="91"/>
<label x="96.52" y="78.74" size="1.778" layer="95"/>
</segment>
</net>
<net name="D-O-1" class="0">
<segment>
<pinref part="U$2" gate="G$1" pin="1Y"/>
<wire x1="58.42" y1="40.64" x2="60.96" y2="40.64" width="0.1524" layer="91"/>
<label x="63.5" y="40.64" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="2@2"/>
<wire x1="139.7" y1="86.36" x2="142.24" y2="86.36" width="0.1524" layer="91"/>
<label x="144.78" y="86.36" size="1.778" layer="95"/>
</segment>
</net>
<net name="D-O-2" class="0">
<segment>
<pinref part="U$2" gate="G$1" pin="1Z"/>
<wire x1="58.42" y1="35.56" x2="60.96" y2="35.56" width="0.1524" layer="91"/>
<label x="63.5" y="35.56" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="1@2"/>
<wire x1="139.7" y1="88.9" x2="142.24" y2="88.9" width="0.1524" layer="91"/>
<label x="144.78" y="88.9" size="1.778" layer="95"/>
</segment>
</net>
<net name="R-O-1" class="0">
<segment>
<pinref part="U$2" gate="G$1" pin="1A"/>
<wire x1="58.42" y1="30.48" x2="68.58" y2="30.48" width="0.1524" layer="91"/>
<wire x1="68.58" y1="30.48" x2="68.58" y2="33.02" width="0.1524" layer="91"/>
<pinref part="R7" gate="G$1" pin="P$1"/>
<wire x1="68.58" y1="33.02" x2="71.12" y2="33.02" width="0.1524" layer="91"/>
<wire x1="71.12" y1="33.02" x2="76.2" y2="33.02" width="0.1524" layer="91"/>
<junction x="71.12" y="33.02"/>
<label x="78.74" y="33.02" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="2@1"/>
<wire x1="109.22" y1="86.36" x2="106.68" y2="86.36" width="0.1524" layer="91"/>
<label x="96.52" y="86.36" size="1.778" layer="95"/>
</segment>
</net>
<net name="R-O-2" class="0">
<segment>
<pinref part="U$2" gate="G$1" pin="1B"/>
<wire x1="58.42" y1="25.4" x2="68.58" y2="25.4" width="0.1524" layer="91"/>
<wire x1="68.58" y1="25.4" x2="68.58" y2="22.86" width="0.1524" layer="91"/>
<pinref part="R7" gate="G$1" pin="P$2"/>
<wire x1="68.58" y1="22.86" x2="71.12" y2="22.86" width="0.1524" layer="91"/>
<wire x1="71.12" y1="22.86" x2="76.2" y2="22.86" width="0.1524" layer="91"/>
<junction x="71.12" y="22.86"/>
<label x="78.74" y="22.86" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="1@1"/>
<wire x1="109.22" y1="88.9" x2="106.68" y2="88.9" width="0.1524" layer="91"/>
<label x="96.52" y="88.9" size="1.778" layer="95"/>
</segment>
</net>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
</eagle>
