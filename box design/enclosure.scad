module base(x, y, h=5, slot=true, hr){
    // x and y refer to screw hole positions
    translate([-1*x/2,y/2,0])screw_post(h, slot=slot, hole_ratio=hr);
    translate([-1*x/2,-1*y/2,0])screw_post(h, slot=slot, hole_ratio=hr);
    rotate([0,0,180]){
        translate([-1*x/2,y/2,0])screw_post(h, slot=slot, hole_ratio=hr);
        translate([-1*x/2,-1*y/2,0])screw_post(h, slot=slot, hole_ratio=hr);
    }//end rotate
    
}// end module base

//base(91,101); // board x=91 y=101


//base(75,32); // lcd

module screw_post(height, nut_h=2.8,slot=true, hole_ratio=0.25){
    translate([0,0,height/2])difference(){
        
        // shell
        cube([8,8,height],center=true);
        // cutouts
        union(){
            // center hole
            translate([0,0,-height/hole_ratio])cylinder(d=3.4, h= height, $fn=18);
            
            if(slot==true){
            // nut
            translate([0,0,height/2-3])cylinder(d=6.95, h= nut_h, center=true,$fn=6);
            // side exit
            translate([-5,0,height/2-3])cube([10,6,nut_h],center=true);
            // overhang trick
            translate([0,0,height/2-1.6])cube([3.4,6,0.3],center=true);}//end if
        }
        
    }// end difference
}// end module screw_post

//screw_post(10);


module ena1j(){ // model of the rotary encoder
    cube([21.5,16,18.5],center=true);
    translate([21.5/2-9.53,0,18.5/2])cylinder(d=9.8,h=6.35,$fn=28);
    translate([21.5/2-9.53,8,18.5/2]){difference(){
        cylinder(h=1.7,d=3,$fn=18);
        translate([0,3.5/2,0])cube(3.5,center=true);
    }//end difference
    }//end translate
}//end ena1j

//ena1j();

module lcd(){
    // screen
    cube([24.5,71.5,8],center=true);
    
    // space for soldered pins
    translate([(24.5+6.6)/2,71.5/2-42/2,-3.3/2])cube([6.6,42,3.3],center=true);
    
    // space for part of backlight
    translate([0,(71.5+4.6)/-2,2.85/2-3.3])cube([24.5,4.6,2.85],center=true);
    
    //screw holes
    translate([16,75/2,0])cylinder(d=3.4,h=15, center=true, $fn=18);
    translate([-15,75/2,0])cylinder(d=3.4,h=15, center=true, $fn=18);
    translate([16,-75/2,0])cylinder(d=3.4,h=15, center=true, $fn=18);
    translate([-15 ,-75/2,0])cylinder(d=3.4,h=15, center=true, $fn=18);
}// end lcd

//lcd();

module pwr_switch(){
    cube([13, 7,8.9],center=true);
    translate([0,0,8.9/2])cylinder(d=6.8,h=8.9,$fn=25);
    translate([6.1,0,8.9/2])cylinder(d=2.5,h=3,$fn=18);
}// end module pwr_switch

//pwr_switch();

module push_switch(){
    cube([6.9,8.4,8.4],center=true);
    translate([0,0,4.2])cylinder(d=5,h=5.6,$fn=18);
}//end module push_switch

//push_switch();

module feet(d, screw_d, head_d, h){
    $fn = 28;
    difference(){
        cylinder(d=d, h=h);
        cylinder(d = screw_d, h=h);
        cylinder(d=head_d, h=h*2/3);
    }//end difference
}// end module feet

//feet(8, 3.4, 5.6, 5);


module top_enclosure(x, y, z, h){
    enj_depth = -8;
    enj_x = -30;
    enj_y = 35;
    translate([0,0,z/2])difference(){
        cube([x, y, z], center=true);
        union(){
            translate([25,0,0.75])lcd();
            
            translate([5,-5,0]){ // ena1j encoders
            translate([enj_x,enj_y,enj_depth])ena1j();
            translate([enj_x,0,enj_depth])ena1j();
            translate([enj_x,-1*enj_y,enj_depth])ena1j();
            }// end translate
            
            translate([25,-48,-3.5])pwr_switch();
            
            translate([5,0,0]){ // push switches
            translate([0,48,-3.2])push_switch();
            translate([-20,48,-3.2])push_switch();
            }// end translate
        }//end union
        }//end difference
        rotate([180,0,0])base(91,101,h);
        
}//end module top_lvl

%top_enclosure(100,114,5,45);

module outer_enclosure(x=105, y=119, z=55){
    inner_dims = [100,114,50];
    
    difference(){
        translate([0,0,-z/2+5])cube([x,y,z],center=true);
        translate([0,0,-20])cube(inner_dims,center=true);
    }//end difference
    base(91,101,5);
}//end module outer_enclosure

%outer_enclosure();

base(91,101,5,slot=false);