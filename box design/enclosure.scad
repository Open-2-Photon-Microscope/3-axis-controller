module base(x, y, h=5, slot=true, hr=0.25, outer=true, hole_diam=3.4){
    // x and y refer to screw hole positions
    translate([-1*x/2,y/2,0])screw_post(h, slot=slot, hole_ratio=hr,outer=outer,hole_diam=hole_diam);
    translate([-1*x/2,-1*y/2,0])screw_post(h, slot=slot, hole_ratio=hr,outer=outer,hole_diam=hole_diam);
    rotate([0,0,180]){
        translate([-1*x/2,y/2,0])screw_post(h, slot=slot, hole_ratio=hr,outer=outer,hole_diam=hole_diam);
        translate([-1*x/2,-1*y/2,0])screw_post(h, slot=slot, hole_ratio=hr,outer=outer,hole_diam=hole_diam);
    }//end rotate
    
}// end module base

//base(91,101); // board x=91 y=101

//base(91,101,h=45,hr=0.5);


//base(75,32); // lcd

module screw_post(height, nut_h=2.8,slot=true, hole_ratio=0.25,outer=true,hole_diam=3.4){
    translate([0,0,height/2])difference(){
        if(outer==true){
            // shell
            cube([8,8,height],center=true);}
        // cutouts
        union(){
            // center hole
            translate([0,0,height/2]){rotate([180,0,0])cylinder(d=hole_diam, h= height*hole_ratio, $fn=18);}
            
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

//screw_post(20,hole_ratio=0.25);


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


module fancy_box(x,y,z,thickness){
    hull(){
        cube([x+thickness,y,z],center=true);
        cube([x,y+thickness,z],center=true);
        cube([x,y,z+thickness],center=true);
    }//end hull
}//end fancy_box


module top_enclosure(x, y, z, h){
    enj_depth = -8;
    enj_x = -30;
    enj_y = 35;
    difference(){
    union(){
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
        rotate([180,0,0])base(91,101.5,h,hr=0.5);
    }
    translate([0,0,5-1])top_markings();
    }//end difference
}//end module top_lvl


module top_markings(){
    assert(ord("\u0000") == 32);
    rotate([0,0,-90]){
        linear_extrude(1.5){
        translate([-30,-35,0])text("X",halign="center",valign="center");
        translate([5,-35,0])text("Y",halign="center",valign="center");
        translate([40,-35,0])text("Z",halign="center",valign="center");
        
        translate([-49,15,0])text("Ø",halign="center",valign="center");
        //translate([-49,-15,0])text("\u2714",halign="center",valign="center");
        
        translate([48,38,0]){scale([1,0.6,1])text("l",halign="center",valign="center");}
        translate([48,15,0]){scale([1,1,1])text("o",halign="center",valign="center");}
    }//end linear_extrude
    }//end rotate
}//end top_markings


module outer_enclosure(x=102, y=116, z=50){
    inner_dims = [100.3,114.3,60];
    thickness=10;
    difference(){
        union(){
    difference(){
        translate([0,0,-z/2+5-thickness/2])fancy_box(x,y,z,10);
        translate([0,0,-20])cube(inner_dims,center=true);
    }//end difference
    //stands
    translate([0,0,-z-thickness/2+3.5])base(91,101.5,5, slot=false);
    } // end union
    //screw holes
    translate([0,0,-z-thickness/2])base(91,101.5,20, hr=1, slot=false,outer=false);
    //nut slots for outer access (just in case)
    translate([0,0,-z-thickness/2+10])base(106,101,5, slot=false, hr=-1);
    //usb hole
    translate([0,-y/2,-31])cube([12,15,9],center=true);
    //power port
    translate([21,-y/2,-39]){rotate([90,0,0])cylinder(d=13,h=15,$fn=6,center=true);}
    //power port slot
    translate([21,-inner_dims[1]/2,5-z/2])cube([10,2.5,inner_dims[2]],center=true);
    // motor output
    translate([inner_dims[0]/2,-8,5-z/2])cube([20,50,inner_dims[2]],center=true);
}// end difference
}//end module outer_enclosure

top_enclosure(100,114,5,45);
%outer_enclosure();
//feet(8, 3.4, 5.6, 5); // print in TPU or something soft for grip