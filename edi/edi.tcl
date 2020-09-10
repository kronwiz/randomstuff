package require Tk

source "./sprite_def_image.tcl"

set WIDTH_KW "width"
set HEIGHT_KW "height"
set TO_KW "to"
set COSTUME_KW "costume"

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
		lrange $params 1 end
	} else {
		$params
	}
}

proc new {what args} {
	global __STAGE__ SPRITE_DEF_IMAGE
	global WIDTH_KW HEIGHT_KW COSTUME_KW

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
			set ck [lsearch -exact $args $COSTUME_KW]
			if {$ck == -1} {
				# if not specified use the default costume
				set costname DEFAULT_COSTUME
				set level #0  ;# global level
			} else {
				set costname [lindex $args $ck+1]
				set level 1
			}
			upvar $level $costname costume
			set images [dict get $costume images]
			set img [$__STAGE__ create image 50 50 -image [lindex $images 0] -anchor nw]
			dict set obj image_ $img
		}

		costume {
			set img [image create photo -data $SPRITE_DEF_IMAGE]  ;# NB: no name
			lappend images $img
			dict set obj images $images
		}
	}

	return $obj
}

set DEFAULT_COSTUME [new costume]  ;# FIXME: add the picture file name

proc move {what to x {y 0}} {
	global __STAGE__
	upvar 1 $what obj

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


#rename proc _proc
#
#_proc proc {name arglist body} {
#	set upvar_all_args {
#		if [info exists arglist] {
#			foreach argname $arglist {
#				upvar 1 $argname tmp$argname
#				set $argname $tmpargname
#			}
#		};
#	}
#
#	set newbody [concat $upvar_all_args $body]
#	_proc $name $arglist $newbody
#}

proc sposta {s} {
	move s to 210 100
}

proc test {} {
	set s [new stage]
	set squirrel [new costume]
	#set a [new sprite costume squirrel]
	set a [new sprite]

	# questo non funziona a causa del fatto che move ecc. si aspettano la variable
	# solo al precedente livello (upvar 1) mentre in questo caso e' sopra due livelli
	#sposta a
	#puts $a

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


# redefining proc example
#
#rename proc _proc
#
#_proc proc {name arglist body} {
#    if {![string match ::* $name]} {
#        #not already an 'absolute' namespace path
#        #qualify it so that traces can find it
#        set name [uplevel 1 namespace current]::[set name]
#    }
#    _proc $name $arglist $body
#
#
# Bella introduzione a Tcl di Antirez: http://antirez.com/articoli/tclmisunderstood.html
#
