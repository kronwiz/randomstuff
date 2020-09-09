package require Tk

source "./sprite_def_image.tcl"

set WIDTH_KW "width"
set HEIGHT_KW "height"
set TO_KW "to"

set __STAGE__ {}

proc tk_wait {} {
	global __TK_WAIT__
	after 5 set __TK_WAIT__ &
	#vwait __TK_WAIT__
	tkwait variable __TK_WAIT__
	unset __TK_WAIT__
}

proc shift_args {params} {
	# removes the unnecessary preposition if there's any at the beginning of params
	# and returns the "clean" list of the remaining parameters
	global TO_KW

	if {[lindex $params 0] eq $TO_KW} {
		return [lrange $params 1 end]
	} else {
		return $params
	}
}

proc new {what args} {
	global __STAGE__ SPRITE_DEF_IMAGE
	global WIDTH_KW HEIGHT_KW

	set obj [dict create id 0 type $what x 0 y 0]

	switch $what {
		stage {
			set wk [lsearch -exact $args $WIDTH_KW]
			set width [expr {$wk == -1 ? 640 : [lindex $args $wk+1]}]
			set hk [lsearch -exact $args $HEIGHT_KW]
			set height [expr {$hk == -1 ? 480 : [lindex $args $hk+1]}]
			dict set obj width $width
			dict set obj height $height

			set c [canvas .stage -height $height -width $width]
			pack $c
			dict set obj canvas_ $c
			set __STAGE__ $c
		}

		sprite {
			image create photo squirrel -data $SPRITE_DEF_IMAGE
			set img [$__STAGE__ create image 50 50 -image squirrel -anchor nw]
			dict set obj image_ $img
		}
	}
}

proc move {what to x {y 0}} {
	global __STAGE__
	upvar 1 $what obj

	puts "what: $what"
	puts "- dictionary: $obj"

	lassign [shift_args [list $to $x $y]] x y
	dict set obj x $x
	dict set obj y $y
	$__STAGE__ moveto [dict get $obj image_] $x $y
	tk_wait
}

proc repeat {times body} {
	for {set t 0} {$t < $times} {incr t} {
		uplevel 1 $body
	}
}

proc test {} {
	set s [new stage]
	set a [new sprite]

	for {set t 0} {$t < 200} {incr t} {
		move a to [expr {10+$t}] 20
		#move a [expr {10+$t}] 20
	}

	set t 0
	repeat 200 {
		incr t
		move a to 209 [expr {20+$t}]
	}
}

test

