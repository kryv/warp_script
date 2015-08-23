(* ::Package:: *)

(* ::Input:: *)
(*$HistoryLength=3;*)
(**)


(* ::Input:: *)
(*dipt=Import["frib_front_sims\\warp\\lattice_dipole\\D5CP5_03A_map.table","Table"];*)


(* ::Input:: *)
(*ffa[{a_,b_,c_,d_}]:={{-c,b,a},-d/10000}*)
(*ans3x=Interpolation[Map[ffa,dipt[[9;;,{1,2,3,6}]]], Method->"Spline",InterpolationOrder->3]*)
(*ffa[{a_,b_,c_,d_}]:={{-c,b,a},-d/10000}*)
(*ans3y=Interpolation[Map[ffa,dipt[[9;;,{1,2,3,5}]]], Method->"Spline",InterpolationOrder->3]*)
(*ffa[{a_,b_,c_,d_}]:={{-c,b,a},-d/10000}*)
(*ans3z=Interpolation[Map[ffa,dipt[[9;;,{1,2,3,4}]]], Method->"Spline",InterpolationOrder->3]*)
(**)


(* ::Input:: *)
(*ffa[{a_,b_,c_,d_}]:={{-c,b,a},d}*)
(*ans1x=Interpolation[Map[ffa,dipt[[9;;,{1,2,3,6}]]], Method->"Spline",InterpolationOrder->1]*)
(*ffa[{a_,b_,c_,d_}]:={{-c,b,a},-d}*)
(*ans1y=Interpolation[Map[ffa,dipt[[9;;,{1,2,3,5}]]], Method->"Spline",InterpolationOrder->1]*)
(*ffa[{a_,b_,c_,d_}]:={{-c,b,a},-d}*)
(*ans1z=Interpolation[Map[ffa,dipt[[9;;,{1,2,3,4}]]], Method->"Spline",InterpolationOrder->1]*)


(* ::Input:: *)
(*(*Grid info*)*)
(*rc=63.5;*)
(*rcr=rc/Sqrt[2];*)
(*zs=53;*)
(*nz=500;*)
(*zlen=zs*2+rc*2*Pi/4.0; (*z length [cm]*)*)
(*dz=zlen/nz*)
(**)
(*xw=42.0;(*x width [cm]*)*)
(*nx=105;*)
(*dx=xw/nx*)
(*yw=10.; (*y width [cm]*)*)
(*ny=25;*)
(*dy=yw/ny*)
(*ot=Pi/4; *)
(**)
(**)


(* ::PageBreak:: *)
(**)


(* ::Input:: *)
(*(*data check scetion*)*)
(*ListContourPlot[Flatten[*)
(*st0=*)
(*Table[*)
(*Which[z<=0,*)
(*zr=-x*Cos[ot]+z*Sin[ot];*)
(*xr=x*Sin[ot]+z*Cos[ot];*)
(*xo=xr+rcr;zo=zr-rcr;*)
(*{z,x,ans1y[xo,0,zo]},*)
(*z<=rc*2*Pi/4.0,*)
(*zo=-(rc+x)*Cos[z/rc+ot];*)
(*xo=(rc+x)*Sin[z/rc+ot];*)
(*{z,x,ans1y[xo,0,zo]},*)
(*z<=zs+rc*2*Pi/4.0,*)
(*zr=-x*Cos[ot+Pi/2]+(z-rc*2*Pi/4.0)*Sin[ot+Pi/2];*)
(*xr=x*Sin[ot+Pi/2]+(z-rc*2*Pi/4.0)*Cos[ot+Pi/2];*)
(*xo=xr+rcr;zo=zr+rcr;*)
(*{z,x,ans1y[xo,0,zo]}*)
(*],{x,-xw/2,xw/2,dx},{z,-zs,zs+rc*2*Pi/4.0,dz}],1]*)
(*,Contours->50,*)
(*AspectRatio->0.5,FrameTicksStyle->20,ImageSize->700,PlotRange->All]*)


