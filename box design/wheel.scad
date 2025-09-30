// Control wheels for 3-axis controller
use <fillets_and_rounds.scad>

module shaft(id=6.6,od=10,slot_w=1,ih=18,oh=5,sl=10){
    $fn=30;
    cylinder(d=id,h=ih);
    translate([0,0,-1])cylinder(d=od,h=oh+1);
    translate([0,0,ih/2])add_rounds(axis="z",R=0.4)cube([slot_w,od,ih],center=true);
}//end shaft

module c_wheel(d=40,h=20,ddimple=15,ddepth=10,fillet=2,fn=40){
    $fn=fn;
    translate([0,0,h/2])difference(){
        hull(){
            cylinder(d=d-fillet,h=h,center=true);
            cylinder(d=d,h=h-fillet,center=true);
        }//end hull
        translate([d/2-ddimple/2-fillet,0,h/2])scale([1,1,ddepth/ddimple])sphere(d=ddimple);
    }//end difference
}//end c_wheel

module wheel(d=60,h=20,ddimple=20,ddepth=10,fillet=2,fn=60,
id=6.4,od=15.5,slot_w=1,ih=18,oh=5,sl=10){
difference(){
c_wheel(d=d,h=h,ddimple=ddimple,ddepth=ddepth,fillet=fillet,fn=fn);
shaft(id=id,od=od,slot_w=slot_w,ih=ih,oh=oh,sl=sl);
}}

wheel();