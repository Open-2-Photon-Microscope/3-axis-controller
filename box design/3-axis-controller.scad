//3-axis controller
use <wheel.scad>
use <enclosure.scad>
use <fillets_and_rounds.scad>

space = 30;

module dial(){
    union(){
translate([-1.22,0,-10])ena1j();
translate([0,0,2.05])color("red",0.3)wheel();}}

module test_box(){
difference(){
    translate([-15,-15,-15])add_rounds(R=4,fn=6)cube(47);
    translate([-16,-16,-16])cube(40);
    translate([0,0,space])rotate([0,0,90])dial();
    translate([0,space,0])rotate([-90,0,0])dial();
    translate([space,0,0])rotate([90,-90,90])dial();}}

//test_box();

module dials(){
color("red",0.3){translate([0,0,space])rotate([0,0,90])dial();
translate([0,space,0])rotate([-90,0,0])dial();
translate([space,0,0])rotate([90,-90,90])dial();}}

//translate([30,30,30])dials();

module Xboard(){
    $fn=6;
    translate([3.6,5.2])cylinder(d=3.3,h=10);
    translate([42,53.5,0])cylinder(d=3.3,h=10);
    %cube([48,60,1]);
}//end Xboard



module box(x=113,y=150,z=56,w=10){
    difference(){
        translate([-w/2,-w/2,0])add_rounds(R=4,fn=7)cube([x+w,y+w,z+w]);
        translate([0,0,-1])cube([x,y,z+1]);
        translate([x+w/2-32,y+w/2-32,z+w-32])dials();
        translate([12,-w,-5])add_rounds(R=4,axis="y")cube([x-24,w*2,35]);
        translate([-w,20,-5])add_rounds(R=4,axis="x")cube([w*2,42,30]);
        translate([x*0.6,y*0.45,z+2])push_switch();
        translate([x*0.85,y*0.45,z+2])push_switch();
        translate([x/2,20,z+7])rotate([0,0,-90])lcd();
        translate([5,20,z+3])rotate([0,0,-90])pwr_switch();
        translate([x+w-60,y-49,z-5])rotate([0,0,90])Xboard();
    }//end difference
    difference(){
    for(xi=[0:101:102]){
            for(yi=[0:90.5:91]){
                translate([xi,yi,4])cube([12,10,z-4]);}}
    translate([0,1,0])board();}
    %translate([x+w/2-32,y+w/2-32,z+w-32])dials();
}//end box

box();

module board(h=10,d=3.3){
        %linear_extrude(5)polygon([[0,0],[0,98.5],[111,98.5],[110,0]]);
        linear_extrude(h)translate([5.5,4.2])for(x=[0:101:102]){
            for(y=[0:90.5:91]){
                translate([x,y])circle(d=d,$fn=6);
            }}//end for
}//end board