(* ::Input:: *)
(*ListContourPlot[Flatten[*)
(*st0=*)
(*Table[*)
(*Which[z<=0,*)
(*zr=-x*Cos[ot]+z*Sin[ot];*)
(*xr=x*Sin[ot]+z*Cos[ot];*)
(*xo=xr+rcr;zo=zr-rcr;*)
(*{x,y,ans1x[xo,y,zo]*Sin[ot]-ans1z[xo,y,zo]*Cos[ot]},*)
(*z<=rc*2*Pi/4.0,*)
(*zo=-(rc+x)*Cos[z/rc+ot];*)
(*xo=(rc+x)*Sin[z/rc+ot];*)
(*{x,y,ans1x[xo,y,zo]*Sin[z/rc+ot]-ans1z[xo,y,zo]*Cos[z/rc+ot]},*)
(*z<=zs+rc*2*Pi/4.0,*)
(*zr=-x*Cos[ot+Pi/2]+(z-rc*2*Pi/4.0)*Sin[ot+Pi/2];*)
(*xr=x*Sin[ot+Pi/2]+(z-rc*2*Pi/4.0)*Cos[ot+Pi/2];*)
(*xo=xr+rcr;zo=zr+rcr;*)
(*{x,y,ans1x[xo,y,zo]*Sin[ot+Pi/2]-ans1z[xo,y,zo]*Cos[ot+Pi/2]}*)
(*],{x,-xw/2,xw/2,dx},{y,-yw/2,yw/2,dy},{z,{50}}],2]*)
(*,Contours->50,*)
(*AspectRatio->0.5,FrameTicksStyle->20,ImageSize->700,PlotRange->All]*)
(**)


(* ::Input:: *)
(*(* Test Vector*)*)
(*fncx[x_,y_,z_]:=1.0*)
(*fncz[x_,y_,z_]:=2.0*)
(**)


(* ::Input:: *)
(*(*Test Vector new Bx*)*)
(*ListPlot[Flatten[*)
(*st0=*)
(*Table[*)
(*Which[z<=0,*)
(*zr=-x*Cos[ot]+z*Sin[ot];*)
(*xr=x*Sin[ot]+z*Cos[ot];*)
(*xo=xr+rcr;zo=zr-rcr;*)
(*{z,fncx[xo,0,zo]*Sin[ot]-fncz[xo,0,zo]*Cos[ot]},*)
(*z<=rc*2*Pi/4.0,*)
(*zo=-(rc+x)*Cos[z/rc+ot];*)
(*xo=(rc+x)*Sin[z/rc+ot];*)
(*{z,fncx[xo,0,zo]*Sin[z/rc+ot]-fncz[xo,0,zo]*Cos[z/rc+ot]},*)
(*z<=zs+rc*2*Pi/4.0,*)
(*zr=-x*Cos[ot+Pi/2]+(z-rc*2*Pi/4.0)*Sin[ot+Pi/2];*)
(*xr=x*Sin[ot+Pi/2]+(z-rc*2*Pi/4.0)*Cos[ot+Pi/2];*)
(*xo=xr+rcr;zo=zr+rcr;*)
(*{z,fncx[xo,0,zo]*Sin[ot+Pi/2]-fncz[xo,0,zo]*Cos[ot+Pi/2]}*)
(*],{x,{0}},{z,-zs,zs+rc*2*Pi/4.0,dz}],1],*)
(*AspectRatio->0.5,FrameTicksStyle->20,ImageSize->700,PlotRange->All,*)
(*GridLines->{Automatic,{-1/Sqrt[2],1,3/Sqrt[2]}},GridLinesStyle->Directive[Red,Thick]]*)
(**)


