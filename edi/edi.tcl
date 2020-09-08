package require Tk

set WIDTH_KW "width"
set HEIGHT_KW "height"


proc new {what args} {
	global WIDTH_KW HEIGHT_KW

	set obj [dict create id 0 type $what x 0 y 0]

	switch $what {
		"stage" {
			set wk [lsearch -exact $args $WIDTH_KW]
			set width [expr {$wk == -1 ? 640 : [lindex $args $wk+1]}]
			set hk [lsearch -exact $args $HEIGHT_KW]
			set height [expr {$hk == -1 ? 480 : [lindex $args $hk+1]}]
			dict set obj width $width
			dict set obj height $height

			set c [canvas .stage -height $height -width $width]
			pack $c
			dict set obj canvas_ $c
		}
	}
}

proc move {what prep x args} {
	upvar 1 $what obj
	if {[llength $args] > 0} {set y [lindex $args 0]} else {set y $x; set x $prep}
	dict set obj x $x
	dict set obj y $y
}

proc test {} {
	set s [new stage]
	puts "stage: $s"
	set a [new sprite]
	move a to 10 20
	puts "sprite: $a"
}

test