(* ::Input:: *)
(*(*Test Vector new Bz*)*)
(*ListPlot[Flatten[*)
(*st0=*)
(*Table[*)
(*Which[z<=0,*)
(*zr=-x*Cos[ot]+z*Sin[ot];*)
(*xr=x*Sin[ot]+z*Cos[ot];*)
(*xo=xr+rcr;zo=zr-rcr;*)
(*{z,fncx[xo,0,zo]*Cos[ot]+fncz[xo,0,zo]*Sin[ot]},*)
(*z<=rc*2*Pi/4.0,*)
(*zo=-(rc+x)*Cos[z/rc+ot];*)
(*xo=(rc+x)*Sin[z/rc+ot];*)
(*{z,fncx[xo,0,zo]*Cos[z/rc+ot]+fncz[xo,0,zo]*Sin[z/rc+ot]},*)
(*z<=zs+rc*2*Pi/4.0,*)
(*zr=-x*Cos[ot+Pi/2]+(z-rc*2*Pi/4.0)*Sin[ot+Pi/2];*)
(*xr=x*Sin[ot+Pi/2]+(z-rc*2*Pi/4.0)*Cos[ot+Pi/2];*)
(*xo=xr+rcr;zo=zr+rcr;*)
(*{z,fncx[xo,0,zo]*Cos[ot+Pi/2]+fncz[xo,0,zo]*Sin[ot+Pi/2]}*)
(*],{x,{10}},{z,-zs,zs+rc*2*Pi/4.0,dz}],1],*)
(*AspectRatio->0.5,FrameTicksStyle->20,ImageSize->700,PlotRange->All,*)
(*GridLines->{Automatic,{3/Sqrt[2],Sqrt[5],1/Sqrt[2]}},GridLinesStyle->Directive[Red,Thick]]*)
(**)
(**)


(* ::PageBreak:: *)
(**)


(* ::Input:: *)
(*(*Make .dat data*)*)
(*stbxyz=*)
(*Table[*)
(*Which[z<=0,*)
(*zr=-x*Cos[ot]+z*Sin[ot];*)
(*xr=x*Sin[ot]+z*Cos[ot];*)
(*xo=xr+rcr;zo=zr-rcr;*)
(*{ans1x[xo,y,zo]*Sin[ot]-ans1z[xo,y,zo]*Cos[ot],*)
(*ans1y[xo,y,zo],*)
(*ans1x[xo,y,zo]*Cos[ot]+ans1z[xo,y,zo]*Sin[ot]},*)
(**)
(*z<=rc*2*Pi/4.0,*)
(*zo=-(rc+x)*Cos[z/rc+ot];*)
(*xo=(rc+x)*Sin[z/rc+ot];*)
(*{ans1x[xo,y,zo]*Sin[z/rc+ot]-ans1z[xo,y,zo]*Cos[z/rc+ot],*)
(*ans1y[xo,y,zo],*)
(*ans1x[xo,y,zo]*Cos[z/rc+ot]+ans1z[xo,y,zo]*Sin[z/rc+ot]},*)
(**)
(*z<=zs+rc*2*Pi/4.0,*)
(*zr=-x*Cos[ot+Pi/2]+(z-rc*2*Pi/4.0)*Sin[ot+Pi/2];*)
(*xr=x*Sin[ot+Pi/2]+(z-rc*2*Pi/4.0)*Cos[ot+Pi/2];*)
(*xo=xr+rcr;zo=zr+rcr;*)
(*{ans1x[xo,y,zo]*Sin[ot+Pi/2]-ans1z[xo,y,zo]*Cos[ot+Pi/2],*)
(*ans1y[xo,y,zo],*)
(*ans1x[xo,y,zo]*Cos[ot+Pi/2]+ans1z[xo,y,zo]*Sin[ot+Pi/2]}*)
(*],{x,-xw/2,xw/2,dx},{y,-yw/2,yw/2,dy},{z,-zs,zs+rc*2*Pi/4.0,dz}];*)
(**)


(* ::Input:: *)
(*(*Export data*)*)
(*Export["bend_trans.dat",Flatten[stbxyz,2],"Table"]*)
